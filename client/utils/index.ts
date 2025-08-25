import { format, parse } from "date-fns";

/**
 * Converts seconds to HH:MM:SS format
 */
const getFullTime = (totalSeconds: number): string => {
    const date = new Date(totalSeconds * 1000);
    return format(date, "HH:mm:ss");
};

/**
 * Parses time string (HH:MM:SS or MM:SS) to Date object
 */
const parseTime = (time: string): Date => {
    const parts = time.split(":").length === 3 ? "HH:mm:ss" : "mm:ss";
    return parse(time, parts, new Date(0));
};

/**
 * Validates if a string is a valid URL
 */
const isValidUrl = (urlString: string): boolean => {
    try {
        new URL(urlString);
        return true;
    } catch {
        return false;
    }
};

/**
 * Formats file size in bytes to human readable format
 */
const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";

    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

/**
 * Formats duration in seconds to human readable format
 */
const formatDuration = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, "0")}:${remainingSeconds.toString().padStart(2, "0")}`;
    }
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
};

/**
 * Debounce function to limit the rate of function execution
 */
const debounce = <T extends (...args: any[]) => any>(func: T, wait: number): ((...args: Parameters<T>) => void) => {
    let timeout: NodeJS.Timeout;
    return (...args: Parameters<T>) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
};

export const utils = {
    getFullTime,
    parseTime,
    isValidUrl,
    formatFileSize,
    formatDuration,
    debounce,
};
