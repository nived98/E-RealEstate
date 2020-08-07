from rest_framework import serializers

from property.models import PropertyListing
from blog.models import BankApi


class PropertyListingSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_owner')

    class Meta:
        model = PropertyListing
        fields = ['title', 'body', 'image', 'date_updated', 'username', 'price', 'image2', 'image3', 'address', 'city', 'state', 'zipcode', 'bathrooms', 'bedrooms', 'sqft', 'types',
                  'stay', 'pool', 'balcony', 'gym', 'parking', 'latitude', 'longitude', 'year_built']

    def get_username_from_owner(self, property_listing):
        username = property_listing.owner.username
        return username


class AreaPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyListing
        fields = ['price']

    def get_username_from_owner(self, property_listing):
        username = property_listing.owner.username
        return username


class BankApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankApi
        fields = ['user', 'property_interested']

    def get_username_from_owner(self, property_listing):
        username = property_listing.owner.username
        return username


class Post11Serializer(serializers.ModelSerializer):
    class meta:
        model = PropertyListing
        fields = ['Verify']
