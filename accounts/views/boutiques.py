from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.boutiques import BoutiqueProfile, BoutiqueCustomer
from ..models.members import MemberProfile
from ..serializers import BoutiqueProfileSerializer, BoutiqueCustomerSerializer, MemberProfileSerializer


class BoutiqueListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        boutiques = BoutiqueProfile.objects.all()
        serializer = BoutiqueProfileSerializer(boutiques, many=True)
        return Response({"boutiques": serializer.data}, status=status.HTTP_200_OK)


class BoutiqueMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, boutique_id):
        try:
            # Get all BoutiqueCustomer objects for this boutique
            customers = BoutiqueCustomer.objects.filter(boutique_id=boutique_id, is_active=True)
            # Get related MemberProfiles for each customer
            members = []
            for customer in customers:
                try:
                    member = MemberProfile.objects.get(user=customer.user)
                    members.append(member)
                except MemberProfile.DoesNotExist:
                    continue
            serializer = MemberProfileSerializer(members, many=True)
            return Response({"members": serializer.data}, status=status.HTTP_200_OK)
        except BoutiqueProfile.DoesNotExist:
            return Response({"error": "Boutique not found"}, status=status.HTTP_404_NOT_FOUND)