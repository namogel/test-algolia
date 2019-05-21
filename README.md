# Logs parser

## Introduction

This program provides with an api to look for the number of distinct queries/most frequent queries from a given log file and for a given time range. For performance consideration, the log file is parsed asynchronously to extract metadata that will allow the api to respond very quickly, no matter the size of the initial log file.
The metadata consists of the number of distinct queries along with the most frequent queries (which number can be adjusted in the settings.) They are stored on the filesystem, split by time unit: year, month, day... The specific metadata locations in the files are stored in the metadatas of the superior time unit to avoid having to parse the whole files (example: the metadata of 2015 in the years file will store the position of the metadata of January 2015 in the month file)

## Setup

* Setup a virtualenv
* Install requirements: `pip3 install -r requirements.txt`
* Parse logs file: `mkdir data && python3 parsing.py <filename>`
* Launch web server: `FLASK_APP=api.py python3 -m flask run`

## Tests

* `mkdir tests && python3 tests.py`
* TODO: run the tests with pytest to have better debugging output

## Notes

* The log file must be sorted before running parsing.py. It can be sorted with the linux command `sort` if the file is not too big, else we should implement a sorting algorithm.
* Parsing efficiency could be improved by parsing split chunks of the same file simultaneously by multiple threads and sharing the results with each others.
* There can be memory issues if the log file is too big as we store in the RAM all the distinct queries of the sub time units.
* It would be possible to improve the RAM use by storing only the lowest time unit metas and reading the above time unit metas from the filesystem, which would result in higher io.
