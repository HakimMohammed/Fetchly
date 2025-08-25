#!/usr/bin/env python3
"""
Simple test script for the download service
"""

from models import DownloadRequest
from download_service import DownloadService

def test_download_request_validation():
    """Test download request validation"""
    print("Testing DownloadRequest validation...")
    
    # Valid video request
    try:
        request = DownloadRequest(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            media_type="video",
            extension="mp4",
            quality="720p"
        )
        print("✓ Valid video request created successfully")
    except Exception as e:
        print(f"✗ Video request failed: {e}")
    
    # Valid audio request
    try:
        request = DownloadRequest(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            media_type="audio",
            extension="mp3",
            quality="128k"
        )
        print("✓ Valid audio request created successfully")
    except Exception as e:
        print(f"✗ Audio request failed: {e}")
    
    # Invalid quality format
    try:
        request = DownloadRequest(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            media_type="video",
            extension="mp4",
            quality="720"  # Missing 'p'
        )
        print("✗ Should have failed for invalid quality format")
    except Exception as e:
        print(f"✓ Correctly rejected invalid quality: {e}")
    
    # Invalid extension (non-alphanumeric)
    try:
        request = DownloadRequest(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            media_type="audio",
            extension="m*p3",  # Invalid characters
            quality="128k"
        )
        print("✗ Should have failed for invalid extension")
    except Exception as e:
        print(f"✓ Correctly rejected invalid extension: {e}")

def test_download_service():
    """Test download service functionality"""
    print("\nTesting DownloadService...")
    
    service = DownloadService()
    print(f"✓ Download service created with directory: {service.downloads_dir}")
    
    # Test path validation
    safe_file = service.get_file_path("test.mp4")
    if safe_file is None:
        print("✓ Correctly rejected non-existent file")
    
    unsafe_file = service.get_file_path("../../../etc/passwd")
    if unsafe_file is None:
        print("✓ Correctly rejected path traversal attempt")
    
    unsafe_file2 = service.get_file_path("test/../../secret.txt")
    if unsafe_file2 is None:
        print("✓ Correctly rejected another path traversal attempt")

def test_command_building():
    """Test yt-dlp command building"""
    print("\nTesting command building...")
    
    service = DownloadService()
    
    # Video request
    video_request = DownloadRequest(
        url="https://www.youtube.com/watch?v=test",
        media_type="video",
        extension="mp4",
        quality="720p"
    )
    
    cmd, mark = service._build_ytdlp_command(video_request)
    print(f"Video command: {' '.join(cmd)} | marker={mark}")
    
    # Audio request
    audio_request = DownloadRequest(
        url="https://www.youtube.com/watch?v=test",
        media_type="audio",
        extension="mp3",
        quality="128k"
    )
    
    cmd, mark = service._build_ytdlp_command(audio_request)
    print(f"Audio command: {' '.join(cmd)} | marker={mark}")
    


if __name__ == "__main__":
    print("=== Download Service Tests ===")
    test_download_request_validation()
    test_download_service()
    test_command_building()
    print("\n=== Tests completed ===")
