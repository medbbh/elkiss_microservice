from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
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
        cagnotte.status = "close"
        cagnotte.save()
        return Response(
            self.get_serializer(cagnotte).data,
            status=status.HTTP_200_OK
        )