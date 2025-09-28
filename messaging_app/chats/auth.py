"""
Authentication helpers for the chats app.
We use SimpleJWT for JSON Web Token authentication.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class.
    Can be extended later for extra validation.
    """
    pass
