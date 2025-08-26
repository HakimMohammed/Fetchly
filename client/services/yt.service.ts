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

    download: async (
        req: DownloadRequest,
        signal?: AbortSignal
    ): Promise<void> => {

        const prep = await retry(async () => {
            const res = await axiosInstance.post<DownloadResponse>(`/download`, req, {
                signal,
            });
            if (!res.data?.download_url || !res.data?.filename) {
                throw new Error("Invalid download response");
            }
            return res.data;
        });

        // Use absolute URL from server
        const fileResp = await retry(
            async () =>
                axiosInstance.get(prep.download_url, {
                    responseType: "blob",
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
    },
};
