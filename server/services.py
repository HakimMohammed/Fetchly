import subprocess
import json
from models import FormatResponse, MediaURL, SubtitleResponse, MediaInfo, CombinedMediaResponse
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
        
        result = MediaFormatService._run_ytdlp_command(
            ["yt-dlp", "--dump-json", "--no-warnings", media_url],
            "get video info"
        )
        
        if result.returncode != 0:
            raise MediaFormatService._handle_ytdlp_error(result.stderr, media_url)
        
        try:
            info_json = json.loads(result.stdout)
            media_info = Utils.extract_video_info(info_json)
            return MediaInfo(**media_info)
        except json.JSONDecodeError:
            raise Exception("Failed to parse yt-dlp JSON output")
        
    @staticmethod
    def get_media_formats(media_url: str) -> FormatResponse:
        MediaFormatService._validate_url(media_url)
        
        result = MediaFormatService._run_ytdlp_command(
            ["yt-dlp", "--list-formats", media_url],
            "get formats"
        )
        
        if result.returncode != 0:
            raise MediaFormatService._handle_ytdlp_error(result.stderr, media_url)

        parsed_data = Utils.parse_ytdlp_output(result.stdout)
        return FormatResponse(**parsed_data)
    
    @staticmethod
    def get_media_subtitles(media_url: str) -> SubtitleResponse:
        MediaFormatService._validate_url(media_url)
        
        result = MediaFormatService._run_ytdlp_command(
            ["yt-dlp", "--list-subs", media_url],
            "get subtitles"
        )
        
        if result.returncode != 0:
            raise MediaFormatService._handle_ytdlp_error(result.stderr, media_url)

        parsed_data = Utils.parse_ytdlp_subtitles(result.stdout)
        return SubtitleResponse(**parsed_data)
    
    @staticmethod
    def get_combined_media_data(media_url: str) -> CombinedMediaResponse:
        """Get all media information in a single call"""
        MediaFormatService._validate_url(media_url)
        
        info = MediaFormatService.get_media_info(media_url)
        formats = MediaFormatService.get_media_formats(media_url)
        subtitles = MediaFormatService.get_media_subtitles(media_url)
        
        return CombinedMediaResponse(
            info=info,
            formats=formats,
            subtitles=subtitles
        )