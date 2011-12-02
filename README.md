# django-staticutils

Some useful additions to `django.contrib.staticfiles` for real-world application
development and deployment.

Currently provides:

* The ability to version static files by an MD5 hash of the file contents (or 
  any other user-defined versioning method.)
* New management commands for static file management, including:
    * `versionstatic`
    * `clearversionedstatic`
* Modifications to the existing `collectstatic` command provided by
  `django.contrib.staticfiles`.

## Rationale

*Why should I be versioning my static files?*

Best practices say that you should set a far-future "Expires" header on
all non-dynamic files so that browsers (and proxies and CDNs) can cache
them for better performance and less overall bandwidth usage. (See
[this Yahoo Best Practices document][Yexpires].)

*How does this application help?*

In a nutshell: `django-staticutils` allows you to set a far-future "Expires"
HTTP header on all of your static files, since every static file will get a
"version tag" added to the filename. Embedding the version tag in the filename,
rather than as part of the querystring, provides several other benefits:

* [some proxies don't cache HTTP responses with a querystring][querycaching],
* enables you to gradually roll out deploys or new features in a distributed
  environment, where some servers might be running a different version of your
  application than others at any moment,
* fast rollback of bad deploys without having to worry about reverting static 
  content on a CDN,
* proxies that modify your HTTP Expires and Cache-Control headers only have an
  effect on one revision on the file, instead of all of them.

[querycaching]: http://www.stevesouders.com/blog/2008/08/23/revving-filenames-dont-use-querystring/
[Yexpires]: http://developer.yahoo.com/performance/rules.html#expires

## Getting Started

### Installation

* Add `staticutils` to your project's `INSTALLED_APPS` setting.
* Add `staticutils.middleware.AssetVersioningMiddleware` to your project's
  `MIDDLEWARE_CLASSES` setting.
* Define a file path for the `VERSIONED_STATIC_ROOT` setting. You'll probably 
  want to make this similar (but not equal) to the `STATIC_ROOT` setting.

### Usage

* Replace every instance of `{{ STATIC_URL }}foo/bar.css` or 
  `{% static 'foo/bar.css' %}` in your templates with the template tag
  `{% versionedstatic "foo/bar.css" %}`. (Replace "`foo/bar.css`" with your 
  actual static asset path.)
* Add `VERSIONED_STATIC_ROOT` to your Django application's settings file. This
  is the location where your generated assets will be stored.

When deploying your static assets, when you would previously run…

    django-admin.py collectstatic

…now you should perform:

    django-admin.py versionstatic
    django-admin.py collectstatic

If you want to be totally under the versioning system you'd do this instead:

    django-admin.py clearversionedstatic # removes old/stale versioned files
    django-admin.py versionstatic --link # symlink, not copy, source files
    django-admin.py collectstatic --only-versioned # only copy versioned assets

## Reference

### Tag Reference

#### {% versionedstatic %} template tag

Replaces the `{{ STATIC_URL }}foo/bar.css` or `{% static 'foo/bar.css' %}`
pattern in templates. This is part of the `versioning` template tag library, 
and can be loaded into a template with `{% load versioning %}`.

Given `{% versionedstatic "foo/bar.css" %}`, the versioned path of the given
static asset is returned instead, with `STATIC_URL` prepended. 

With the default path generator, these given inputs will return these outputs:

* `foo/bar.css` -> `foo/bar.a8d2bd908f64.css`
* `foo/bar` -> `foo/bar.a8d2bd908f64`
* `foo/bar.baz.css` -> `foo/bar.baz.a8d2bd908f64.css`
* `foo/.hiddenfile` -> `foo/.hiddenfile.a8d2bd908f64`

If you'd like hidden files (beginning with a dot/`.`) to not be versioned, set
the `STATIC_VERSION_IGNORE_HIDDEN_FILES` setting to `True`.

### Command Reference

#### versionstatic command

"Collects" versioned static files (the same way `collectstatic` would) into the
filesystem at `VERSIONED_STATIC_ROOT`.

Similar to `collectstatic`, the `--link` option simply turns the versioned path
at `VERSIONED_STATIC_ROOT` into a symlink to the original (wherever it may be).
This is useful if you want to use `collectstatic` to deploy these resources
where they may later be cached (to a secondary webserver, S3/CloudFront or
similar CDN, etc.) This *is* the intended use, but won't work on Windows due to
platform limitations. By default (i.e. without `--link`), this command makes a 
copy of every static asset.

##### Usage

    django-admin.py versionstatic [options] 

    Collects static files from apps and other locations into 
    `VERSIONED_STATIC_ROOT` with a versioned filename. (Used in conjunction 
    with the {% versionedstatic %} template tag.)

All options to this command are identical to the default `collectstatic` 
implementation, and vary between Django versions.

#### clearversionedstatic command

##### Usage

    django-admin.py clearversionedstatic [options]

    Purges *old* versioned static files from `VERSIONED_STATIC_ROOT`. (Files 
    where the version *matches* the source file's current version are not 
    removed, unless the `--all` flag is given.)

    Options:

    --all                 Removes *everything* from `VERSIONED_STATIC_ROOT`, not
                          just old versions
    --noinput             Does not prompt for confirmation when deleting.

#### collectstatic command

Modified to include `VERSIONED_STATIC_ROOT` in addition to the files returned 
by `STATICFILES_FINDERS`. This commands adds the options `--only-versioned` and 
`--plain`, described below.

##### Usage

    django-admin.py collectstatic [options] 

    Collect static files in a single location.

    Options:
    --only-versioned      Only collect static assets from
                          `VERSIONED_STATIC_ROOT`. Cannot be used with
                          `--plain`.
    --plain               Ignore `VERSIONED_STATIC_ROOT`. (Original behavior.)
                          Cannot be used with `--only-versioned`.

## Settings

### STATIC_VERSION_GENERATOR

Defaults to `staticutils.hashing.get_file_hash`.

This should be a callable that accepts two arguments:

* `path`: the path to a file,
* `storage`: the storage instance where the file is located.

The callable should return a string that represent's the file's version.

### STATIC_VERSION_PATH_GENERATOR

Defaults to `staticutils.utils.get_versioned_path`.

This should be a callable that accepts two arguments:

* `path`: the path to a file, relative to `STATIC_ROOT` and `STATIC_URL`,
* `version`: the file's version.

The callable should return a string that represents the versioned file path.

### STATIC_VERSION_HASH_LENGTH

Defaults to `12`.

If using `staticutils.hashing.get_file_hash` for `STATIC_VERSION_GENERATOR`, 
this is the length of the hash's hexdigest returned.

### STATIC_VERSION_IGNORE_HIDDEN_FILES

Defaults to `False`.

If this setting is `True`, files that have a name starting with a leading 
period (`.`) will not be versioned.

## Caveats

* `{% versionedstatic %}` does not version assets when `settings.DEBUG` is 
  `True`.
* The asset versions are defined once at server startup. To update the asset 
  versions, the code must be reloaded -- this can be achived with a server 
  restart. Many servers also provide a POSIX signal interface where a `HUP`
  signal will gracefully reload code without restarting the server and dropping
  existing connections, but refer to your Python server software's documentation 
  for more information.

## Authors

* Ted Kaemming: [Github](http://github.com/tkaemming),
  [Twitter](http://twitter.com/tkaemming)
* Mike Tigas: [Github](http://github.com/mtigas),
  [Twitter](http://twitter.com/mtigas)
