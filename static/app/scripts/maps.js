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
	 * 
	 */
	OpenStreetMap.prototype.createHoneycomb = function() {
		var self = this;
		
		if(self.honeycomb) {
			self.removeHoneycomb();
		}
		
		self.honeycomb = new HoneycombLayer(self.changedViewport);
		self.honeycomb.addTo(self.map);
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
	};
	
	
	/**
	 * Leaflet layer for the honeycomb.
	 * Wrapper around HoneycombCanvas.
	 * 
	 * @class
	 * @see Source code of Leaflet.heat.
	 */
	var HoneycombLayer = L.Class.extend({
		initialize: function(changedViewport) {
			var self = this;
			
			self.canvas = null;
			self.ctx = null;
			self.cells = [];
			
			self.changedViewport = changedViewport;
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
		
		_initCanvas: function() {
			var self = this;
			
			self.canvas = L.DomUtil.create('canvas', 'leaflet-layer honeycomb');
			L.DomUtil.addClass(self.canvas, 'leaflet-zoom-hide');
			
			var size = self.map.getSize();
			self.canvas.width = size.x;
			self.canvas.height = size.y;
			
			// self.honeycomb = new HoneycombCanvas(self.canvas);
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
			
			self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
			self.cells = [];
			
			
			var a = 20;
			var h = Math.sin(Math.PI / 3) * a;
			
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
			
			self.changedViewport.dispatch(coords);
		},
		
		redraw: function(data) {
			var self = this;
			
			self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
			
			var a = 20;
			var h = Math.sin(Math.PI / 3) * a;
			
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
		},
		
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
		}
	});
	
	
	/**
	 * Handles the (re-)drawing of the honeycomb.
	 * Encapsulates the canvas interactions.
	 * 
	 * @class
	 * @param The canvas to draw the honeycomb on.
	 */
	var HoneycombCanvas = function(canvas) {
		var self = this;
		
		self.canvas = canvas;
		self.ctx = self.canvas.getContext('2d');
		
		self.points = [];
	};
	
	/**
	 * Clears the canvas and draws the hexagons on it.
	 */
	HoneycombCanvas.prototype.redraw = function() {
		var self = this;
		
		self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height);
		self.points = [];
		
		var a = 10;
		var h = Math.sin(Math.PI / 3) * a;
		var x = 0, y = 0, row = 0;
		
		while(true) {
			x = (row % 2) ? -3/2*a : 0;
			y = row*h;
			
			while(true) {
				// self.drawHexagon(x, y, a, h, 'black');
				self.points.push([x, y]);
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
	};
	
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
	HoneycombCanvas.prototype.drawHexagon = function(x, y, a, h, colour) {
		var self = this;
		
		self.ctx.beginPath();
		self.ctx.moveTo(x-a, y);
		self.ctx.lineTo(x-a/2, y+h);
		self.ctx.lineTo(x+a/2, y+h);
		self.ctx.lineTo(x+a, y);
		self.ctx.lineTo(x+a/2, y-h);
		self.ctx.lineTo(x-a/2, y-h);
		self.ctx.closePath();
		
		// self.ctx.fillStyle = colour;
		// self.ctx.fill();
		self.ctx.stroke();
	};
	
	
	/**
	 * Module exports.
	 */
	return {
		OpenStreetMap: OpenStreetMap
	};
	
}());
