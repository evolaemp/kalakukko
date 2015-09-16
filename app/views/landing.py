from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View


class LandingView(View):
	def get(self, request):
		"""
		Renders the landing page.
		"""
		return render_to_response(
			'landing.html',
			{
			},
			context_instance = RequestContext(request)
		)



