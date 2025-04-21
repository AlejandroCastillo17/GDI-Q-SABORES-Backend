from rest_framework import viewsets, filters
from .models import Productos, Proveedores
from .serializer import ProductosSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductoView(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Búsqueda por nombre, categoría, proveedor, etc.
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'categoria',] # 'proveedorid'

    # @action(detail=False, methods=['POST'])
    # def login(self, request):
    #     request.data["username"] = "sabores"
    #     user = get_object_or_404(User, username=request.data["username"])

    #     if not user.check_password(request.data["password"]):
    #         return Response({"error: " "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     token, created = Token.objects.get_or_create(user=user)
    #     serializer = UserSerializer(instance=user)

    #     return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK);