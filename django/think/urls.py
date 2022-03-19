from django.urls import path
from think.views import HomeView, IndexView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/login/', IndexView.as_view(), name='login'),
]