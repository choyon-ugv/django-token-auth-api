from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import update_session_auth_hash
from rest_framework.authtoken.models import Token
from .permissions import IsOwnerOrReadOnly
from .serializers import UserRegistrationSerializer, UserLoginSerializer, PasswordChangeSerializer, UserProfileSerializer


class UserRegistrationView(APIView):        # API for User Registration
    permission_classes = []  # Allow anyone to register
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  # Generate token
            response = {
                'status' : 201,
                'success' : True,
                'message' : 'User registered successfully',
                'data' : serializer.data,
                'token': token.key  # Return token as response
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):          # API for User Login (Only for authenticated users)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'status' : 200,
                'success' : True,
                'message' : 'Login successful',
                'data' : serializer.data,
                'token': token.key  # Return token as response
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):              # API for User Logout (Deletes Token)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # Delete the user's token
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class PasswordChangeView(APIView):            # API for Changing Password
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            # Check if old password is correct
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            response = {
                'status' : 200,
                'success' : True,
                'message' : 'Password changed successfully',
                "email": user.email,
                "username": user.username,
                "new_password": new_password  # Returning new password
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):         # API for Viewing & Updating User Profile
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve user profile details"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user profile details (except password)"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : 201,
                'success' : True,
                'message' : 'Profile updated successfully',
                'data': serializer.data  # Return updated user profile details
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):       # API for User Logout (Token Revocation)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user by deleting token"""
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Remove the token from the database
            response = {
                'status' : 200,
                'success' : True,
                'message' : 'User logged out successfully'
            }
            return Response(response)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or already logged out"}, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserProfileView(APIView):              # API for Viewing & Updating User Profile
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        """Retrieve user profile details"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user profile details (Only the owner can update)"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : 201,
                'success' : True,
                'message' : 'Profile updated successfully',
                'data': serializer.data  # Return updated user profile details
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)