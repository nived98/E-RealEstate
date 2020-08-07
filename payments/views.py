import hashlib
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from property.models import PropertyListing
from property.forms import CreatePropertyListingForm, UpdatePropertyListingForm
from blog.models import UserProfile
from django.contrib.auth.models import User

from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import random
# Create your views here.
from blog.models import Invoice

from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from django.core.files.base import ContentFile
from django.utils.text import slugify


invoices = Invoice.objects.all()
length = len(invoices)
# print(invoices)
# print(length)


class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block_Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n"


class Blockchain:

    diff = 1
    maxNonce = 2**32
    target = 2 ** (256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                return(block)
                break
            else:
                block.nonce += 1


blockchain = Blockchain()


@csrf_exempt
def payment_done(request, slug, *args, **kwargs):
    context = {}
    user = request.user
    property_listings = get_object_or_404(PropertyListing, slug=slug)
    previous_owner = property_listings.owner
    property_listings.owner = user
    property_listings.save()
    print("Printing list", property_listings.price)
    context = {
        'date': datetime.date(datetime.now()),
        'property': property_listings,
        'user': user,
        'registery': property_listings.price*0.1,
        'tax': property_listings.price*0.01,
        'final': property_listings.price*1.11,
        'invoice_id': random.randint(10000, 99999)
    }
    obj = Invoice(issued_to=user, property_purchased=property_listings, date=datetime.date(datetime.now()),
                  registery=property_listings.price*.1, tax=property_listings.price*.01, final=property_listings.price*1.11, invoice_id=random.randint(10000, 99999),
                  slug=slugify(user.username + "-" + property_listings.title))
    obj.save()

    return render(request, 'done.html', context)


def blockchain_ledger(request):

    context = {}
    ledger = [0]*length
    print(invoices)
    for i in range(length):
        ledger[i] = blockchain.mine(Block(invoices[i]))

    while blockchain.head != None:
        blockchain.head = blockchain.head.next

    context['ledger'] = ledger
    return render(request, 'blockchain_ledger.html', context)


@csrf_exempt
def payment_canceled(request):
    return render(request, 'canceled.html')


def buy_property_view(request, slug):
    context = {}

    user = request.user
    property_listings = get_object_or_404(PropertyListing, slug=slug)
    paypal_dict = {
        "business": "hyp6773@gmail.com",
        "amount": property_listings.price,
        "item_name": property_listings.title,
        "invoice": property_listings.title,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payments:done', kwargs={'slug': property_listings.slug})),
        "cancel_return": request.build_absolute_uri(reverse('payments:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payments.html", context)


def make_property_premium(request, slug):
    context = {}
    user = request.user
    property_listings = get_object_or_404(PropertyListing, slug=slug)

    paypal_dict = {
        "business": "hyp6773@gmail.com",
        "amount": property_listings.price,
        "item_name": property_listings.title,
        "invoice": property_listings.title,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payments:done', kwargs={'slug': property_listings.slug})),
        "cancel_return": request.build_absolute_uri(reverse('payments:canceled')),
    }

    property_listings.premium = "Y"
    property_listings.save()

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "premium.html", context)


def invoice(request, slug):
    context = {}
    invoices = get_object_or_404(Invoice, slug=slug)
    context = {
        'date': invoices.date,
        'property': invoices.property_purchased,
        'user': invoices.issued_to,
        'registery': invoices.registery,
        'final': invoices.final,
        'invoice_id': invoices.invoice_id
    }
    return render(request, 'done.html', context)
