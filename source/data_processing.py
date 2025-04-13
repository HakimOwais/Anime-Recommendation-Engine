import os
import pandas as pd
import joblib
import numpy as np
import sys

from source.custom_logger import get_logger
from source.custom_exception import CustomException
from config.path_config import *

print(ANIMELIST_CSV)

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.rating_df = None
        self.anime_df = None
        self.X_train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.item2item_encoded = {}
        self.item2item_decoded = {}

        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Data Processor Initialization")

    def load_data(self, usecols):
        try:
            self.rating_df = pd.read_csv(self.input_file, low_memory=True, usecols=usecols)
            logger.info("Dataset loaded successfully")
        except Exception as e:
            raise CustomException(f"Failed to load dataset {e}")
        
    def filter_data(self, min_rating=400):
        try:
            n_ratings = self.rating_df["user_id"].value_counts()
            self.rating_df = self.rating_df[self.rating_df["user_id"].isin(n_ratings[n_ratings>=min_rating].index)].copy()
            logger.info("Filtered data successfully")
        except Exception as e:
            raise CustomException(f"Failed to filter dataset {e}")
        
    def scale_ratings(self):
        try:
            min_rating =min(self.rating_df["rating"])
            max_rating =max(self.rating_df["rating"])
            self.rating_df["rating"] = self.rating_df["rating"].apply(lambda x : (x-min_rating)/(max_rating-min_rating)).values.astype(np.float64)
            logger.info("Scaled rating feature successfullly")
        except Exception as e:
            raise CustomException(f"Failed to scale rating feature {e}")

        
    def encode_data(self):
        try:
            user_ids = self.rating_df["user_id"].unique().tolist()
            self.user2user_encoded = {x : i for i , x in enumerate(user_ids)}
            self.user2user_decoded = {i : x for i , x in enumerate(user_ids)}
            self.rating_df["user"] = self.rating_df["user_id"].map(self.user2user_encoded)

            logger.info("User ids encoded successfully")

            anime_ids = self.rating_df["anime_id"].unique().tolist()
            self.item2item_encoded = {x : i for i , x in enumerate(anime_ids)}
            self.item2item_decoded = {i : x for i , x in enumerate(anime_ids)}
            self.rating_df["anime"] = self.rating_df["anime_id"].map(self.item2item_encoded)

            logger.info("Item ids encoded successfully")
        except Exception as e:
            raise CustomException(f"Failed to encode feature {e}")
        
    def split_data(self, test_size=2000, random_state=42):
        try:
            X = self.rating_df[["user","anime"]].values
            y = self.rating_df["rating"]

            train_indices = self.rating_df.shape[0] - test_size
            X_train, X_test, y_train, y_test = (
                                                X[ :train_indices],
                                                X[train_indices: ],
                                                y[ :train_indices],
                                                y[train_indices: ]
                                            )
            self.X_train_array = [X_train[: , 0] , X_train[: ,1]]
            self.X_test_array = [X_test[: , 0] , X_test[: ,1]]
            self.y_train = y_train
            self.y_test = y_test
            logger.info("Data splitted sucesfullyy")

        except Exception as e:
            raise CustomException("Failed to split data", e)


    # X_trains arrays and X_test are numpy arrays and should be saved as pkl file format
    def save_artifacts(self):
        try:
            artifacts = {
                "user2user_encoded": self.user2user_encoded,
                "user2user_decoded": self.user2user_decoded,
                "item2item_encoded": self.item2item_encoded,
                "item2item_decoded": self.item2item_decoded,
            }
            for name, data in artifacts.items():
                joblib.dump(data, os.path.join(self.output_dir, f"{name}.pkl"))
                logger.info("Artifacts saved successfully")

            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)

            self.rating_df.to_csv(RATING_DF, index=False)

            logger.info("All the files have been saved successfully ")

        except Exception as e:
            raise CustomException("Failed to save the artifacts", e)


    # Read Anime CSV file 
    def process_anime_data(self):
        try:
            df = pd.read_csv(ANIME_CSV)
            # Reading Synopsis data also
            cols = ["MAL_ID","Name","Genres","sypnopsis"]

            synopsis_df = pd.read_csv(SYNOPSIS_CSV, usecols=cols)

            df = df.replace("Unknown", np.nan)

            def getAnimeName(anime_id):
                try:
                    name = df[df.anime_id==anime_id].eng_version.values[0]
                    if name is np.nan:
                        name = df[df.anime_id==anime_id].Name.values[0]

                except:
                    print("Error")
                return name
            
            df["anime_id"] = df["MAL_ID"]
            df["eng_version"] = df["English name"]
            df["eng_version"] = df.anime_id.apply(lambda x:getAnimeName(x))

            df.sort_values(by = ["Score"], inplace=True, ascending=False, kind="quicksort", na_position="last")

            df = df[["anime_id" , "eng_version","Score","Genres","Episodes","Type","Premiered","Members"]]
    
            df.to_csv(DF, index=False)
            synopsis_df.to_csv(SYNOPSIS_DF, index=False)
            logger.info("Anime and anime with synopsis datasets preprocessed successfully")

        except Exception as e:
            raise CustomException("Failed to preprocesss the anime and anime with synopsis datasets", e)
        

    def run(self):
        try:
            self.load_data(usecols=["user_id", "anime_id", "rating"])
            self.filter_data()
            self.scale_ratings()
            self.encode_data()
            self.split_data()
            self.save_artifacts()
            self.process_anime_data()

            logger.info("Data processing pipeline run successfully...... CONGRATS")
        except Exception as e:
            logger.error(str(e))
            raise CustomException("Failed to processs the Data processor Pipeline", e)
        
if __name__=="__main__":
    data_processor = DataProcessor(ANIMELIST_CSV,PROCESSED_DIR)
    data_processor.run()

