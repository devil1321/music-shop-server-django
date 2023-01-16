from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Track, Price
from django.template.loader import render_to_string
import stripe

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]
        line_items = stripe.checkout.Session.list_line_items(session["id"])
        stripe_price_id = line_items["data"][0]["price"]["id"]
        items = []
        for item in line_items['data']:
            track = Track.objects.get(price_id = stripe_price_id)
            items.append({'name':track.title,'price':track.price,'image':track.image})

        send_mail(
            subject='Your order has been completed',
            message=render_to_string('email.html',{'items':items}),
            from_email='music_shop@foscoalma.com',
            recipient_list=[customer_email],
            fail_silently=False,
        )

    return HttpResponse(status=200)