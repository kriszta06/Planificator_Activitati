import numpy as np
from sklearn.ensemble import RandomForestRegressor #alg de ML
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import pandas as pd

class ActivityModel:
    def __init__(self):
        self.model =RandomForestRegressor(n_estimators=50, random_state=42) #modelul de baza pt predictie
        self.scaler = StandardScaler() #pt normalizarea datelor
        self.data_path = "data/training_data.csv"
        os.makedirs("data", exist_ok=True)

        if not self.load_training_data():
            initial_data = np.array([
                [30, 5, 3, 0.8],
                [60, 3, 2, 0.6],
                [15, 8, 1, 0.9]
            ])
            X = initial_data[:, :-1] # X= toate coloanele fara cea de scor
            y = initial_data[:, -1] # Y= coloana de scor
            #normalizare
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            #antrenare pe date normalizate
            self.model.fit(X_scaled, y)

    #pt a antrena modelul pe datele din fisier
    def load_training_data(self):
        try: 
            data = pd.read_csv(self.data_path)
            if len(data) > 0:
                X = data[["durata", "prioritate", "nr_ramase"]].values
                y = data["scor"].values
                self.model.fit(X,y)
                return True
        except FileNotFoundError:
            pass
        return False
    
    #pt a aduga date noi de antrenament
    def add_training_data(self, durata, prioritate, nr_ramase, scor):

        new_data = pd.DataFrame([[durata, prioritate, nr_ramase, scor]], columns=["durata", "prioritate", "nr_ramase", "scor"])

        if os.path.exists(self.data_path):
            new_data.to_csv(self.data_path, mode="a", header=False, index=False)
        else:
            new_data.to_csv(self.data_path, index=False)

        self.load_training_data()

    #precizare scor
    def predict(self, durata, prioritate, nr_ramase):
        try:
            features = np.array([[durata, prioritate, nr_ramase]])
            features_scaled = self.scaler.transform(features)
            #antrenare, cu restrictii de [0,1]
            return max(0, min(1, self.model.predict(features_scaled)[0]))
        except:
            #pt cazul in care nu merge predictia
            score = (prioritate/10.0) * 0.6 + (1 - durata/240.0) * 0.3 + (1 - nr_ramase/20.0) * 0.1
            return max(0, min(1, score))