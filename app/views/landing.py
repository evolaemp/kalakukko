from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View

from app.models import Language
from utils.json import make_json


class LandingView(View):
	def get(self, request):
		"""
		Renders the landing page.
		"""
		languages = Language.objects.filter(
			latitude__isnull = False,
			longitude__isnull = False
		)
		
		return render_to_response(
			'landing.html',
			{
				'languages': make_json(
					[language.to_dict() for language in languages]
				),
				'OSM_ACCESS_TOKEN': settings.OSM_ACCESS_TOKEN,
				'OSM_ID': settings.OSM_ID
			},
			context_instance = RequestContext(request)
		)



