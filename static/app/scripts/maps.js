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
	 */
	var OpenStreetMap = function(dom) {
		var self = this;
		
		self.dom = dom;
		self.map = L.map(self.dom.get(0));
		self.map.setView([42, 42], 5);
		
		L.tileLayer(
			'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
			{
				attribution: '<a href="http://openstreetmap.org">OpenStreetMap</a>',
				accessToken: OSM_ACCESS_TOKEN,
				id: OSM_ID,
				maxZoom: 15
			}
		).addTo(self.map);
		
		self.markers = {};
		
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
	 */
	OpenStreetMap.prototype.highlightLanguage = function(id) {
		var self = this;
	};
	
	/**
	 * Removes the highlight of the language with the ID specified.
	 * 
	 * @param The ID of the language to be lowlighted.
	 */
	OpenStreetMap.prototype.lowlightLanguage = function(id) {
		var self = this;
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
	};
	
	/**
	 * Removes the point marker with the ID specified.
	 * 
	 * @param The ID of the point marker to be removed.
	 */
	OpenStreetMap.prototype.removePoint = function(id) {
		var self = this;
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
	};
	
	/**
	 * Removes the circle with the ID specified.
	 * 
	 * @param The ID of the circle to be removed.
	 */
	OpenStreetMap.prototype.removeCircle = function(id) {
		var self = this;
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
