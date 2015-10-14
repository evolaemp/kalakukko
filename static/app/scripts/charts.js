/**
 * Handles the chart making.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires chartist
 */
app.charts = (function() {
	
	"use strict";
	
	
	/**
	 * Class definition for correlation charts.
	 * 
	 * @class
	 * @param The chart container as a jQuery element.
	 */
	var Chart = function(dom) {
		var self = this;
		
		self.dom = dom;
		self.chart = null;
		self.tooltip = null;
	};
	
	/**
	 * Draws the chart with the data given.
	 * 
	 * @param The points in {name: [x, y]} format.
	 * @return Promise that the chart is drawn.
	 */
	Chart.prototype.draw = function(d) {
		var self = this;
		var deferred = $.Deferred();
		
		var data = [];
		
		for(var key in d) {
			data.push({
				meta: key,
				x: d[key][0],
				y: d[key][1]
			});
		}
		
		/**
		 * Chartist throws an error with series: [[]].
		 */
		if(data.length) {
			data = [data];
		}
		
		self.chart = new Chartist.Line(
			self.dom.get(0),
			{
				series: data
			},
			{
				axisX: {
					type: Chartist.AutoScaleAxis,
					low: 0,
					high: 1,
					scaleMinSpace: 50,
					showLabel: false,
					offset: 0
				},
				axisY: {
					type: Chartist.AutoScaleAxis,
					low: 0,
					high: 1,
					scaleMinSpace: 50,
					showLabel: false,
					offset: 0
				},
				chartPadding: {
					bottom: 15,
					left: 15,
					right: 15,
					top: 15
				},
				showLine: false
			}
		);
		
		self.chart.on('created', function() {
			self.initTooltip();
			deferred.resolve();
		});
		
		return deferred.promise();
	};
	
	/**
	 * Creates tooltip with more info on hover.
	 * For the tooltip to work properly, self.dom should be with position
	 * relative or absolute.
	 */
	Chart.prototype.initTooltip = function() {
		var self = this;
		
		self.tooltip = $('<div class="tooltip"></div>');
		self.tooltip.appendTo(self.dom);
		self.tooltip.hide();
		
		self.dom.on('mouseenter', '.ct-point', function() {
			var point = $(this);
			var text = '';
			
			text += point.attr('ct:meta');
			text += '<br />';
			text += point.attr('ct:value').replace(',', '; ');
			
			self.tooltip.html(text).show();
		});
		
		self.dom.on('mouseleave', '.ct-point', function() {
			self.tooltip.hide();
		});
		
		self.dom.on('mousemove', function(e) {
			self.tooltip.css({
				left: (e.offsetX || e.originalEvent.layerX) - self.tooltip.width() / 2 - 10,
				top: (e.offsetY || e.originalEvent.layerY) - self.tooltip.height() - 12
			});
		});
	};
	
	/**
	 * Destroys the chart.
	 */
	Chart.prototype.destroy = function() {
		var self = this;
		
		self.chart.detach();
		self.dom.empty();
		
		self.chart = null;
		self.tooltip = null;
	};
	
	
	/**
	 * Module exports.
	 */
	return {
		Chart: Chart
	};
	
}());
