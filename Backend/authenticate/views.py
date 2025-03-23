from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from datetime import timedelta, date
from .models import SadhanaEntry
from .serializers import UserSerializer, SadhanaEntrySerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User Created Successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email) #find user by email
        except User.DoesNotExist:
            return Response({ 'error' : 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if check_password(password, user.password):
            refresh = RefreshToken.for_user(user)  # Generate JWT token
            return Response({
                'message': 'Login Successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            'error' : 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)

class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully"}, status=200)
    
    
class SadhanaEntryView(APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = SadhanaEntrySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sadhana entry submitted successfully'}, status=status.HTTP_201_CREATED)
        print("Validation Errors : ", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WeeklyReportView(generics.ListAPIView):
    """Fetches Sadhana entries for the current user in the current week."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        today = date.today()
        start_date = today - timedelta(days=today.weekday()) # Calculate Monday of this week
        end_date = start_date + timedelta(days=6)

        weekly_entries  = SadhanaEntry.objects.filter(user=user, card_filled_at__range=[start_date, end_date])
        serializer = SadhanaEntrySerializer(weekly_entries, many=True)
        return Response(serializer.data)
