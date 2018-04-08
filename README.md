# kalakukko

Source code of project kalakukko.

The back end is powered by [Django][dj] and fuelled by [Python3][py]. The front
end has a README of its own in the `static` directory.


## setup

Do something like:

```bash
# clone this repo
git clone https://github.com/evolaemp/kalakukko
cd kalakukko

# create a virtual environment
python3 -m venv meta/env
source meta/env/bin/activate

# install the dependencies
pip install -r requirements.txt
```

Now you have to create your own `settings_local.py` in the `project` directory.
You should include at least the following settings:

* `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
* `STATICFILES_DIRS`, `STATIC_ROOT`, `STATIC_URL`
* `MEDIA_ROOT`, `MEDIA_URL`
* `JS_TESTS_ROOT`, `QUNIT_ROOT`
* `DATABASES`
* `CACHES` (needed for storing uploaded files for subsequent API requests)
* `EMAIL_BACKEND` (e.g. `locmem` for testing and `console` for developing),
  `DEFAULT_FROM_EMAIL`, `EMAIL_SUBJECT_PREFIX`
* `ADMINS`, `MANAGERS`
* `OSM_ACCESS_TOKEN`, `OSM_ID` (auth for an Open Street Maps tile provider)

There is an example configuration in `project/settings_local.example`. You can
use it for local development by copying the file (do not move it, as this would
delete it from the repo). However, do not forget to generate a fresh
`SECRET_KEY` whenever deploying on a publicly visible server.

And now you are safe to `python manage.py migrate`.


## fixtures

The following fixtures are provided for the purposes of unit testing:

* `app/fixtures/berg.tsv` is a sample .tsv file; these files are the main source
  of data input for project Kalakukko.
* `app/fixtures/iso-639-3.tab` is used by the `extract_languages` command in
  order to fix the ISO codes problem (see below). The file is downloaded from
  [SIL International][si], the registration authority for ISO 639-3.
* `app/fixtures/languages.tab` is used to harvest language information such as
  geographical coordinates.
* `app/fixtures/languages.json` is the database dump of the languages found in
  `app/fixtures/berg.tsv` extracted using the `extract_languages` command.
* `app/fixtures/locations` is used for unit testing the
  `harvest_language_locations` command.


## workflow

```bash
source meta/env/bin/activate
python manage.py runserver
```

Do not forget `python manage.py test` and `python manage.py migrate`, they are
your friends!


### custom commands

The following two commands are used to populate the database. The latter
consists of a single model, `Language`, with four fields: `iso_639_3`,
`iso_639_1`, `latitude`, and `longitude`. You may populate the database in any
way you want, the commands below are just helpers.

```bash
python manage.py extract_languages <tsv_file> [iso_codes_file]
```

Extracts the ISO codes present in the .tsv file supplied as an argument to the
command. For each ISO code a language entry is created in the database, unless
such already exists.

It also takes care of the ISO code problem: while the language info files use
ISO 639-3, the .tsv files use ISO 639-1 where available. That is why when a
two-letter ISO code is encountered, it is looked up in the iso codes file,
specified in the second (optional) command argument, the default value of which
is `app/fixtures/iso-639-3.tab`.

```bash
python manage.py harvest_language_info <language_info_file>
```

Collects and stores to the database the geographical locations for the languages
currently in the database. Languages which are not in the database are ignored.
If there is discrepancy between file and database, the user is notified.

```bash
python manage.py harvest_language_locations <language_locations_file>
```

Same as above, but the input format is different. While the previous command
expects Jäger's language info data files, this command wants to be fed with
lines of whitespace-separated ISO 639-3 code, latitude, and longitude. If you
want to use another input format, use this command's code as a starting point.
Warning: this command overwrites other latlng info in the database.


[dj]: https://www.djangoproject.com
[py]: https://www.python.org
[si]: http://www-01.sil.org/iso639-3/download.asp
