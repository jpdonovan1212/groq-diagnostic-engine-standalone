import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from groq import Groq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Groq Code Diagnostic Engine",
    version="1.0.0",
    description="High-performance code analysis powered by Groq's Llama 3.1 models"
)


class DiagnosisRequest(BaseModel):
    language: str = Field(..., description="Programming language of the code (e.g., python, javascript)")
    code: str = Field(..., description="Source code to diagnose")
    context: Optional[str] = Field(None, description="Additional context for diagnosis")
    
    @validator('language')
    def validate_language(cls, v):
        supported_languages = ['python', 'javascript', 'typescript', 'java', 'c++', 'go', 'rust', 'ruby', 'php', 'swift']
        if v.lower() not in supported_languages:
            raise ValueError(f"Language must be one of: {', '.join(supported_languages)}")
        return v.lower()
    
    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty")
        if len(v) > 50000:  # ~50KB limit
            raise ValueError("Code exceeds maximum length of 50,000 characters")
        return v


class DiagnosisResponse(BaseModel):
    result: str
    model_used: str = "llama-3.1-8b-instant"


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "version": app.version}


@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    logger.info(f"Received diagnosis request for {request.language}")
    
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable not set")
        
        client = Groq(api_key=api_key)
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior software engineer specializing in code quality and best practices. "
                        "Analyze the provided code and return ONLY one of the following formats:\n\n"
                        "[CLEAN] No issues found.\n\n"
                        "OR\n\n"
                        "[ISSUE] <issue_type>: <description>\n\n"
                        "If multiple issues exist, list each on a new line starting with [ISSUE].\n"
                        "Keep responses concise and actionable."
                    )
                },
                {
                    "role": "user",
                    "content": f"Language: {request.language}\nContext: {request.context or 'None'}\n\nCode:\n{request.code}"
                }
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        ai_response = completion.choices[0].message.content.strip()
        logger.info(f"Successfully processed diagnosis request")
        return {
            "result": ai_response,
            "model_used": "llama-3.1-8b-instant"
        }

    except Exception as e:
        logger.error(f"AI Service error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Service error: {str(e)}")
