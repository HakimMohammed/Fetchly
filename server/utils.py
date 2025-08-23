import re
from typing import Dict, List, Any

class Utils:

    @staticmethod
    def extract_video_info(info_json: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'title': info_json.get('title', 'Unknown'),
            'duration': info_json.get('duration', 0),
            'duration_string': info_json.get('duration_string', ''),
            'thumbnail': info_json.get('thumbnail', ''),
            'views': info_json.get('view_count'),
        }

    @staticmethod
    def parse_ytdlp_output(output_text: str) -> Dict[str, Dict[str, List[str]]]:
        lines = output_text.split('\n')
        
        video_formats = {}
        audio_formats = {}
        
        for line in lines:
            line = line.strip()
            
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
            
            # Validate that format_id is actually a format ID (should be alphanumeric)
            if not re.match(r'^[a-zA-Z0-9_-]+$', format_id):
                continue
                
            # Validate that extension is a valid file extension
            if not re.match(r'^[a-zA-Z0-9]+$', extension) or extension == 'mhtml':
                continue
            
            # More robust audio detection
            is_audio_only = (
                ('audio only' in line.lower()) or 
                ('audio-only' in line.lower()) or
                (re.search(r'\baudio\b.*\bonly\b', line.lower())) or
                (re.search(r'\bonly\b.*\baudio\b', line.lower()))
            )
            
            # Additional check: if it has video resolution info, it's not audio-only
            if re.search(r'\d+p|\d+x\d+', line):
                is_audio_only = False
            
            if is_audio_only:
                bitrate_match = re.search(r'(\d+k)', line)
                quality = bitrate_match.group(1) if bitrate_match else "unknown"
                
                if extension not in audio_formats:
                    audio_formats[extension] = []
                
                if quality not in audio_formats[extension]:
                    audio_formats[extension].append(quality)
            else:
                quality_match = re.search(r'(\d+)p', line)
                if quality_match:
                    quality = quality_match.group(0)
                else:
                    res_match = re.search(r'(\d+)x(\d+)', line)
                    if res_match:
                        height = res_match.group(2)
                        quality = f"{height}p"
                    else:
                        quality = "unknown"
                
                if extension not in video_formats:
                    video_formats[extension] = []
                
                if quality not in video_formats[extension]:
                    video_formats[extension].append(quality)
        
        for ext in video_formats:
            video_formats[ext] = sorted(
                video_formats[ext], 
                key=lambda x: int(x.replace('p', '')) if x != 'unknown' else 0
            )
        
        for ext in audio_formats:
            audio_formats[ext] = sorted(
                audio_formats[ext],
                key=lambda x: int(x.replace('k', '')) if x != 'unknown' else 0
            )
        
        return {
            'video_formats': video_formats,
            'audio_formats': audio_formats,
        }

    @staticmethod
    def parse_ytdlp_subtitles(output_text: str) -> Dict[str, Dict[str, List[str]]]:
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
            
            # Validate language code (should be valid language format)
            if not re.match(r'^[a-z]{2,3}(-[a-zA-Z]+)?$', language_code):
                continue
            
            # Extract formats from the formats text
            # Remove common descriptive text and split by comma and space
            formats_clean = re.sub(r'\s*,\s*', ',', formats_text)
            available_formats = [f.strip() for f in formats_clean.split(',') if f.strip()]
            
            # Filter out invalid formats (keep only alphanumeric format names)
            valid_formats = []
            for fmt in available_formats:
                if re.match(r'^[a-zA-Z0-9]+$', fmt):
                    valid_formats.append(fmt)
            
            if valid_formats:
                subtitles[language_code] = {
                    'language_name': language_name,
                    'formats': valid_formats
                }
        
        return {
            'subtitles': subtitles
        }