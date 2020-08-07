from django import forms

from property.models import PropertyListing


class CreatePropertyListingForm(forms.ModelForm):

    class Meta:
        model = PropertyListing
        fields = ['title', 'body', 'image', 'price', 'image2', 'image3', 'image4',
                  'address', 'city', 'area', 'state', 'zipcode', 'bathrooms', 'bedrooms', 'sqft', 'types',
                  'stay', 'pool', 'balcony', 'gym', 'parking', 'latitude', 'longitude', 'year_built']


class UpdatePropertyListingForm(forms.ModelForm):

    class Meta:
        model = PropertyListing
        fields = ['title', 'body', 'image', 'image2', 'image3', 'price',
                  'address', 'city', 'area', 'state', 'zipcode', 'bathrooms', 'bedrooms', 'sqft',
                  'stay', 'pool', 'balcony', 'gym', 'parking', 'latitude', 'longitude', 'year_built']

    def save(self, commit=True):
        property_listings = self.instance
        property_listings.title = self.cleaned_data['title']
        property_listings.body = self.cleaned_data['body']
        property_listings.address = self.cleaned_data['address']
        property_listings.city = self.cleaned_data['city']
        property_listings.area = self.cleaned_data['area']
        property_listings.state = self.cleaned_data['state']
        property_listings.zipcode = self.cleaned_data['zipcode']
        property_listings.price = self.cleaned_data['price']
        property_listings.bedrooms = self.cleaned_data['bedrooms']
        property_listings.bathrooms = self.cleaned_data['bathrooms']
        property_listings.sqft = self.cleaned_data['sqft']
        property_listings.types = self.cleaned_data['types']
        property_listings.pool = self.cleaned_data['pool']
        property_listings.gym = self.cleaned_data['gym']
        property_listings.parking = self.cleaned_data['parking']
        property_listings.balcony = self.cleaned_data['balcony']
        property_listings.latitude = self.cleaned_data['latitude']
        property_listings.longitude = self.cleaned_data['longitude']
        property_listings.stay = self.cleaned_data['stay']
        property_listings.year_built = self.cleaned_data['year_built']

        if self.cleaned_data['image']:
            property_listings.image = self.cleaned_data['image']

        if self.cleaned_data['image2']:
            property_listings.image = self.cleaned_data['image2']

        if self.cleaned_data['image3']:
            property_listings.image = self.cleaned_data['image3']

        if commit:
            property_listings.save()
        return property_listings
