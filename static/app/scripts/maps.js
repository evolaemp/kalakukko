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
	 * Assumes that L, OSM_ACCESS_TOKEN and OSM_ID are present.
	 * 
	 * @class
	 * @param The map container as a jQuery element.
	 * @param Whether not to load the tiles.
	 */
	var OpenStreetMap = function(dom, withoutTiles) {
		var self = this;
		
		self.dom = dom;
		self.map = L.map(self.dom.get(0), {
			center: [42, 42],
			zoom: 5,
			zoomControl: false
		});
		
		if(!withoutTiles) {
			L.tileLayer(
				'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
				{
					attribution: '<a href="http://openstreetmap.org">OpenStreetMap</a>',
					accessToken: OSM_ACCESS_TOKEN,
					id: OSM_ID,
					maxZoom: 15
				}
			).addTo(self.map);
		}
		
		/**
		 * Stuff on the map.
		 */
		self.markers = {};
		self.circles = {};
		self.points = {};
		
		/**
		 * Fired when language marker is clicked.
		 */
		self.clickedOnLanguage = new signals.Signal();
		
		/**
		 * Fired when the map is clicked.
		 */
		self.clicked = new signals.Signal();
		self.map.on('click', function(e) {
			self.clicked.dispatch(e.latlng.lat, e.latlng.lng);
		});
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
		}).addTo(self.map);
		
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
	 * Turns the heat on!
	 */
	/*OpenStreetMap.prototype.turnHeatOn = function(origin, distances) {
		var self = this;
		
		var keys = Object.keys(self.markers);
		var key = null;
		
		var redness = null;
		var nonRedness = null;
		
		for(var i = 0; i < keys.length; i++) {
			key = keys[i];
			if(key == origin) {
				self.markers[key]._icon.style.backgroundColor = 'red';
				continue;
			}
			if(!distances.hasOwnProperty(key)) {
				continue;
			}
			
			redness = parseInt((1 - distances[key]) * 255);
			nonRedness = 255 - redness;
			
			self.markers[key]._icon.style.backgroundColor = 'rgb('+ redness +', '+ nonRedness +', '+ nonRedness +')';
		}
	};*/
	
	/**
	 * Turns the heat off.
	 */
	/*OpenStreetMap.prototype.turnHeatOff = function() {
		var self = this;
		
		var keys = Object.keys(self.markers);
		
		for(var i = 0; i < keys.length; i++) {
			self.markers[keys[i]]._icon.style.backgroundColor = null;
		}
	};*/
	
	
	/**
	 * Module exports.
	 */
	return {
		OpenStreetMap: OpenStreetMap
	};
	
}());
