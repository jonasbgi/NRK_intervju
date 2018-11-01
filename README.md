# Solutions for interview with NRK
## Running:
### Prerequisites: 
 - Python 3 

### Run:
Clone the repository, and enter the folder:
```
git clone git@github.com:jonasbgi/NRK_intervju.git
cd NRK_intervju/
``` 
and run using:
```
python3 Main.py
```

## Overview:
### Rationale: 
Python was selected as the programming language because of the extremely simple setup. Because I cannot demonstrate by running the project on my laptop, and "it runs on my machine" might not soffice, I prioritized a simple setup.

### Architecture: 
The app is a simple console-based python-script which uses built-in functions to create a minimalisitc and at times less-than user-friendly user-experience. 

To parse request, simple dictionaries map strings to functions (and descriptions of functions for help). 
The main console-menu will call two functions, ```showScreeningMenu ``` or ```listMenu``` depending on input. These create menus to either display a given screening based on id and date, or list several screenings depending or parameters respectively. 

The function responsible for getting several screenings, ```listSeries``` takes an input of a nested list, and accumulated a dictionary looking like ```{serieId: {[# of views, latestDate]}``` which effectively collects data about all the series. Only screenings which pass a given filter are added. 

The filter-classes are simple classes which can be set to various settings, and accepts screenings formatted as ```[title, year, type, views]``` and returns true or false based on the list. For example, it may only give true if type='tv'. Among those filters are also the CombinedFilter, which will run the list trough several given filters, such that one may filter on both date and type for example. 

## Other solutions: 
With performance in mind, the by far easiest and likely fastest solution would be a simple database with a shell to write SQL-queries. This would however require me to a) host a database online or b) have the interviewers install and run the database. 

With respect to making useful code, the best would maybe be a form of RESTful API, for instance built on Node and Express. This would let any app use data we process, and would be much easier to use across applications. However, given the timeframe of less than one working-day, this was considered overambitious. This API could then use a database-server to also have quite good performance. 

