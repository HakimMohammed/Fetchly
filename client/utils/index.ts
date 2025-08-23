import { format, parse } from "date-fns";

const getFullTime = (totalSeconds: number) => {
    const date = new Date(totalSeconds * 1000);
    return format(date, "HH:mm:ss");
};

const parseTime = (time: string): Date => {
    const parts = time.split(":").length === 3 ? "HH:mm:ss" : "mm:ss";
    return parse(time, parts, new Date(0));
};

export const utils = {
    getFullTime,
    parseTime,
};
