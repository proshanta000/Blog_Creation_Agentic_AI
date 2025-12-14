import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv


class GroqLLm:
    """
    Handles initialization and configuration of the Groq LLM using environment variables.
    """
    def __init__(self):
        """
        Initializes the GroqLLm class.
        
        Loads environment variables from a .env file to ensure configuration is available.
        """
        # Load environment variables from the .env file
        load_dotenv()


    def get_llm(self):
        """
        Retrieves the configured Groq LLM instance.

        Fetches the API key from the environment and initializes the ChatGroq model
        with the model name "llama-3.1-8b-instant".
        
        Returns:
            ChatGroq: An instance of the Groq model.
        
        Raises:
            ValueError: If there is an error during model initialization,
                        often due to a missing or invalid API key.
        """
        try:
            # Fetch the GROQ_API_KEY from the environment
            self.groq_api_key = os.getenv("GROQ_API_KEY")
            
            # Check if the key was found
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")

            # Initialize the ChatGroq model
            llm = ChatGroq(api_key=self.groq_api_key, model="llama-3.1-8b-instant")

            return llm
        
        except Exception as e:
            # Catch any exception during the process and raise a detailed error
            raise ValueError(f"Failed to initialize GroqLLm: {e}")