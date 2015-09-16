from django.contrib import admin

from app.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
	list_display = (
		'iso_639_3', 'iso_639_1',
		'latitude', 'longitude',
	)
	search_fields = ('iso_639_3', 'iso_639_1', )



