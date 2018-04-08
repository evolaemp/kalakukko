from django.shortcuts import render
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
						longitude__isnull = False)

		context = {
			'languages': make_json([lang.to_dict() for lang in languages]) }

		return render(request, 'js_tests.html', context)
