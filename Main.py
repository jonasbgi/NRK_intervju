import Dataloader
import Filters

# Excecutes task 1 - 4
# Creates a blank dict series, which is used to accumulate number of views.
# Views are only added if they pass the filter, which can be either specific type, year or both (Dependency injection).
# (See Filters.py)
# Sorts either by name or number of views.
def listSeries(screeningsRawData, sortOnDate = False, filter=Filters.NoFilter()):
	# Series takes the following structure:
	# {seriesId: [# of views, (int) latest date]
	series = {}
	# Note: rows are structured ['title', 'date', 'views']
	for row in screeningsRawData:
		if (row[0] in series.keys()) and filter.filter(row):
			if( int(row[1]) > series[row[0]][1]):
				latestDate = int(row[1])
			else:
				latestDate = int(series[row[0]][1])
			series[row[0]] = [series[row[0]][0] + int(row[3]), latestDate]
		else:
			series[row[0]] = [int(row[3]), int(row[1])]
	
	
	if(sortOnDate):
		sortedSeriesKeys = sorted(series.keys(), key= lambda key: series[key][1], reverse=True)
	else:
		sortedSeriesKeys = sorted(series.keys())
	
	print("SeriesID".ljust(24) +"Views".rjust(10) + "Date".rjust(12))
	for key in sortedSeriesKeys:
		#TODO: Prettier print
		print(str(key).ljust(24) + str(series[key][0]).rjust(10) + str(series[key][1]).rjust(12))

# Excecutes task 5
def getScreening(screeningRawData, showTitle, date):
	for screening in screeningRawData:
		if screening[0] == showTitle and screening[1] == date:
			return screening
	return None

# Command-line menu to select a specific screening. Will list all serieIds, then return.
# Answers tasks 1 trough 4 by using various user-inputs.
def listMenu(screeningsRawData):
	options = {
		'year=xxxx':'Filters on year. I.e. year=2018 will only allow screenings from 2018 to be listed',
		'type=xx': "Filters on screening type. Can be 'tv', 'mobile', 'tablet', 'desktop'. I.e. type='tv' will only count TV-screenings",
		'sort-on-date': "Sorts screenings on date"
	}
	
	sort_on_date = False
	
	
	print("Listing various screenings:\n"
		  "Please enter options, or type 'help' for list of options. For several options, separate by with space")
	selectedOptions = input().lower().split()
	
	filterList = []
	if "help" in selectedOptions:
		printHelpFromDict(options)
		listMenu(screeningsRawData)
		
	else:
		if len(selectedOptions) == 0:
			print("No options found. Listings series based on default values.")
		for opt in selectedOptions:
			if 'year' in opt:
				year = opt.split('=')[1]
				filterList.append(Filters.FilterOnYear(year=year))
			elif 'type' in opt:
				type = opt.split('=')[1]
				filterList.append(Filters.FilterOnType(type=type))
			elif 'sort-on-date' in opt:
				sort_on_date = True
		
		
		filter = Filters.CombinedFilter(filterList)
		listSeries(screeningsRawData, sortOnDate=sort_on_date, filter=filter)

# Command-line menu to select a specific screening. Loops until one has been found, or user input "exit"
# Answers task 5 - "Hent all data for en gitt serieid og en gitt dato"
def showScreeningMenu(screeningsRawData):
	succeeded = False
	while not succeeded:
		print("Showing specific screening:\n"
			  "Please enter seriesId and date separated by space. Note that date must have format 'yyyymmdd'.")
		queryOptions = input().lower().split()
		if len(queryOptions) >= 2:
			seriesId = queryOptions[0]
			date = queryOptions[1]
			screening = getScreening(screeningsRawData, seriesId, date)
			if screening:
				print("SeriesID: %s \n"
					  "Date: %s \n"
					  "Type: %s \n"
					  "Views: %s \n" %(screening[0], screening[1], screening[2], screening[3]))
				succeeded = True
			else:
				print("Screening not found. Please retry, or input exit to quit. ")
		else:
			if 'exit' in queryOptions:
				succeeded = True
				print("Exiting screening submenu")

# Utility to print out possible commands from menu or submenu.
# If the dict is {function: description}, subkey is not needed. In nested dicts, subkey can be set to access correct value.
def printHelpFromDict(functionDict, subkey=None):
	print("Possible commands: ")
	for key in functionDict.keys():
		if subkey:
			desc = str(functionDict[key][subkey])
		else:
			desc = str(functionDict[key])
		print(key +": "+ desc +"\n")

if __name__ == '__main__':
	#Load data:
	screeningsRawData = Dataloader.loadData('./visningsdata.csv')
	
	# List of usable commands with functions. Executed by using commans[key]["function"](screeningsRawData)
	# Using dict for easier modifications of code.
	commands = {
		"list-series": {
			"function": listMenu,
			"description": "Lists all screeningIds with optional filters on year and type. Can sort by # of views or date"
		},
		"show-screening": {
			"function": showScreeningMenu,
			"description": "Lets you try to find a screening with a given seriesId and date. "
		},
		"exit": {
			"function": lambda: True,
			"description": "Quits the program"
		}
	}
	
	# Loop to get user-input.
	hasQuit = False
	while not hasQuit:
		print("\nPlease enter a command or type help for a list of commands. Quit by typing exit ")
		command = input().lower()
		
		if command == "exit":
			hasQuit = True
		elif command in commands.keys():
			commands[command]['function'](screeningsRawData)
		elif command == "help":
			printHelpFromDict(commands, subkey="description")
		