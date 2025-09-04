from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from ..models.members import MemberProfile, MemberBodyProfile
from ..serializers import MemberProfileSerializer, MemberBodyProfileSerializer

class MemberView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def post(self, request):
        print("POST data:", request.data)
        serializer = MemberProfileSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            body_profile_data = request.data.get("body_profile")
            print("Body profile data:", body_profile_data)
            if body_profile_data:
                MemberBodyProfile.objects.create(member=member, **body_profile_data)
            else:
                MemberBodyProfile.objects.create(member=member)
            refresh = RefreshToken.for_user(member.user)
            print("Member created:", member)
            return Response({
                "message": "Member profile created successfully.",
                "refresh": str(refresh),
                "access":  str(refresh.access_token),
                "member": MemberProfileSerializer(member).data,
                "body_profile": MemberBodyProfileSerializer(member.body_profile).data if hasattr(member, "body_profile") else None,
            }, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        print("GET request by user:", request.user)
        try:
            member = request.user.profile
            member_serializer = MemberProfileSerializer(member)
            body_profile_serializer = MemberBodyProfileSerializer(member.body_profile) if hasattr(member, "body_profile") else None
            print("Member data:", member_serializer.data)
            print("Body profile data:", body_profile_serializer.data if body_profile_serializer else None)
            return Response({
                "member": member_serializer.data,
                "body_profile": body_profile_serializer.data if body_profile_serializer else None,
            })
        except MemberProfile.DoesNotExist:
            print("Member profile not found for user:", request.user)
            return Response({"error": "Member profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        print("PUT data:", request.data)
        try:
            member = request.user.profile

            # Only update member fields that are present and valid
            member_fields = ['bio', 'phone', 'address', 'avatar', 'social_media']
            member_update_data = {field: request.data.get(field) for field in member_fields if field in request.data}
            print("Member update data:", member_update_data)

            member_serializer = MemberProfileSerializer(member, data=member_update_data, partial=True)

            body_profile_data = request.data.get("body_profile")
            print("Body profile data for update:", body_profile_data)

            if member_serializer.is_valid():
                member_serializer.save()
                body_profile, created = MemberBodyProfile.objects.get_or_create(member=member)
                print("Body profile instance:", body_profile, "Created:", created)
                if body_profile_data:
                    # Only update body profile fields, not nested member
                    clean_body_profile_data = {k: v for k, v in body_profile_data.items() if k != "member"}
                    body_profile_serializer = MemberBodyProfileSerializer(
                        body_profile, data=clean_body_profile_data, partial=True
                    )
                    if body_profile_serializer.is_valid():
                        body_profile_serializer.save()
                        print("Body profile updated:", body_profile_serializer.data)
                    else:
                        print("Body profile serializer errors:", body_profile_serializer.errors)
                        return Response(body_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                print("Member updated:", member_serializer.data)
                return Response({
                    "message": "Member updated successfully",
                    "member": member_serializer.data,
                    "body_profile": MemberBodyProfileSerializer(body_profile).data,
                })

            print("Member serializer errors:", member_serializer.errors)
            return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MemberProfile.DoesNotExist:
            print("Member profile not found for user:", request.user)
            return Response({"error": "Member profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        print("DELETE request by user:", request.user)
        try:
            member = request.user.profile
            member.delete()
            print("Member deleted:", member)
            return Response({"message": "Member deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except MemberProfile.DoesNotExist:
            print("Member profile not found for user:", request.user)
            return Response({"error": "Member profile not found."}, status=status.HTTP_404_NOT_FOUND)