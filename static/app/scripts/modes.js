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
	
	/**
	 * Hooks for adding the mode's signal handlers.
	 * 
	 * @param The map.
	 */
	NormalMode.prototype.bind = function(map) {};
	
	/**
	 * Hook for removing the mode's signal handlers.
	 */
	NormalMode.prototype.unbind = function() {};
	
	
	/**
	 * Handles the state when valid data source file is uploaded.
	 * 
	 * @class
	 * @param The file ID.
	 */
	var PointMode = function(fileId) {
		var self = this;
		self.fileId = fileId;
	};
	
	/**
	 * Hooks for adding the mode's signal handlers.
	 * 
	 * @param The map.
	 */
	PointMode.prototype.bind = function(map) {
		var self = this;
		self.map = map;
		
		self.map.clicked.add(self.click, self);
	};
	
	/**
	 * 
	 */
	PointMode.prototype.click = function(latitude, longitude) {
		var self = this;
		
		$.post('/api/point/', JSON.stringify({
			id: self.fileId,
			latitude: latitude,
			longitude: longitude
		}))
		.done(function(data) {
			console.log(data);
		})
		.fail(function(jqXHR) {
			var error = "Could not connect to server!";
			try {
				error = jqXHR.responseJSON.error;
			} catch (e) {}
			app.messages.error(error);
		});
	};
	
	/**
	 * Hook for removing the mode's signal handlers.
	 */
	PointMode.prototype.unbind = function() {
		var self = this;
		self.map.clicked.remove(self.click);
	};
	
	
	/**
	 * Handles the state when the heatmap is requested.
	 * 
	 * @class
	 * @param The file ID.
	 */
	var HeatMode = function(fileId) {
		var self = this;
		self.fileId = fileId;
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
