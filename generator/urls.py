from django.urls import path
from .views import PortfolioFormView, home

urlpatterns = [
    path("portfolio/", PortfolioFormView.as_view(), name="portfolio-form"),
    path("", home, name="home"),
]
