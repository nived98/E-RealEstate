from django.urls import path
from payments.views import(
    buy_property_view,
    payment_done,
    payment_canceled,
    make_property_premium,
    blockchain_ledger,
    invoice
)

app_name = "payments"

urlpatterns = [
    path('invoices/<slug>/', invoice, name="invoices"),
    path('blockchain/', blockchain_ledger, name="ledger"),
    path('<slug>/buy', buy_property_view, name="buy"),
    path('<slug>/premium/', make_property_premium, name='premium'),
    path('done/<slug>/', payment_done, name="done"),
    path('canceled/', payment_canceled, name="canceled"),
]
