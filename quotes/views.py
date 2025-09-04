from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quote, QuoteItem
from .serializers import QuoteSerializer, QuoteItemSerializer


class QuoteListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuoteDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            quote = Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            quote = Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuoteSerializer(quote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            quote = Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)
        quote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
