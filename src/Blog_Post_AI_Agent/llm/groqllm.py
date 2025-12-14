import os
from langchain_groq import ChatGroq


class GroqLLm:
    """
    Handles initialization and configuration of the Groq LLM.
    
    This class strictly requires both the API key and model name to be passed 
    directly during initialization, enabling a fully dynamic system based 
    on user selections from the UI.
    """
    def __init__(self, api_key: str, model_name: str):
        """
        Initializes the GroqLLm class and the ChatGroq instance.
        
        Args:
            api_key (str): The Groq API key provided directly from the UI form. 
                           (Mandatory)
            model_name (str): The name of the Groq model to use, selected from the UI form.
                              (Mandatory)
        """
        
        # 1. Store mandatory arguments
        self._api_key = api_key
        self._model_name = model_name
        
        # 2. Validation: Ensure both critical pieces of data are present
        if not self._api_key or not self._api_key.strip():
            raise ValueError("API Key is required but was not provided.")
            
        if not self._model_name or not self._model_name.strip():
            raise ValueError("Model Name is required but was not provided.")
        
        try:
            # Initialize the ChatGroq model with the user-provided key and model
            self._llm = ChatGroq(
                api_key=self._api_key, 
                model=self._model_name,
                temperature=0.0
            )
            print(f"Successfully initialized GroqLLM with model: {self._model_name}")
            
        except Exception as e:
            # Catch any exception during initialization (e.g., connection errors, invalid model name)
            raise ValueError(f"Failed to initialize ChatGroq model '{self._model_name}': {e}")


    def get_llm(self):
        """
        Retrieves the configured Groq LLM instance.

        Returns:
            ChatGroq: The initialized Groq model instance.
        """
        return self._llm