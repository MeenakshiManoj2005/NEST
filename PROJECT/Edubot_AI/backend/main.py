from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API Key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Create FastAPI App
app = FastAPI(title="EduBot AI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class ChatRequest(BaseModel):
    message: str

# Home Route
@app.get("/")
def home():
    return {
        "message": "EduBot AI Groq Backend Running"
    }

# Chat Route
@app.post("/chat")
async def chat(request: ChatRequest):
    try:

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are EduBot AI, a personal learning assistant.

                    Help students with:
                    - Study doubts
                    - Programming questions
                    - Note summarization
                    - Learning tips
                    - Career guidance

                    Give clear and beginner-friendly answers.
                    """
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        )

        response = completion.choices[0].message.content

        return {
            "response": response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
