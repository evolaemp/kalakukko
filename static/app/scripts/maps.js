/**
 * Handles the maps.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires L
 * @requires app.messages
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
	};
	
	/**
	 * Adds new marker on the map.
	 * 
	 * @param The marker ID.
	 * @param The latitude.
	 * @param The longitude.
	 */
	OpenStreetMap.prototype.addMarker = function(id, latitude, longitude) {
		var self = this;
		
		var icon = L.divIcon({
			className: 'language-marker',
			html: id
		});
		
		var marker = L.marker([latitude, longitude], {
			icon: icon
		}).addTo(self.map);
		
		self.markers[id] = marker;
	};
	
	/**
	 * Removes the marker with the ID specified.
	 * 
	 * @param The ID of the marker to be removed.
	 */
	OpenStreetMap.prototype.removeMarker = function(id) {
		var self = this;
		
		if(self.markers.hasOwnProperty(id)) {
			self.map.removeLayer(self.markers[id]);
			delete self.markers[id];
		}
	};
	
	OpenStreetMap.prototype.turnHeatOn = function() {
		var self = this;
	};
	
	
	
	/**
	 * 
	 */
	var Map = function(dom) {
		var self = this;
		self.map = new OpenStreetMap(dom);
	};
	
	
	
	/**
	 * Module exports.
	 */
	return {
		Map: OpenStreetMap
	};
	
}());
