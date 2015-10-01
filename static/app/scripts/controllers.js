/**
 * Home of the controllers.
 * 
 * @module
 * 
 * @requires jQuery
 * @requires signals
 * @requires app.maps
 * @requires app.messages
 * @requires app.modes
 */
app.controllers = (function() {
	
	"use strict";
	
	
	/**
	 * Class definition for the main controller.
	 * 
	 * @class
	 */
	var Controller = function() {
		var self = this;
		
		self.dom = null;
		self.map = null;
		self.mode = null;
		
		self.fileId = null;
		
		/**
		 * Fired upon change of mode.
		 */
		self.switchedMode = new signals.Signal();
	};
	
	/**
	 * Inits self.dom, self.map, self.mode.
	 * Called upon the document ready event.
	 */
	Controller.prototype.init = function() {
		var self = this;
		
		/* self.dom */
		self.dom = $('header .controls');
		
		self.fileInput = new FileInput(
			self.dom.find('input[name=file]'),
			self.dom.find('button')
		);
		
		self.modeSelect = new ModeSelect(self.dom.find('select[name=mode]'));
		self.methodSelect = new MethodSelect(
			self.dom.find('select[name=variable]')
		);
		self.parameterInput = new ParameterInput(
			self.dom.find('input[name=value]')
		);
		
		/* self.map */
		var mapElement = $('[data-maps=map]');
		
		if(mapElement.length != 1) {
			app.messages.error('Map not found.');
			return;
		}
		
		self.map = new app.maps.OpenStreetMap(mapElement);
		
		for(var i = 0; i < LANGUAGES.length; i++) {
			self.map.addLanguage(
				LANGUAGES[i].iso_639_3,
				LANGUAGES[i].latitude,
				LANGUAGES[i].longitude
			);
		}
		
		/* self.mode */
		self.mode = new app.modes.NormalMode();
		self.mode.bind(self.map);
		
		var lastFileId = localStorage.getItem('kalakukkoLastFileId');
		var lastFileName = localStorage.getItem('kalakukkoLastFileName');
		if(lastFileId != null && lastFileName != null) {
			self.fileId = lastFileId;
			self.fileInput.button.html(lastFileName);
			self.switchMode('point');
		}
	};
	
	/**
	 * Changes the mode.
	 * 
	 * @param The mode to switch to.
	 */
	Controller.prototype.switchMode = function(newMode) {
		var self = this;
		
		self.mode.unbind();
		
		if(newMode == 'normal') {
			self.mode = new app.modes.NormalMode();
		}
		else if(newMode == 'point') {
			self.mode = new app.modes.PointMode(
				self.fileId, self.methodSelect, self.parameterInput
			);
		}
		else if(newMode == 'heat') {
			self.mode = new app.modes.HeatMode(self.fileId);
		}
		else {
			app.messages.error('Unknown mode requested.');
			self.mode = new app.modes.NormalMode();
			newMode = 'normal';
		}
		
		self.mode.bind(self.map);
		self.switchedMode.dispatch(newMode);
	};
	
	/**
	 * Uploads the file given through XHR.
	 * 
	 * @param File instance to be uploaded.
	 * @returns Promise that resolves into the file name.
	 */
	Controller.prototype.uploadFile = function(file) {
		var self = this;
		var deferred = $.Deferred();
		
		app.messages.info('Loading file&hellip;');
		
		var formData = new FormData();
		formData.append('file', file);
		
		$.ajax({
			url: '/api/file/',
			method: 'POST',
			data: formData,
			processData: false,
			contentType: false
		})
		.done(function(data) {
			self.fileId = data.id;
			self.switchMode('point');
			
			deferred.resolve(data.name);
			app.messages.success('File loaded.');
			
			localStorage.setItem('kalakukkoLastFileId', data.id);
			localStorage.setItem('kalakukkoLastFileName', data.name);
		})
		.fail(function(xhr) {
			var error = 'File could not be loaded.';
			try {
				error = xhr.responseJSON.error;
			} catch(e) {};
			
			app.messages.error('Error: ' + error);
			deferred.reject();
		});
		
		return deferred.promise();
	};
	
	
	/**
	 * Follow some class definitions, one for each of the controls.
	 */
	/**
	 * @class
	 */
	var MethodSelect = function(dom) {
		var self = this;
		self.dom = dom;
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.dom.addClass('hidden');
			}
			else {
				self.dom.removeClass('hidden');
			}
		});
	};
	
	MethodSelect.prototype.getValue = function() {
		var self = this;
		
		if(self.dom.val() != 'circle' && self.dom.val() != 'neighbourhood') {
			app.messages.error('Method set to circle.');
			self.dom.val('circle');
		}
		
		return self.dom.val();
	};
	
	/**
	 * @class
	 */
	var ParameterInput = function(dom) {
		var self = this;
		self.dom = dom;
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.dom.addClass('hidden');
			}
			else {
				self.dom.removeClass('hidden');
			}
		});
	};
	
	ParameterInput.prototype.getValue = function() {
		var self = this;
		var value = parseInt(self.dom.val());
		
		if(isNaN(value) || value <= 0) {
			app.messages.error('Parameter set to one.');
			self.dom.val(1);
			value = 1;
		}
		
		return value;
	};
	
	/**
	 * @class
	 */
	var ModeSelect = function(dom) {
		var self = this;
		self.dom = dom;
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.dom.addClass('hidden');
			}
			else {
				self.dom.removeClass('hidden');
			}
		});
		
		self.dom.on('change', function() {
			mainController.switchMode(self.dom.val());
		});
	};
	
	/**
	 * @class
	 */
	var FileInput = function(input, button) {
		var self = this;
		
		self.input = input;
		self.button = button;
		
		self.button.on('click', function() {
			self.input.click();
		});
		
		self.input.on('change', function() {
			var fileList = self.input.get(0).files;
			
			if(fileList.length != 1) {
				app.messages.error('No file selected.');
				return;
			}
			self.button.prop('disabled', true);
			
			mainController.uploadFile(fileList[0])
			.done(function(fileName) {
				self.button.off();
				self.button.html(fileName);
				self.button.prop('disabled', false);
			})
			.fail(function() {
				self.button.prop('disabled', false);
			});
		});
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.button.off();
				self.button.html('set source');
				self.button.on('click', function() {
					self.input.click();
				});
			}
		});
	};
	
	
	/**
	 * Init (before DOM ready).
	 */
	var mainController = new Controller();
	
	/**
	 * Init (after DOM ready).
	 */
	$(document).ready(function() {
		mainController.init();
	});
	
	
	/**
	 * Module exports.
	 */
	return {
		getMainController: function() {
			return mainController;
		},
		Controller: Controller
	};
	
}());
