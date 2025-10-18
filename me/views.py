import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class ProfileView(View):
    def get(self, request):
        try:
            timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            fact = self.get_cat_fact()
            
            response_data = {
                "status": "success",
                "user": {
                    "email": settings.USER_EMAIL,
                    "name": settings.USER_NAME,
                    "stack": settings.USER_STACK
                },
                "timestamp": timestamp,
                "fact": fact
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return JsonResponse({
                "status": "error",
                "message": "Internal server error"
            }, status=500)
    
    def get_cat_fact(self):
        try:
            response = requests.get(
                "https://catfact.ninja/fact",
                timeout=settings.CAT_FACT_TIMEOUT
            )
            response.raise_for_status()
            return response.json().get("fact", settings.FALLBACK_FACT)
        except:
            return settings.FALLBACK_FACT

class HealthView(View):
    def get(self, request):
        return JsonResponse({
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        })