# DjangoCon Yearbook

WIP: When I wrote this years ago, my goal was to compile a DjangoCon Yearbook to track all of the talks, speakers, and organizers from all of the DjangoCons over the years.

## getting started

```shell
# install libraries
$ pip install grab rich typer

# see all options
$ python djangocon_yearbook.py --help

# fetch data from 2008 to 2015 (some may timeout)
$ python djangocon_yearbook.py fetch-all

# list all talks from our CSV files (should rename this)
$ python djangocon_yearbook.py build-csv
```
