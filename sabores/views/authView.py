from ..serializers.UsuariosSerializer import UserSerializer 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action

from rest_framework import viewsets

class UserView(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def login(self, request):
        request.data["nombre"] = "Qsabores"
        user = get_object_or_404(User, username=request.data["nombre"])

        if not user.check_password(request.data["contrasena"]):
            return Response({"error: " "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK);
