"""Load the settings. If there is no settings file create it."""

import os
from typing import List
import ast
import pathlib
import logging

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DEFAULT_SETTINGS_PATH = ROOT / "config" / "settings.yaml"

logger = logging.getLogger(__name__)

if not DEFAULT_SETTINGS_PATH.exists():
    default_texts = {
        "welcome_main_text": "Welcome on this Application",
        "welcome_sub_text": "Click the Buzzer",
        "layout_text_2": "",
        "layout_text_3": ""
    }

    default_paths = {
          "layout_path": "samples/layouts",
          "font_path": "samples/fonts",
    }

    default_prompts = {
        "poem_prompt": """You are are poem writer. You see a picture from a party with happy people. 
        Interprete the Picture and details you see. Write a Haiku about the picture."""

    }

    default_config = {
        "texts": default_texts,
        "paths": default_paths,
        "prompts": default_prompts
    }
    with open(DEFAULT_SETTINGS_PATH, "w") as file:
        yaml.safe_dump(default_config, file)

class Settings():
    """Class for setting and getting the config"""
    def __init__(self, settings: pathlib.Path = DEFAULT_SETTINGS_PATH):
        self.settings = settings
        self.settings_list: List[str] = []
        self.load_settings()
    
    def load_settings(self):
        """Load the settings in the environment"""

        setting_list = []
        with open(self.settings, "r") as file:
            tmp = yaml.safe_load(file)
        
        for base_key in tmp.keys():
            for setting in tmp[base_key]:
                os.environ[setting] = tmp[base_key][setting]
                setting_list.append(setting)

        os.environ["available_settings_app"] = str(setting_list)
        self.settings_list = setting_list

    def get_setting(self, setting: str) -> str | None:
        """Return the setting"""
        available_settings = ast.literal_eval(os.getenv("available_settings_app"))
        if setting not in available_settings:
            logging.error("Setting %s not in available settings.", setting)
            return None
        return os.environ[setting]
    
    def change_setting(self, category: str, setting: str, setting_value: str) -> None:
        """Change a setting"""
        with open(self.settings, "r") as file:
            tmp: dict = yaml.safe_load(file)
        
        if tmp.get(category) is None:
            logger.warning("Category %s not found will create it.", category)
            tmp[category] = {setting: setting_value}
        elif tmp.get(category).get(setting) is None:
            logger.warning("Setting %s not found will create it.", setting)
        tmp[category][setting] = setting_value

        with open(self.settings, "w") as file:
            yaml.safe_dump(tmp, file)
        self.load_settings()
        