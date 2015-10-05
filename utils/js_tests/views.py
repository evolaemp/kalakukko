from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View

from app.models import Language
from utils.json import make_json



class JsTestsView(View):
	def get(self, request):
		"""
		Renders the landing page.
		"""
		languages = Language.objects.filter(
			latitude__isnull = False,
			longitude__isnull = False
		)
		
		return render_to_response(
			'js_tests.html',
			{
				'languages': make_json(
					[language.to_dict() for language in languages]
				),
			},
			context_instance = RequestContext(request)
		)



