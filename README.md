# fetching-soccer-matches
Python script that uses [football-data-api](https://pypi.org/project/football-data-api/) to pull data for each match from Europe's top 5 leagues and the Champions League into a local excel spreadsheet, allowing the user to keep track of which soccer matches they've already watched / seen highlights of (or to just gather all the data).

## What it does
When the get_matches.py script runs, it finds the most recent match date currently stored in matches.xlsx and, for every match that occurred on or after that date and is from one of the leagues specified in the `competitions` variable, it adds a row to matches.xlsx. This way, once the script finishes, you know that the spreadsheet contains every match that has been played since the first time you ran it.


The fields saved for each match are:
* Done with? ("NO" if the match was not already saved in the spreadsheet, otherwise keeps the value that the match already had) 
* Date
* Day of Week
* Time
* Home Team
* Home Score
* Away Team
* Away Score
* Competition
* Match ID (used to check if a match is already in the spreadsheet and determine its appropriate "Done with?" value)

I use the spreadsheet to keep track of which matches I still want to watch highlights for by changing a match's Done with? value to "YES" once I've watched its highlights or if I don't want to watch its highlights.

If the script is run on a spreadhseet that's empty, it will get data for matches from the past 7 days. 

## Set up / instructions
1) Download this entire repository.
2) Run `pip install -r requirements.txt` in your commnnand line to install the necessary packages.
3) Run the get_matches.py script. If it's your first time running it you'll be prompted to enter your API key, which you can get for free [here](https://www.football-data.org/client/register). For convenience, I recommend hardcoding your API key (as long as your script is only stored locally) by chaning this line in the code 
`os.environ["FOOTBALL_DATA_API"] = input("Enter your api key: ")` \ 
to \
`os.environ["FOOTBALL_DATA_API"] = "your_api_string"`.
4) Open the matches.xlsx file and you'll see the new data added!

## Optional Modifications
1) Change the `competitions` variable to get match data for more leagues (but some leagues require you to pay).
2) To specify your own date range to get match data for, modify this line: \
`matches = data.get_info('matches', dateFrom=last_date_date, dateTo=n_days_ago_or_in_the_future(0))["matches"]` \
to something like this \
`matches = data.get_info('matches', dateFrom=n_days_ago_or_in_the_future(-10), dateTo=n_days_ago_or_in_the_future(10))["matches"]` \
which will get all the matches that were played on or after the date 10 days ago and on or before the date 10 days in the future. \
or something like this \
`matches = data.get_info('matches', dateFrom=datetime(2022, 8, 20), dateTo=datetime(2022, 8, 27))["matches"]` \
which will get data for all matches on or after August 20, 2022 and on or before August 27, 2022.
