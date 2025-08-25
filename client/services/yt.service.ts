import axiosInstance from "@/lib/axios";
import type { DownloadRequest, DownloadResponse, VideoInfo } from "@/types";

const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));

async function retry<T>(fn: () => Promise<T>, tries = 3, delayMs = 600) {
    let lastErr: unknown;
    for (let i = 0; i < tries; i++) {
        try {
            return await fn();
        } catch (e) {
            lastErr = e;
            if (i < tries - 1) await sleep(delayMs * (i + 1));
        }
    }
    throw lastErr;
}

export const ytService = {
    getMetaData: async (url: string): Promise<VideoInfo> =>
        retry(async () => {
            if (!url?.trim()) throw new Error("Please provide a valid URL");
            const res = await axiosInstance.get(`/info`, { params: { url } });
            if (!res.data) throw new Error("No metadata found");
            return res.data as VideoInfo;
        }),

    downloadWithProgress: async (
        req: DownloadRequest,
        onProgress?: (progress: number) => void,
        signal?: AbortSignal
    ): Promise<void> => {
        onProgress?.(10);

        const prep = await retry(async () => {
            const res = await axiosInstance.post<DownloadResponse>(`/download`, req, {
                signal,
            });
            if (!res.data?.download_url || !res.data?.filename) {
                throw new Error("Invalid download response");
            }
            return res.data;
        });

        onProgress?.(50);

        // Use absolute URL from server
        const fileResp = await retry(
            async () =>
                axiosInstance.get(prep.download_url, {
                    responseType: "blob",
                    onDownloadProgress: evt => {
                        if (evt.total) {
                            const p = 50 + (evt.loaded / evt.total) * 50;
                            onProgress?.(Math.min(100, Math.max(50, Math.round(p))));
                        }
                    },
                    signal,
                }),
            2,
            800
        );

        const ext = req.extension?.toLowerCase();
        const mime =
            req.media_type === "video"
                ? `video/${ext || "mp4"}`
                : req.media_type === "audio"
                ? `audio/${ext || "mp3"}`
                : `text/${ext || "plain"}`;

        const blob = new Blob([fileResp.data], { type: mime });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = prep.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);

        onProgress?.(100);
    },
};
