from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from ..models.members import MemberProfile, MemberBodyProfile
from ..serializers import UserSerializer

class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Allow anyone to POST (register); require auth for GET/PUT/DELETE
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.save()
            member = MemberProfile.objects.create(user=user, created_by=user)
            MemberBodyProfile.objects.create(member=member)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully.",
                "refresh": str(refresh),
                "access":  str(refresh.access_token),
                "user": {
                    "id":       user.id,
                    "username": user.username,
                    "email":    user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "user":    serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


