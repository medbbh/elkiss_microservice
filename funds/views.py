from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from .models import Fund
from .serializers import FundSerializer


class FundListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all cagnottes (optionally filter by status).
    POST: Create a new cagnotte for the authenticated user.
    """
    serializer_class = FundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Fund.objects.all()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FundRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Detail of a specific cagnotte.
    PUT/PATCH: Update a cagnotte if you're the owner and no donations are made yet.
    DELETE: Delete a cagnotte if you're the owner and no donations are made yet.
    """
    serializer_class = FundSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Fund.objects.all()

    def update(self, request, *args, **kwargs):
        cagnotte = self.get_object()
        # Ensure only the owner can update
        if cagnotte.owner != request.user:
            return Response(
                {"detail": "Only the owner can update this cagnotte."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Ensure no donations made (if your business rule requires that)
        if cagnotte.current_amount > 0:
            return Response(
                {"detail": "Cannot update a cagnotte that has donations."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cagnotte = self.get_object()
        if cagnotte.owner != request.user:
            return Response(
                {"detail": "Only the owner can delete this cagnotte."},
                status=status.HTTP_403_FORBIDDEN
            )
        if cagnotte.current_amount > 0:
            return Response(
                {"detail": "Cannot delete a cagnotte that has donations."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class DonateAPIView(APIView):
    """
    POST /api/transactions/donate -> user donates to a cagnotte
    {
      "cagnotte_id": "uuid",
      "amount": 50.00,
      "note": "Happy Birthday!"
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cagnotte_id = request.data.get("cagnotte_id")
        amount = request.data.get("amount", 0)
        note = request.data.get("note", "")
        
        # Basic validations
        if not cagnotte_id:
            return Response({"detail": "cagnotte_id is required"}, status=400)
        if float(amount) < 5:
            return Response({"detail": "Minimum donation is 5 MRU"}, status=400)
        
        try:
            cagnotte = Fund.objects.get(pk=cagnotte_id, status="open")
        except Fund.DoesNotExist:
            return Response({"detail": "Fund not found or not Open"}, status=404)
        
        # Check user solde
        if user.solde < float(amount):
            return Response({"detail": "Insufficient funds"}, status=400)
        
        # Calculate tax (1% example)
        tax = float(amount) * 0.01
        total_amount = float(amount) + tax
        
        # Deduct from user solde
        user.solde -= total_amount
        user.save()
        
        # Update cagnotte
        cagnotte.current_amount += float(amount)
        cagnotte.total_participants += 1
        cagnotte.save()

        # Check if we reached or exceeded the target
        if cagnotte.current_amount >= cagnotte.target_amount:
            cagnotte.status = "close"

        cagnotte.save()
        
        # Create transaction record
        transaction = Transaction.objects.create(
            user=user,
            cagnotte=cagnotte,
            amount=amount,
            note=note,
            tax=tax
        )
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=201)


class CloseFundAPIView(generics.UpdateAPIView):
    """
    PUT /api/cagnottes/{id}/close -> Closes the cagnotte if you're the owner.
    """
    serializer_class = FundSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Fund.objects.all()

    def update(self, request, *args, **kwargs):
        cagnotte = self.get_object()
        if cagnotte.owner != request.user:
            return Response(
                {"detail": "Only the owner can close this cagnotte."},
                status=status.HTTP_403_FORBIDDEN
            )
        if cagnotte.status != "open":
            return Response(
                {"detail": "Fund is already closed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Mark as CLOSED
        cagnotte.status = "closed"
        cagnotte.save()
        return Response(
            self.get_serializer(cagnotte).data,
            status=status.HTTP_200_OK
        )
    

# class OpenFundAPIView(generics.UpdateAPIView):
#     """
#     PUT /api/cagnottes/{id}/open -> opens the cagnotte if you're the owner.
#     """
#     serializer_class = FundSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Fund.objects.all()

#     def update(self, request, *args, **kwargs):
#         cagnotte = self.get_object()
#         if cagnotte.owner != request.user:
#             return Response(
#                 {"detail": "Only the owner can close this cagnotte."},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         if cagnotte.status != "close":
#             return Response(
#                 {"detail": "Fund is already open."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         # Mark as CLOSED
#         cagnotte.status = "open"
#         cagnotte.save()
#         return Response(
#             self.get_serializer(cagnotte).data,
#             status=status.HTTP_200_OK
#         )