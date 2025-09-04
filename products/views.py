from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from products.models import Product
from products.serializers import ProductSerializer

from products.models import ProductCategory
from products.serializers import ProductCategorySerializer

class ProductCategoryView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response({
                "message": "Product category created successfully.",
                "category": ProductCategorySerializer(category).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request, pk=None):
        # Get specific product
        if pk is not None:
            try:
                product = Product.objects.select_related('category').get(pk=pk)
            except Product.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        # List view: get all products
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = ProductSerializer(data=request.data)
        # 1) run validation (raises 400 if invalid)
        serializer.is_valid(raise_exception=True)
        # 2) save, injecting the current user as created_by
        product = serializer.save(created_by=request.user)
        return Response({
            "message": "Product created successfully.",
            "product": ProductSerializer(product).data
        }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        print("=== RAW PUT request.data ===")
        print(request.data)

        product_id = request.data.get('id')
        print(">> Parsed product_id:", product_id)

        if not product_id:
            print("!! ERROR: No product_id in request")
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
            print(">> Found product:", product.name)
        except Product.DoesNotExist:
            print(f"!! ERROR: Product with ID {product_id} not found")
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a mutable version of request.data WITHOUT deep copying file objects
        data = request.data.dict()  # this skips files and gives a flat dict of form fields

        # Add file fields back from request.FILES (if they exist)
        for img_field in ['img1', 'img2', 'img3', 'img4', 'img5', 'img6']:
            if img_field in request.FILES:
                data[img_field] = request.FILES[img_field]

        # Clean read-only or auto-managed fields
        for key in ['created_at', 'updated_at', 'created_by', 'boutique']:
            data.pop(key, None)

        print(">> Cleaned request data:", data)

        # Pass both data and files to the serializer
        serializer = ProductSerializer(product, data=data, partial=True)

        print(">> Is serializer valid?", serializer.is_valid())
        if not serializer.is_valid():
            print("!! Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_product = serializer.save()
        print(">> Product updated successfully:", updated_product.name)

        return Response({
            "message": "Product updated successfully.",
            "product": ProductSerializer(updated_product).data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
