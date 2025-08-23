import subprocess
from starlette.responses import JSONResponse
from typing import List, Dict, Any

from .file_utils import FileManager


class Downloader:
    def __init__(self, file_manager=None):
        self.file_manager = file_manager or FileManager()

    def _extract_subtitle_languages_and_extensions(self, captions_dict):
        lang_map = {}
        if not captions_dict:
            return lang_map

        for lang_code, tracks in captions_dict.items():
            if not tracks:
                continue

            # Pick the human-readable name from the first track
            lang_name = tracks[0].get("name", lang_code)

            lang_map[lang_name] = [
                {
                    "ext": track.get("ext", "vtt"),
                    "url": track.get("url")
                }
                for track in tracks if "url" in track
            ]

        return lang_map


    def _extract_media_streams(self, data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
        video_streams = []
        audio_streams = []

        for item in data:
            if not isinstance(item, dict):
                continue

            vcodec = item.get("vcodec", "none")
            acodec = item.get("acodec", "none")
            url = item.get("url")
            
            if not url:
                continue

            if vcodec != 'none':

                format = item.get("format_note")
                if format:
                    video_streams.append({
                        "Extension": item.get("ext", "N/A"),
                        "Quality": format,
                        "URL": url
                    })
                
            elif acodec != 'none' and vcodec == 'none':

                quality = item.get("format_note")
                if not quality and item.get("abr"):
                    quality = f"{item.get('abr')}k"
                elif not quality:
                    quality = "N/A"

                audio_streams.append({
                    "Extension": item.get("audio_ext", item.get("ext", "N/A")),
                    "Quality": quality,
                    "URL": url
                })

        return {
            "video": video_streams,
            "audio": audio_streams
        }

    def download_video(self, url: str, start: str = None, end: str = None, ext: str = 'mp4', quality: str = None) -> str:
        file_path = self.file_manager.create_temp_file("video", f".{ext}")
        format_selector = f"bestvideo[format_note={quality}]+bestaudio/best" if quality else "bestvideo+bestaudio/best"
        cmd = [
            "yt-dlp",
            "-f", format_selector,
            "-o", file_path,
            "--recode-video", ext
        ]
        if start or end:
            section = f"*{start}-{end}" if start and end else f"*{start or '0'}-"
            cmd += ["--download-sections", section]
        cmd.append(url)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp video download failed: {e}")
        return file_path

    def download_audio(self, url: str, start: str = None, end: str = None, ext: str = "mp3", quality: str = None) -> str:
        file_path = self.file_manager.create_temp_file("audio", f".{ext}")
        # If quality is specified, use format selector for audio quality
        if quality:
            format_selector = f"bestaudio[abr={quality}]"
        else:
            format_selector = "bestaudio/best"
        cmd = [
            "yt-dlp",
            "-f", format_selector,
            "-o", file_path,
            "--extract-audio",
            "--audio-format", ext
        ]
        if start or end:
            args = f"-ss {start or '0'}"
            if end:
                args += f" -to {end}"
            cmd += ["--postprocessor-args", args]
        cmd.append(url)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp audio download failed: {e}")
        return file_path

    def download_subtitles(self, url: str, lang: str = "en", format: str = "vtt") -> str:
        file_path = self.file_manager.create_temp_file("subs", f".{format}")
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-subtitles",
            "--sub-langs", lang,
            "--sub-format", format,
            "-o", file_path,
            url
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp subtitle download failed: {e}")
        return file_path

    def _get_best_thumbnail(self, thumbnails: dict) -> str:
        return max(thumbnails, key=lambda x: x['preference'])['url']

    def _format_response(self, response: dict) -> dict:
        return {
            "id": response["id"],
            "title": response["title"],
            "thumbnail": self._get_best_thumbnail(response["thumbnails"]),
            "views": response["view_count"],
            "channels": response["channel"],
            "duration": response["duration"],
            "duration_string": response["duration_string"],
            "streams": self._extract_media_streams(response.get("formats", [])),
            "subtitles": self._extract_subtitle_languages_and_extensions(response["automatic_captions"])
        }

    def get_metadata(self, url: str) -> dict:
        import json
        cmd = ["yt-dlp", "-j", url]
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            info = json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp metadata extraction failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse yt-dlp output: {e}")
        return self._format_response(info)
