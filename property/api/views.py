from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from blog.models import UserProfile, BankApi
from property.models import PropertyListing
from property.api.serializers import PropertyListingSerializer, AreaPriceSerializer, BankApiSerializer
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
import numpy as np


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_view(request, slug):

    try:
        property_listing = PropertyListing.objects.get(slug=slug)

    except PropertyListing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PropertyListingSerializer(property_listing)

    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_property_view(request, slug):

    try:
        property_listing = PropertyListing.objects.get(slug=slug)

    except PropertyListing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if PropertyListing.owner != user:
        return Response({'response': "You dont have enough permissions for that"})

    serializer = PropertyListingSerializer(property_listing, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "updated success"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_delete_property_view(request, slug):

    try:
        property_listing = PropertyListing.objects.get(slug=slug)

    except PropertyListing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if PropertyListing.owner != user:
        return Response({'response': "You dont have enough permissions for that"})

    operation = property_listing.delete()
    data = {}
    if operation:
        data["success"] = "deleted success"
    else:
        data["faliure"] = "failed"
    return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_property_view(request):

    account = request.user
    property_listing = PropertyListing(owner=account)

    serializer = PropertyListingSerializer(property_listing, data=request.data)
    deta = {}
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ApiPropertyListView(ListAPIView):
#     queryset = PropertyListing.objects.all()

#     serializer_class = PropertyListingSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     pagination_class = PageNumberPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['city', 'price']


class ApiPropertyListView(ListAPIView):
    queryset = PropertyListing.objects.all()

    serializer_class = PropertyListingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'price']


class ApiPropertyListView1(ListAPIView):
    queryset = PropertyListing.objects.filter(Verify='N')

    serializer_class = PropertyListingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'price']


class ApiAreaPriceView(ListAPIView):

    def get(self, request, format=None):
        snippets = PropertyListing.objects.all()
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)
        pagination_class = PageNumberPagination
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ['area', 'price']
        serializer = AreaPriceSerializer(snippets, many=True)
        value = []
        for i in serializer.data:
            value.append(i['price'])
        avg = np.mean(value)
        print(avg)
        return Response(avg)


class ApiBankListView(ListAPIView):

    def get(self, request, format=None):
        snippets = BankApi.objects.all()
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)
        pagination_class = PageNumberPagination
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ['city', 'price']
        serializer = BankApiSerializer(snippets, many=True)
        return Response(serializer.data)


class followview(APIView):

    def post(self, request):

        for each in request.data:

            p1 = request.data[each]['title']
            status1 = request.data[each]['status']

            prop = PropertyListing.objects.get(title=p1)

            if status1 == 'Accepted':

                prop.Verify = 'V'
                prop.save()

            else:

                prop.Verify = 'R'
                prop.save()
                return Response("fknlenl")
