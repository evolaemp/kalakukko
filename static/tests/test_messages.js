QUnit.module('app.messages', {
	beforeEach: function() {
		$('<div class="messages"></div>')
			.appendTo($('#qunit-fixture'));
		app.messages.init();
	}
});

QUnit.test('spawn error message', function(assert) {
	app.messages.error("Lorem ipsum!");
	var elem = $('.messages .message');
	assert.equal(elem.length, 1);
	assert.strictEqual(elem.hasClass('error'), true);
	assert.equal(elem.text(), "Lorem ipsum!");
});

QUnit.test('spawn info message', function(assert) {
	app.messages.info("Lorem ipsum!");
	var elem = $('.messages .message');
	assert.equal(elem.length, 1);
	assert.strictEqual(elem.hasClass('info'), true);
	assert.equal(elem.text(), "Lorem ipsum!");
});

QUnit.test('spawn success message', function(assert) {
	app.messages.success("Lorem ipsum!");
	var elem = $('.messages .message');
	assert.equal(elem.length, 1);
	assert.strictEqual(elem.hasClass('success'), true);
	assert.equal(elem.text(), "Lorem ipsum!");
});

QUnit.test('clear messages', function(assert) {
	for(var i = 0; i < 5; i++) {
		app.messages.info("Lorem ipsum!");
	}
	app.messages.clear();
	assert.equal($('.messages .message').length, 0);
	
	var m = app.messages.info("Lorem ipsum!");
	m.remove();
	assert.equal($('.messages .message').length, 0);
	
	m = app.messages.info("Lorem ipsum!");
	for(var i = 0; i < 5; i++) {
		app.messages.info("Test!");
	}
	assert.equal($('.messages .message').length, 1);
	assert.equal($('.messages .message').html(), 'Test!');
});

