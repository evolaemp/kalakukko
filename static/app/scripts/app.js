/**
 * The god object.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires app.*
 */
var app = (function() {
	
	"use strict";
	
	
	/**
	 * Class definition for the global controller.
	 * 
	 * @class
	 */
	var App = function() {
		var self = this;
		
		self.map = null;
	};
	
	/**
	 * Common AJAX setup.
	 */
	App.prototype.ajax = {
		init: function() {
			var self = this;
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
					if(!this.crossDomain) {
						xhr.setRequestHeader(
							'X-CSRFToken',
							self.utils.getCookie('csrftoken')
						);
					}
				},
				contentType: 'application/json; charset=UTF-8',
				dataType: 'json'
			});
		}
	};
	
	/**
	 * Various utils.
	 */
	App.prototype.utils = {
		
		/**
		 * Gives cookies.
		 * 
		 * @param The cookie's name.
		 * @see https://docs.djangoproject.com/en/1.8/ref/csrf/#ajax
		 */
		getCookie: function(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
	};
	
	
	/**
	 * Init (before DOM ready).
	 */
	var appInstance = new App();
	
	
	/**
	 * Init (after DOM ready).
	 */
	$(document).ready(function() {
		appInstance.ajax.init();
		
		/* app.maps */
		var domQuery = $('[data-maps=map]');
		if(domQuery.length) {
			domQuery.each(function() {
				appInstance.map = new app.maps.Map($(this));
				
				var i, language = null;
				for(i = 0; i < LANGUAGES.length; i++) {
					language  = LANGUAGES[i];
					appInstance.map.addMarker(
						language.iso_639_3,
						language.latitude,
						language.longitude
					);
				}
			});
		}
	});
	
	
	/**
	 * Module exports.
	 */
	return {
		getMap: function() {
			return appInstance.map;
		},
		utils: appInstance.utils
	};
	
}());
