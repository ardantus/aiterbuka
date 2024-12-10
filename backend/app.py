from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_logic import handle_chat
from database import init_db, save_chat, get_response

app = FastAPI()

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],  # Tambahkan URL frontend
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

# Initialize database
init_db()

# Global variable for model name
MODEL_NAME = "llama3.2:latest"  # Default model

class ChatRequest(BaseModel):
    prompt: str

class ModelUpdate(BaseModel):
    model_name: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Endpoint untuk chat AI."""
    response = get_response(request.prompt)
    if response:
        return {"response": response}
    else:
        # Pass the selected model to the handle_chat function
        ai_response = handle_chat(request.prompt, MODEL_NAME)
        save_chat(request.prompt, ai_response)
        return {"response": ai_response}

@app.put("/model")
async def update_model(model_update: ModelUpdate):
    """Endpoint untuk mengubah model yang digunakan."""
    global MODEL_NAME
    MODEL_NAME = model_update.model_name
    return {"message": f"Model updated to {MODEL_NAME}"}
