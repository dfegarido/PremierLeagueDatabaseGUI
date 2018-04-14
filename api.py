# -*- coding: utf-8 -*-
import json
import requests as r
from bs4 import BeautifulSoup 




def table_menu():
    urls = "http://uk.soccerway.com/national/england/premier-league/20172018/regular-season/r41547/"
    sess = r.Session()
    data = sess.get(urls).text
    soup = BeautifulSoup(data, 'lxml')
    table_menu_dics = {}
    team_a = soup.find_all("td",{'class','team-a'})
    team_b = soup.find_all("td",{'class','team-b'})
    score = soup.find_all("td",{'class','score-time'})
    
    for i in range(len(team_a)):
        table_menu_dics.update({'key_'+str(i):{
                                    'date':soup.find_all('td', {'class','date'})[i].text.replace('\n',''),
                                    'team_a':team_a[i].find('a')['title'],
                                    'score_a':score[i].find_all('span')[0].text,
                                    'team_b':team_b[i].find('a')['title'],
                                    'score_b':score[i].find_all('span')[1].text}})
    with open('api/premier_matches.json', 'w') as file:
        json.dump(table_menu_dics,file)


def goals_deff():
    urls = "http://uk.soccerway.com/national/england/premier-league/20172018/regular-season/r41547/"
    sess = r.Session()
    data = sess.get(urls).text
    soup = BeautifulSoup(data, 'lxml')
    goals_deff_dics = {}
    rank = soup.find_all('tr',{'class':"team_rank"})
    for i in range(20):
        team = rank[i].find_all('td',{"class":"team"})[0].text.replace('\n','')
        mp = rank[i].find_all('td',{"class":"mp"})[0].text.replace('\n','')
        won = rank[i].find_all('td',{"class":"won"})[0].text.replace('\n','')
        drawn = rank[i].find_all('td',{"class":"drawn"})[0].text.replace('\n','')
        loss = rank[i].find_all('td',{"class":"lost"})[0].text.replace('\n','')
        goals_for = rank[i].find_all('td',{"class":"gf"})[0].text.replace('\n','')
        goals_againts = rank[i].find_all('td',{"class":"ga"})[0].text.replace('\n','')
        goals_diff = rank[i].find_all('td',{"class":"gd"})[0].text.replace('\n','')
        points = rank[i].find_all('td',{"class":"points"})[0].text.replace('\n','')
        goals_deff_dics.update({"rank_"+str(i+1):{"rank":i+1,
                                               "team":team,
                                               "mp":mp,
                                               "won":won,
                                               "drawn":drawn,
                                               "loss":loss,
                                               "goals_for":goals_for,
                                               "goals_againts":goals_againts,
                                               "goals_diff":goals_diff,
                                               "points":points,}})
        
    with open('api/goals_deff_dics.json', 'w') as file: 
        json.dump(goals_deff_dics,file)


def card():
    url_ry = "http://www.espnfc.com/english-premier-league/23/statistics/fairplay"
    sess = r.Session()
    data = sess.get(url_ry).text
    soup = BeautifulSoup(data, 'lxml')
    rank_team = soup.find_all('tr')
    cards = {}
    for i in range(1,21):
        club = rank_team[i].find_all('td',{'headers':'team'})[0].text
        yellow_card = rank_team[i].find_all('td',{'headers':'goals'})[0].text
        red_card = rank_team[i].find_all('td',{'headers':'goals'})[1].text
        points = rank_team[i].find_all('td',{'headers':'goals'})[2].text
        
        cards.update({"rank_"+str(i): {"club":club,
                                       "yc":yellow_card,
                                       "rc":red_card,
                                       "points":points,}})
        
    with open('api/cards.json', 'w') as file:
        json.dump(cards, file)



def team_fouls():
    url_fouls = "https://www.msn.com/en-us/sports/soccer/premier-league/player-stats/sp-vw-discipline"
    sess = r.Session()
    data = sess.get(url_fouls).text
    soup = BeautifulSoup(data, 'lxml')
    players = soup.find_all('tr',{"class":"rowlink"})
    team_foul = {}
    for i in range(len(players)):
        rank = i+1
        name = players[i].find_all('td')[1].text
        teamname = players[i].find_all('td')[2].text
        games_played = players[i].find_all('td')[4].text
        yellow_cards = players[i].find_all('td')[5].text
        red_cards = players[i].find_all('td')[6].text
        foul_commited = players[i].find_all('td')[7].text
        foul_suffered = players[i].find_all('td')[8].text
        offsite = players[i].find_all('td')[9].text
        team_foul.update({"rank_"+str(rank):{"rank":rank,
                                            "name":name,
                                            "team":teamname,
                                            "gp":games_played,
                                            "yc":yellow_cards,
                                            "rc":red_cards,
                                            "fc":foul_commited,
                                            "fs":foul_suffered,
                                            "off":offsite,}})
    with open('api/teamfoul.json','w') as file:
        json.dump(team_foul, file)
def player_statistic():
    url_player = "https://www.msn.com/en-us/sports/soccer/premier-league/player-stats"
    sess = r.Session()
    data = sess.get(url_player).text
    soup = BeautifulSoup(data, 'lxml')
    players = soup.find_all('tr',{"class":"rowlink"})
    player_statistic = {}
    for i in range(len(players)):
        rank = i+1
        name = players[i].find_all('td')[1].text
        teamname = players[i].find_all('td')[2].text
        games_played = players[i].find_all('td')[4].text
        games_started = players[i].find_all('td')[5].text
        minutes_played = players[i].find_all('td')[6].text
        goal = players[i].find_all('td')[7].text
        asst = players[i].find_all('td')[8].text
        shots = players[i].find_all('td')[9].text
        sog = players[i].find_all('td')[10].text
        player_statistic.update({"rank_"+str(rank):{"rank":rank,
                                            "name":name,
                                            "team":teamname,
                                            "gp":games_played,
                                            "gs":games_started,
                                            "mins":minutes_played,
                                            "g":goal,
                                            "asst":asst,
                                            "shots":shots,
                                            "sog":sog,
                                            "web":"https://www.premierleague.com/search?term="+name}})
    with open('api/player_statistic.json','w') as file:
        json.dump(player_statistic, file)
        
def call_func():
    print("Updating.....")
    table_menu()
    card()
    goals_deff()
    team_fouls()
    player_statistic()
    print("Done...")




        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    



















    
