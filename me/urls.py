from django.urls import path
from .views import ProfileView, HealthView, APIDocumentationView

urlpatterns = [
    path('me', ProfileView.as_view()),
    path('health', HealthView.as_view()),
    
    path('', APIDocumentationView.as_view(), name='docs'),  # Root URL for documentation
    path('docs', APIDocumentationView.as_view(), name='docs'),

]