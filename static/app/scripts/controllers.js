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
		 * Fired upon change of mode (point / honeycomb).
		 */
		self.switchedMode = new signals.Signal();
		
		/**
		 * Fired upon change of method (circle / neighbourhood).
		 */
		self.switchedMethod = new signals.Signal();
	};
	
	/**
	 * Inits self.dom and friends.
	 * Called upon the document ready event.
	 */
	Controller.prototype.initDom = function() {
		var self = this;
		
		self.dom = $('header .controls');
		if(self.dom.length != 1) {
			self.dom = null;
			return;
		}
		
		self.fileInput = new FileInput(
			self.dom.find('input[name=file]'),
			self.dom.find('button.file-button')
		);
		
		self.modeSelect = new ModeSelect(self.dom.find('.mode-select'));
		self.methodSelect = new MethodSelect(self.dom.find('.method-select'));
		
		self.parameterInput = new ParameterInput(self.dom.find('.parameter-input'));
	};
	
	/**
	 * Inits self.map.
	 * Called upon the document ready event.
	 */
	Controller.prototype.initMap = function() {
		var self = this;
		var mapElement = $('[data-maps=map]');
		
		if(mapElement.length != 1) {
			app.messages.error('Map not found.');
			return;
		}
		
		self.map = new app.maps.OpenStreetMap(mapElement);
		self.map.loadTiles();
		
		for(var i = 0; i < LANGUAGES.length; i++) {
			self.map.addLanguage(
				LANGUAGES[i].iso_code,
				LANGUAGES[i].latitude,
				LANGUAGES[i].longitude
			);
		}
	};
	
	/**
	 * Inits self.mode.
	 * Called upon the document ready event.
	 */
	Controller.prototype.initMode = function() {
		var self = this;
		
		self.mode = new app.modes.NormalMode();
		self.mode.bind(self.map);
		
		/**
		 * Use file from last time.
		 */
		var lastFileId = localStorage.getItem('kalakukkoLastFileId');
		var lastFileName = localStorage.getItem('kalakukkoLastFileName');
		if(lastFileId != null && lastFileName != null) {
			self.fileId = lastFileId;
			self.fileInput.setSource(lastFileName);
			self.switchMode('point');
		}
		
		/**
		 * Update the map when the method switch is used.
		 */
		self.switchedMethod.add(function() {
			self.mode.update();
		});
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
			self.mode.received404.add(function() {
				self.switchMode('normal');
			});
		}
		else if(newMode == 'heat') {
			self.mode = new app.modes.HoneycombMode(
				self.fileId, self.methodSelect, self.parameterInput
			);
			self.mode.received404.add(function() {
				self.switchMode('normal');
			});
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
	 * Control for switching the method (circle / neighbourhood).
	 * 
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
		
		self.dom.find('button').on('click', function() {
			self.set($(this).data('value'));
		});
	};
	
	MethodSelect.prototype.set = function(value) {
		var self = this;
		self.dom.find('button').removeClass('active');
		self.dom.find('button[data-value='+ value +']').addClass('active');
		mainController.switchedMethod.dispatch(value);
	};
	
	MethodSelect.prototype.get = function() {
		var self = this;
		var value = self.dom.find('button.active').data('value');
		
		if(value != 'circle' && value != 'neighbourhood') {
			app.messages.error('Method set to circle.');
			value = 'circle';
			self.set(value);
		}
		
		return value;
	};
	
	/**
	 * Control for adjusting the radius (for the circle method).
	 * This class is used by ParameterInput.
	 * 
	 * @class
	 */
	var RadiusInput = function(dom) {
		var self = this;
		self.dom = dom;
		
		mainController.switchedMethod.add(function(newMethod) {
			if(newMethod == 'circle') {
				self.dom.removeClass('hidden');
			}
			else {
				self.dom.addClass('hidden');
			}
		});
	};
	
	RadiusInput.prototype.set = function(value) {
		var self = this;
		self.dom.find('input').val(value);
	};
	
	RadiusInput.prototype.get = function() {
		var self = this;
		var value = parseInt(self.dom.find('input').val());
		
		if(isNaN(value) || value <= 0) {
			app.messages.error('Radius set to 1500.');
			self.set(1500);
			value = 1500;
		}
		
		return value;
	};
	
	/**
	 * Control for adjusting the k parameter (for the neighbourhood method).
	 * This class is used by ParameterInput.
	 * 
	 * @class
	 */
	var KInput = function(dom) {
		var self = this;
		self.dom = dom;
		
		mainController.switchedMethod.add(function(newMethod) {
			if(newMethod == 'neighbourhood') {
				self.dom.removeClass('hidden');
			}
			else {
				self.dom.addClass('hidden');
			}
		});
	};
	
	KInput.prototype.set = function(value) {
		var self = this;
		self.dom.find('input').val(value);
	};
	
	KInput.prototype.get = function() {
		var self = this;
		var value = parseInt(self.dom.find('input').val());
		
		if(isNaN(value) || value <= 0) {
			app.messages.error('K set to 10.');
			self.set(10);
			value = 10;
		}
		
		return value;
	};
	
	/**
	 * Control for adjusting the parameters.
	 * 
	 * @class
	 */
	var ParameterInput = function(dom) {
		var self = this;
		self.dom = dom;
		
		self.radiusInput = new RadiusInput(self.dom.find('.radius-input'));
		self.kInput = new KInput(self.dom.find('.k-input'));
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.dom.addClass('hidden');
			}
			else {
				self.dom.removeClass('hidden');
			}
		});
	};
	
	ParameterInput.prototype.get = function() {
		var self = this;
		
		if(self.dom.find('.radius-input').hasClass('hidden')) {
			return self.kInput.get();
		}
		else {
			return self.radiusInput.get();
		}
	};
	
	/**
	 * Control for switching the mode (point / honeycomb).
	 * 
	 * @class
	 */
	var ModeSelect = function(dom) {
		var self = this;
		self.dom = dom;
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.set('point');
				self.dom.addClass('hidden');
			}
			else {
				self.dom.removeClass('hidden');
			}
		});
		
		self.dom.find('button').on('click', function() {
			var clicked = $(this);
			self.dom.find('button').removeClass('active');
			clicked.addClass('active');
			mainController.switchMode(clicked.data('value'));
		});
	};
	
	ModeSelect.prototype.set = function(value) {
		var self = this;
		self.dom.find('button').removeClass('active');
		self.dom.find('button[data-value='+ value +']').addClass('active');
	};
	
	ModeSelect.prototype.get = function() {
		var self = this;
		return self.dom.find('button.active').data('value');
	};
	
	/**
	 * Control for file uploads and file status display.
	 * 
	 * @class
	 */
	var FileInput = function(input, button) {
		var self = this;
		
		self.input = input;
		self.button = button;
		
		self.input.on('change', function() {
			var fileList = self.input.get(0).files;
			
			if(fileList.length != 1) {
				app.messages.error('No file selected.');
				return;
			}
			self.button.prop('disabled', true);
			
			mainController.uploadFile(fileList[0])
			.done(function(fileName) {
				self.setSource(fileName);
			})
			.always(function() {
				self.button.prop('disabled', false);
			});
		});
		
		mainController.switchedMode.add(function(newMode) {
			if(newMode == 'normal') {
				self.reset();
			}
		});
		
		self.reset();
	};
	
	/**
	 * Enters the file-uploaded state.
	 */
	FileInput.prototype.setSource = function(sourceName) {
		var self = this;
		
		self.button.html(sourceName);
		
		self.button.off('click');
		self.button.on('click', function() {
			/**
			 * Which will in turn invoke self.reset().
			 */
			mainController.switchMode('normal');
		});
	};
	
	/**
	 * Resets to the no-file-uploaded state.
	 */
	FileInput.prototype.reset = function() {
		var self = this;
		
		self.button.html('set source');
		
		self.button.off('click');
		self.button.on('click', function() {
			self.input.click();
		});
	};
	
	
	/**
	 * Init (before DOM ready).
	 */
	var mainController = new Controller();
	
	/**
	 * Init (after DOM ready).
	 * The if prevents mainController from running when testing.
	 */
	$(document).ready(function() {
		mainController.initDom();
		if(mainController.dom) {
			mainController.initMap();
			mainController.initMode();
		}
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
