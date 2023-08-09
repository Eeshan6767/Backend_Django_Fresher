from django.urls import path
from .views import authenticate, whatsapp, shortenURL, sms


urlpatterns = [
    path("", authenticate.Register.as_view() , name="login"),
    path("register", authenticate.Register.as_view() , name="register"),
    path("login", authenticate.Login.as_view() , name="login"),
    path("getUserData", authenticate.EntrySuccessful.as_view(), name="entrySuccessful"),
    path("whatsapp", whatsapp.WhatsappAPI.as_view(), name='whatsapp'),
    path("shorten_url", shortenURL.ShortenURL.as_view(), name='shortner-url'),
    path("sms", sms.SMS.as_view(), name='sms')
]