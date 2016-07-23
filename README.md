polso
=====

Tools for scraping Twitter/Facebook/WWW


# AMIS Scraper

This package contains tools for scraping data from

* bloomberg.com
* nogger-noggersblog.blogspot.it
* world-grain.com
* euractiv.com
* agrimoney.com

in orrder to construct a crisis prediction model based on a sentiment index.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

You need to install scrapy to run the scaper.

```
pip install scrapy
```

### Running the Scraper

The scraping Machine can be run automatically

```
python amis_runner.py
```
or single sources can be scraped

```
scrapy crawl <spider name>
```

where the available spiders are

* bloomberg
* noggers
* worldgrain
* euractiv
* agrimoney


