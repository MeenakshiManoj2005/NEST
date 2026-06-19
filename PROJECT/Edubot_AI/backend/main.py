
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

GROQ_API_KEY=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
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "EduBot AI Groq Backend Running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": request.message}
            ],
        )
        reply = completion.choices[0].message.content
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
