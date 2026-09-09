from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.db.models import Q
from rest_framework.pagination import CursorPagination



class ProductCursorPagination(CursorPagination):
    page_size=2
    ordering="id"

class ProductListCreateAPIView(APIView):

    def get(self,request):

     
        products=Product.objects.filter(is_deleted=False)
        search=request.GET.get("search")
        if search:
            products=products.filter(
                Q(name__icontains=search)|
                Q(description__icontains=search)|
                Q(category__icontains=search)
            )


        # pagination
        paginator=ProductCursorPagination()

        result_page=paginator.paginate_queryset(
            products,
            request
        )

        serializer=ProductSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

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

      
        product=Product.objects.get(pk=pk,is_deleted=False)
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
        product=Product.objects.get(pk=pk,is_deleted=False)
        product.is_deleted=True
        product.save()
      
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ProductRestoreAPIView(APIView):
    def post(self,request,pk):
        product=Product.objects.get(
            pk=pk,
            is_deleted=True
        )

        product.is_deleted=False
        product.save()
        serializer=ProductSerializer(product)

        return Response(
            {
                "message":"product is restored",
                "product":serializer.data,
            },
            status=status.HTTP_200_OK
        )


