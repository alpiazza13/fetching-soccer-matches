import os
import time
import calendar
import pandas as pd
from football_data_api import data_fetchers
from datetime import datetime, timedelta

os.environ["FOOTBALL_DATA_API"] = input("Enter your api key: ")
data = data_fetchers.CompetitionData()

def n_days_ago_or_in_the_future(n):
    today = datetime.today()
    return today + timedelta(days=n)

old_matches = pd.read_excel("matches.xlsx")
if len(old_matches) > 0:
    last_date = old_matches["Date"].tolist()[0]
    last_date_date = datetime.strptime(last_date, "%m/%d/%Y")
else:
    last_date_date = n_days_ago_or_in_the_future(-7)

def get_match_info(match, competition):
    home_team = match["homeTeam"]['name']
    away_team =  match["awayTeam"]["name"]
    home_team_score = match["score"]["fullTime"]["homeTeam"]
    away_team_score = match["score"]["fullTime"]["awayTeam"]
    result = match["score"]['winner']
    date_and_time = match["utcDate"]

    date_and_time_separate = date_and_time.split("T")
    date, time = date_and_time_separate[0], date_and_time_separate[1][:-4]
    print(f"{date} at {time}: {home_team} vs {away_team}, {home_team_score}-{away_team_score}")
    return {"Home": home_team, "Away": away_team, "Home Score": home_team_score, "Away Score": away_team_score, "match_date": date_and_time, "Match ID": match["id"], "Competition": competition}

def get_data(competition):
    data.competition = competition
    matches = data.get_info('matches', dateFrom=last_date_date, dateTo=n_days_ago_or_in_the_future(0))["matches"]

    print(f"\n{competition} matches:")
    return [get_match_info(match, competition) for match in matches]

competitions = ['serie a', 'premier league', 'uefa champions league', 'ligue 1', 'bundesliga', 'primera division']
all_data_dicts = []
print(f"Getting all matches since {last_date_date.strftime('%-m/%d/%Y')}...")
for competition in competitions:
    data_dicts = get_data(competition)
    all_data_dicts += data_dicts

new_matches = pd.DataFrame(all_data_dicts) # all new matches
dates = pd.to_datetime(new_matches['match_date'])
new_matches["match_date"] = dates
dates_eastern = dates.apply(lambda date: date + timedelta(hours=-4))
new_matches["Date"] = dates_eastern.apply(lambda x: x.strftime("%-m/%d/%Y"))
new_matches["Time"] = dates_eastern.apply(lambda x: x.strftime("%-I %p"))
new_matches["Day"] = dates_eastern.apply(lambda x: calendar.day_name[x.weekday()])

ids = new_matches["Match ID"].tolist() # all new match ids
assert len(ids) == len(set(ids)) # check that no duplicate new ids
old_matches = pd.read_excel("matches.xlsx")
print(f"You previously had {len(old_matches)} matches.")
old_match_ids = old_matches["Match ID"].tolist()

# for any id that is in both new and old data, keep the old done_with value by changing it in the new_matches table
def pick_done_with_value(match_id):
    if match_id in old_match_ids:
        return old_matches[old_matches["Match ID"] == match_id]["Done with?"].tolist()[0]
    else:
        return "NO"

new_matches["Done with?"] = new_matches.apply(lambda row: pick_done_with_value(row["Match ID"]), axis=1)
old_matches = old_matches[~old_matches["Match ID"].isin(ids)] # remove ids in old data that are in new data
all_matches = old_matches.append(new_matches) # combine new and old data

all_match_ids = all_matches["Match ID"].tolist() # all new and old ids
assert len(all_match_ids) == len(set(all_match_ids)) # check that no duplicate ids in final data
all_matches.sort_values("match_date", inplace=True, ascending=False) # sort by date
all_matches.reset_index(drop=True, inplace=True) # drop index
all_matches.drop(labels="Unnamed: 0", axis=1, inplace=True, errors="ignore")
all_matches.drop(labels="match_date", axis=1, inplace=True)

column_ordering = ["Done with?", "Date", "Day", "Time", "Home", "Home Score", "Away Score", "Away", "Competition", "Match ID"]
all_matches = all_matches[column_ordering] # reorder columns
all_matches.to_excel("matches.xlsx", index=False) # send to excel
print(f"You now have {len(all_matches)} matches.")
