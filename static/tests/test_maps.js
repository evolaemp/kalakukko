QUnit.module('app.maps.OpenStreetMap', {
	beforeEach: function() {
		var self = this;
		
		self.dom = $('<div class="map"></div>');
		self.dom.appendTo($('#qunit-fixture'));
		
		self.map = new app.maps.OpenStreetMap(self.dom, true);
	}
});

QUnit.test('signals', function(assert) {
	var self = this;
	var clickedOnMap = assert.async();
	var clickedOnLanguage = assert.async();
	
	assert.expect(3);
	
	self.map.clicked.add(function(latitude, longitude) {
		assert.ok(latitude);
		assert.ok(longitude);
		clickedOnMap();
	});
	self.dom.click();
	
	self.map.addLanguage('caucasus', 42, 42);
	self.map.clickedOnLanguage.add(function(languageId) {
		assert.equal(languageId, 'caucasus');
		clickedOnLanguage();
	});
	self.dom.find('.language-marker:first').click();
});

QUnit.test('add/remove languages', function(assert) {
	var self = this;
	var i;
	
	for(i = 0; i < 10; i++) {
		self.map.addLanguage(i, 42, 42);
		assert.equal(self.dom.find('.language-marker').length, i+1);
	}
	for(i = 0; i < 10; i++) {
		self.map.removeLanguage(i);
		assert.equal(self.dom.find('.language-marker').length, 10-i-1);
	}
});

QUnit.test('highlight/lowlight languages', function(assert) {
	var self = this;
	self.map.addLanguage('test', 42, 42);
	
	self.map.highlightLanguage('test', 1);
	assert.ok(self.dom.find('.language-marker').hasClass('highlight-primary'));
	assert.notOk(self.dom.find('.language-marker').hasClass('highlight-secondary'));
	
	self.map.lowlightLanguage('test');
	assert.notOk(self.dom.find('.language-marker').hasClass('highlight-primary'));
	assert.notOk(self.dom.find('.language-marker').hasClass('highlight-secondary'));
});

QUnit.test('add/remove points', function(assert) {
	var self = this;
	var i;
	
	for(i = 0; i < 10; i++) {
		self.map.addPoint(i, 42, 42);
		assert.equal(self.dom.find('.point').length, i+1);
	}
	for(i = 0; i < 10; i++) {
		self.map.removePoint(i);
		assert.equal(self.dom.find('.point').length, 10-i-1);
	}
});

QUnit.test('add/remove circles', function(assert) {
	var self = this;
	var i;
	
	for(i = 0; i < 10; i++) {
		self.map.addCircle(i, 42, 42, 500);
		assert.equal(self.dom.find('.circle').length, i+1);
	}
	for(i = 0; i < 10; i++) {
		self.map.removeCircle(i);
		assert.equal(self.dom.find('.circle').length, 10-i-1);
	}
});

QUnit.test('add/remove draggables', function(assert) {
	var self = this;
	var i;
	
	for(i = 0; i < 10; i++) {
		self.map.addDraggable(i);
		assert.equal(self.dom.parent().find('.draggable').length, i+1);
	}
	for(i = 0; i < 10; i++) {
		self.map.removeDraggable(i);
		assert.equal(self.dom.parent().find('.draggable').length, 10-i-1);
	}
});

