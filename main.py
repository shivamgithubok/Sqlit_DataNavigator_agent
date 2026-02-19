from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents import app as agent_app

app = FastAPI()

# Serve static files for the frontend
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Initialize state with user query
        initial_state = {"query": request.message, "messages": [], "attempts": 0}
        
        # Invoke the LangGraph agent
        result = agent_app.invoke(initial_state)
        
        # Prepare response
        response = {
            "messages": result.get("messages", []),
            "data": result.get("data", []),
            "sql_query": result.get("sql_query", ""),
            "error": result.get("error")
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
