# Hello, Heroku! #

A skeleton project for running a django project on Heroku. While Heroku have [official](http://devcenter.heroku.com/articles/django) instructions for deploying django on Heroku, I found I still had quite a few questions regarding the _proper_ way to do things like:

* Managing the local development environment in a multi-developer setting
* Handling of editable requirements/non-pypi requirements
* Handling static files
* Good filesystem layout for a project

## Quickstart ##

### Development ###

    source bin/bootstrap
    foreman start
    open http://localhost:5000

### Production deploy ###

    heroku create -s cedar --buildpack https://github.com/Audish/heroku-buildpack-python.git
    heroku labs:enable git_submodules -a <app_name>
    heroku config:add <relevant configuration items>
    git push heroku master
    heroku open

If you're not sure what are the `relevant configuration items` above, run the heroku-config helper to see what environment variables you have in development. Only some of them are relevant for a heroku deployment, I'll make this easier in a later release.

## Features ##

### bin/bootstrap ###

Source bin/bootstrap to create a development virtualenv and install requirements. Every time you activate, bin/activate-local in your project's directory will be sourced, including the handy function 'rebootstrap', that will destroy and recreate your virtualenv. bin/bootstrap also takes care of development environment variables (see below).

### Augmented Python requirements ###

While development requirements and production requirements are slightly different (so django can be installed --editable, for example), you only need to maintain a single `requirements.txt` (and `requirements.txt.dev` will use special syntax to output the development requirements). At the moment, the only special syntax is the `#@prefix` keyword (if you didn't understand, take a look at `requirements.txt` and run `requirements.txt.dev` - it's trivial).

### Development environment variables ###

Rather than littering your code with environment defeaults (i.e., os.environ.get('DEBUG', 'TRUE')), there's an explicit environment.dev file. If it's a _plain_ file, it's expected to contain key=value lines (quote values if necessary) that will be sourced every time you activate. If it's an _executable_, its output will be `eval`uated when you activate, you can do anything there.

### Static files ###

Probably the most opinionated thing in this repository is the way I opted to handle static files, which is rather unorthodox. You can read my lengthy lamentation regarding static asset management [here](http://tech.blog.aknin.name/2011/12/28/i-wish-someone-wrote-django-static-upstream-maybe-even-me/), but it all boils down to my feeling that a modern website has static assets that aren't static at all, and hence I wrote [django-static-upstream](https://github.com/yaniv-aknin/django-static-upstream), a package that aims to treat what are conventionally static assets as dynamic assets. The good news is that you clone this repo and do the quickstart as outlined above, and wham, you have something that works in development and production (for very, very convenient values of "production", like, a blog). There are *significant* things to do if you want this to work in production in a manner that I'd agree with, like putting a caching reverse proxy in front of your static serving URLs and settings `RELEASE_ID` properly in your django `settings.py` file. You will be able to read more about this (and should do that!) in `django-static-upstream`'s documentation, once it will have any. Sometime. Hopefully.


### Submodules ###

Not exactly a feature I implemented, but a demonstration of how I chose to use Heroku's [submodule lab feature](http://devcenter.heroku.com/articles/git-submodules) and the ability to customize `requirements.txt` in development vs. production so that I'll have an editable django module, in case you (like me) needed a couple of inescapable django patches and bugfix backports. Also note that there's a `.slugignore` file that takes care of removing cruft (`.git`, tests, documentation) from the django submodule in order to [keep slug size down](http://devcenter.heroku.com/articles/slug-size). Naturally, this isn't limited just to django.

## Planned features ##

* sample usage of more Heroku addons (postgres, redis, scheduler, etc)

## Caveats ##

Unfortunately, I wrote `bootstrap` before I got familiar with *buildpacks*, Heroku's mostly-smart and definitely very open way of creating the runtime environment (here's the [Python buildpack](https://github.com/heroku/heroku-buildpack-python)). In retrospect, I probably should have thought of a sneaky way to make `bootstrap` script actually use and extend the Python buildpack, maybe I'll do it some day, maybe no. Also, I'm not entirely happy with the fact that this project template needs a custom buildpack, with at least one feature (at the time of this writing) that Heroku refuse to merge - and I understand their judgment on this. I will do my best to send pull requests and follow upstream with the custom buildpack.

Another caveat is that I write all this on `zsh`, and it should work on `bash`, but only out of good intentions, I don't test it there much (if at all). If you use `csh` or a descendant, then you must enjoy pain so much that I will leave it to you do adapt everything here to your weird shell. I'm also doing it all on OSX, so sorry, I'm a weak and bad person.

## Legal and rationale and credits ##
I'm Yaniv Aknin, how do you do. This repository represents my baby steps as I try to iron stuff out on Heroku. Like I said above, I made it because I felt I had a lot of unanswered questions regarding the proper way to do things as [we](http://www.audish.com) are considering/doing the switch to Heroku. This repo ought to be accompanied by a series of posts on my blog, which will be ready, ah, once I get to it. Feel free to browse around, see how I did things, suggest your approach and take anything you want - it's all licensed under the [MIT](http://www.opensource.org/licenses/mit-license.php) license.
