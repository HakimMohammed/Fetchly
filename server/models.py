from pydantic import BaseModel, HttpUrl, field_validator
from pydantic import ValidationInfo
from typing import Optional, Literal
import re
"""Pydantic models and request validation primitives.

Keep environment-dependent validation (like probing ffmpeg) out of models;
services enforce capability checks at runtime.
"""

class MediaURL(BaseModel):
    url: HttpUrl

class MediaInfo(BaseModel):
    title: str
    duration: int
    duration_string: str
    thumbnail: str
    views: Optional[int] = None

    

class ErrorResponse(BaseModel):
    error: str

class DownloadRequest(BaseModel):
    url: str
    media_type: Literal["video", "audio"]
    extension: Optional[str] = None
    quality: Optional[str] = None
    # Trimming
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    @field_validator("url")
    def validate_url(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("URL cannot be empty")
        return v.strip()

    @field_validator("quality")
    def validate_quality(cls, v: Optional[str], info: ValidationInfo):
        if not v:
            return v
        data = info.data or {}
        media_type = data.get("media_type")
        if media_type == "video":
            if not v.endswith("p") or not v[:-1].isdigit():
                raise ValueError('Video quality must be in format like "720p", "1080p"')
        elif media_type == "audio":
            if not (v.endswith("k") or v.endswith("K")) or not v[:-1].isdigit():
                raise ValueError('Audio quality must be in format like "128k", "192k"')
        return v

    @field_validator("extension")
    def validate_extension(cls, v: Optional[str], info: ValidationInfo):
        if not v:
            return v
        # Only syntactic validation here; capability checks are done in services
        if not re.match(r"^[a-zA-Z0-9]{2,5}$", v):
            raise ValueError("Extension must be 2-5 alphanumeric characters")
        return v

    @field_validator("start_time", "end_time")
    def validate_time_hms(cls, v: Optional[str]):
        if not v:
            return v
        if not re.match(r"^\d{2}:\d{2}:\d{2}$", v):
            raise ValueError("Time must be HH:MM:SS")
        return v

class DownloadResponse(BaseModel):
    message: str
    filename: Optional[str] = None
    download_url: Optional[str] = None