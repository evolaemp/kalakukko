# Kalakukko: Static Files

Static files comprise the front end scripts of project Kalakukko. For the sake
of convenience, all static files live in this directory; the latter follows the
standard webapp structure.

CSS: built with [LESS](http://lesscss.org/) on top of
[Skeleton](http://getskeleton.com/).

JS: powered by [jQuery](http://jquery.com).


## Initialisation

Global dependencies: you will need [npm](https://www.npmjs.com),
[gulp](http://gulpjs.com) and [bower](http://bower.io). After you install `npm`
on your system, you should be able to install `gulp` and `bower` globally
through it:

```
npm install -g gulp
npm install -g bower
```

Once you have successfully configured all three of them, do something like:

```
npm install
bower install
gulp
```

If you do not want to make any front-end-related changes, you may stop here.


## Workflow

```
gulp
```
Watches for changes and updates the `build` directory correspondingly. In a
typical workflow, you would have `python manage.py runserver` and `gulp` running
simultaneously.


### Tests

There are also QUnit-powered unit tests for some of the JavaScript modules. You
can access these by pointing your browser to `/js_tests` (the django development
server has to be running, of course).

