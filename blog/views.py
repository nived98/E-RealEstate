from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse,  get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from property.models import PropertyListing

from blog.models import UserProfile
from .choices import type_choices, price_choices
from django.db.models import Q
import json
from .forms import UserUpdateForm

def home(request):
    context = {}
    if request.user.is_authenticated:
        property_listings_r = PropertyListing.objects.filter(
            Q(types='R') | Q(types='B')).exclude(owner=request.user)
        property_listings_s = PropertyListing.objects.filter(
            Q(types='S') | Q(types='B')).exclude(owner=request.user)
        lati = PropertyListing.objects.all().values_list('latitude').exclude(owner=request.user)
        longi = PropertyListing.objects.all().values_list('longitude').exclude(owner=request.user)
        slug = PropertyListing.objects.all().values_list('slug').exclude(owner=request.user)
    else:
        property_listings_r = PropertyListing.objects.filter(
            Q(types='R') | Q(types='B'))
        property_listings_s = PropertyListing.objects.filter(
            Q(types='S') | Q(types='B'))
        lati = PropertyListing.objects.all().values_list('latitude')
        longi = PropertyListing.objects.all().values_list('longitude')
        slug = PropertyListing.objects.all().values_list('slug')
    cities = PropertyListing.objects.all().values_list('city', flat=True).distinct()

    lat= []
    lon = []
    slugs = []
    for i in lati:
        lat +=[i[0]]
    for i in longi:
        lon +=[i[0]]
    for i in slug:
        slugs+=[i[0]]
    context = {"property_listings_r": property_listings_r, "property_listings_s": property_listings_s,
               "cities": cities, "type_choices":type_choices, "price_choices":price_choices,
               "lat":lat, "lon":lon, "slug":slugs, "values":request.GET}
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
def buymaps(request):
    return render(request,'buymaps.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:home'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login but failed!")
            print("Username: {} and password {}".format(username, password))
            return render(request, 'login.html', {'msg': 'Invalid Details Provided!'})
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("blog:login")
    context = {}
    property_listings = PropertyListing.objects.filter(owner=request.user)
    context['property_listings'] = property_listings
    return render(request, "account.html", context)




def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
       
        if u_form.is_valid():
            u_form.save()
           
            messages.success(request, f'Your account has been updated!')
            return redirect('http://127.0.0.1:8000/profile/')

    else:
        u_form = UserUpdateForm(instance=request.user)
       

    context = {
        'u_form': u_form,
       
    }

    return render(request, 'profile.html', context)

# def edit_profile_view(request):
#     context = {}
#     user = request.user
#     if not user.is_authenticated:
#         return redirect("must_authenticate")
#     user_details = UserProfile.objects.filter(user=request.user)
#     if request.POST:
#         form = UpdateProfileForm(
#             request.POST or None, request.FILES or None, instance=user_details)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.save()
#             context['success_message'] = "Updated"
#             user_details = obj
#     form = UpdateProfileForm(
#         initial={
#             "first_name": user_details.first_name,
#             "last_name": user_details.last_name,
#         }
#     )
#     context['form'] = form
#     return render(request, 'blog/edit_profile.html', context)


def search_view(request):
    if request.user.is_authenticated:
        search_listing = PropertyListing.objects.all().exclude(owner=request.user)
    else:
        search_listing = PropertyListing.objects.all()

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            search_listing = search_listing.filter(city__iexact = city)

    if 'type' in request.GET:
        type = request.GET['type']
        if type:
            search_listing = search_listing.filter(types__iexact = type)

    if 'minprice' in request.GET:
        minprice = request.GET['minprice']
        if minprice:
            search_listing = search_listing.filter(price__gte = minprice)

    if 'maxprice' in request.GET:
        maxprice = request.GET['maxprice']
        if maxprice:
            search_listing = search_listing.filter(price__lte = maxprice)

    context = {"search_listing": search_listing}
    return render(request, "search.html", context)


def sell_search_view(request):
    if request.user.is_authenticated:
        search_listing = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).exclude(owner=request.user)
    else:
        search_listing = PropertyListing.objects.filter(Q(types='S') | Q(types='B'))

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            search_listing = search_listing.filter(city__iexact = city)

    if 'minprice' in request.GET:
        minprice = request.GET['minprice']
        if minprice:
            search_listing = search_listing.filter(price__gte = minprice)

    if 'maxprice' in request.GET:
        maxprice = request.GET['maxprice']
        if maxprice:
            search_listing = search_listing.filter(price__lte = maxprice)

    context = {"search_listing": search_listing}
    return render(request, "search.html", context)


def rent_search_view(request):
    if request.user.is_authenticated:
        search_listing = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).exclude(owner=request.user)
    else:
        search_listing = PropertyListing.objects.filter(Q(types='R') | Q(types='B'))

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            search_listing = search_listing.filter(city__iexact = city)

    if 'minprice' in request.GET:
        minprice = request.GET['minprice']
        if minprice:
            search_listing = search_listing.filter(price__gte = minprice)

    if 'maxprice' in request.GET:
        maxprice = request.GET['maxprice']
        if maxprice:
            search_listing = search_listing.filter(price__lte = maxprice)

    context = {"search_listing": search_listing}
    return render(request, "search.html", context)


def t1_search_view(request):
    if request.user.is_authenticated:
        search_listing = PropertyListing.objects.filter(stay='H').exclude(owner=request.user)
    else:
        search_listing = PropertyListing.objects.filter(stay='H')

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            search_listing = search_listing.filter(city__iexact = city)

    if 'type' in request.GET:
        type = request.GET['type']
        if type:
            search_listing = search_listing.filter(types__iexact = type)

    if 'minprice' in request.GET:
        minprice = request.GET['minprice']
        if minprice:
            search_listing = search_listing.filter(price__gte = minprice)

    if 'maxprice' in request.GET:
        maxprice = request.GET['maxprice']
        if maxprice:
            search_listing = search_listing.filter(price__lte = maxprice)

    context = {"search_listing": search_listing}
    return render(request, "search.html", context)


def t2_search_view(request):
    if request.user.is_authenticated:
        search_listing = PropertyListing.objects.filter(stay='A').exclude(owner=request.user)
    else:
        search_listing = PropertyListing.objects.filter(stay='A')

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            search_listing = search_listing.filter(city__iexact = city)

    if 'type' in request.GET:
        type = request.GET['type']
        if type:
            search_listing = search_listing.filter(types__iexact = type)

    if 'minprice' in request.GET:
        minprice = request.GET['minprice']
        if minprice:
            search_listing = search_listing.filter(price__gte = minprice)

    if 'maxprice' in request.GET:
        maxprice = request.GET['maxprice']
        if maxprice:
            search_listing = search_listing.filter(price__lte = maxprice)

    context = {"search_listing": search_listing}
    return render(request, "search.html", context)


def type1_view(request):
    context = {}
    if request.user.is_authenticated:
        property_listings_t1 = PropertyListing.objects.filter(
            stay='H').exclude(owner=request.user)
        latitudes = PropertyListing.objects.filter(stay='H').values_list('latitude').exclude(owner=request.user)
        longitudes = PropertyListing.objects.filter(stay='H').values_list('longitude').exclude(owner=request.user)
        slug = PropertyListing.objects.filter(stay='H').values_list('slug').exclude(owner=request.user)
    else:
        property_listings_t1 = PropertyListing.objects.filter(stay='H')
        latitudes = PropertyListing.objects.filter(stay='H').values_list('latitude')
        longitudes = PropertyListing.objects.filter(stay='H').values_list('longitude')
        slug = PropertyListing.objects.filter(stay='H').values_list('slug')
    cities = PropertyListing.objects.all().values_list('city', flat=True).distinct()
    lat= []
    lon = []
    slugs = []
    for i in latitudes:
        lat +=[i[0]]
    for i in longitudes:
        lon +=[i[0]]
    for i in slug:
        slugs+=[i[0]]
    context = {"property_listings_t1": property_listings_t1,
               "cities": cities, "type_choices":type_choices, "price_choices":price_choices,"lat":lat, "lon":lon,"slug":slugs,
               "values":request.GET}
    print(lat)
    print(lon)
    print(property_listings_t1)
    return render(request, "type1.html", context)


def type2_view(request):
    context = {}
    if request.user.is_authenticated:
        property_listings_t2 = PropertyListing.objects.filter(
            stay='A').exclude(owner=request.user)
        latitudes = PropertyListing.objects.filter(stay='A').values_list('latitude').exclude(owner=request.user)
        longitudes = PropertyListing.objects.filter(stay='A').values_list('longitude').exclude(owner=request.user)
        slug = PropertyListing.objects.filter(stay='A').values_list('slug').exclude(owner=request.user)
    else:
        property_listings_t2 = PropertyListing.objects.filter(stay='A')
        latitudes = PropertyListing.objects.filter(stay='A').values_list('latitude')
        longitudes = PropertyListing.objects.filter(stay='A').values_list('longitude')
        slug = PropertyListing.objects.filter(stay='A').values_list('slug')
    cities = PropertyListing.objects.all().values_list('city', flat=True).distinct()
    lat= []
    lon = []
    slugs = []
    for i in latitudes:
        lat +=[i[0]]
    for i in longitudes:
        lon +=[i[0]]
    for i in slug:
        slugs+=[i[0]]
    context = {"property_listings_t2": property_listings_t2,
               "cities": cities, "type_choices":type_choices, "price_choices":price_choices,"lat":lat, "lon":lon,"slug":slugs,
               "values":request.GET}
    return render(request, "type2.html", context)


def rent_view(request):
    context = {}
    if request.user.is_authenticated:
        property_listings_r1 = PropertyListing.objects.filter(
            Q(types='R') | Q(types='B')).exclude(owner=request.user)
        latitudes = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).values_list('latitude').exclude(owner=request.user)
        longitudes = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).values_list('longitude').exclude(owner=request.user)
        slug = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).values_list('slug').exclude(owner=request.user)

    else:
        property_listings_r1 = PropertyListing.objects.filter(
            Q(types='R') | Q(types='B'))
        latitudes = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).values_list('latitude')
        longitudes = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).values_list('longitude')
        slug = PropertyListing.objects.filter(Q(types='R') | Q(types='B')).values_list('slug')

    cities = PropertyListing.objects.all().values_list('city', flat=True).distinct()
    lat= []
    lon = []
    slugs = []
    for i in latitudes:
        lat +=[i[0]]
    for i in longitudes:
        lon +=[i[0]]
    for i in slug:
        slugs+=[i[0]]
    context = {"property_listings_r1": property_listings_r1,
               "cities": cities, "type_choices":type_choices, "price_choices":price_choices,"lat":lat,"lon":lon,"slug":slugs,
               "values":request.GET}
    return render(request, "rent.html", context)


def sell_view(request):
    context = {}
    if request.user.is_authenticated:
        property_listings_s1 = PropertyListing.objects.filter(
            Q(types='S') | Q(types='B')).exclude(owner=request.user)
        latitudes = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).values_list('latitude').exclude(owner=request.user)
        longitudes = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).values_list('longitude').exclude(owner=request.user)
        slug = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).values_list('slug').exclude(owner=request.user)

    else:
        property_listings_s1 = PropertyListing.objects.filter(
            Q(types='S') | Q(types='B'))
        latitudes = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).values_list('latitude')
        longitudes = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).values_list('longitude')
        slug = PropertyListing.objects.filter(Q(types='S') | Q(types='B')).values_list('slug')

    cities = PropertyListing.objects.all().values_list('city', flat=True).distinct()
    lat= []
    lon = []
    slugs = []
    for i in latitudes:
        lat +=[i[0]]
    for i in longitudes:
        lon +=[i[0]]
    for i in slug:
        slugs+=[i[0]]
    context = {"property_listings_s1": property_listings_s1,
               "cities": cities, "type_choices":type_choices, "price_choices":price_choices,"lat":lat,"lon":lon,"slug":slugs,
               "values":request.GET}
    return render(request, "sell.html", context)



def city_view(request, city):
    context = {}
    if request.user.is_authenticated:
        city_props = PropertyListing.objects.filter(
            city=city).exclude(owner=request.user)
    else:
        city_props = PropertyListing.objects.filter(city=city)
    cities = PropertyListing.objects.all().values_list('city', flat=True).distinct()
    props_count = city_props.count()
    context['cities'] = cities
    context['props_count'] = props_count
    return render(request, "city.html", context)


def city_props(request, city):
    context = {}
    if request.user.is_authenticated:
        city_props = PropertyListing.objects.filter(
            city=city).exclude(owner=request.user)
    else:
        city_props = PropertyListing.objects.filter(city=city)
    context['city_props'] = city_props
    return render(request, "city_props.html", context)


def must_authenticate_view(request):
    return render(request, 'must_authenticate.html', {})
