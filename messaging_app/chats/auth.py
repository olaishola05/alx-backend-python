from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission

class CustomHeaderAuth(BaseAuthentication):
  def authenticate(self, request):
    username = request.headers.get('X-Username')
    if not username:
      return None
    
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      raise AuthenticationFailed('No such user')
    
    return (user, None)
  
def get_tokens_for_user(user):
  token = RefreshToken.for_user(user)
  return {
    'refresh': str(token),
    'access': str(token.access_token)
  }
  
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user