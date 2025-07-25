import time
import logging
from datetime import datetime, time as t, timedelta
from rest_framework import status
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.core.cache import cache

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
  """
  A simple middleware for logging each user requests to a file, including the timestamp, user and the request path.
  """
  def __init__(self, get_response):
    """
      This runs once when Django starts up.
      get_response is a function that represents the next step in the chain.
    """
    self.get_response = get_response
    
  def __call__(self, request):
    """
    This runs for every request
    """
    
    start_time = time.time()
    
    logger.info(f"📥 Incoming request: {request.method} {request.path}")
    logger.info(f"👤 User: {request.user if hasattr(request, 'user') else 'Anonymous'}")
    
    response = self.get_response(request)
    
    end_time = time.time()
    duration = end_time - start_time
        
    # Add custom headers to the response
    response['X-Response-Time'] = f"{duration:.3f}s"
    response['X-Custom-Header'] = 'Processed by RequestLoggingMiddleware'
    response['X-Django-Rocks'] = 'Yes!'
        
    # Log the response
    logger.info(f"📤 Response: {response.status_code} ({duration:.3f}s)")
    logger.info(f"{datetime.now()} - User: {request.user if hasattr(request, 'user') else 'Anonymous'} - Path: {request.path}")
    
    return response
  
  
  class RestrictAccessByTimeMiddleware:
    """
    A middleware that restricts access to the messaging up during certain hours of the day
    """
    
    def __init__(self, get_response):
      self.get_response = get_response
      
    def __call__(self, request):
      
      if not check_access_time():
        if request.path == request.path.endswith('/messages/'):
          request.status_code = status.HTTP_403_FORBIDDEN
      response = self.get_response(request)
      request.status_code = status.HTTP_200_OK
      
      return response
        
class OffensiveLanguageMiddleware:
  """
  Middleware that limits the number of chat messages a user can send within a certain time window, based on their IP address
  """
  def __init__(self, get_response) -> None:
     self.get_response = get_response
     
  def __call__(self, request):
      if request.user._is_authenticated and request.method == 'POST':
          identifier = f"user_{request.user.user_id}-ip{self.get_client_ip(request=request)}"
      else:
          identifier = f"ip_{self.get_client_ip(request=request)}"
          
      if not identifier:
          return self.get_response(request)
      
                  
      cache_key = f"rate_limit{identifier}"
      request_timestamps = cache.get(cache_key, [])
      
      current_time = datetime.now()
      time_window_start = current_time - timedelta(minutes=1)
      recent_timestamps = [ts for ts in request_timestamps if ts > time_window_start]
      
      recent_timestamps.append(current_time)
      
      MAX_MESSAGES_PER_MINUTE = 5
      
      if len(recent_timestamps) > MAX_MESSAGES_PER_MINUTE:
          return HttpResponseForbidden("You have exceeded the message limit. Please wait a minute before sending more messages.")
      else:
          cache.set(cache_key, recent_timestamps, timeout=65)
          
      response = self.get_response(request)
      return response
     
   
  def get_client_ip(self, request):
     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
     if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
     return request.META.get('REMOTE_ADDR')

class RolepermissionMiddleware:
    """
    A middleware that checks the user’s role i.e admin, before allowing access to specific actions
    """
    
    def __init__(self, get_response) -> None:
       self.get_response = get_response
       
    def __call__(self, request):
       if not request.user.is_authenticated:
           return HttpResponseNotAllowed("Unathenticated user, action not allowed")
       privilege_roles = ['admin', 'moderator']
       if not request.user.groups.filter(name__in=privilege_roles):
           return HttpResponseForbidden("You have exceeded the message limit. Please wait a minute before sending more messages.")
       
       response = self.get_response(request)
       return response

def check_access_time():
    """
    Checks if the current time is within the allowed access window.
    The allowed time is between 6 PM and 9 PM.
    """
    now = datetime.now()
    current_time = now.time()

    # Define the allowed time window
    start_time = t(18, 0, 0)  # 6 PM
    end_time = t(21, 0, 0)    # 9 PM

    if start_time <= current_time <= end_time:
        print("Access granted. Welcome!")
        return True
    else:
        print("Access denied. The chat is only available between 6 PM and 9 PM.")
        return False