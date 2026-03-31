"""
Utility Functions for Matchup Predicting

Author: Phillip Kornberg
Date: 3.31.25
"""

def matchup(team1, team2, ratingData):
    """
    Function to Predict Outcome in Matchup

    : param str team1 - Name of Team 1
    : param str team2 - Name of Team 2
    : param dataFrame ratingData - Data Frame Containing Overall Ratings

    : print - Projected Winner Along with Percentages
    """

    # Finding Team Scores
    team1Score = ratingData.loc[ratingData["Team Name"] == team1, "Overall Rating"].values[0]
    team2Score = ratingData.loc[ratingData["Team Name"] == team2, "Overall Rating"].values[0]

    # Calculating Percentages
    totalScore = team1Score + team2Score
    team1Percent = (team1Score / totalScore) * 100
    team2Percent = (team2Score / totalScore) * 100

    # Printing Out Mathcup Details
    if team1Score > team2Score:
        print(f"Projected Winner: {team1}")
        print(f"{team1}: {round(team1Percent, 2)}%")
        print(f"{team2}: {round(team2Percent, 2)}%")
    else:
        print(f"Projected Winner: {team2}")
        print(f"{team2}: {round(team2Percent, 2)}%")
        print(f"{team1}: {round(team1Percent, 2)}%")
    print()
