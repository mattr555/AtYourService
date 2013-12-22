from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def process_request(self, request):
        """
        tz = request.session.get('django_timezone')
        if tz:
            timezone.activate(tz)
        elif request.user and not request.user.is_anonymous():
            if request.user.user_profile.timezone:
                tz = pytz.timezone(request.user.user_profile.timezone)
                request.session['django_timezone'] = tz
                timezone.activate(tz)
        else:
            timezone.deactivate()
        """
        pass
