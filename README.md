# UniCharter

A program taking and parsing data from University websites and making it into an understandable and easily digestable format for tracking a progress or learning tree.

* `run.sh`: Script to download the data using the API and run the parser

### data/

### parsers/

* `prereqs.py`: A script for reading the units file to get a formatted list of the prerequisities

### scrapers/

* `courses.py`: Queries the API for all the relevant information on the different courses
* `units.py`: Similar functions to the courses script, but for unit information
* `utilities.py`: This is just for shared functions, currently for input sanitation