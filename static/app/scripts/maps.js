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
		
		/*L.tileLayer(
			'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
			{
				attribution: '<a href="http://openstreetmap.org">OpenStreetMap</a>',
				accessToken: OSM_ACCESS_TOKEN,
				id: OSM_ID,
				maxZoom: 15
			}
		).addTo(self.map);*/
		
		self.markers = {};
		
		/**
		 * Fired when language marker is clicked.
		 */
		self.languageSelected = new signals.Signal();
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
		
		marker.on('click', self.handleMarkerClick.bind(self));
		
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
	OpenStreetMap.prototype.handleMarkerClick = function(e) {
		var self = this;
		var id = $(e.originalEvent.target).html();
		
		self.languageSelected.dispatch(id);
	};
	
	/**
	 * Turns the heat on!
	 */
	OpenStreetMap.prototype.turnHeatOn = function(origin, distances) {
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
	};
	
	/**
	 * Turns the heat off.
	 */
	OpenStreetMap.prototype.turnHeatOff = function() {
		var self = this;
		
		var keys = Object.keys(self.markers);
		
		for(var i = 0; i < keys.length; i++) {
			self.markers[keys[i]]._icon.style.backgroundColor = null;
		}
	};
	
	
	/**
	 * Module exports.
	 */
	return {
		OpenStreetMap: OpenStreetMap
	};
	
}());
