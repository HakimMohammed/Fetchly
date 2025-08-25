interface VideoInfo {
    title: string;
    duration: number;
    duration_string: string;
    thumbnail: string;
    views?: number | null;
}

// New types for download functionality
interface DownloadRequest {
    url: string;
    media_type: "video" | "audio";
    extension?: string;
    quality?: string;
    language?: string;
    format?: string;
    start_time?: string;
    end_time?: string;
}

interface DownloadResponse {
    message: string;
    filename: string;
    download_url: string;
}

// Export all types
export type { DownloadRequest, DownloadResponse, VideoInfo };
