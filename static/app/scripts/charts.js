/**
 * Handles the charts making.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires signals
 */
app.charts = (function() {
	
	"use strict";
	
	
	/**
	 * Class definition for charts.
	 * 
	 * @class
	 * @param The chart container as a jQuery element.
	 */
	var Chart = function(dom) {
		var self = this;
		self.dom = dom;
	};
	
	/**
	 * Draws the points given.
	 * 
	 * @param The points in {name: [x, y]} format.
	 */
	Chart.prototype.drawPoints = function(d) {
		var self = this;
		console.log(d);
	};
	
	
	/**
	 * Module exports.
	 */
	return {
		Chart: Chart
	};
	
}());
