import time
import logging
from datetime import datetime

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
    