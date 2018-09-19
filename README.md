polso
=====

## Description

The folder is now devided in two subfolders:

* blog
* twitter

In the `blog` folder the AmisScraper is performed, using as spiders:
   * bloomberg.com
   * nogger-noggersblog.blogspot.it
   * world-grain.com
   * euractiv.com
   * agrimoney.com

In the `twitter` folder a scraper based on aabbassian's followers is performed
 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

`Virtualenv` is required to ensure the dependencies are identical accross
different developers.

First install `virtualenv`.

```
pip install virtualenv
```

Then create the directory to store the packages.

```
virtualenv venv/
```

After the `virtualenv` has been installed, we can then activate the
`virtualenv`.

```
source venv/bin/activate
```

You should see your prompt modified with `(venv)` concatenated at the beginning.

After the activation, you can then install the current dependency based on the
`requirements.txt`.

```
pip install -r requirements.txt
```

Once you are done and finished working, deactivate the `virtualenv` by

```
deactivate
```

The `virtualenv` should be invoked every single time you start working on the
project.

To update the `requirement.txt`, simply run the following within the virtual
environment.

```
pip freeze > requirements.txt
```

## Running the `blog` scraper

The scraping Machine can be run automatically, inside the `blog` folder

```
python amis_runner.py
```

or single sources can be scraped

```
scrapy crawl <spider name>
```


## Running the `twitter` scraper

It is important to have the credential to access the Twitter API in `~/credentials.txt`

Inside the `twitter folder`

```
python twitter_followers.py
```
