import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import pickle
import os
import joblib

class Pre_processing:
    def __init__(self, path_file): #
        self.path_file = path_file
        self.data = None
        self.feature = None
        self.target = None

    def read_data(self):
        self.data = pd.read_csv(self.path_file)

    def dropNan(self):
        self.data = self.data.dropna()
        self.data = self.data.reset_index(drop=True)

    def dropIrrelevant(self, column):
        if column in self.data.columns:
            self.data = self.data.drop(column, axis=1)

    def targetEncode(self, column):
        encode = LabelEncoder()
        self.data[column] = encode.fit_transform(self.data[column])

    def makeFeatureTarget(self, column_target):
        self.feature = self.data.drop(column_target, axis=1)
        self.target = self.data[column_target]

class Modelling:
    def __init__(self, feature_data, target_data):
        self.feature_data = feature_data
        self.target_data = target_data
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.prediction = None
        self.model()

    def split(self, test_size=0.2, random_state=42):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.feature_data, self.target_data, test_size=test_size, random_state=random_state)

    def encode_categorical(self, column_categorical):
        OneEncode = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

        encoded_train = OneEncode.fit_transform(self.x_train[column_categorical])
        encoded_train_df = pd.DataFrame(encoded_train, columns=OneEncode.get_feature_names_out(column_categorical), index=self.x_train.index)

        encoded_test = OneEncode.transform(self.x_test[column_categorical])
        encoded_test_df = pd.DataFrame(encoded_test, columns=OneEncode.get_feature_names_out(column_categorical), index=self.x_test.index)

        self.x_train = pd.concat([self.x_train.drop(columns=column_categorical), encoded_train_df], axis=1)
        self.x_test = pd.concat([self.x_test.drop(columns=column_categorical), encoded_test_df], axis=1)
        self.OneEncode = OneEncode
    
    def IDXReseting(self):
        self.x_train = self.x_train.reset_index(drop=True)
        self.x_test = self.x_test.reset_index(drop=True)
        self.y_train = self.y_train.reset_index(drop=True)
        self.y_test = self.y_test.reset_index(drop=True)
    
    def model(self):
        self.RF_model = RandomForestClassifier(random_state=42)

    def training(self):
        self.RF_model.fit(self.x_train, self.y_train)

    def predicting(self):
        self.prediction = self.RF_model.predict(self.x_test)

    def reporting(self):
        print("Classification Report:\n")
        print(classification_report(self.y_test, self.prediction, target_names=["Canceled", "Not_Canceled"]))

    def saving(self, path_save, filename):
        path_file = os.path.join(path_save, filename)
        with open(path_file, 'wb') as file:
            joblib.dump(self.RF_model, file, compress=3)

    
path_file = 'C://Users/narzo/Downloads/Code/Code Binus/Model Deploy/Dataset_B_hotel.csv'
Pre_process = Pre_processing(path_file)
Pre_process.read_data()
Pre_process.dropNan()
Pre_process.dropIrrelevant('Booking_ID')
Pre_process.targetEncode('booking_status')
Pre_process.makeFeatureTarget('booking_status')

feature = Pre_process.feature
target = Pre_process.target

models = Modelling(feature, target)
models.split()
column_categorical = ['type_of_meal_plan', 'room_type_reserved', 'market_segment_type']
models.encode_categorical(column_categorical)
models.IDXReseting()
models.training()
models.predicting()
models.reporting()
path_save = 'C://Users/narzo/Downloads/Code/Code Binus/Model Deploy'
models.saving(path_save, 'RF_model.pkl')