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
		
		self.elem = $('<div>'+text+'</div>').addClass('message '+ type);
		self.elem.appendTo(dom);
	};
	
	/**
	 * Removes the message's dom element and the reference to the latter.
	 */
	Message.prototype.remove = function() {
		var self = this;
		
		if(self.elem) {
			self.elem.remove();
			self.elem = null;
		}
	};
	
	
	/**
	 * Module init.
	 */
	var init = function() {
		dom = $('.messages');
	};
	
	$(document).ready(init);
	
	
	/**
	 * Module exports.
	 */
	var exports = {
		init: function() {
			init();
		},
		error: function(text) {
			exports.clear();
			current = new Message('error', text);
			setTimeout(exports.clear, 5000);
			return current;
		},
		info: function(text) {
			exports.clear();
			current = new Message('info', text);
			setTimeout(exports.clear, 5000);
			return current;
		},
		success: function(text) {
			exports.clear();
			current = new Message('success', text);
			setTimeout(exports.clear, 5000);
			return current;
		},
		clear: function() {
			if(current) {
				current.remove();
			}
		}
	};
	return exports;
	
}());
