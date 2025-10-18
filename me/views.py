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
    
class APIDocumentationView(View):
    """
    API Documentation View
    Provides comprehensive documentation for the API endpoints in JSON format
    """
    
    def get(self, request):
        base_url = f"http://{request.get_host()}"
        
        documentation = {
            "api_name": "Profile API",
            "version": "1.0.0",
            "description": "Dynamic Profile Endpoint with Cat Facts Integration",
            "base_url": base_url,
            "endpoints": {
                "profile": {
                    "path": "/me",
                    "method": "GET",
                    "description": "Returns user profile information with a dynamic cat fact",
                    "authentication": "None",
                    "parameters": "None",
                    "request_example": f"curl -X GET {base_url}/me",
                    "response_format": {
                        "status": "string (always 'success')",
                        "user": {
                            "email": "string",
                            "name": "string", 
                            "stack": "string"
                        },
                        "timestamp": "string (ISO 8601 UTC format)",
                        "fact": "string (random cat fact)"
                    },
                    "example_response": {
                        "status": "success",
                        "user": {
                            "email": getattr(settings, 'USER_EMAIL', 'your.email@example.com'),
                            "name": getattr(settings, 'USER_NAME', 'Your Full Name'),
                            "stack": getattr(settings, 'USER_STACK', 'Python/Django')
                        },
                        "timestamp": "2024-01-15T10:30:00.123Z",
                        "fact": "Cats can jump up to 6 times their length."
                    }
                },
                "health": {
                    "path": "/health", 
                    "method": "GET",
                    "description": "Health check endpoint",
                    "authentication": "None",
                    "parameters": "None",
                    "request_example": f"curl -X GET {base_url}/health",
                    "response_format": {
                        "status": "string",
                        "timestamp": "string (ISO 8601 UTC format)"
                    },
                    "example_response": {
                        "status": "healthy",
                        "timestamp": "2024-01-15T10:30:00.123Z"
                    }
                }
            },
            "external_integrations": {
                "cat_facts_api": {
                    "endpoint": "https://catfact.ninja/fact",
                    "description": "Fetches random cat facts",
                    "timeout": f"{getattr(settings, 'CAT_FACT_TIMEOUT', 5)} seconds",
                    "fallback": getattr(settings, 'FALLBACK_FACT', 'Cats are amazing creatures.')
                }
            },
            "error_handling": {
                "cat_facts_api_failure": "Returns fallback fact with error indication",
                "server_errors": "Returns 500 status with error message",
                "timeouts": "Handled with 5-second timeout"
            },
            "testing": {
                "profile_endpoint": f"{base_url}/me",
                "health_endpoint": f"{base_url}/health"
            },
            "specifications": {
                "timestamp_format": "ISO 8601 UTC",
                "content_type": "application/json",
                "cors": "Enabled for all origins"
            }
        }
        
        return JsonResponse(documentation)