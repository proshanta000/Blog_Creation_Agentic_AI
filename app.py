import os
import numpy as np
import uvicorn
from fastapi import FastAPI, Request, Form
from src.Blog_Post_AI_Agent.graphs.graphBuilder import GraphBuilder
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.Blog_Post_AI_Agent.llm.groqllm import GroqLLm

import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()


if "LANGCHAIN_API_KEY" in os.environ:
    os.environ["LANGSMITH_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]

# API

@app.post("/blogs")
async def create_blog(request:Request):
    data = await request.json()
    topic = data.get("topic", "")
    language = data.get("language", "")

    # Get the llm object
    groqllm = GroqLLm()
    llm = groqllm.get_llm()

    # Get the graph
    graph_builder = GraphBuilder(llm)

    if language and topic:
        graph = graph_builder.setup_graph(usecase="language")
        state = graph.invoke({"topic": topic, "current_language": language.lower()})


    elif topic:
        graph = graph_builder.setup_graph(usecase="topic")
        state = graph.invoke({"topic": topic})
    


    return {"data":state}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)