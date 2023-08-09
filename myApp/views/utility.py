from django.conf import settings

def header():
    return {
                "api-key": settings.API_KEY,
                "Content-Type": "application/json"
        }