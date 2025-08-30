import subprocess
import json
from pathlib import Path
from models import MediaURL, MediaInfo
from utils import Utils

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
        
        # Base yt-dlp command to fetch JSON info
        command = ["yt-dlp", "-J", "--no-warnings", "--skip-download", media_url]

        # If a Netscape cookies file exists and has entries, add it
        try:
            cookies_path = Path(__file__).parent / "cookies.txt"
            if cookies_path.exists() and cookies_path.is_file():
                try:
                    lines = cookies_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                except Exception:
                    lines = []
                has_entries = any(line.strip() and not line.lstrip().startswith('#') for line in lines)
                if has_entries:
                    command.extend(["--cookies", str(cookies_path.resolve())])
        except Exception:
            # Ignore cookies issues for info command as a non-fatal path
            pass

        result = MediaFormatService._run_ytdlp_command(command, "get video info")
        
        if result.returncode != 0:
            raise MediaFormatService._handle_ytdlp_error(result.stderr, media_url)
        
        try:
            info_json = json.loads(result.stdout)
            media_info = Utils.extract_video_info(info_json)
            return MediaInfo(**media_info)
        except json.JSONDecodeError:
            raise Exception("Failed to parse yt-dlp JSON output")