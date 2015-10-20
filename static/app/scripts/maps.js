/**
 * Handles the maps.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires signals
 * @requires L
 */
app.maps = (function() {
	
	"use strict";
	
	
	/**
	 * Class definition for Open Street Maps instances.
	 * 
	 * Assumes that L is present.
	 * 
	 * @class
	 * @param The map container as a jQuery element.
	 */
	var OpenStreetMap = function(dom) {
		var self = this;
		
		self.dom = dom;
		self.map = L.map(self.dom.get(0), {
			center: [42, 42],
			zoom: 5,
			zoomControl: false
		});
		
		/**
		 * Stuff on the map.
		 */
		self.markers = {};
		self.circles = {};
		self.points = {};
		self.draggables = {};
		self.honeycomb = null;
		
		/**
		 * Signals.
		 */
		self._initSignals();
	};
	
	/**
	 * Loads the tiles. Unnecessary to invoke when unit testing.
	 * Assumes that OSM_ACCESS_TOKEN and OSM_ID are present.
	 */
	OpenStreetMap.prototype.loadTiles = function() {
		var self = this;
		
		L.tileLayer(
			'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
			{
				attribution: '<a href="http://openstreetmap.org">OpenStreetMap</a>',
				accessToken: OSM_ACCESS_TOKEN,
				id: OSM_ID,
				maxZoom: 15
			}
		).addTo(self.map);
	};
	
	/**
	 * Inits the various signals that the map will emit.
	 * Purpose: to avoid making the constructor too large.
	 * 
	 * @private
	 */
	OpenStreetMap.prototype._initSignals = function() {
		var self = this;
		
		/**
		 * Fired when language marker is clicked.
		 */
		self.clickedOnLanguage = new signals.Signal();
		
		/**
		 * Fired when the map is clicked.
		 * @see app.modes.PointMode
		 */
		self.clicked = new signals.Signal();
		
		self.map.on('click', function(e) {
			self.clicked.dispatch(e.latlng.lat, e.latlng.lng);
		});
		
		/**
		 * Fired when the map is moved or zoomed.
		 * @see app.modes.HoneycombMode
		 * @see initHoneycomb()
		 */
		self.changedViewport = new signals.Signal();
	};
	
	/**
	 * Adds new language marker on the map.
	 * 
	 * @param The language ID.
	 * @param The latitude.
	 * @param The longitude.
	 */
	OpenStreetMap.prototype.addLanguage = function(id, latitude, longitude) {
		var self = this;
		
		var icon = L.divIcon({
			className: 'language-marker',
			html: id
		});
		
		var marker = L.marker([latitude, longitude], {
			icon: icon
		}).addTo(self.map);
		
		marker.on('click', self._handleLanguageClick.bind(self));
		
		self.markers[id] = marker;
	};
	
	/**
	 * Removes the language with the ID specified.
	 * 
	 * @param The ID of the language to be removed.
	 */
	OpenStreetMap.prototype.removeLanguage = function(id) {
		var self = this;
		
		if(self.markers.hasOwnProperty(id)) {
			self.map.removeLayer(self.markers[id]);
			self.markers[id].off();
			delete self.markers[id];
		}
	};
	
	/**
	 * Event handler for clicking on markers.
	 * Attached to DOM in self.addMarker().
	 * 
	 * @private
	 * @param The L-augmented event.
	 */
	OpenStreetMap.prototype._handleLanguageClick = function(e) {
		var self = this;
		var id = $(e.originalEvent.target).html();
		
		self.clickedOnLanguage.dispatch(id);
	};
	
	/**
	 * Highlights the language with the ID specified.
	 * 
	 * @param The ID of the language to be highlighted.
	 * @param The level of highlight: primary (1) or secondary (2).
	 */
	OpenStreetMap.prototype.highlightLanguage = function(id, level) {
		var self = this;
		var className = '';
		
		if(level == 1) {
			className = 'highlight-primary';
		}
		else {
			className = 'highlight-secondary';
		}
		
		for(var key in self.markers) {
			if(key == id) {
				self.markers[key]._icon.classList.add(className);
				break;
			}
		}
	};
	
	/**
	 * Removes the highlight of the language with the ID specified.
	 * 
	 * @param The ID of the language to be lowlighted.
	 */
	OpenStreetMap.prototype.lowlightLanguage = function(id) {
		var self = this;
		
		for(var key in self.markers) {
			if(key == id) {
				self.markers[key]._icon.classList.remove('highlight-primary');
				self.markers[key]._icon.classList.remove('highlight-secondary');
				break;
			}
		}
	};
	
	/**
	 * Removes the highlights of all the languages on the map.
	 */
	OpenStreetMap.prototype.lowlightAll = function() {
		var self = this;
		
		for(var key in self.markers) {
			self.markers[key]._icon.classList.remove('highlight-primary');
			self.markers[key]._icon.classList.remove('highlight-secondary');
		}
	};
	
	/**
	 * Draws a point marker.
	 * 
	 * @param The ID of the point.
	 * @param The latitude of the point.
	 * @param The longitude of the point.
	 */
	OpenStreetMap.prototype.addPoint = function(id, latitude, longitude) {
		var self = this;
		
		var point = L.circle([latitude, longitude], 10, {
			className: 'point',
			color: 'red'
		}).addTo(self.map);
		
		self.points[id] = point;
	};
	
	/**
	 * Removes the point marker with the ID specified.
	 * 
	 * @param The ID of the point marker to be removed.
	 */
	OpenStreetMap.prototype.removePoint = function(id) {
		var self = this;
		
		for(var key in self.points) {
			if(key == id) {
				self.map.removeLayer(self.points[key]);
				delete self.points[key];
				break;
			}
		}
	};
	
	/**
	 * Draws a circle.
	 * 
	 * @param The ID of the circle (see removeCircle).
	 * @param The latitude of the circle's centre.
	 * @param The longitude of the circle's centre.
	 * @param The circle's radius in kilometres.
	 */
	OpenStreetMap.prototype.addCircle = function(id, latitude, longitude, radius) {
		var self = this;
		
		var circle = L.circle([latitude, longitude], radius*1000, {
			className: 'circle',
			color: 'red',
			fillColor: '#EA7525',
			fillOpacity: 0.25
		});
		circle.addTo(self.map);
		
		self.circles[id] = circle;
	};
	
	/**
	 * Removes the circle with the ID specified.
	 * 
	 * @param The ID of the circle to be removed.
	 */
	OpenStreetMap.prototype.removeCircle = function(id) {
		var self = this;
		
		for(var key in self.circles) {
			if(key == id) {
				self.map.removeLayer(self.circles[key]);
				delete self.circles[key];
				break;
			}
		}
	};
	
	/**
	 * Adds draggable <div> to the bottom right corner of the map.
	 * 
	 * @param The ID of the draggable.
	 * @return jQuery instance of the new element.
	 */
	OpenStreetMap.prototype.addDraggable = function(id) {
		var self = this;
		
		var elem = $('<div>');
		elem.addClass('draggable');
		elem.appendTo(self.dom.parent());
		
		L.DomUtil.setPosition(elem.get(0), L.point(0, 0));
		
		var draggable = new L.Draggable(elem.get(0));
		draggable.enable();
		
		self.draggables[id] = {
			'element': elem,
			'draggable': draggable
		};
		
		return elem;
	};
	
	/**
	 * Removes the draggable <div> with the ID specified.
	 * 
	 * @param The ID of the draggable to remove.
	 */
	OpenStreetMap.prototype.removeDraggable = function(id) {
		var self = this;
		
		for(var key in self.draggables) {
			if(key == id) {
				self.draggables[key].draggable.disable();
				self.draggables[key].element.remove();
				delete self.draggables[key];
				break;
			}
		}
	};
	
	/**
	 * Adds honeycomb layer on the map.
	 * There is only one honeycomb layer at a time.
	 */
	OpenStreetMap.prototype.createHoneycomb = function() {
		var self = this;
		
		if(self.honeycomb) {
			self.removeHoneycomb();
		}
		
		self.honeycomb = new HoneycombLayer();
		self.honeycomb.addSignal(self.changedViewport);
		self.honeycomb.addTo(self.map);
		
		self.hexagonMarker = new HoneycombLayer();
		self.hexagonMarker.addTo(self.map);
		
		self.map.on('click', self._handleHoneycombClick, self);
	};
	
	/**
	 * Event handler for honeycomb clicking.
	 * 
	 * @private
	 * @param The L-augmented event.
	 */
	OpenStreetMap.prototype._handleHoneycombClick = function(e) {
		var self = this;
		
		var cell = self.honeycomb.getContainingHexagon(e.containerPoint.x, e.containerPoint.y);
		var temperature = self.honeycomb.getHexagonTemperature(cell[0], cell[1]);
		
		self.hexagonMarker.clear();
		
		self.hexagonMarker.drawMarker(cell[0], cell[1], temperature);
	};
	
	/**
	 * Updates the honeycomb cells.
	 * 
	 * @param [] of [latitude, longitude, temperature].
	 */
	OpenStreetMap.prototype.updateHoneycomb = function(cells) {
		var self = this;
		self.honeycomb.redraw(cells);
	};
	
	/**
	 * Removes the honeycomb layer from the map.
	 * There is only one honeycomb layer at a time.
	 */
	OpenStreetMap.prototype.removeHoneycomb = function() {
		var self = this;
		
		if(self.honeycomb) {
			self.map.removeLayer(self.honeycomb);
		}
		if(self.hexagonMarker) {
			self.map.removeLayer(self.hexagonMarker);
		}
		
		self.map.off('click', self._handleHoneycombClick, self);
	};
	
	
	/**
	 * Leaflet layer for the honeycomb.
	 * 
	 * This class is used by two layers: one for the honeycomb itself, and
	 * another one for individual cell highlighting.
	 * 
	 * @class
	 * @see Source code of Leaflet.heat.
	 */
	var HoneycombLayer = L.Class.extend({
		initialize: function() {
			var self = this;
			
			self.map = null;
			self.canvas = null;
			self.ctx = null;
			
			/**
			 * [] of [x, y]
			 * [] of [latitude, longitude, temperature]
			 * Indices coincide.
			 * But the latter is only defined after redraw() and before the
			 * next _reset() call.
			 */
			self.cells = [];
			self.data = null;
			
			/**
			 * The hexagon side and height.
			 */
			self.a = 20;
			self.h = Math.sin(Math.PI / 3) * self.a;
			
			/**
			 * If set, the signal will be dispatched at _reset().
			 * @see addSignal().
			 */
			self.changedViewport = null;
		},
		
		onAdd: function(map) {
			var self = this;
			self.map = map;
			
			if(!self.canvas) {
				self._initCanvas();
			}
			
			self.map.getPanes().overlayPane.appendChild(self.canvas);
			
			self.map.on('moveend', self._reset, self);
			
			self._reset();
		},
		
		onRemove: function(map) {
			var self = this;
			
			self.map.getPanes().overlayPane.removeChild(self.canvas);
			
			self.map.off('moveend', self._reset, self);
		},
		
		addTo: function(map) {
			var self = this;
			map.addLayer(self);
			return self;
		},
		
		addSignal: function(signal) {
			var self = this;
			self.changedViewport = signal;
		},
		
		_initCanvas: function() {
			var self = this;
			
			self.canvas = L.DomUtil.create('canvas', 'leaflet-layer honeycomb');
			L.DomUtil.addClass(self.canvas, 'leaflet-zoom-hide');
			
			var size = self.map.getSize();
			self.canvas.width = size.x;
			self.canvas.height = size.y;
			
			self.ctx = self.canvas.getContext('2d');
		},
		
		_reset: function() {
			var self = this;
			
			var topLeft = self.map.containerPointToLayerPoint([0, 0]);
			L.DomUtil.setPosition(self.canvas, topLeft);
			
			var size = self.map.getSize();
			if(self.canvas.width !== size.x) {
				self.canvas.width = size.x;
			}
			if(self.canvas.height !== size.y) {
				self.canvas.height = size.y;
			}
			
			self.clear();
			self.cells = [];
			self.data = null;
			
			
			var a = self.a, h = self.h;
			var x = 0, y = 0, row = 0, latLng = [], coords = [];
			
			while(true) {
				x = (row % 2) ? -3/2*a : 0;
				y = row*h;
				
				while(true) {
					self.cells.push([x, y]);
					
					latLng = self.map.containerPointToLatLng([x, y]);
					coords.push([latLng.lat, latLng.lng]);
					
					x += 3*a;
					if(x > self.canvas.width + 3*a) {
						break;
					}
				}
				
				row += 1;
				
				if(y > self.canvas.height) {
					break;
				}
			}
			
			if(self.changedViewport) {
				self.changedViewport.dispatch(coords);
			}
		},
		
		/**
		 * Fills the canvas with hexagons, the centres of which should have
		 * already been calculated by the _reset() method.
		 * 
		 * @see OpenStreetMap.updateHoneycomb().
		 * @param [] of [latitude, longitude, temperature].
		 */
		redraw: function(data) {
			var self = this;
			
			self.clear();
			
			var a = self.a, h = self.h;
			var i = 0, colour = '', lightness = 0;
			
			for(i = 0; i < self.cells.length; i++) {
				if(data[i][2] == 0) {
					continue;
				}
				else if(data[i][2] > 0) {
					lightness = 100 - parseInt(data[i][2] * 50);
					colour = 'hsl(0, 100%, '+ lightness +'%)';
				}
				else {
					lightness = 100 + parseInt(data[i][2] * 50);
					colour = 'hsl(240, 100%, '+ lightness +'%)';
				}
				
				self._drawHexagon(self.cells[i][0], self.cells[i][1], a, h, colour);
			}
			
			self.data = data;
		},
		
		/**
		 * Draws a hexagon.
		 * 
		 * The perpendicular is derivable from the side, but we do not want to make
		 * the same calculation over and over when mass producing hexagons.
		 * 
		 * @param The x of hexagon's centre.
		 * @param The y of hexagon's centre.
		 * @param The hexagon's side.
		 * @param The hexagon's perpendicular (centre to side).
		 * @param The colour to fill the hexagon with.
		 */
		_drawHexagon: function(x, y, a, h, colour) {
			var self = this;
			
			self.ctx.beginPath();
			self.ctx.moveTo(x-a, y);
			self.ctx.lineTo(x-a/2, y+h);
			self.ctx.lineTo(x+a/2, y+h);
			self.ctx.lineTo(x+a, y);
			self.ctx.lineTo(x+a/2, y-h);
			self.ctx.lineTo(x-a/2, y-h);
			self.ctx.closePath();
			
			self.ctx.fillStyle = colour;
			self.ctx.fill();
		},
		
		/**
		 * Returns the centre of the hexagon that contains the point given.
		 * 
		 * @param The x of the point.
		 * @param The y of the point.
		 * @return [x, y] of the hexagon's centre.
		 */
		getContainingHexagon: function(x, y) {
			var self = this;
			
			var A = [], B = [], AP = null, BP = null;
			var rectWidth = 3/2 * self.a;
			var rectHeight = self.h;
			
			var rectX = parseInt(x / rectWidth);
			var rectY = parseInt(y / rectHeight);
			
			if((rectX % 2 && rectY % 2) || (!(rectX % 2) && !(rectY %2))) {
				A = [rectX * rectWidth, rectY * rectHeight];
				B = [(rectX + 1) * rectWidth, (rectY + 1) * rectHeight];
			}
			else {
				A = [rectX * rectWidth, (rectY + 1) * rectHeight];
				B = [(rectX + 1) * rectWidth, rectY * rectHeight];
			}
			
			AP = Math.sqrt(Math.pow(x - A[0], 2) + Math.pow(y - A[1], 2));
			BP = Math.sqrt(Math.pow(x - B[0], 2) + Math.pow(y - B[1], 2));
			
			if(AP < BP) {
				return A;
			}
			else {
				return B;
			}
		},
		
		/**
		 * Finds the temperature of the cell, the centre of which is (x, y).
		 * 
		 * @param The x of the cell's centre.
		 * @param The y of the cell's centre.
		 */
		getHexagonTemperature: function(x, y) {
			var self = this;
			
			for(var i = 0; i < self.cells.length; i++) {
				if(self.cells[i][0] == x && self.cells[i][1] == y) {
					return self.data[i][2];
				}
			}
			
			return 0;
		},
		
		/**
		 * Draws an empty cell with border.
		 * 
		 * Used by the hexagonMarker layer instance.
		 * @see OpenStreetMap._handleHoneycombClick().
		 * 
		 * @param The x of the cell's centre.
		 * @param The y of the cell's centre.
		 * @param The cell's temperature.
		 */
		drawMarker: function(x, y, temperature) {
			var self = this;
			var a = self.a, h = self.h;
			
			self.ctx.beginPath();
			self.ctx.moveTo(x-a, y);
			self.ctx.lineTo(x-a/2, y+h);
			self.ctx.lineTo(x+a/2, y+h);
			self.ctx.lineTo(x+a, y);
			self.ctx.lineTo(x+a/2, y-h);
			self.ctx.lineTo(x-a/2, y-h);
			self.ctx.closePath();
			
			self.ctx.strokeStyle = 'red';
			self.ctx.lineWidth = 2;
			self.ctx.stroke();
			
			self.ctx.font = '16px Fira Sans';
			self.ctx.textAlign = 'center';
			self.ctx.textBaseline = 'middle';
			self.ctx.fillStyle = 'black';
			
			temperature = temperature.toString().substr(0, 4);
			self.ctx.fillText(temperature, x, y);
		},
		
		/**
		 * Clears the layer's canvas.
		 */
		clear: function() {
			var self = this;
			self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
		}
	});
	
	
	/**
	 * Module exports.
	 */
	return {
		OpenStreetMap: OpenStreetMap
	};
	
}());
