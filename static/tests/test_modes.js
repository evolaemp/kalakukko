QUnit.module('app.modes.PointMode', {
	beforeEach: function() {
		var self = this;
		
		self.controller = new app.controllers.Controller();
		
		/* init dom */
		self.controller.methodSelect = {
			getValue: function() {
				return 'circle';
			}
		};
		self.controller.parameterInput = {
			getValue: function() {
				return 500;
			}
		};
		
		/* init map */
		var FakeMap = function() {
			this.clicked = new signals.Signal();
		};
		self.controller.map = new FakeMap();
		
		/* init mode */
		self.controller.mode = new app.modes.NormalMode();
		self.fileId = 'test_file_id';
		self.controller.switchMode('point');
	}
});

QUnit.test('signals get cleared', function(assert) {
	var self = this;
	assert.ok(true);
});

