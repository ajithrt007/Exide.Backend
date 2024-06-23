from functools import wraps
from django.http import HttpResponseForbidden
import time
from django.core.cache import cache

def limit_post_submissions(rate_limit=10, time_window=3600):
    """
    Decorator to limit the number of POST requests from an IP address.
    
    rate_limit: Number of allowed submissions in the given time window.
    time_window: Time window in seconds within which the submissions are counted.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == "POST":
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
                cache_key = f"ip_{ip}"
                submission_info = cache.get(cache_key)

                if submission_info:
                    count, last_submission_time = submission_info
                    current_time = time.time()

                    if current_time - last_submission_time > time_window:
                        count = 0

                    if count >= rate_limit:
                        return HttpResponseForbidden("Rate limit exceeded. Try again later.")

                    cache.set(cache_key, (count + 1, current_time), timeout=time_window)
                else:
                    cache.set(cache_key, (1, time.time()), timeout=time_window)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
