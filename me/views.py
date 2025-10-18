import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class ProfileView(View):
    """
    View to handle GET requests for profile endpoint
    """
    
    def get(self, request):
        """
        Returns user profile with dynamic cat fact
        """
        try:
            # Get current UTC timestamp in ISO 8601 format
            timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            
            # Fetch cat fact from external API
            fact = self._fetch_cat_fact()
            
            # Prepare response data
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
            
            logger.info(f"Profile request served at {timestamp}")
            return JsonResponse(response_data, status=200)
            
        except Exception as e:
            logger.error(f"Unexpected error in profile endpoint: {e}")
            return JsonResponse({
                "status": "error",
                "message": "Internal server error"
            }, status=500)
    
    def _fetch_cat_fact(self):
        """
        Fetch random cat fact from Cat Facts API
        Returns fallback fact if API call fails
        """
        try:
            response = requests.get(
                "https://catfact.ninja/fact",
                timeout=settings.CAT_FACT_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return data.get("fact", settings.FALLBACK_FACT)
            
        except requests.Timeout:
            logger.error("Cat Facts API timeout")
            return f"{settings.FALLBACK_FACT} (API timeout)"
            
        except requests.RequestException as e:
            logger.error(f"Cat Facts API request failed: {e}")
            return f"{settings.FALLBACK_FACT} (API unavailable)"
            
        except Exception as e:
            logger.error(f"Unexpected error fetching cat fact: {e}")
            return settings.FALLBACK_FACT

class HealthCheckView(View):
    """
    Health check endpoint
    """
    
    def get(self, request):
        return JsonResponse({
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        })