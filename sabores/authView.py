from .serializer import UserSerializer 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action

from rest_framework import viewsets

class UserView(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = False
    # authentication_classes = False

    @action(detail=False, methods=['POST'])
    def login(self, request):
        request.data["username"] = "sabores"
        user = get_object_or_404(User, username=request.data["username"])

        if not user.check_password(request.data["password"]):
            return Response({"error: " "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK);



# @api_view(["POST"])
# def login(request):