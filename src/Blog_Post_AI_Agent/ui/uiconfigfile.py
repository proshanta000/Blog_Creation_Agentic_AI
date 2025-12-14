from configparser import ConfigParser
from pathlib import Path

class Config:
    """
    Configuration helper class to read settings from the INI file.
    The path is now dynamically resolved relative to this script's location.
    """
    def __init__(self, config_file_name="uiconfigfile.ini"):
        """
        Initialize the Config parser.
        
        Args:
            config_file_name (str): The name of the configuration file 
                                    (assumed to be in the same directory as this script).
        """
        # 1. Get the path to the directory containing THIS Python file (uiconfigfile.py)
        # __file__ gives the path to the current module.
        # .resolve() handles symbolic links and gets the absolute path.
        # .parent gets the directory containing the file.
        config_dir = Path(__file__).resolve().parent
        
        # 2. Construct the full, absolute path to the INI file
        # This joins the directory path and the file name reliably.
        config_file_path = config_dir / config_file_name

        self.config = ConfigParser()
        
        # Check if the file exists before trying to read it
        if not config_file_path.exists():
             raise FileNotFoundError(
                 f"Configuration file not found at the expected path: {config_file_path}"
             )
        
        # Read the file using the robust path
        self.config.read(config_file_path)

    
    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_gemini_model_options(self):
        return self.config["DEFAULT"].get("GEMINI_MODEL_OPTIONS").split(", ")
    
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")