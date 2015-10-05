from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from app.views.landing import LandingView

from app.views.file_api import FileApiView
from app.views.point_api import PointApiView
from app.views.distances_api import DistancesApiView

import utils.js_tests.urls



urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/distances/([\w]+)/$', DistancesApiView.as_view(), name='distances_api'),
	url(r'^api/file/$', FileApiView.as_view(), name='file_api'),
	url(r'^api/point/$', PointApiView.as_view(), name='point_api'),
	url(r'^$', LandingView.as_view(), name='landing'),
]


if settings.DEBUG:
	urlpatterns += [
		url(r'^js_tests/', include(utils.js_tests.urls)),
	]



