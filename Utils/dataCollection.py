"""
Utility Functions for Data Collection  

Author: Phillip Kornberg
Date: 3.31.25
"""

import requests as rq
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs

def offenseDataCollection():
    """
    Function to Collect NFL Team Offensive Passing and Rushing Data

    : return dataFrame df - Data Frame with Various Team Statistics
    """

    # Initializing List of Teams
    nflTeams = ["arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills", "carolina-panthers", "chicago-bears",
                "cincinnati-bengals", "cleveland-browns", "dallas-cowboys", "denver-broncos", "detroit-lions", "green-bay-packers", 
                "houston-texans", "indianapolis-colts", "jacksonville-jaguars", "kansas-city-chiefs", "las-vegas-raiders",
                "los-angeles-chargers", "los-angeles-rams", "miami-dolphins", "minnesota-vikings", "new-england-patriots", "new-orleans-saints",
                "new-york-giants", "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers", "san-francisco-49ers", "seattle-seahawks",
                "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"] 
    
    # Offense Data Storage
    pointsPerDrive = []
    avgPassingYards = []
    turnoverRate = []
    sacks = []
    thirdDownConvsersionRate = []
    fourthDownConversionRate = []
    firstDownPassing = []
    winPercent = []  
    avgRushingYards = []
    turnoverRate = []
    firstDownRushing = []

    # Websraping with Requests and BeautifulSoup
    for team in nflTeams:
        page = rq.get("https://www.nfl.com/teams/" + team + "/stats")
        soup = bs(page.text, "html.parser")
        table = soup.find(class_ = "nfl-o-team-h2h-stats__list")
        stats = table.find_all(class_ = "nfl-o-team-h2h-stats__value")

        # Offense Data Collection
        offensePassing = stats[10].getText().strip()
        avgYards = float(offensePassing.split("\n")[1].strip())
        avgPassingYards.append(avgYards)

        # Average Rushing Yards
        offenseRushing = stats[14].getText().strip()
        avgYards = float(offenseRushing.split("\n")[1].strip())
        avgRushingYards.append(avgYards)

        # Third Down Conversion Rate
        thirdDownConversion = stats[4].getText().strip()
        thirdDownConvsersionRate.append(float(thirdDownConversion.split("/")[0].strip()) / float(thirdDownConversion.split("/")[1].strip()))

        # First Down Rushing and Passing
        firstDownPassing.append(float((stats[2].getText().strip()).split("\n")[1].strip()))
        firstDownRushing.append(float((stats[2].getText().strip()).split("\n")[0].strip()))

        # Points Per Drive
        rushingTouchdowns = (stats[26].getText().strip()).split("\n")[0].strip()
        passingTouchdowns = float(stats[24].getText().strip()) - float(rushingTouchdowns)
        fieldgoals = (stats[22].getText().strip()).split("/")[0].strip()
        pointsPerDrive.append(((float(passingTouchdowns)*7) + (float(fieldgoals)*3))/126)

        # Sacks and Turnovers
        sacks.append(float(stats[20].getText().strip())/3)
        turnovers = stats[28].getText().strip()
        turnoverRate.append((float(turnovers))/126)
        
        # Fourth Down Conversion Rate
        fourthDownConversion = stats[6].getText().strip()
        fourthDownConversionRate.append(float(fourthDownConversion.split("/")[0].strip()) / float(fourthDownConversion.split("/")[1].strip()))

        # Win Percentage
        header = soup.find('div', class_ = "nfl-c-team-header__stats nfl-u-hide-empty")
        record = header.getText().split("-")
        winPercent.append(float(record[0])/(float(record[0]) + float(record[1])))
    
    # Reformatting Team Names
    nflTeams = [team.replace("-", " ").title() for team in nflTeams]
    
    # Returning Data Frame
    df = pd.DataFrame({"Team Name": nflTeams, "PPD": pointsPerDrive, "AVG Pass": avgPassingYards, "AVG Rush": avgRushingYards, "TURN": turnoverRate, "SACKS": sacks, 
                       "TDCR": thirdDownConvsersionRate, "FDCR": fourthDownConversionRate, "FDP": firstDownPassing, "FDR": firstDownRushing, "W%": winPercent})
    
    # Rounding
    df = round(df, 3)

    return df

def defenseDataCollection():
    """
    Function to Collect NFL Team Defensive Passing and Rushing Data

    : return dataFrame df - Data Frame with Various Team Statistics
    """

    # Initializing List of Teams
    nflTeams = ["arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills", "carolina-panthers", "chicago-bears",
                "cincinnati-bengals", "cleveland-browns", "dallas-cowboys", "denver-broncos", "detroit-lions", "green-bay-packers", 
                "houston-texans", "indianapolis-colts", "jacksonville-jaguars", "kansas-city-chiefs", "las-vegas-raiders",
                "los-angeles-chargers", "los-angeles-rams", "miami-dolphins", "minnesota-vikings", "new-england-patriots", "new-orleans-saints",
                "new-york-giants", "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers", "san-francisco-49ers", "seattle-seahawks",
                "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"] 

    # Defensive Data Storage
    pointsPerDriveAllowed = []
    avgRushingYardsAllowed = []
    avgPassingYardsAllowed = []
    interceptions = []
    sacks = []
    thirdDownStopRate = []
    fourthDownStopRate = []
    winPercent = []

    # Websraping with Requests and BeautifulSoup
    for team in nflTeams:
        page = rq.get("https://www.nfl.com/teams/" + team + "/stats")
        soup = bs(page.text, "html.parser")
        data = soup.find_all(class_ = "nfl-o-team-h2h-stats__value")

        # Average Rushing and Passing Yards Allowed
        avgRushingYardsAllowed.append(float(data[15].text.strip().split("\n")[1]))
        avgPassingYardsAllowed.append(float(data[19].text.strip().split("\n")[3]))

        # Interceptions and Sacks
        interceptions.append(float(data[19].text.strip().split("\n")[2]))
        sacks.append(float(data[21].text.strip()))
    
        # Third and Fourth Down Stop Rate
        thirdDown = data[5].text.strip().split("/")
        thirdDownStopRate.append(1 - (float(thirdDown[0]) / float(thirdDown[1])))
        fourthDown = data[7].text.strip().split("/")
        fourthDownStopRate.append(1 - (float(fourthDown[0]) / float(fourthDown[1])))
    
        # Points Per Drive Allowed
        pointsPerDriveAllowed.append(((3*int(data[23].text.strip().split("/")[0]) + 7*(int(data[27].text.strip().split("\n")[0])))/126))

        # Win Percentage
        stats = soup.find('div', class_ = "nfl-c-team-header__stats nfl-u-hide-empty")
        record = stats.getText().split("-")
        winPercent.append(float(record[0])/(float(record[0]) + float(record[1])))
        
    # Reformatting Team Names
    nflTeams = [team.replace("-", " ").title() for team in nflTeams]

    # Returning Data Frame
    df = pd.DataFrame({"Team Name": nflTeams, "PPDA": pointsPerDriveAllowed, "AVG Rush": avgRushingYardsAllowed, "AVG Pass": avgPassingYardsAllowed, "INT": interceptions,
                       "SACKS": sacks, "TDSR": thirdDownStopRate, "FDSR": fourthDownStopRate, "W%": winPercent})
    
    # Rounding
    df = round(df, 3)

    return df