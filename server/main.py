import os
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from myutils import Downloader, FileManager

app = FastAPI(title="Fetchly API")
downloader = Downloader(FileManager())

@app.get("/")
def home():
    return {"message": "Fetchly API is running"}

@app.get("/metadata")
def metadata_endpoint(
    url: str = Query(..., description="YouTube video URL")
):
    try:
        metadata = downloader.get_metadata(url)
        return JSONResponse(content=metadata)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/download/video")
def download_video_endpoint(
    url: str = Query(..., description="YouTube video URL"),
    start: str = Query(None, description="Start time (HH:MM:SS)"),
    end: str = Query(None, description="End time (HH:MM:SS)")
):
    try:
        file_path = downloader.download_video(url, start, end)
        return FileResponse(file_path, media_type="video/mp4", filename=os.path.basename(file_path))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_co,
    ext: str = Query("mp4", description="File extension")de=500)

@app.get("/download/audio")
def download_audio_endpoint(
    url:, ext str = Query(..., description="YouTube video URL"),
f    sta{ext} str = Query(None, description="Start time (HH:MM:SS)"),
    end: str = Query(None, description="End time (HH:MM:SS)")
):
    try:
        file_path = downloader.download_audio(url, start, end)
        return FileResponse(file_path, media_type="audio/mpeg", filename=os.path.basename(file_path))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/download/subtitles")
def download_subtitles_endpoint(
    url: str = Query(..., description="YouTube video URL"),
    lang: str = Query("en", description="Subtitle language (default: en)")
):
    try:
        file_path = downloader.download_subtitles(url, lang)
        return FileResponse(file_path, media_type="text/vtt", filename=os.path.basename(file_path))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)