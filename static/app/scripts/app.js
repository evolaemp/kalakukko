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
	 * Common AJAX setup.
	 */
	var ajax = {
		init: function() {
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
					if(!this.crossDomain) {
						xhr.setRequestHeader(
							'X-CSRFToken',
							utils.getCookie('csrftoken')
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
	var utils = {
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
	var mapInstance = null;
	
	
	/**
	 * Init (after DOM ready).
	 */
	$(document).ready(function() {
		ajax.init();
		
		/* app.maps */
		var domQuery = $('[data-maps=map]');
		if(domQuery.length) {
			domQuery.each(function() {
				mapInstance = new app.maps.Map($(this), LANGUAGES);
			});
		}
	});
	
	
	/**
	 * Module exports.
	 */
	return {
		getMap: function() {
			return mapInstance;
		},
		utils: utils
	};
	
}());
