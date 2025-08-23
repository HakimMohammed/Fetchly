import re
from typing import Dict, List, Any

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

    @staticmethod
    def parse_ytdlp_output(output_text: str) -> Dict[str, Dict[str, List[str]]]:
        """Parse yt-dlp format list output into structured data"""
        lines = output_text.split('\n')
        
        video_formats = {}
        audio_formats = {}
        
        for line in lines:
            line = line.strip()
            
            # Skip irrelevant lines
            if (not line or 
                line.startswith('ID') or 
                line.startswith('--') or
                '[info]' in line or
                'FILESIZE' in line or
                'storyboard' in line or
                'Extracting' in line or
                line.endswith(':')):
                continue
            
            parts = line.split()
            if len(parts) < 3:
                continue
                
            format_id = parts[0]
            extension = parts[1]
            
            # Validate format components
            if not re.match(r'^[a-zA-Z0-9_-]+$', format_id):
                continue
                
            if not re.match(r'^[a-zA-Z0-9]+$', extension) or extension == 'mhtml':
                continue
            
            # Determine if this is audio-only
            is_audio_only = Utils._is_audio_only_format(line)
            
            if is_audio_only:
                quality = Utils._extract_audio_quality(line)
                Utils._add_format(audio_formats, extension, quality)
            else:
                quality = Utils._extract_video_quality(line)
                Utils._add_format(video_formats, extension, quality)
        
        # Sort qualities
        Utils._sort_video_formats(video_formats)
        Utils._sort_audio_formats(audio_formats)
        
        return {
            'video_formats': video_formats,
            'audio_formats': audio_formats,
        }
    
    @staticmethod
    def _is_audio_only_format(line: str) -> bool:
        """Determine if a format line represents audio-only content"""
        line_lower = line.lower()
        
        # Check for audio-only indicators
        audio_only = (
            ('audio only' in line_lower) or 
            ('audio-only' in line_lower) or
            (re.search(r'\baudio\b.*\bonly\b', line_lower)) or
            (re.search(r'\bonly\b.*\baudio\b', line_lower))
        )
        
        # If it has video resolution info, it's not audio-only
        if re.search(r'\d+p|\d+x\d+', line):
            audio_only = False
            
        return audio_only
    
    @staticmethod
    def _extract_audio_quality(line: str) -> str:
        """Extract audio quality (bitrate) from format line"""
        bitrate_match = re.search(r'(\d+k)', line)
        return bitrate_match.group(1) if bitrate_match else "unknown"
    
    @staticmethod
    def _extract_video_quality(line: str) -> str:
        """Extract video quality (resolution) from format line"""
        quality_match = re.search(r'(\d+)p', line)
        if quality_match:
            return quality_match.group(0)
        
        res_match = re.search(r'(\d+)x(\d+)', line)
        if res_match:
            height = res_match.group(2)
            return f"{height}p"
        
        return "unknown"
    
    @staticmethod
    def _add_format(formats_dict: dict, extension: str, quality: str) -> None:
        """Add format to dictionary if not already present"""
        if extension not in formats_dict:
            formats_dict[extension] = []
        
        if quality not in formats_dict[extension]:
            formats_dict[extension].append(quality)
    
    @staticmethod
    def _sort_video_formats(video_formats: dict) -> None:
        """Sort video formats by resolution"""
        for ext in video_formats:
            video_formats[ext] = sorted(
                video_formats[ext], 
                key=lambda x: int(x.replace('p', '')) if x != 'unknown' else 0
            )
    
    @staticmethod
    def _sort_audio_formats(audio_formats: dict) -> None:
        """Sort audio formats by bitrate"""
        for ext in audio_formats:
            audio_formats[ext] = sorted(
                audio_formats[ext],
                key=lambda x: int(x.replace('k', '')) if x != 'unknown' else 0
            )

    @staticmethod
    def parse_ytdlp_subtitles(output_text: str) -> Dict[str, Dict[str, List[str]]]:
        """Parse yt-dlp subtitle list output into structured data"""
        lines = output_text.split('\n')
        subtitles = {}
        
        for line in lines:
            line = line.strip()
            
            # Skip header lines and empty lines
            if (not line or 
                line.startswith('Language') or 
                line.startswith('--') or
                '[info]' in line):
                continue
            
            # Split the line into parts
            parts = line.split(None, 2)  # Split into max 3 parts
            if len(parts) < 3:
                continue
                
            language_code = parts[0]
            language_name = parts[1]
            formats_text = parts[2]
            
            # Validate language code
            if not re.match(r'^[a-z]{2,3}(-[a-zA-Z]+)?$', language_code):
                continue
            
            # Extract and validate formats
            valid_formats = Utils._extract_subtitle_formats(formats_text)
            
            if valid_formats:
                subtitles[language_code] = {
                    'language_name': language_name,
                    'formats': valid_formats
                }
        
        return {'subtitles': subtitles}
    
    @staticmethod
    def _extract_subtitle_formats(formats_text: str) -> List[str]:
        """Extract valid subtitle formats from format text"""
        formats_clean = re.sub(r'\s*,\s*', ',', formats_text)
        available_formats = [f.strip() for f in formats_clean.split(',') if f.strip()]
        
        # Filter out invalid formats
        valid_formats = []
        for fmt in available_formats:
            if re.match(r'^[a-zA-Z0-9]+$', fmt):
                valid_formats.append(fmt)
        
        return valid_formats