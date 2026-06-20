from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home():
    return {"message": "EduBot AI Backend Running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  
            messages=[
                {
                    "role": "system",
                    "content": "You are EduBot AI, a helpful learning assistant."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        )

        if completion and completion.choices:
            return {
                "response": completion.choices[0].message.content
            }
        else:
            raise HTTPException(
                status_code=502,
                detail="Groq API returned an empty response."
            )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"API Error: {str(e)}"
        )
