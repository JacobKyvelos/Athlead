from traceback import print_tb
import mysql.connector
from asyncio.windows_events import NULL
import requests
import json
import pandas as pd
import time

# url = "https://api-nba-v1.p.rapidapi.com/teams"

# headers = {
#     'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
#     'x-rapidapi-key': "71df5c7d97msh81656ed06f59badp159b26jsna1076804ff4f"
#     }

# response = requests.request("GET", url, headers=headers)

# games_ids = response.json()

# with open('koumpo.json', "w") as games_ids_file:
#     json.dump(games_ids, games_ids_file)
# games_ids_file.close()



mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="199938-41",
  database="basketball"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE Basketball")

# teams = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]


# with open("koumpo.json") as jsonFile:
#     data = json.load(jsonFile)
#     jsonData = data["response"]
#     #for i in range(0, 62):
#     #print(jsonData[2]["points"])
#     c = 0
#     lista = []
#     for data in jsonData:
#         if data["id"] == 16:
#             print(data["name"])
#             sql = "INSERT INTO `team` (`team_id`, `team_name`, `team_nickname`, `code`, `city`, `logo_url`) VALUES (%s, %s, %s, %s, %s, %s)"
#             val = (data["id"], data["name"], data["nickname"], data["code"], data["city"], data["logo"])
#             mycursor.execute(sql, val)

#             mydb.commit()

#             print(mycursor.rowcount, "record inserted.")

###############################################################################

# mycursor.execute("select `team_id`, `lineup` from team")

# myresult = mycursor.fetchall()

# for x in myresult:
#     team_id = x[0]
#     lineup = x[1]


#     # 1) FIND ALL PLAYERS

#     url = "https://api-nba-v1.p.rapidapi.com/players/teamId/" + str(team_id)

#     headers = {
#         'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
#         'x-rapidapi-key': "62c9fa5bfamshed0ab97c3766b02p1fcfb5jsnc9e3c94f89ed"
#         }

#     response = requests.request("GET", url, headers=headers)

#     all_players = response.json()

#     with open('all_players.json', "w") as all_players_file:
#         json.dump(all_players, all_players_file)
#     all_players_file.close()

#     print("All players inserted successfully!")

#     dict = {}
#     players_api = []
#     with open("all_players.json") as jsonFile:
#         data = json.load(jsonFile)
#         jsonData = data["api"]
#         results = 0
#         for i in jsonData['players']:
#             results += 1
#         for i in range(0, results):
#             name = jsonData['players'][i]["firstName"] + ' ' + jsonData['players'][i]["lastName"]
#             id = jsonData['players'][i]["playerId"]
#             players_api.append(name)
#             dict[id] = name
#     jsonFile.close()

#     # 2) FIND CURRENT PLAYERS

#     url = lineup
#     current_players = []
#     df = pd.read_html(url)
#     for i in df[0]['Name']:
#         i = i.split(' ')
#         x = len(i)/2
#         x = int(x)
#         word = ''
#         for j in range(0, x):
#             word = word + ' ' + i[j]
#         current_players.append(word[1:])


#     # 3) FIND COMMON PLAYERS
#     dict2 = {}
#     for key in dict:
#         if dict[key] in current_players:
#             dict2[key] = dict[key]
#     dict = dict2
#     print(dict)
#     for y in dict:
#         sql = "INSERT INTO `player` (`player_id`, `team_id`, `full_name`) VALUES (%s, %s, %s)"
#         val = (int(y), team_id, dict[y])
#         mycursor.execute(sql, val)

#         mydb.commit()

#         print(mycursor.rowcount, "record inserted.")
#     time.sleep(30)

###############################################################################

def games_ids(team_id, year):
    url = "https://api-nba-v1.p.rapidapi.com/games/teamId/" + str(team_id)

    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "62c9fa5bfamshed0ab97c3766b02p1fcfb5jsnc9e3c94f89ed"
        }

    response = requests.request("GET", url, headers=headers)

    games_ids = response.json()

    with open('all_games_ids.json', "w") as games_ids_file:
        json.dump(games_ids, games_ids_file)
    games_ids_file.close()

    game_ids_list = []
    with open("all_games_ids.json") as jsonFile:
        data = json.load(jsonFile)
        jsonData = data["api"]
        #for i in range(0, 62):
        results = 0
        for i in jsonData['games']:
            results += 1
        for i in range(0, results):
            if jsonData['games'][i]["seasonYear"] == str(year):
                game_ids_list.append(int(jsonData['games'][i]["gameId"]))
    #print(game_ids_list)
    jsonFile.close()
    return game_ids_list


def players_stats(game_ids_list, player_id):
    url = "https://api-nba-v1.p.rapidapi.com/statistics/players/playerId/" + str(player_id)
    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "62c9fa5bfamshed0ab97c3766b02p1fcfb5jsnc9e3c94f89ed"
        }
    response = requests.request("GET", url, headers=headers)
    players_games = response.json()
    with open('player_stats.json', "w") as stats_file:
        json.dump(players_games, stats_file)
    stats_file.close()

    with open("player_stats.json") as jsonFile:
        data = json.load(jsonFile)
        jsonData = data["api"]
        #for i in range(0, 62):
        results = 0
        for i in jsonData['statistics']:
            results += 1
        points = 0
        active_games = 0
        for i in range(0, results):
            if jsonData['statistics'][i]["points"] == '':
                pass
            elif int(jsonData['statistics'][i]["gameId"]) in game_ids_list:
                points += int(jsonData['statistics'][i]["points"])
                active_games += 1
        ppg = "{:.1f}".format(points/active_games)
        assists = 0
        for i in range(0, results):
            if jsonData['statistics'][i]["assists"] == '':
                pass
            elif int(jsonData['statistics'][i]["gameId"]) in game_ids_list:
                assists += int(jsonData['statistics'][i]["assists"])
        apg = "{:.1f}".format(assists/active_games)
        rebs = 0
        for i in range(0, results):
            if jsonData['statistics'][i]["totReb"] == '':
                pass
            elif int(jsonData['statistics'][i]["gameId"]) in game_ids_list:
                rebs += int(jsonData['statistics'][i]["totReb"])
        rpg = "{:.1f}".format(rebs/active_games)
        print(ppg,' ', apg,' ', rpg)

    jsonFile.close()
    return ppg, apg, rpg



game_ids_list = games_ids(21, year)
players_stats(game_ids_list, player_id)