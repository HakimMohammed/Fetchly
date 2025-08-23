import subprocess
from models import FormatResponse, MediaURL, SubtitleResponse, MediaInfo
from utils import Utils
import json

class MediaFormatService:
    
    @staticmethod
    def get_media_info(media_url: str) -> MediaInfo:
        try:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "--dump-json",
                    "--no-warnings",
                    media_url
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise Exception(f"yt-dlp error: {result.stderr}")
            
            info_json = json.loads(result.stdout)
            media_info = Utils.extract_video_info(info_json)
            return MediaInfo(**media_info)

        except subprocess.TimeoutExpired:
            raise Exception("Request timed out")
        except json.JSONDecodeError:
            raise Exception("Failed to parse yt-dlp JSON output")
        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")
        
    @staticmethod
    def get_media_formats(media_url: str) -> FormatResponse:
        try:
            MediaURL(url=media_url)
            
            result = subprocess.run(
                [
                    "yt-dlp", 
                    "--list-formats", 
                    media_url
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = result.stderr
                if "Unsupported URL" in error_msg:
                    raise Exception(f"Unsupported media URL: {media_url}")
                elif "Private video" in error_msg:
                    raise Exception("This video is private or requires authentication")
                elif "Video unavailable" in error_msg:
                    raise Exception("Video is unavailable or has been removed")
                else:
                    raise Exception(f"yt-dlp error: {error_msg}")
            
            print("\n=================================================\n")
            print(result.stdout)
            print("\n=================================================\n")
            parsed_data = Utils.parse_ytdlp_output(result.stdout)
            return FormatResponse(**parsed_data)

        except subprocess.TimeoutExpired:
            raise Exception("Request timed out after 30 seconds")
        except Exception as e:
            raise Exception(f"Failed to get formats: {str(e)}")
    
    @staticmethod
    def get_media_subtitles(media_url: str) -> SubtitleResponse:
        try:
            MediaURL(url=media_url)
            
            result = subprocess.run(
                [
                    "yt-dlp", 
                    "--list-subs", 
                    media_url
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = result.stderr
                if "Unsupported URL" in error_msg:
                    raise Exception(f"Unsupported media URL: {media_url}")
                elif "Private video" in error_msg:
                    raise Exception("This video is private or requires authentication")
                elif "Video unavailable" in error_msg:
                    raise Exception("Video is unavailable or has been removed")
                else:
                    raise Exception(f"yt-dlp error: {error_msg}")
            
            print("\n================= SUBTITLES ===================\n")
            print(result.stdout)
            print("\n==============================================\n")
            parsed_data = Utils.parse_ytdlp_subtitles(result.stdout)
            return SubtitleResponse(**parsed_data)

        except subprocess.TimeoutExpired:
            raise Exception("Request timed out after 30 seconds")
        except Exception as e:
            raise Exception(f"Failed to get subtitles: {str(e)}")