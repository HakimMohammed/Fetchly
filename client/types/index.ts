type MetaData = {
    id: string;
    title: string;
    thumbnail: string;
    views: number;
    channel: string;
    duration_string: string;
    duration: number;
    streams: {
        video: Stream[];
        audio: Stream[];
    };
    subtitles: Subtitle[];
};

type Stream = {
    Extension: string;
    Quality: string;
    URL: string;
};

type Subtitle = {
    lang: string;
    ext: string;
    url: string;
};
