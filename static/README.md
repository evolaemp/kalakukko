# kalakukko: static files

Static files comprise the front end scripts of project kalakukko. For the sake
of convenience, all static files live in this directory; the latter follows the
standard webapp structure.

CSS: built with [LESS][le] on top of [Skeleton][sk].

JS: powered by [jQuery][jq].


## setup

Global dependencies: you will need [npm][np], [gulp][gu] and [bower][bo]. After
you install `npm` on your system, you should be able to install `gulp` and
`bower` globally through it:

```bash
npm install -g gulp
npm install -g bower
```

Once you have successfully configured all three of them, do something like:

```bash
npm install
bower install
gulp
```

If you do not want to make any front-end-related changes, you may stop here.


## workflow

```bash
gulp
```

Watches for changes and updates the `build` directory correspondingly. In a
typical workflow, you would have `python manage.py runserver` and `gulp` running
simultaneously.


### Tests

There are also QUnit-powered unit tests for some of the JavaScript modules. You
can access these by pointing your browser at `localhost:8000/js_tests`.


[le]: http://lesscss.org
[sk]: http://getskeleton.com
[jq]: https://jquery.com
[np]: https://www.npmjs.com
[gu]: https://gulpjs.com
[bo]: https://bower.io
