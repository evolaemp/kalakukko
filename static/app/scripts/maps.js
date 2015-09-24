/**
 * Handles the maps.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires signals
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
	};
	
	
	
	/**
	 * Class definition for archeo-linguistic maps.
	 * 
	 * @class
	 * @param The map container as a jQuery element.
	 * @param The languages to be displayed on the map.
	 */
	var Map = function(dom, languages) {
		var self = this;
		self.paper = new OpenStreetMap(dom);
		
		for(var i = 0; i < languages.length; i++) {
			self.paper.addMarker(
				languages[i].iso_639_3,
				languages[i].latitude,
				languages[i].longitude
			);
		}
		
		self.paper.languageSelected.add(self.setOrigin, self);
	};
	
	/**
	 * Heats up the map showing the distances from the language given.
	 * 
	 * @param The new heat origin or null.
	 * @return A promise.
	 */
	Map.prototype.setOrigin = function(languageId) {
		var self = this;
		
		$.get(
			'/api/distances/'+ languageId +'/'
		)
		.done(function(data) {
			self.paper.turnHeatOn(languageId, data.distances);
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
	 * Module exports.
	 */
	return {
		Map: Map
	};
	
}());
