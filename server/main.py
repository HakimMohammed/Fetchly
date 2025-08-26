from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from models import DownloadRequest, DownloadResponse, ErrorResponse, MediaInfo
from services import MediaFormatService
from download_service import download_service
import mimetypes
from ffmpeg_util import supported_video_exts, supported_audio_exts


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

@app.get("/capabilities")
async def capabilities():
    """Expose what the server can actually output based on ffmpeg."""
    return {
        "video": sorted(list(supported_video_exts())),
    "audio": sorted(list(supported_audio_exts())),
    }

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

# Downloading
@app.post(
    "/download",
    response_model=DownloadResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def download_media(request: DownloadRequest, background_tasks: BackgroundTasks, req: Request):
    try:
        file_path, filename = download_service.download_media(request)
        
        # Schedule file cleanup
        background_tasks.add_task(download_service.cleanup_file, file_path)
        
        # Absolute URL for reliable client download
        absolute_url = str(req.url_for("download_file", filename=filename))

        return DownloadResponse(
            message="Download ready",
            filename=filename,
            download_url=absolute_url
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

@app.get("/download-file/{filename}", name="download_file")
async def download_file(filename: str):
    """Serve the downloaded file securely"""
    file_path = download_service.get_file_path(filename)
    
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    
    guessed, _ = mimetypes.guess_type(str(file_path))
    media_type = guessed or 'application/octet-stream'

    return FileResponse(
        str(file_path),
        media_type=media_type,
        filename=filename,
        headers={"Cache-Control": "no-store"}
    )
    
# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "media-formats-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)