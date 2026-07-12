from django.urls import path

from . import views

app_name = "providers"

urlpatterns = [
    path("", views.home, name="home"),
    path("providers/<str:npi>/", views.provider_detail, name="detail"),
]
