import os
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLLm:
    """
    Handles initialization and configuration of the Gemini LLM using LangChain.
    
    This class strictly requires both the API key and model name to be passed 
    directly during initialization, enabling a fully dynamic system based 
    on user selections from the UI (BYOK and dynamic model).
    """
    def __init__(self, api_key: str, model_name: str):
        """
        Initializes the GeminiLLm class and the ChatGoogleGenerativeAI instance.
        
        Args:
            api_key (str): The Google AI API key provided directly from the UI form. 
                           (Mandatory)
            model_name (str): The name of the Gemini model to use, selected from the UI form.
                              (Mandatory)
        """
        
        # 1. Store mandatory arguments
        self._api_key = api_key
        self._model_name = model_name
        
        # 2. Validation: Ensure both critical pieces of data are present
        if not self._api_key or not self._api_key.strip():
            raise ValueError("API Key is required but was not provided to GeminiLLm.")
            
        if not self._model_name or not self._model_name.strip():
            raise ValueError("Model Name is required but was not provided to GeminiLLm.")
        
        try:
            # 3. Initialize the ChatGoogleGenerativeAI model
            self._llm = ChatGoogleGenerativeAI(
                google_api_key=self._api_key, 
                model=self._model_name,
                temperature=0.2
            )
            print(f"Successfully initialized GeminiLLM with model: {self._model_name}")
            
        except Exception as e:
            # Catch any exception during initialization (e.g., connection errors, invalid model name)
            raise ValueError(f"Failed to initialize ChatGoogleGenerativeAI model '{self._model_name}': {e}")


    def get_llm(self):
        """
        Retrieves the configured Gemini LLM instance.

        Returns:
            ChatGoogleGenerativeAI: The initialized Gemini model instance.
        """
        return self._llm