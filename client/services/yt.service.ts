import axiosInstance from "@/lib/axios";

export const ytService = {
    getMetaData: async (url: string) => {
        const response = await axiosInstance.get(`/metadata?url=${encodeURIComponent(url)}`);
        return response.data;
    },

    downloadVideo: async (url: string, start: string, end: string, ext: string, quality: string) => {
        try {
            const response = await axiosInstance.get(
                `/download/video?url=${encodeURIComponent(
                    url
                )}&start=${start}&end=${end}&ext=${ext}&quality=${encodeURIComponent(quality)}`,
                { responseType: "blob" }
            );

            const blob = new Blob([response.data], { type: `video/${ext}` });
            const link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = `video.${ext}`;
            link.click();
            window.URL.revokeObjectURL(link.href);
        } catch (error) {
            console.error("Download failed:", error);
        }
    },

    downloadAudio: async (url: string, start: string, end: string, ext: string, quality: string) => {
        try {
            const response = await axiosInstance.get(
                `/download/audio?url=${encodeURIComponent(url)}&start=${start}&end=${end}&ext=${ext}&quality=${encodeURIComponent(quality)}`,
                { responseType: "blob" }
            );
            const blob = new Blob([response.data], { type: `audio/${ext}` });
            const link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = `audio.${ext}`;
            link.click();
            window.URL.revokeObjectURL(link.href);
        } catch (error) {
            console.error("Download failed:", error);
        }
    },

    downloadSubtitles: async (url: string, lang: string, format: string) => {
        try {
            const response = await axiosInstance.get(
                `/download/subtitles?url=${encodeURIComponent(url)}&lang=${lang}&format=${format}`,
                { responseType: "blob" }
            );
            const blob = new Blob([response.data], { type: `text/${format}` });
            const link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = `subtitles.${format}`;
            link.click();
            window.URL.revokeObjectURL(link.href);
        } catch (error) {
            console.error("Download failed:", error);
        }
    },
};
