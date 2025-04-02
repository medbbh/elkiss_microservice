
from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer


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