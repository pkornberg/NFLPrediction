"""
Utility Functions for Model Fitting

Author: Phillip Kornberg
Date: 3.31.25
"""

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd

def correlationAnalysis(dataFrame):
    """
    Function to Correlate Stats to Win Percentage

    : param dataFrame dataFrame - Offense or Defense Stats Data Frame  
    
    : return series weights - Associated Weights with Each Statistics in Data Frame
    """

    # Initializing Features
    features = dataFrame.drop(columns = ["Team Name", "W%"]).columns.tolist()
    outcome = "W%"

    # Conducting Correlation Anaalysis
    X = dataFrame[features]
    y = dataFrame[outcome]

    # Scaling Data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fitting Model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Extracting Weights
    weights = pd.Series(model.coef_, index=features).sort_values(key=abs, ascending=False)
    weights = pd.Series(model.coef_, index=features).abs().sort_values(ascending=False)
    
    return weights

