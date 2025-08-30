import subprocess
import json
from pathlib import Path
from models import MediaURL, MediaInfo
from utils import Utils
from ytdlp_config import extract_info, ydl_options

class MediaFormatService:
    
    @staticmethod
    def _validate_url(media_url: str) -> None:
        """Validate media URL format"""
        MediaURL(url=media_url)
    
    @staticmethod
    def _handle_ytdlp_error(error_msg: str, media_url: str) -> Exception:
        """Handle common yt-dlp errors"""
        if "Unsupported URL" in error_msg:
            return Exception(f"Unsupported media URL: {media_url}")
        elif "Private video" in error_msg:
            return Exception("This video is private or requires authentication")
        elif "Video unavailable" in error_msg:
            return Exception("Video is unavailable or has been removed")
        else:
            return Exception(f"yt-dlp error: {error_msg}")
    
    @staticmethod
    def _run_ytdlp_command(command: list, operation: str) -> subprocess.CompletedProcess:
        """Run yt-dlp command with consistent error handling"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result
        except subprocess.TimeoutExpired:
            raise Exception("Request timed out after 30 seconds")
        except Exception as e:
            raise Exception(f"Failed to {operation}: {str(e)}")
    
    @staticmethod
    def get_media_info(media_url: str) -> MediaInfo:
        MediaFormatService._validate_url(media_url)

        # Prefer the yt_dlp Python API for info extraction using shared options
        try:
            info_json = extract_info(media_url, options=ydl_options(skip_download=True, extract_flat=True))
            media_info = Utils.extract_video_info(info_json)
            return MediaInfo(**media_info)
        except Exception as e:
            # Map common error messages
            msg = str(e)
            raise MediaFormatService._handle_ytdlp_error(msg, media_url)