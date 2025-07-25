import time
import logging
from datetime import datetime, time as t
from rest_framework import status

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