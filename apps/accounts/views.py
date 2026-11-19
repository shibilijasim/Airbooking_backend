# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth import get_user_model
# from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

# User = get_user_model()

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserRegistrationSerializer

# class CustomLoginView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# # --- Admin Views ---
# class PendingUsersList(generics.ListAPIView):
#     permission_classes = [permissions.IsAdminUser]
    
#     def get_queryset(self):
#         return User.objects.filter(approval_status='Pending')
    
#     def list(self, request, *args, **kwargs):
#         users = self.get_queryset().values('id', 'username', 'email', 'approval_status')
#         return Response(users)

# class ApproveUserView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, id):
#         try:
#             user = User.objects.get(id=id)
#             user.approval_status = 'Approved'
#             user.save()
#             return Response({"message": f"User {user.username} approved successfully."})
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# from django.contrib.auth import get_user_model
# from rest_framework import generics, permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .serializers import AdminUserSerializer
# from .tasks import send_account_activated_email

# User = get_user_model()


# class AdminUserListView(generics.ListAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#     serializer_class = AdminUserSerializer

#     def get_queryset(self):
#         status_filter = self.request.query_params.get('status', 'Pending')
#         qs = User.objects.filter(is_staff=False).order_by('-date_joined')
#         if status_filter and status_filter != 'All':
#             qs = qs.filter(approval_status=status_filter)
#         return qs


# class AdminUserReviewActionView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, pk):
#         try:
#             target_user = User.objects.get(pk=pk, is_staff=False)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#         action = request.data.get('action')
#         if action not in ('approve', 'reject'):
#             return Response(
#                 {'error': 'Action must be "approve" or "reject".'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if action == 'approve':
#             target_user.is_active = True
#             target_user.approval_status = 'Approved'
#             target_user.save()

#             if target_user.email:
#                 send_account_activated_email.delay(target_user.email, target_user.username)
#         else:
#             target_user.is_active = False
#             target_user.approval_status = 'Rejected'
#             target_user.save()

#         return Response(AdminUserSerializer(target_user).data, status=status.HTTP_200_OK)


from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    AdminUserSerializer,
)
from .tasks import send_account_activated_email

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer


class CustomLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class AdminUserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        status_filter = self.request.query_params.get('status', 'Pending')
        qs = User.objects.filter(is_staff=False).order_by('-date_joined')
        if status_filter and status_filter != 'All':
            qs = qs.filter(approval_status=status_filter)
        return qs


class AdminUserReviewActionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            target_user = User.objects.get(pk=pk, is_staff=False)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action not in ('approve', 'reject'):
            return Response(
                {'error': 'Action must be "approve" or "reject".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'approve':
            target_user.is_active = True
            target_user.approval_status = 'Approved'
            target_user.save()

            if target_user.email:
                send_account_activated_email.delay(target_user.email, target_user.username)
        else:
            target_user.is_active = False
            target_user.approval_status = 'Rejected'
            target_user.save()

        return Response(AdminUserSerializer(target_user).data, status=status.HTTP_200_OK)