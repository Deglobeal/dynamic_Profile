from django.urls import path
from .views import ProfileView, HealthView

urlpatterns = [
    path('me', ProfileView.as_view()),
    path('health', HealthView.as_view()),

]