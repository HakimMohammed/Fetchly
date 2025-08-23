from pydantic import BaseModel
from typing import Dict, List, Optional

class MediaURL(BaseModel):
    url: str

class MediaInfo(BaseModel):
    title: str
    duration: int
    duration_string: str
    thumbnail: str
    views: Optional[int] = None

class FormatResponse(BaseModel):
    video_formats: Dict[str, List[str]]
    audio_formats: Dict[str, List[str]]

class SubtitleInfo(BaseModel):
    language_name: str
    formats: List[str]

class SubtitleResponse(BaseModel):
    subtitles: Dict[str, SubtitleInfo]

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None