from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.db.models import Q


class ProductListCreateAPIView(APIView):

    def get(self,request):

        products=Product.objects.all()
        search=request.GET.get("search")
        if search:
            products=products.filter(
                Q(name__icontains=search)|
                Q(description__icontains=search)|
                Q(category__icontains=search)
            )

        ordering=request.GET.get("ordering")
        if ordering:
            print("ORDERING VALUE:", ordering)
            products=products.order_by(ordering)

        serializer=ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    def post(self,request):

        serializer=ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDetailAPIView(APIView):

    def get(self,request,pk):

        product=Product.objects.get(pk=pk)
        serializer=ProductSerializer(product)
        return  Response(serializer.data)
    
    # def put(self,request,pk):
    #     product=Product.objects.get(pk=pk)
    #     serializer=ProductSerializer(
    #         product,
    #         data=request.data
    #     )

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)

    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )


    def put(self, request, pk):

        product = Product.objects.get(pk=pk)

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self,request,pk):
        product=Product.objects.get(pk=pk)
        product.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )




# - ka meaning

# Django ORM mein:

# Product.objects.all().order_by("price")

# means ascending.

# Product.objects.all().order_by("-price")