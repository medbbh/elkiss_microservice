
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Transaction
from funds.models import Fund
from .serializers import TransactionSerializer

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


class UserTransactionsAPIView(generics.ListAPIView):
    """
    GET /api/transactions -> list of current user's transactions
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class FundTransactionsAPIView(generics.ListAPIView):
    """
    GET /api/cagnottes/{id}/transactions -> list transactions for that cagnotte
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cagnotte_id = self.kwargs.get("pk")
        return Transaction.objects.filter(cagnotte_id=cagnotte_id)