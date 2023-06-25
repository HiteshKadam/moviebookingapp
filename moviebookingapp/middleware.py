import time
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session = request.session
            last_activity = session.get('last_activity')
            current_timestamp = int(time.time())
            if last_activity is None or (current_timestamp - last_activity) > settings.SESSION_EXPIRE_SECONDS:
                # Session has expired, log out the user
                auth.logout(request)
                # Redirect to the login page or any other appropriate page
                return HttpResponseRedirect(reverse('login'))

            # Update the last activity timestamp
            session['last_activity'] = current_timestamp

        response = self.get_response(request)
        return response
