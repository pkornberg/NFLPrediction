"""
Utility Functions for Rating Generation Using Correlation Weights

Author: Phillip Kornberg
Date: 3.31.25
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def offensiveRatingCreation(dataFrame, weights):
    """
    Function to Create Offensive Pass and Rush Ratings

    : param dataFrame dataFrame - Data Frame from Data Collection
    : param series weights - Array of Correlation Weights for Offense

    : return dataFrame df - Data Frame with Offensive Ratings
    """

    # Creating Offensive Pass Rating
    positiveStats = ["PPD", "AVG Pass", "TDCR", "FDCR", "FDP", "TURN"]
    negativeStats = ["SACKS"]  

    signedWeights = weights.abs().copy()
    signedWeights[negativeStats] *= -1

    selected = positiveStats + negativeStats
    offensivePass = dataFrame[selected].mul(signedWeights[selected]).sum(axis = 1)

    # Creating Offensive Rush Rating
    positiveStats = ["PPD", "AVG Rush", "TDCR", "FDCR", "FDR", "TURN"]
    negativeStats = ["SACKS"]  

    signedWeights = weights.abs().copy()
    signedWeights[negativeStats] *= -1

    selected = positiveStats + negativeStats
    offensiveRush = dataFrame[selected].mul(signedWeights[selected]).sum(axis = 1)

    # Adding Team Names
    offensivePass = pd.DataFrame({
        "Team Name": dataFrame["Team Name"],
        "Offensive Pass Rating": offensivePass
    })
    
    offensiveRush = pd.DataFrame({
        "Team Name": dataFrame["Team Name"],
        "Offensive Rush Rating": offensiveRush
    })

    # Returning Rating
    return round(pd.merge(offensiveRush, offensivePass, on = "Team Name"), 3)

def defensiveRatingCreation(dataFrame, weights):
    """
    Function to Create Defensive Pass and Rush Ratings

    : param dataFrame dataFrame - Data Frame from Data Collection
    : param series weights - Array of Correlation Weights for Defense

    : return dataFrame df - Data Frame with Team Ratings
    """

    # Creating Defensive Pass Rating
    positiveStats = ["INT", "TDSR", "FDSR"]
    negativeStats = ["PPDA", "AVG Pass"]  

    signedWeights = weights.abs().copy()
    signedWeights[negativeStats] *= -1

    selected = positiveStats + negativeStats
    defensivePass = dataFrame[selected].mul(signedWeights[selected]).sum(axis = 1)

    # Creating Defensive Rush Rating
    positiveStats = ["SACKS", "TDSR", "FDSR"]
    negativeStats = ["PPDA", "AVG Rush"]  

    signedWeights = weights.abs().copy()
    signedWeights[negativeStats] *= -1

    selected = positiveStats + negativeStats
    defensiveRush = dataFrame[selected].mul(signedWeights[selected]).sum(axis = 1)

    # Adding Team Names
    defensivePass = pd.DataFrame({
        "Team Name": dataFrame["Team Name"],
        "Defensive Pass Rating": defensivePass
    })
    
    defensiveRush = pd.DataFrame({
        "Team Name": dataFrame["Team Name"],
        "Defensive Rush Rating": defensiveRush
    })

    # Returning Rating
    return round(pd.merge(defensiveRush, defensivePass, on = "Team Name"), 3)

def overallRating(offesniveDataFrame, defensiveDataFrame):
    """
    Function to Create Overall Team Ratings by Adding Up All Individual Ratings

    : param dataFrame offensiveDataFrame - Data Frame with Offensive Ratings
    : param dataFrame defensiveDataFrame - Data Frame with Defensive Ratings

    : return dataFrame df - Data Frame with Final Ratings
    """

    # Merging Data Frames
    df = pd.merge(offesniveDataFrame, defensiveDataFrame, on = "Team Name")

    # Normalizing Data Frames
    scaler = MinMaxScaler()
    cols = ["Offensive Pass Rating", "Offensive Rush Rating", "Defensive Pass Rating", "Defensive Rush Rating"]
    df[cols] = scaler.fit_transform(df[cols])

    # Calculating Overall Rating
    df["Overall Rating"] = ((df["Offensive Pass Rating"] * 0.40) + (df["Offensive Rush Rating"] * 0.15) +
                            (df["Defensive Pass Rating"] * 0.30) + (df["Defensive Rush Rating"] * 0.15))
    
    return round(df, 3)










    

