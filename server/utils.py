from typing import Dict, Any

class Utils:
    
    @staticmethod
    def extract_video_info(info_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant video information from yt-dlp JSON output"""
        return {
            'title': info_json.get('title', 'Unknown'),
            'duration': info_json.get('duration', 0),
            'duration_string': info_json.get('duration_string', ''),
            'thumbnail': info_json.get('thumbnail', ''),
            'views': info_json.get('view_count'),
        }