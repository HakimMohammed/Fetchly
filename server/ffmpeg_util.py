import subprocess
from functools import lru_cache

DEFAULT_VIDEO = {"mp4", "webm", "mkv"}
DEFAULT_AUDIO = {"mp3", "m4a", "opus", "wav"}
DEFAULT_SUBS: set[str] = set()

def _run_cmd(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="ignore")
    except Exception:
        return ""

@lru_cache(maxsize=1)
def probe_ffmpeg() -> dict[str, set[str]]:
    muxers_raw = _run_cmd(["ffmpeg", "-hide_banner", "-muxers"])
    encoders_raw = _run_cmd(["ffmpeg", "-hide_banner", "-encoders"])

    # Start with safe defaults
    video_exts = set(DEFAULT_VIDEO)
    audio_exts = set(DEFAULT_AUDIO)
    sub_exts = set(DEFAULT_SUBS)

    # Muxers availability
    has_mp4_mux = " E mov," in muxers_raw or " E mp4" in muxers_raw or "mov,mp4,m4a" in muxers_raw
    has_webm_mux = " E webm" in muxers_raw
    has_mkv_mux = " E matroska" in muxers_raw
    has_mp3_mux = " E mp3" in muxers_raw  # often included under muxers/encoders

    # Encoders availability
    has_aac = "aac " in encoders_raw
    has_libmp3 = "libmp3lame" in encoders_raw
    has_libopus = "libopus" in encoders_raw
    has_pcm = "pcm_s16le" in encoders_raw or "pcm_f32le" in encoders_raw

    # Video outputs depend on muxers
    if not has_mp4_mux:
        video_exts.discard("mp4")
        audio_exts.discard("m4a")
    if not has_webm_mux:
        video_exts.discard("webm")
    if not has_mkv_mux:
        video_exts.discard("mkv")

    # Audio outputs depend on encoders/muxers
    if not has_libmp3 or not has_mp3_mux:
        audio_exts.discard("mp3")
    if not has_aac or not has_mp4_mux:
        audio_exts.discard("m4a")
    if not has_libopus:
        audio_exts.discard("opus")
    if not has_pcm:
        audio_exts.discard("wav")

    # Subtitles removed from public API; keep empty set for internal consistency

    return {
        "video": video_exts,
        "audio": audio_exts,
    "subs": sub_exts,
    }

def supported_video_exts() -> set[str]:
    return probe_ffmpeg()["video"]

def supported_audio_exts() -> set[str]:
    return probe_ffmpeg()["audio"]

def supported_sub_exts() -> set[str]:
    return set()