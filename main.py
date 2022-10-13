from cgi import print_directory
from tkinter.font import names
from flask import Flask, render_template
import requests
import json
import pandas as pd
from unittest import result 
import mysql.connector
import os
from flask_jsglue import JSGlue

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="199938-41",
  database="basketball"
)


def basketball_player_stats(cat, url):
    #url = 'https://www.basketball-reference.com/players/a/antetgi01.html'
    df = pd.read_html(url)
    print(df[cat])

    mega_list = []
    lista = []

    mega_list2 = []
    columns = []

    for col in df[cat].columns:
        columns.append(col)
    mega_list2.append(columns)

    for col in df[cat].columns:
        lista = []
        for i in df[cat][col]:
            lista.append(i)
        mega_list.append(lista)

    length = len(mega_list[0])

    for i in range(0, length):
        lista2 = []
        for item in mega_list:
            lista2.append(item[i])
        mega_list2.append(lista2)

    return  mega_list2




def all_season_league_stats():
    url = 'https://www.basketball-reference.com/leagues/NBA_stats_per_game.html'
    df = pd.read_html(url)

    mega_list = []
    lista = []

    mega_list2 = []
    lista2 = []

    for col in df[0].head(20).columns:
        lista2.append(col[1])
    mega_list2.append(lista2)

    for col in df[0].head(20).columns:
        lista = []
        for i in df[0].head(20)[col[0]][col[1]]:
            lista.append(i)
        mega_list.append(lista)

    # print(mega_list)
    # print(len(mega_list[1]))

    for i in range(0, 20):
        lista2 = []
        for item in mega_list:
            lista2.append(item[i])
        mega_list2.append(lista2)
    
    return mega_list2


def sql_to_json(player_id):
   cur = mydb.cursor()
   sql = "SELECT * FROM player_stats WHERE player_id = %s ORDER BY year ASC"
   adr = (player_id, )
   cur.execute(sql, adr)
   row_headers=[x[0] for x in cur.description] #this will extract row headers
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   return json_data

def list_of_players(team_id):
    url = "https://api-nba-v1.p.rapidapi.com/players/teamId/" + str(team_id)

    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "62c9fa5bfamshed0ab97c3766b02p1fcfb5jsnc9e3c94f89ed"
        }

    response = requests.request("GET", url, headers=headers)

    all_players = response.json()

    with open('all_players.json', "w") as all_players_file:
        json.dump(all_players, all_players_file)
    all_players_file.close()

    print("All players inserted successfully!")

    dict = {}
    with open("all_players.json") as jsonFile:
        data = json.load(jsonFile)
        jsonData = data["api"]
        results = 0
        for i in jsonData['players']:
            results += 1
        for i in range(0, results):
            name = jsonData['players'][i]["firstName"] + ' ' + jsonData['players'][i]["lastName"]
            id = jsonData['players'][i]["playerId"]
            dict[id] = name
    jsonFile.close()
    return dict


def cur_players():
    url = "https://www.lineups.com/nba/roster/milwaukee-bucks"
    current_players = []
    df = pd.read_html(url)
    for i in df[0]['Name']:
        i = i.split(' ')
        x = len(i)/2
        x = int(x)
        word = ''
        for j in range(0, x):
            word = word + ' ' + i[j]
        current_players.append(word[1:])
    return current_players

def common_players(current_players, dict):
    dict2 = {}
    for key in dict:
        if dict[key] in current_players:
            dict2[key] = dict[key]
    return dict2

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


def pandas_fixture():
    url = "https://www.espn.com/nba/team/schedule/_/name/mil"
    lista = []
    df = pd.read_html(url)
    df = df[0]
    x = df[df[2] == 'TIME'].index
    for j in range(0, 3):
        for i in df[x[0]+1:][j]:
            print(i)
            lista.append(i)
    # print(len(lista))
    # step = int(len(lista) / 3)
    # for i in range(0, step):
    #     print(lista[i], ' ', lista[i+step], ' ',lista[i+2*step])
    return lista

app = Flask(__name__)
JSGlue(app)

@app.route("/")
def home():
    return render_template("home_no1.html")


@app.route("/categories")
def categories():
    return render_template("selection.html")



@app.route("/football_leagues")
def football_leagues():
    leaguesIds = []
    leaguesLogos = []
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("select `league_id`, `league_log` from football_leagues")
    myresult = mycursor.fetchall()
    for x in myresult:
        leaguesIds.append(x[0])
        leaguesLogos.append(x[1])
    step = len(leaguesIds)
    return render_template("football_leagues_2.html", leaguesIds = leaguesIds, leaguesLogos = leaguesLogos, step = step)

@app.route("/football/league:<league_id>")
def league_home(league_id):
    return render_template("football_home.html", league_id = league_id)

@app.route("/football/league:<league_id>/teams")
def league_teams(league_id):
    teamIds = []
    teamLogos = []
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT team_id, logo FROM football_team WHERE league_id = %s"
    adr = (league_id, )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    for row in myresult:
        teamIds.append(row[0])
        teamLogos.append(row[1])
    step = len(teamIds)
    print(step)
    print(league_id)
    return render_template("football_teams.html", league_id = league_id, teamIds = teamIds, teamLogos = teamLogos, step = step)

# @app.route("/football/league:<league_id>/team:<team_id>")
# def football_team_home(league_id, team_id):
#     mycursor = mydb.cursor(buffered=True)
#     sql = "SELECT logo FROM football_team WHERE team_id = %s"
#     adr = (team_id, )
#     mycursor.execute(sql, adr)
#     myresult = mycursor.fetchone()
#     logo = myresult[0]
#     return render_template("football_team_home.html", league_id = league_id, team_id = team_id, logo = logo)




@app.route("/football/league:<league_id>/team:<team_id>/player:<player_id>")
def football_player_home(league_id, team_id, player_id):
    # mycursor = mydb.cursor(buffered=True)
    # sql = "SELECT logo FROM football_team WHERE team_id = %s"
    # adr = (team_id, )
    # mycursor.execute(sql, adr)
    # myresult = mycursor.fetchone()
    # print(myresult)
    # logo = myresult[0]
    return render_template("football_player_home.html", league_id = league_id, team_id = team_id, player_id = player_id)





@app.route("/football/league:<league_id>/team:<team_id>/players")
def football_team_players(league_id, team_id):
    return render_template("football_team_players_2.html", league_id = league_id, team_id = team_id)

@app.route("/football/league:<league_id>/team:<team_id>/fixtures")
def football_team_fixtures(league_id, team_id):
    return render_template("football_team_fixtures.html", league_id = league_id, team_id = team_id)

@app.route("/football/league:<league_id>/team:<team_id>/results")
def football_team_results(league_id, team_id):
    return render_template("football_team_results.html", league_id = league_id, team_id = team_id)

@app.route("/football/league:<league_id>/team:<team_id>/team_stats")
def football_team_stats(league_id, team_id):
    return render_template("football_team_stats.html", league_id = league_id, team_id = team_id)

@app.route("/football/league:<league_id>/team:<team_id>/live_results")
def football_team_live(league_id, team_id):
    return render_template("football_team_live.html", league_id = league_id, team_id = team_id)








@app.route("/football/league:<league_id>/fixtures")
def league_fixtures(league_id):
    return render_template("football_fixtures.html", league_id = league_id)

@app.route("/football/league:<league_id>/stats")
def league_stats(league_id):
    return render_template("football_league_stats.html", league_id = league_id)

@app.route("/football/league:<league_id>/results")
def league_results(league_id):
    return render_template("football_results.html", league_id = league_id)

@app.route("/football/league:<league_id>/players_comparison")
def league_players_comparison(league_id):
    return render_template("football_comparison_2.html", league_id = league_id)

@app.route("/football/league:<league_id>/results/<game_id>")
def football_game_details(league_id, game_id):
    return render_template("football_game_details.html", league_id = league_id, game_id = game_id)



@app.route("/football/league:<league_id>/tables")
def league_tables(league_id):
    return render_template("football_tables.html", league_id = league_id)

@app.route("/football/league:<league_id>/live_games")
def league_live(league_id):
    return render_template("football_league_live.html", league_id = league_id)




#---------------------------------------BASKETBALL LEAGUE--------------------------------------------------

@app.route("/basketball/clubs")
def basketball_teams():
    logos = []
    team_ids = []
    names = []
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("select `team_name`, `logo_url`, `team_id` from team")
    myresult = mycursor.fetchall()
    for x in myresult:
        names.append(x[0])
        logos.append(x[1])
        team_ids.append(x[2])
    print(myresult)
    # lista1 = ['https://upload.wikimedia.org/wikipedia/fr/e/ee/Hawks_2016.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/6/65/Celtics_de_Boston_logo.svg/1024px-Celtics_de_Boston_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Brooklyn_Nets_newlogo.svg/130px-Brooklyn_Nets_newlogo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/f/f3/Hornets_de_Charlotte_logo.svg/1200px-Hornets_de_Charlotte_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/d/d1/Bulls_de_Chicago_logo.svg/1200px-Bulls_de_Chicago_logo.svg.png', 'https://www.nba.com/resources/static/team/v2/cavaliers/images/170531-partial-logo.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/b/b8/Mavericks_de_Dallas_logo.svg/150px-Mavericks_de_Dallas_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/3/35/Nuggets_de_Denver_2018.png/180px-Nuggets_de_Denver_2018.png', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Detroit_Pistons_primary_logo_2017.png/150px-Detroit_Pistons_primary_logo_2017.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/d/de/Warriors_de_Golden_State_logo.svg/1200px-Warriors_de_Golden_State_logo.svg.png',"https://upload.wikimedia.org/wikipedia/en/thumb/2/28/Houston_Rockets.svg/240px-Houston_Rockets.svg.png", 'https://upload.wikimedia.org/wikipedia/fr/thumb/c/cf/Pacers_de_l%27Indiana_logo.svg/1180px-Pacers_de_l%27Indiana_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/d/d6/Los_Angeles_Clippers_logo_2010.png', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Memphis_Grizzlies.svg/1200px-Memphis_Grizzlies.svg.png']
    # lista2 = ['https://upload.wikimedia.org/wikipedia/fr/thumb/1/1c/Miami_Heat_-_Logo.svg/1200px-Miami_Heat_-_Logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/3/34/Bucks2015.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/d/d9/Timberwolves_du_Minnesota_logo_2017.png/200px-Timberwolves_du_Minnesota_logo_2017.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/2/21/New_Orleans_Pelicans.png/200px-New_Orleans_Pelicans.png', 'https://upload.wikimedia.org/wikipedia/fr/d/dc/NY_Knicks_Logo_2011.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/4/4f/Thunder_d%27Oklahoma_City_logo.svg/1200px-Thunder_d%27Oklahoma_City_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/b/bd/Orlando_Magic_logo_2010.png', 'https://upload.wikimedia.org/wikipedia/fr/4/48/76ers_2016.png', 'https://upload.wikimedia.org/wikipedia/fr/5/56/Phoenix_Suns_2013.png', 'https://upload.wikimedia.org/wikipedia/en/thumb/2/21/Portland_Trail_Blazers_logo.svg/1200px-Portland_Trail_Blazers_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/thumb/9/95/Kings_de_Sacramento_logo.svg/1200px-Kings_de_Sacramento_logo.svg.png', 'https://upload.wikimedia.org/wikipedia/fr/0/0e/San_Antonio_Spurs_2018.png', 'https://upload.wikimedia.org/wikipedia/fr/8/89/Raptors2015.png', 'https://upload.wikimedia.org/wikipedia/fr/3/3b/Jazz_de_l%27Utah_logo.png', 'https://upload.wikimedia.org/wikipedia/fr/archive/d/d6/20161212034849%21Wizards2015.png']
    return render_template("basket_teams.html", names = names, logos = logos, team_ids = team_ids)


@app.route("/basketball/home")
def basket_league_stats():
    stats = all_season_league_stats()
    tools = ['Ranking', '', 'League', '', 'Height', 'Weight', 'Games played', 'Minutes Played per Game', 'Average Field Goals Made', 'Average Field Goals Attempted', 'Average 3 Pointers Made', 'Average 3 Pointers Attempted', 'Average Free Throws Made', 'Average Free Throws Attempted', 'Average Offensive Rebounds', 'Average Defensive Rebounds', 'Average Total Rebounds', 'Average Assists per Game', 'Average Steals per Game', 'Average Blocks per Game', 'Average Turnovers per Game', 'Average Fouls per Game', 'Average Points per Game', 'Average Field Goals Percentage', 'Average 3 Pointers Percentage', 'Average Free Throws Percentage', '', 'Average Effective Field Goals Percentage', 'Average Turnovers Percentage', 'Average Offensive Rebounds Percentage', 'Free Throws Made per Field Goals Attempted', 'Offensive Rating']
    return render_template("basket_league_stats.html", headers = stats[0], stats = stats, tools = tools)

@app.route("/basketball/news")
def basket_league_news():
    return render_template("league_news.html")

@app.route("/basketball/standings")
def basket_league_standings():
    return render_template("basket_standings.html")


#--------------------------------BASKETBALL TEAM---------------------------------------------------------------


# @app.route("/basketball/<team_id>/home_%_stats")
# def team_home(team_id):
#     mycursor = mydb.cursor(buffered=True)
#     sql = "SELECT team_name, logo_url FROM team WHERE team_id = %s"
#     adr = (team_id, )
#     mycursor.execute(sql, adr)
#     myresult = mycursor.fetchall()
#     teamName = myresult[0][0]
#     teamLogo = myresult[0][1]
#     stats = all_season_stats()
#     print(stats[0])
#     print('sssssssssssssssss')
#     return render_template("basketball_home.html", headers = stats[0], stats = stats, teamName = teamName, teamLogo = teamLogo, teamId = team_id)


@app.route("/basketball/<team_id>/results")
def team_results(team_id):
    return render_template("basket_results_2.html", teamId = team_id)



@app.route("/basketball/<team_id>/stats")
def team_stats(team_id):
    dict = {}
    logos = []
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT team_name, team_id, logo_url FROM team")
    myresult = mycursor.fetchall()
    for res in myresult:
        if res[1] != int(team_id):
            dict[res[1]] = res[0] 
            logos.append(res[2])
    return render_template("basket_team_stats.html", teamId = team_id, dict = dict, logos = logos)


@app.route("/basketball/<team_id>/fixtures")
def team_fixtures(team_id):
    # print(team_id)
    # fixt = pandas_fixture()
    # step = int(len(fixt)/3)
    # print(fixt)
    return render_template("basket_team_fixtures.html", teamId = team_id)


@app.route("/basketball/<team_id>/squad")
def team_players(team_id):
    new_data = []
    # dict = list_of_players(21)
    # current_players = cur_players()
    # dict = common_players(current_players, dict)
    mycursor = mydb.cursor(buffered=True)
    #sql = "SELECT player_id, full_name, headshot FROM player WHERE team_id = %s"
    sql = "select player.player_id, player2.name, player.headshot, player2.jersey, player2.position, player2.country from (`player` join `player2`) where player.full_name = player2.name and player2.team_id = %s;"
    adr = (team_id, )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
        y = list(x)
        print(y[2])
        if y[2] == None:
            y[2] = 'https://www.kitshouse.org/wp-content/uploads/2019/09/no-image-1.jpg'
        else:
            y[2] = 'https://cdn.nba.com/headshots/nba/latest/1040x760/' + str(y[2]) + '.png'
        x = tuple(y)
        new_data.append(x)
    print(new_data)
    return render_template("basketball_players_2.html", data = new_data, team_id = team_id)


@app.route("/basketball/<team_id>/results/<game_id>")
def game_stats(team_id, game_id):
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT player_id, full_name, headshot FROM player"
    # adr = (team_id, )
    mycursor.execute(sql)
    data = []
    myresult = mycursor.fetchall()
    for x in myresult:
        temp = []
        temp.append(x[0])
        temp.append('https://cdn.nba.com/headshots/nba/latest/1040x760/' + str(x[2]) + '.png')
        data.append(temp)
    print(data)
    return render_template("game_stats.html", teamId = team_id, data = data, game_id = game_id)


@app.route("/basketball/<team_id>/comparison")
def basket_player_comp(team_id):
    new_data = []
    mycursor = mydb.cursor(buffered=True)
    #sql = "SELECT player_id, full_name FROM player WHERE team_id = %s"
    sql = "select player.player_id, player2.name, player.headshot from (`player` join `player2`) where player.full_name = player2.name;"
    #adr = (team_id, )
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        new_data.append(x)
    print(new_data)
    return render_template("basketball_players_comparison.html", team_id = team_id, data = new_data)


#--------------------------------------------------BASKETBALL PLAYERS----------------------------------------------------


# @app.route("/basketball/<team_id>/squad/<player_id>")
# def player_page(team_id, player_id):
#     print("running")
#     return render_template("index.html", team_id = team_id, player_id = player_id)


@app.route("/basketball/<team_id>/squad/<player_id>")
def player_page(team_id, player_id):
    print("running")
    mycursor = mydb.cursor(buffered=True)
    #sql = "SELECT full_name, headshot FROM player WHERE player_id = %s"
    sql = """SELECT player.full_name, player.headshot, player2.linkaki FROM (`player` join `player2`) WHERE player.full_name = player2.name AND player.player_id = %s;"""
    adr = (player_id, )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    name = myresult[0]
    headshot = myresult[1]
    urlaki = myresult[2]
    new_url = 'https://cdn.nba.com/headshots/nba/latest/1040x760/' + str(headshot) + '.png'

    stats_reg = basketball_player_stats(1, urlaki)
    stats_pl = basketball_player_stats(2, urlaki)

    a = 0
    while a == 0:
        if stats_reg[-1][0] == 'Career':
            a = 1
        else:
            stats_reg.pop()

    b = 0
    while b == 0:
        if stats_pl[-1][0] == 'Career':
            b = 1
        else:
            stats_pl.pop()

    print(stats_reg)

    return render_template("index2.html", headers = stats_reg[0], stats_pl = stats_pl[1:], stats_reg = stats_reg[1:], data = name, player_id = player_id, team_id = team_id, headshot = new_url)






@app.route("/basketball/<team_id>/<player_id>/games")
def player_games(team_id, player_id):
    return render_template("basket_player_games.html", player_id = player_id, team_id = team_id)

@app.route("/basketball/<team_id>/<player_id>/games/<game_id>")
def player_game_info(team_id, player_id, game_id):
    return render_template("basket_player_game_info.html", player_id = player_id, team_id = team_id, game_id = game_id)

  
    
if __name__ == "__main__":
    app.run(debug=True)