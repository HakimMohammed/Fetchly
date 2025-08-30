"""
Centralized yt-dlp configuration and helpers.

Provides:
- ydl_options(): default YoutubeDL options dict
- extract_info(url): convenience wrapper to fetch info via yt_dlp API
- cli_base_args(): common CLI flags for subprocess calls (downloads)

This ensures a single place to manage cookies, user-agent, and TLS options.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yt_dlp


# Default desktop UA helps some providers return better streams
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)


def _cookies_path_if_present() -> Optional[str]:
    """Return absolute cookies.txt path if it exists and has any entries."""
    try:
        cookies_path = Path(__file__).parent / "cookies.txt"
        if not (cookies_path.exists() and cookies_path.is_file()):
            return None
        try:
            lines = cookies_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            lines = []
        has_entries = any(line.strip() and not line.lstrip().startswith('#') for line in lines)
        return str(cookies_path.resolve()) if has_entries else None
    except Exception:
        return None


def ydl_options(
    *,
    skip_download: bool = True,
    extract_flat: bool = True,
    fmt: str = "best",
    user_agent: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build default yt_dlp options used across the server.

    Args:
        skip_download: Do not download media, just extract info
        extract_flat: Extract without resolving all formats/playlists
        fmt: Preferred format expression when relevant
        user_agent: Override default UA
        extra: Additional options to merge/override
    """
    ua = user_agent or DEFAULT_USER_AGENT
    opts: Dict[str, Any] = {
        "quiet": True,
        "skip_download": skip_download,
        "format": fmt,
        "extract_flat": extract_flat,
        "nocheckcertificate": True,
        "user_agent": ua,
    }

    ck = _cookies_path_if_present()
    if ck:
        opts["cookiefile"] = ck

    if extra:
        opts.update(extra)

    return opts


def extract_info(url: str, *, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Extract media info using yt_dlp Python API with shared options.

    Raises yt_dlp.utils.DownloadError or other exceptions with provider messages
    that callers can map to API errors.
    """
    opts = options or ydl_options()
    with yt_dlp.YoutubeDL(opts) as ydl:
        # download=False ensures info only even if skip_download=False
        return ydl.extract_info(url, download=False)


def cli_base_args(*, user_agent: Optional[str] = None) -> list[str]:
    """Common CLI args mirroring ydl_options for subprocess usage.

    Includes certificate handling, UA, and cookies when available.
    """
    args: list[str] = ["--no-check-certificate"]

    ua = user_agent or DEFAULT_USER_AGENT
    if ua:
        args.extend(["--user-agent", ua])

    ck = _cookies_path_if_present()
    if ck:
        args.extend(["--cookies", ck])

    return args
