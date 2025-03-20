import os
import yaml


from source.custom_exception import CustomException
from source.custom_logger import get_logger

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found")
        
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config
        
    except Exception as e:
        logger.error("Error ")
        raise CustomException("Failed to read ")
    