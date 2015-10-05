from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import TemplateView

from utils.js_tests.views import JsTestsView


urlpatterns = [
	url(r'^$', JsTestsView.as_view()),
]

urlpatterns += static('qunit', document_root=settings.QUNIT_ROOT)
urlpatterns += static('/', document_root=settings.JS_TESTS_ROOT)

