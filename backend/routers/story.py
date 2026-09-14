"""
Story API Router
"""

import uuid
from fastapi import APIRouter, HTTPException
from backend.schemas.story import StoryGenerateRequest, StoryGenerateResponse, SceneItemSchema
from core_pipeline.script_engine import generate_storyboard

router = APIRouter(prefix="/story", tags=["Kịch bản (Story)"])

@router.post("/generate", response_model=StoryGenerateResponse)
async def generate_story(req: StoryGenerateRequest):
    """
    Sinh kịch bản video ngắn từ ý tưởng hoặc chủ đề do người dùng cung cấp.
    """
    try:
        storyboard = generate_storyboard(
            topic=req.topic,
            scenes_count=req.scenes_count,
            language=req.language,
            api_key=req.api_key
        )
        
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        scenes_data = [
            SceneItemSchema(
                scene_id=s.scene_id,
                narration=s.narration,
                image_prompt=s.image_prompt,
                keywords=s.keywords
            )
            for s in storyboard.scenes
        ]

        return StoryGenerateResponse(
            project_id=project_id,
            title=storyboard.title,
            topic=req.topic,
            scenes=scenes_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi sinh kịch bản: {str(e)}")
