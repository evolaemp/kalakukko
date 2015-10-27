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
		self.charts = {};
		
		/**
		 * Fired upon receiving 404 from the server.
		 */
		self.received404 = new signals.Signal();
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
					latitude, longitude, parameter,
					data.d, data.p
				);
			}
			else {
				self.addPointOfNearest(
					latitude, longitude, parameter,
					data.origin, data.d, data.p
				);
			}
		})
		.fail(function(xhr) {
			var error = "Could not connect to server!";
			try {
				error = xhr.responseJSON.error;
			} catch (e) {}
			app.messages.error(error);
			
			if(xhr.status == 404) {
				self.received404.dispatch();
			}
		});
	};
	
	/**
	 * Adds point with method = 'radius'.
	 * 
	 * @param The latitude of the circle's centre.
	 * @param The longitude of the circle's centre.
	 * @param The radius in kilometres.
	 * @param The languages in {id: [global, real]} format.
	 * @param The swadeshness.
	 */
	PointMode.prototype.addPointOfCircle = function(latitude, longitude, radius, d, swadeshness) {
		var self = this;
		
		var point = {type: 'circle', id: self.points.length};
		
		self.map.addPoint(point.id, latitude, longitude);
		self.map.addCircle(point.id, latitude, longitude, radius);
		
		var languages = [], key = null, i = null;
		for(key in d) {
			key = key.split(',');
			if(key.length != 2) {
				continue;
			}
			for(i in [0, 1]) {
				if(languages.indexOf(key[i]) == -1) {
					languages.push(key[i]);
				}
			}
		}
		
		for(i = 0; i < languages.length; i++) {
			self.map.highlightLanguage(languages[i], 2);
		}
		
		var div = self.map.addDraggable(point.id);
		self.addChart(point.id, div, d, swadeshness);
		
		self.points.push(point);
	};
	
	/**
	 * Adds point with method = 'nearest'.
	 * 
	 * @param The latitude of the circle's centre.
	 * @param The longitude of the circle's centre.
	 * @param The k parameter.
	 * @param The ID of the origin language.
	 * @param The languages in {id: [global, real]} format.
	 * @param The swadeshness.
	 */
	PointMode.prototype.addPointOfNearest = function(latitude, longitude, k, origin, d, swadeshness) {
		var self = this;
		
		var point = {type: 'neighbourhood', id: self.points.length};
		
		self.map.addPoint(point.id, latitude, longitude);
		
		self.map.highlightLanguage(origin, 1);
		
		for(var languageId in d) {
			self.map.highlightLanguage(languageId, 2);
		}
		
		var div = self.map.addDraggable(point.id);
		self.addChart(point.id, div, d, swadeshness);
		
		self.points.push(point);
	};
	
	/**
	 * Creates a chart.
	 * 
	 * @param The ID of the chart (internal for PointMode).
	 * @param jQuery instance of the chart container.
	 * @param The data to populate the chart with.
	 * @param The swadeshness.
	 */
	PointMode.prototype.addChart = function(id, dom, d, swadeshness) {
		var self = this;
		
		$('<div class="swadeshness"></div>')
			.html(swadeshness)
			.appendTo(dom);
		
		$('<div class="chart"></div>')
			.appendTo(dom);
		
		var chart = new app.charts.Chart(dom.find('.chart'));
		chart.draw(d);
		
		self.charts[id] = chart;
	};
	
	/**
	 * Clears the map from the mode's annotations.
	 */
	PointMode.prototype.clearMap = function() {
		var self = this;
		var key = null;
		
		/* clear all charts */
		for(key in self.charts) {
			self.charts[key].destroy();
		}
		self.charts = {};
		
		/* clear all objects on the map */
		for(key in self.points) {
			if(self.points[key].type == 'circle') {
				self.map.removeCircle(self.points[key].id);
				self.map.removePoint(self.points[key].id);
				self.map.removeDraggable(self.points[key].id);
			}
			else {
				self.map.removePoint(self.points[key].id);
				self.map.removeDraggable(self.points[key].id);
			}
		}
		self.points = [];
		
		/* remove language highlighting */
		self.map.lowlightAll();
	};
	
	/**
	 * Hook for removing the mode's signal handlers.
	 */
	PointMode.prototype.unbind = function() {
		var self = this;
		self.received404.removeAll();
		self.map.clicked.removeAll();
		self.clearMap();
	};
	
	
	/**
	 * Handles the state when the honeycomb is requested.
	 * 
	 * @class
	 * 
	 * @param The file ID.
	 * @param The method select.
	 * @param The parameter input.
	 */
	var HoneycombMode = function(fileId, methodSelect, parameterInput) {
		var self = this;
		self.fileId = fileId;
		
		self.methodSelect = methodSelect;
		self.parameterInput = parameterInput;
		
		/**
		 * Prevents drawing the wrong honeycomb.
		 * Keeps the first cell of the currently awaited honeycomb.
		 */
		self.firstCell = [null, null];
		
		/**
		 * Fired upon receiving 404 from the server.
		 */
		self.received404 = new signals.Signal();
	};
	
	/**
	 * Hooks for adding the mode's signal handlers.
	 * 
	 * @param The map.
	 */
	HoneycombMode.prototype.bind = function(map) {
		var self = this;
		
		self.map = map;
		
		self.map.changedViewport.add(self.changeViewport, self);
		
		self.map.createHoneycomb();
	};
	
	/**
	 * Handles changing the viewport in honeycomb mode.
	 * 
	 * @param [] of [latitude, longitude].
	 */
	HoneycombMode.prototype.changeViewport = function(cells) {
		var self = this;
		
		app.messages.info('Loading honeycomb&hellip;');
		
		self.firstCell = cells[0];
		
		var method = self.methodSelect.getValue();
		var parameter = self.parameterInput.getValue();
		
		$.post('/api/honeycomb/', JSON.stringify({
			id: self.fileId,
			cells: cells,
			method: method,
			parameter: parameter
		}))
		.done(function(data) {
			var cells = data.cells;
			if(self.firstCell[0] == cells[0][0] && self.firstCell[1] == cells[0][1]) {
				self.map.updateHoneycomb(cells);
			}
			app.messages.clear();
		})
		.fail(function(xhr) {
			var error = "Could not connect to server!";
			try {
				error = xhr.responseJSON.error;
			} catch (e) {}
			app.messages.error(error);
			
			if(xhr.status == 404) {
				self.received404.dispatch();
			}
		});
	};
	
	/**
	 * Cools down the map to normality.
	 */
	HoneycombMode.prototype.clearMap = function() {
		var self = this;
		self.map.removeHoneycomb();
	};
	
	/**
	 * Hook for removing the mode's signal handlers.
	 */
	HoneycombMode.prototype.unbind = function() {
		var self = this;
		self.received404.removeAll();
		self.map.changedViewport.removeAll();
		self.clearMap();
	};
	
	
	/**
	 * Module exports.
	 */
	return {
		NormalMode: NormalMode,
		PointMode: PointMode,
		HoneycombMode: HoneycombMode
	};
	
}());
