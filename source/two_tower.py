import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input, Embedding, Flatten, Activation, BatchNormalization, Dot, Dense, Concatenate
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateSchedular, TensorBoard, EarlyStopping

from source.custom_exception import CustomException
from source.custom_logger import get_logger
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class TwoTowerModel:
    def __init__(self, config_path):
        try:
            self.config = config_path
            logger.info("Loaded configuration from config.yaml")

        except Exception as e:
            raise CustomException("FAiled to load configuration", e)
        
    def RecommenderNet(self, n_users, n_item):
        try:
            embedding_size = self.config["model"]["embedding_size"]

            # User Tower
            user_input = Input(name="user", shape=[1])
            user_embedding = Embedding(name="user_embedding", input_dim=n_users, output_dim=embedding_size)(user_input)
            user_embedding = Flatten()(user_embedding)
            user_dense = Dense(64, activation="relu")(user_embedding)
            user_dense = Dense(32, activation="relu")(user_dense)

            # Anime (Item) Tower
            item_input = Input(name="item", shape=[1])
            item_embedding = Embedding(name="item_embedding", input_dim=n_item, output_dim=embedding_size)(item_input)
            item_embedding = Flatten()(item_embedding)
            item_dense = Dense(64, activation="relu")(item_embedding)
            item_dense = Dense(32, activation="relu")(item_dense)

            # Concatenation of Towers
            merged = Concatenate()([user_dense, item_dense])

            # Fully Connected Layers
            x = Dense(32, activation="relu")(merged)
            x = BatchNormalization()(x)
            x = Dense(16, activation="relu")(x)
            x = Dense(1, activation="sigmoid")(x)

            # Define Model
            model = Model(inputs=[user_input, item_input], outputs=x)
            model.compile(
                loss=self.config["model"]["loss"],
                optimizer=self.config["model"]["optimizer"],
                metrics=self.config["model"]["metrics"]
            )

            logger.info("Two-Tower Model created successfully.")
            return model

        except Exception as e:
            logger.error(f"Error occurred during model architecture creation: {e}")
            raise CustomException("Failed to create model", e)
