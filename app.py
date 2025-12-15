import os
import numpy as np
import uvicorn
from fastapi import FastAPI, Request, Form

# Assuming Blog_Post_AI_Agent is the project root
from src.Blog_Post_AI_Agent.graphs.graphBuilder import GraphBuilder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.Blog_Post_AI_Agent.llm.groqllm import GroqLLm
from src.Blog_Post_AI_Agent.llm.geminillm import GeminiLLm
from src.Blog_Post_AI_Agent.ui.uiconfigfile import Config


# --- 1. Load Configuration ---
try:
    # CONFIG_FILE_PATH must be relative to the execution root (where you run uvicorn)
    CONFIG_FILE_PATH = "uiconfigfile.ini"
    app_config = Config(config_file_name=CONFIG_FILE_PATH)
except Exception as e:
    print(f"Error loading configuration file: {e}")
    raise e


# --- 2. FastAPI App Initialization ---
app = FastAPI(title=app_config.get_page_title())
templates = Jinja2Templates(directory="templates")

os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

if "LANGCHAIN_API_KEY" in os.environ:
    os.environ["LANGSMITH_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]


# --- 3. FastAPI Routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders the main input form page, passing LLM options from the config.
    """
    llm_options = app_config.get_llm_options()
    groq_models = app_config.get_groq_model_options()
    gemini_models = app_config.get_gemini_model_options()

    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "page_title": app_config.get_page_title(),
            "llm_options": llm_options,
            "groq_models": groq_models,
            "gemini_models": gemini_models,
        }
    )

# --- 4. API Route with Dynamic LLM Selection ---
@app.post("/blogs")
async def create_blog(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    language = data.get("language", "")
    
    # LLM Configuration fields
    llm_provider = data.get("llm_provider", "").lower()
    llm_model = data.get("llm_model", "")
    api_key = data.get("api_key", "")

    if not all([topic, llm_provider, llm_model, api_key]):
        return JSONResponse(
            status_code=400,
            content={"message": "Missing required fields: topic, provider, model, or API key."}
        )

    # Dynamically select and initialize the correct LLM object
    llm = None
    try:
        if llm_provider == "groq":
            # ENABLED: Initialize the GroqLLm class
            llm_wrapper = GroqLLm(api_key=api_key, model_name=llm_model)
            llm = llm_wrapper.get_llm()
            
        elif llm_provider == "gemini":
            # ENABLED: Initialize the GeminiLLm class
            llm_wrapper = GeminiLLm(api_key=api_key, model_name=llm_model)
            llm = llm_wrapper.get_llm()
        
        else:
            return JSONResponse(
                status_code=400,
                content={"message": f"Unsupported LLM provider: {llm_provider}"}
            )

    except Exception as e:
        print(f"LLM Initialization Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": f"Failed to initialize LLM client: {e}"}
        )
        
    # Proceed with graph execution using the selected LLM
    graph_builder = GraphBuilder(llm)

    try:
        if language and topic:
            graph = graph_builder.setup_graph(usecase="language")
            state = graph.invoke({"topic": topic, "current_language": language.lower()})

        elif topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke({"topic": topic})

        # Final successful return
        return {"data": state}
        
    except Exception as e:
        print(f"Graph Execution Error: {e}")
        return JSONResponse(status_code=500, content={"message": f"Graph execution failed: {e}"})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
