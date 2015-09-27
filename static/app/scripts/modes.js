/**
 * @module
 */
app.modes = (function() {
	
	"use strict";
	
	
	/**
	 * Handles the state when there is no data source file uploaded.
	 * 
	 * @class
	 */
	var NormalMode = function() {
		var self = this;
	};
	
	NormalMode.prototype.bind = function(map) {
		var self = this;
		self.map = map;
	};
	
	NormalMode.prototype.unbind = function() {
		var self = this;
	};
	
	
	/**
	 * Handles the state when valid data source file is uploaded.
	 * 
	 * @class
	 */
	var PointMode = function() {
		var self = this;
	};
	
	PointMode.prototype.bind = function(map) {
		var self = this;
		self.map = map;
	};
	
	PointMode.prototype.choose = function(languageId) {
		var self = this;
		
		$.get(
			'/api/distances/'+ languageId +'/'
		)
		.done(function(data) {
			self.map.turnHeatOn(languageId, data.distances);
		})
		.fail(function(jqXHR) {
			var error = "Could not connect to server!";
			try {
				error = jqXHR.responseJSON.error;
			} catch (e) {}
			app.messages.error(error);
		});
	};
	
	PointMode.prototype.unbind = function() {
		var self = this;
	};
	
	
	/**
	 * Handles the state when the heatmap is requested.
	 * 
	 * @class
	 */
	var HeatMode = function() {
		var self = this;
	};
	
	HeatMode.prototype.bind = function(map) {
		var self = this;
		self.map = map;
	};
	
	HeatMode.prototype.unbind = function() {
		var self = this;
	};
	
	
	/**
	 * Module exports.
	 */
	return {
		NormalMode: NormalMode,
		PointMode: PointMode,
		HeatMode: HeatMode
	};
	
}());
