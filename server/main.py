from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import FormatResponse, SubtitleResponse, ErrorResponse, MediaInfo, CombinedMediaResponse
from services import MediaFormatService

app = FastAPI(
    title="Media Formats API",
    description="API to get available media formats using yt-dlp",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _handle_service_error(e: Exception) -> HTTPException:
    """Convert service exceptions to appropriate HTTP errors"""
    return HTTPException(
        status_code=400 if any(keyword in str(e).lower() for keyword in [
            "unsupported", "private", "unavailable", "invalid"
        ]) else 500,
        detail=str(e)
    )

@app.get("/")
async def root():
    return {
        "message": "Media Formats API", 
        "version": "1.0.0",
    }

@app.get(
    "/formats",
    response_model=FormatResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_media_formats(url: str = Query(..., description="Media URL")):
    try:
        return MediaFormatService.get_media_formats(url)
    except Exception as e:
        raise _handle_service_error(e)

@app.get(
    "/subtitles",
    response_model=SubtitleResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_media_subtitles(url: str = Query(..., description="Media URL")):
    try:
        return MediaFormatService.get_media_subtitles(url)
    except Exception as e:
        raise _handle_service_error(e)

@app.get(
    "/info",
    response_model=MediaInfo,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_media_info(url: str = Query(..., description="Media URL")):
    try:
        return MediaFormatService.get_media_info(url)
    except Exception as e:
        raise _handle_service_error(e)

@app.get(
    "/mediadata",
    response_model=CombinedMediaResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_media_data(url: str = Query(..., description="Media URL")):
    """Get all media information (info, formats, and subtitles) in a single request"""
    try:
        return MediaFormatService.get_combined_media_data(url)
    except Exception as e:
        raise _handle_service_error(e)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "media-formats-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)