from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import traceback

from chat_logic import run_chat  # ✅ async function from chat_logic


app = FastAPI(title="DataBuddy 🧠")


# ==========================================================
# 🌐 CORS Setup
# ==========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (fine for dev; restrict in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# 🧱 Static + Template Setup
# ==========================================================
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend")


# ==========================================================
# 📦 Request Schema
# ==========================================================
class QueryRequest(BaseModel):
    message: str
    session_id: str = "default_user"
    thread_id: str = "default_thread"
    model_provider: str = "groq"
    model_name: str = "llama-3.1-8b-instant"
    api_key: str | None = None
    db_uri: str | None = None


# ==========================================================
# 🧹 Helper to make JSON safe
# ==========================================================
def safe_json(data):
    """Recursively convert sets (and nested sets) to lists for safe JSON encoding."""
    if isinstance(data, set):
        return list(data)
    elif isinstance(data, dict):
        return {k: safe_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [safe_json(v) for v in data]
    return data


# ==========================================================
# 🏠 Route: Home
# ==========================================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve main chat page."""
    return templates.TemplateResponse("index.html", {"request": request})


# ==========================================================
# 💬 Route: Query DataBuddy
# ==========================================================
@app.post("/query")
async def query_data_buddy(req: QueryRequest):
    """
    Handle user query → run DataBuddy agent → return text or structured error.
    """
    try:
        # ✅ Async agent call
        response_text = await run_chat(
            model_name=req.model_name,
            provider=req.model_provider,
            api_key=req.api_key,
            db_uri=req.db_uri or "sqlite:///data/demo.db",
            user_query=req.message,
            thread_id=req.thread_id,
        )

        # ✅ Return Markdown text for frontend rendering
        return PlainTextResponse(content=str(response_text))

    except Exception as e:
        # Log error
        print(f"⚠️ Error in /query: {e}")
        traceback.print_exc()

        err_str = str(e).lower()

        # Handle common known issues
        if "tool_use_failed" in err_str or "sql_db_schema" in err_str:
            return JSONResponse(
                status_code=400,
                content=safe_json({
                    "error": "Database schema retrieval failed. The table might not exist or is inaccessible.",
                    "details": str(e),
                }),
            )

        if "rate_limit_exceeded" in err_str:
            return JSONResponse(
                status_code=429,
                content=safe_json({
                    "error": "Rate limit exceeded for the LLM API.",
                    "message": "Please wait a few seconds and try again.",
                }),
            )

        # Fallback for unexpected errors
        return JSONResponse(
            status_code=500,
            content=safe_json({
                "error": str(e),
                "message": "An internal error occurred. Try providing more context or check DB connection."
            }),
        )


# ==========================================================
# 🧪 Dev Entrypoint
# ==========================================================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
