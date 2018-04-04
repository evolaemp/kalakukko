from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View

from app.models import Language
from utils.json import make_json



class LandingView(View):

	@method_decorator(ensure_csrf_cookie)
	def dispatch(self, *args, **kwargs):
		"""
		Ensures sending of csrf cookie.
		"""
		return super(LandingView, self).dispatch(*args, **kwargs)


	def get(self, request):
		"""
		Renders the landing page.
		"""
		languages = Language.objects.filter(
			latitude__isnull = False,
			longitude__isnull = False)

		context = {
			'languages': make_json([lang.to_dict() for lang in languages]),
			'OSM_ACCESS_TOKEN': settings.OSM_ACCESS_TOKEN,
			'OSM_ID': settings.OSM_ID }

		return render(request, 'landing.html', context)
