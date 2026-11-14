import os
import yaml
from pydantic import BaseModel

class AppSettings(BaseModel):
    DB_FILE_RELATIVE_PATH: str
    ChromaDB_PERSIST_DIRECTORY: str
    OPENAI_EMBEDDING_MODEL: str
    OPENAI_SUBTITLE_ANALYZER_MODEL: str

    @classmethod
    def load_from_yaml(cls) -> "AppSettings":
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, "settings.yaml")
        
        with open(yaml_path, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
            
        return cls(**yaml_data)