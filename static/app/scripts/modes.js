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
	 * 
	 * @param The file ID.
	 * @param The method select.
	 * @param The parameter input.
	 */
	var PointMode = function(fileId, methodSelect, parameterInput) {
		var self = this;
		
		self.fileId = fileId;
		
		self.methodSelect = methodSelect;
		self.parameterInput = parameterInput;
		
		self.points = [];
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
	 * Handles map clicking in point mode.
	 * 
	 * @param The latitude of the point clicked.
	 * @param The longitude of the point clicked.
	 */
	PointMode.prototype.click = function(latitude, longitude) {
		var self = this;
		
		var method = self.methodSelect.getValue();
		var parameter = self.parameterInput.getValue();
		
		self.clearMap();
		
		$.post('/api/point/', JSON.stringify({
			id: self.fileId,
			latitude: latitude,
			longitude: longitude,
			method: method,
			parameter: parameter
		}))
		.done(function(data) {
			if(method == 'circle') {
				self.addPointOfCircle(
					latitude, longitude,
					parameter, data.d
				);
			}
			else {
				self.addPointOfNearest(
					latitude, longitude,
					parameter, data.d
				);
			}
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
	 * Adds point with method = 'radius'.
	 * 
	 * @param The latitude of the circle's centre.
	 * @param The longitude of the circle's centre.
	 * @param The radius in kilometres.
	 * @param The languages in {id: [global, real]} format.
	 */
	PointMode.prototype.addPointOfCircle = function(latitude, longitude, radius, d) {
		var self = this;
		
		var point = {type: 'circle', id: self.points.length};
		
		self.map.addPoint(point.id, latitude, longitude);
		self.map.addCircle(point.id, latitude, longitude, radius);
		
		self.points.push(point);
	};
	
	/**
	 * Adds point with method = 'nearest'.
	 * 
	 * @param The latitude of the circle's centre.
	 * @param The longitude of the circle's centre.
	 * @param The k parameter.
	 * @param The languages in {id: [global, real]} format.
	 */
	PointMode.prototype.addPointOfNearest = function(latitude, longitude, k, d) {
		var self = this;
		
		var point = {type: 'neighbourhood', id: self.points.length};
		
		self.map.addPoint(point.id, latitude, longitude);
		
		for(var languageId in d) {
			self.map.highlightLanguage(languageId);
		}
		
		self.points.push(point);
	};
	
	/**
	 * Clears the map from the mode's annotations.
	 */
	PointMode.prototype.clearMap = function() {
		var self = this;
		
		for(var key in self.points) {
			if(self.points[key].type == 'circle') {
				self.map.removeCircle(self.points[key].id);
			}
		}
	};
	
	/**
	 * Hook for removing the mode's signal handlers.
	 */
	PointMode.prototype.unbind = function() {
		var self = this;
		self.map.clicked.remove(self.click);
		self.clearMap();
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
	
	/**
	 * Hooks for adding the mode's signal handlers.
	 * 
	 * @param The map.
	 */
	HeatMode.prototype.bind = function(map) {
		var self = this;
		self.map = map;
	};
	
	/**
	 * Hook for removing the mode's signal handlers.
	 */
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