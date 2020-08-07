
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from property.models import PropertyListing
from property.forms import CreatePropertyListingForm, UpdatePropertyListingForm
from blog.models import UserProfile, BankApi
from django.contrib.auth.models import User

from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from django_pandas.io import read_frame
import numpy as np
from sklearn import linear_model
from sklearn import preprocessing


def create_property_view(request):
    context = {}
    user = request.user
    user = User.objects.get(username=user)
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreatePropertyListingForm(
        request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.owner = user
        obj.save()
        form = CreatePropertyListingForm()
    else:
        print(form.errors)
        print("main \n\n\n\n\n\n\\n")
    context['form'] = form
    return render(request, "property/create_property.html", context)


def detail_property_view(request, slug):
    context = {}
    user = request.user
    property_listings = get_object_or_404(PropertyListing, slug=slug)
    lists = PropertyListing.objects.filter(city=property_listings.city)
    context['lists'] = lists
    context['property_listings'] = property_listings
    context['user'] = user
    return render(request, 'property/detail_property.html', context)


def edit_property_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    property_listing = get_object_or_404(PropertyListing, slug=slug)

    if property_listing.owner != user:
        return HttpResponse('You are not the owner of that property.')
    if request.POST:
        form = UpdatePropertyListingForm(
            request.POST or None, request.FILES or None, instance=property_listing)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            property_listing = obj

    form = UpdatePropertyListingForm(
        initial={
            "title": property_listing.title,
            "body": property_listing.body,
            "image": property_listing.image,
        }
    )

    context['form'] = form
    return render(request, 'property/edit_property.html', context)


def getProperties(data, properties):
    li = []
    x = data.latitude+1
    y = data.latitude-1
    for i in properties:
        if i.latitude >= x and i.latitude <= y:
            li.append(i)

    x = data.longitude+1
    y = data.longitude-1
    for i in properties:
        if i.longitude >= x and i.longitude <= y:
            li.append(i)

    return list(set(li))


def check_price(request, slug):
    context = {}
    property_listing = get_object_or_404(PropertyListing, slug=slug)
    # qs = PropertyListing.objects.filter(latitude=property_listing.latitude < 1 and property_listing.latitude > -1).filter(
    #     longitude=property_listing.longitude < 1 and property_listing.longitude > -1)
    qs = PropertyListing.objects.filter(
        area=property_listing.area).filter(city=property_listing.city)
    df = read_frame(qs, fieldnames=[
                    'pool', 'parking', 'gym', 'balcony', 'bedrooms', 'bathrooms', 'sqft', 'price'])
    mm_scaler = preprocessing.MinMaxScaler()

    reg = linear_model.LinearRegression()
    data = df.drop('price', axis='columns')
    price = df.price
    norm_data = mm_scaler.fit_transform(data)

    reg.fit(norm_data, price)
    context['price'] = reg.predict(
        [[property_listing.pool, property_listing.parking, property_listing.gym, property_listing.balcony, property_listing.bedrooms, property_listing.bathrooms, property_listing.sqft]])
    return render(request, 'property/check_price.html', context)


def bank_api(request, slug):
    context = {}
    user = request.user
    property_listings = get_object_or_404(PropertyListing, slug=slug)
    a = BankApi.objects.filter(user=user).filter(
        property_interested=property_listings)
    if a:
        return HttpResponse("You have already done that!")
    obj = BankApi(user=user, property_interested=property_listings,
                  date_queried=datetime.date(datetime.now()))
    obj.save()
    return HttpResponse("Done")
