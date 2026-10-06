from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from backend.config import OUTPUT_DIR
    from backend.services.llm_service import generate_script
    from backend.services.tts_service import generate_audio
    from backend.services.video_service import generate_video
    from backend.services.social_service import plan_social_post
except ImportError:
    # دعم التشغيل من داخل مجلد backend مباشرة: `cd backend && uvicorn app:app`
    from config import OUTPUT_DIR
    from services.llm_service import generate_script
    from services.tts_service import generate_audio
    from services.video_service import generate_video
    from services.social_service import plan_social_post

app = FastAPI(title="منشئ المحتوى الذكي", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    topic: str
    tone: str = "إعلامي"
    platform: str = "YouTube Shorts"
    language: str = "ar"
    duration_seconds: int = 20


@app.get("/health")
def health():
    return {"status": "ok", "message": "الخادم يعمل بشكل طبيعي"}


@app.get("/")
def root():
    return {"message": "منشئ المحتوى الذكي - API"}


@app.post("/generate")
def generate_content(request: GenerateRequest):
    try:
        script = generate_script(
            topic=request.topic,
            tone=request.tone,
            platform=request.platform,
            language=request.language,
        )

        audio_path = generate_audio(script)
        video_path = generate_video(
            script=script,
            audio_path=audio_path,
            platform=request.platform,
            duration_seconds=request.duration_seconds,
        )
        post = plan_social_post(request.topic, request.platform, script)

        return {
            "status": "success",
            "topic": request.topic,
            "script": script,
            "audio": audio_path,
            "video": video_path,
            "social_plan": post,
            "output_dir": str(OUTPUT_DIR),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
