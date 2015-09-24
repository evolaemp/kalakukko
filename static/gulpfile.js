/* ѣ */

var gulp = require('gulp');


// task: delete build/*
var del = require('del');

gulp.task('clean', function(callback) {
	del(['build/**'], callback);
});


// task: process css files
var less = require('gulp-less');
var LessPluginCleanCss = require('less-plugin-clean-css');
var cleanCss = new LessPluginCleanCss({advanced: true});

gulp.task('styles', function() {
	gulp.src('app/styles/style.less')
		.pipe(less({
			plugins: [cleanCss]
		}))
		.pipe(gulp.dest('build/styles'));
});


// task: process fonts
gulp.task('fonts', function() {
	gulp.src([
			'bower_components/fira/woff/*'
		])
		.pipe(gulp.dest('build/fonts'));
});


// task: process js
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');

gulp.task('scripts', function() {
	gulp.src([
		'app/scripts/*.js'
	])
	.pipe(uglify({
		mangle: false
	}))
	.pipe(concat('app.js'))
	.pipe(gulp.dest('build/scripts'));
});


// task: handle dependencies
gulp.task('dependencies', function() {
	// skeleton
	// leaflet
	gulp.src([
			'bower_components/skeleton/css/*.css',
			'bower_components/leaflet/dist/leaflet.css'
		])
		.pipe(less({
			plugins: [cleanCss]
		}))
		.pipe(concat('skeleton.css'))
		.pipe(gulp.dest('build/styles'));
	
	// jquery
	// signals
	// leaflet
	gulp.src([
			'bower_components/jquery/dist/jquery.min.js',
			'bower_components/js-signals/dist/signals.min.js',
			'bower_components/leaflet/dist/leaflet.js'
		])
		.pipe(concat('vendor.js'))
		.pipe(gulp.dest('build/scripts'));
});


// task: watch
gulp.task('watch', function() {
	gulp.watch('app/styles/style.less', ['styles']);
	gulp.watch('app/scripts/**/*.js', ['scripts']);
});


// task: default
gulp.task('default', ['clean'], function() {
	gulp.start([
		'dependencies',
		'styles',
		'fonts',
		'scripts',
		'watch'
	]);
});

