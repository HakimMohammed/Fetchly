import os
import uuid
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple
from models import DownloadRequest
from ffmpeg_util import supported_video_exts, supported_audio_exts

class DownloadService:
    
    def __init__(self, downloads_dir: str = "downloads"):
        self.downloads_dir = Path(downloads_dir)
        self.downloads_dir.mkdir(exist_ok=True)
        self._cleanup_interval = 3600

    # Removed legacy filename helper; we rely on yt-dlp templating with marker

    def _build_ytdlp_command(self, request: DownloadRequest, marker: str | None = None) -> tuple[list, str]:
        """Build yt-dlp command based on request parameters and return (command, marker)"""
        # Generate unique marker used in filename for later identification
        if not marker:
            marker = f"{int(time.time())}_{str(uuid.uuid4())[:8]}"
        unique_filename = f"%(title)s_{marker}.%(ext)s"
        output_template = str(self.downloads_dir / unique_filename)
        
        command = ["yt-dlp", "-o", output_template, request.url]

        # Optional trimming via download sections
        section = self._build_download_sections(request.start_time, request.end_time)
        if section:
            command.extend(["--download-sections", section])

        if request.media_type == "video":
            format_selector = self._build_video_format_selector(request)
            command.extend(["-f", format_selector])
            # Prefer output containers via merge rather than filtering formats by ext
            # If user specified an extension, honor it; otherwise provide preferences
            merge_pref = request.extension if request.extension else "mp4/mkv/webm"
            command.extend(["--merge-output-format", merge_pref])
        elif request.media_type == "audio":
            command.extend(self._build_audio_command(request))

        return command, marker

    def _build_download_sections(self, start: Optional[str], end: Optional[str]) -> Optional[str]:
        """Build yt-dlp --download-sections value like *HH:MM:SS-HH:MM:SS"""
        if not start and not end:
            return None
        s = start or "00:00:00"
        e = end or ""
        return f"*{s}-{e}"

    def _build_video_format_selector(self, request: DownloadRequest) -> str:
        """Build a robust selector that prefers separate streams within a height cap.

        Examples:
        - With quality=720p -> "bv*[height<=720]+ba/b[height<=720]"
        - Without quality -> "bv*[height<=1080]+ba/b[height<=1080]"
        """
        # Determine height cap
        height_cap = None
        if request.quality:
            h = request.quality.replace('p', '')
            if h.isdigit():
                height_cap = h
        if not height_cap:
            height_cap = "1080"

        filt = f"[height<={height_cap}]" if height_cap else ""
        # Do not constrain by ext here; let merge-output-format decide container
        return f"bv*{filt}+ba/b{filt}"

    def _build_audio_command(self, request: DownloadRequest) -> list:
        """Build audio extraction command"""
        audio_cmd = ["-x"]  # Extract audio
        
        # Choose a sensible default if not provided
        chosen_ext = request.extension
        if not chosen_ext:
            # preference order
            prefs = ["mp3", "m4a", "opus", "wav"]
            avail = supported_audio_exts()
            for p in prefs:
                if p in avail:
                    chosen_ext = p
                    break
            # if still None, let yt-dlp decide
        if chosen_ext:
            audio_cmd.extend(["--audio-format", chosen_ext])
            
        # For audio quality, yt-dlp expects bitrate values like 128, 192, etc.
        if request.quality:
            # Remove 'k' suffix if present and validate
            quality_value = request.quality.replace('k', '').replace('K', '')
            try:
                bitrate = int(quality_value)
                audio_cmd.extend(["--audio-quality", str(bitrate)])
            except ValueError:
                pass
                
        return audio_cmd

    # Subtitle downloads removed to focus on core video/audio functionality

    def _find_downloaded_file(self, marker: str | None = None) -> Optional[Path]:
        """Find the downloaded file; if marker provided, prefer files containing it"""
        try:
            # Get all files that are not partial downloads
            files = [
                f for f in self.downloads_dir.iterdir() 
                if f.is_file() and not f.name.endswith(('.part', '.tmp'))
            ]
            
            if not files:
                return None
            
            if marker:
                marked = [f for f in files if marker in f.name]
                if marked:
                    return max(marked, key=lambda f: f.stat().st_mtime)
            
            # Fallback: Return the most recent file
            return max(files, key=lambda f: f.stat().st_mtime)
            
        except Exception:
            return None

    def download_media(self, request: DownloadRequest) -> Tuple[str, str]:
        # Validate requested extensions
        if request.media_type == "video":
            allowed = supported_video_exts()
            if request.extension and request.extension not in allowed:
                raise ValueError(f"Unsupported video extension '{request.extension}'. Allowed: {sorted(allowed)}")
        elif request.media_type == "audio":
            allowed = supported_audio_exts()
            if request.extension and request.extension not in allowed:
                raise ValueError(f"Unsupported audio extension '{request.extension}'. Allowed: {sorted(allowed)}")

        try:
            # Validate URL
            if not request.url or not request.url.strip():
                raise ValueError("URL cannot be empty")

            # Clean up old files before starting new download
            self._cleanup_old_files()

            # Build and execute command
            command, marker = self._build_ytdlp_command(request)

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=str(self.downloads_dir.parent)  # Set working directory
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                if "Unsupported URL" in error_msg:
                    raise ValueError(f"Unsupported media URL: {request.url}")
                elif "Private video" in error_msg:
                    raise ValueError("This video is private or requires authentication")
                elif "Video unavailable" in error_msg:
                    raise ValueError("Video is unavailable or has been removed")
                else:
                    raise ValueError(f"Download failed: {error_msg}")

            # Find the downloaded file
            downloaded_file = self._find_downloaded_file(marker)

            if not downloaded_file:
                raise ValueError("No file was downloaded")

            return str(downloaded_file), downloaded_file.name

        except subprocess.TimeoutExpired:
            raise ValueError("Download timed out after 5 minutes")
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Download error: {str(e)}")

    def _cleanup_old_files(self) -> None:
        """Remove files older than the cleanup interval from downloads dir"""
        try:
            now = time.time()
            for f in self.downloads_dir.iterdir():
                try:
                    if f.is_file():
                        age = now - f.stat().st_mtime
                        if age > self._cleanup_interval:
                            f.unlink(missing_ok=True)
                except Exception:
                    # Ignore errors for individual files
                    pass
        except Exception:
            # Ignore errors during cleanup sweep
            pass

    def get_file_path(self, filename: str) -> Optional[Path]:
        """
        Safely get file path for a given filename
        
        Args:
            filename: The filename to look for
            
        Returns:
            Path object if file exists and is safe, None otherwise
        """
        # Validate filename to prevent path traversal
        if not filename or '..' in filename or '/' in filename or '\\' in filename:
            return None
            
        file_path = self.downloads_dir / filename
        
        # Ensure the file is within our downloads directory
        try:
            file_path.resolve().relative_to(self.downloads_dir.resolve())
        except ValueError:
            return None
            
        if file_path.exists() and file_path.is_file():
            return file_path
            
        return None

    def cleanup_file(self, file_path: str, delay: int = 300) -> None:
        """
        Schedule file cleanup after a delay
        
        Args:
            file_path: Path to the file to clean up
            delay: Delay in seconds before cleanup (default 5 minutes)
        """
        import threading
        
        def delayed_cleanup():
            time.sleep(delay)
            try:
                path = Path(file_path)
                if path.exists():
                    path.unlink()
            except Exception:
                pass  # Ignore cleanup errors
                
        # Start cleanup in background thread
        cleanup_thread = threading.Thread(target=delayed_cleanup, daemon=True)
        cleanup_thread.start()

# Global instance
download_service = DownloadService()