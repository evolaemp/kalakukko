/**
 * Handles messages to user.
 * 
 * @module
 * 
 * @requires jQuery
 */
app.messages = (function() {
	
	"use strict";
	
	/**
	 * The dom container.
	 */
	var dom = null;
	
	/**
	 * One message at a time.
	 */
	var current = null;
	
	
	/**
	 * Class definition for messages.
	 * 
	 * @class
	 * @param One of: 'error', 'success'.
	 * @param The message text.
	 */
	var Message = function(type, text) {
		var self = this;
		
		// create dom element
		self.elem = $('<div>'+text+'</div>').addClass('message '+ type);
		self.elem.appendTo(dom);
		
		// private methods
		self._remove = function() {
			self.elem.remove();
		};
	};
	
	Message.prototype.remove = function() {
		this._remove();
	};
	
	
	/**
	 * Module init.
	 */
	$(document).ready(function() {
		dom = $('.messages');
	});
	
	
	/**
	 * Module exports.
	 */
	var exports = {
		error: function(text) {
			exports.clear();
			current = new Message('error', text);
			setTimeout(exports.clear, 5000);
		},
		info: function(text) {
			exports.clear();
			current = new Message('info', text);
			setTimeout(exports.clear, 5000);
		},
		success: function(text) {
			exports.clear();
			current = new Message('success', text);
			setTimeout(exports.clear, 5000);
		},
		clear: function() {
			if(current) {
				current.remove();
			}
		}
	};
	return exports;
	
}());
