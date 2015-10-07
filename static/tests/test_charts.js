QUnit.module('app.charts.Chart', {
	beforeEach: function() {
		var self = this;
		self.dom = $('<div class="ct-square"></div>');
		self.dom.appendTo($('#qunit-fixture'));
		self.chart = new app.charts.Chart(self.dom);
	}
});

QUnit.test('drawPoints', function(assert) {
	var self = this;
	var done = assert.async();
	
	var points = {
		A: [0.1, 0.1],
		B: [0.2, 0.2],
		C: [0.9, 0.9]
	};
	
	var promise = self.chart.draw(points)
	
	promise.done(function() {
		assert.equal(self.dom.children('svg').length, 1);
		assert.equal(self.dom.children('.tooltip').length, 1);
		assert.equal(self.dom.find('.ct-point').length, 3);
		done();
	});
});

