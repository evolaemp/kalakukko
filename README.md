# Kalakukko

Source code of project Kalakukko.

The back end is powered by [Django](https://www.djangoproject.com) and fuelled
by [Python3](https://www.python.org/). The front end has a README of its own in
the `static` directory.

The `development` directory is ignored by git by default, so you can use it for
local storage.


## Initialisation

Do something like:

```
git clone && cd
virtualenv /path/to/environments/kalakukko
source /path/to/environments/kalakukko/bin/activate
pip install -r requirements.txt
```

Now you have to create your own `settings_local.py` in the `project` directory.
You should include at least the following settings:

* `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
* `STATICFILES_DIRS`, `STATIC_ROOT`, `STATIC_URL`
* `MEDIA_ROOT`, `MEDIA_URL`
* `DATABASES`
* `EMAIL_BACKEND` (e.g. `locmem` for testing and `console` for developing),
  `DEFAULT_FROM_EMAIL`, `EMAIL_SUBJECT_PREFIX`
* `ADMINS`, `MANAGERS`
* `OSM_ACCESS_TOKEN`, `OSM_ID` (auth for an Open Street Maps tile provider)

There is an example configuration in `project/settings_local.example`. You can
use it for local development by copying the file (do not move it, as this would
delete it from the repo).

And now you are safe to `python manage.py syncdb`.


## Fixtures

The following fixtures are provided for the purposes of unit testing:

* `app/fixtures/berg.tsv` is a sample .tsv file---these files are the main
  source of data input for project Kalakukko.
* `app/fixtures/iso-639-3.tab` is used by the `extract_languages` command in
  order to fix the ISO codes problem (see below). The file is downloaded from
  [SIL International](http://www-01.sil.org/iso639-3/download.asp), which is the
  registration authority for ISO 639-3.
* `app/fixtures/languages.tab` is used to harvest language information such as
  geographical coordinates.


## Workflow

```
source /path/to/environments/kalakukko/bin/activate
python manage.py runserver
```
Do not forget `python manage.py test` and `python manage.py migrate`, they are
your friends!


### Custom commands

```
python manage.py extract_languages <tsv_file> [iso_codes_file]
```
Extracts the ISO codes present in the .tsv file that is supplied as an argument
to the command. For each ISO code a language entry is created in the database,
unless such already exists.

It also takes care of the ISO code problem: while the language info files use
ISO 639-3, the .tsv files use ISO 639-1 where available. That is why when a
two-letter ISO code is encountered, it is looked up in the iso codes file,
specified in the second (optional) command argument, the default value of which
is `app/fixtures/iso-639-3.tab`.


```
python manage.py harvest_language_info <language_info_file>
```
Collects and stores to the database the geographical distances for the languages
currently in the database. Languages which are not in the database are ignored.
If there is a discrepancy between file and database, the user is notified.


