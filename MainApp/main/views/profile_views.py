from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View


@method_decorator(login_required, name='dispatch')
class ProtectedView(View):
    pass
