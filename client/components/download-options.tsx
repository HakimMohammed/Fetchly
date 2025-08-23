"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ytService } from "@/services/yt.service"
import { utils } from "@/utils"
import { isBefore } from "date-fns"
import { Clock, Download, FileText, Video } from "lucide-react"
import { useEffect, useState } from "react"

interface DownloadOptionsProps {
  url: string,
  videos: Stream[],
  audios: Stream[],
  subtitles: Subtitle[],
  duration: number
}

function isValidTimeRange(startTime: string, endTime: string, duration: string): boolean {
  const start = utils.parseTime(startTime);
  const end = utils.parseTime(endTime);
  const max = utils.parseTime(duration);

  return isBefore(start, end) && isBefore(end, max);
}

export function DownloadOptions({ videos, audios, duration, url, subtitles }: DownloadOptionsProps) {


  const [isDownloading, setIsDownloading] = useState(false);

  // Video Section
  const [videoQuality, setVideoQuality] = useState("");
  const [videoExt, setVideoExt] = useState("mp4");

  const uniqueVideoExtensions = [...new Set(videos.map(video => video.Extension))];
  const uniqueQualities = [...new Set(videos.filter(v => v.Extension === videoExt).map(v => v.Quality))];

  const handleDownloadVideo = async () => {
    console.log('====================================');
    console.log({
      startTime,
      endTime,
      videoExt,
      videoQuality
    });
    console.log('====================================');
    if (!isValidTimeRange(startTime, endTime, utils.getFullTime(duration))) {
      alert("Invalid time range. Please ensure start time is before end time and within video duration.");
      return;
    }
    setIsDownloading(true);
    await ytService.downloadVideo(
      url,
      startTime,
      endTime,
      videoExt,
      videoQuality
    );
    setIsDownloading(false);
  };

  const [audioQuality, setAudioQuality] = useState("");
  const [audioExt, setAudioExt] = useState("mp3");

  const uniqueAudioExtensions = [...new Set(audios.map(audio => audio.Extension))];
  const uniqueAudioQualities = [...new Set(audios.filter(a => a.Extension === audioExt).map(a => a.Quality))];

  const handleDownloadAudio = async () => {
    if (!isValidTimeRange(startTime, endTime, utils.getFullTime(duration))) {
      alert("Invalid time range. Please ensure start time is before end time and within audio duration.");
      return;
    }
    setIsDownloading(true);
    await ytService.downloadAudio(
      url,
      startTime,
      endTime,
      audioExt,
      audioQuality
    );
    setIsDownloading(false);
  };

  const [subtitleLang, setSubtitleLang] = useState("en");
  const [subtitleFormat, setSubtitleFormat] = useState("srt");

  function handleSubtitleDownload(url: string, lang: string, ext: string) {
    fetch(url)
      .then(res => res.blob())
      .then(blob => {
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = `${lang}.${ext}`;
        link.click();
        window.URL.revokeObjectURL(link.href);
      });
  }

  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState(utils.getFullTime(duration));

  useEffect(()=> {
    console.log('====================================');
    console.log(subtitles);
    console.log('====================================');
  },[])



  return (
    <div className="grid gap-6 md:grid-cols-3">
      {/* Video Download */}
      <Card className="transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 font-serif">
            <Video className="w-5 h-5 text-primary" />
            Download Video
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-2">
            <div className="flex flex-col gap-2">
              <Label htmlFor="video-ext" className="font-bold">Extension</Label>
              <Select value={videoExt} onValueChange={setVideoExt}>
                <SelectTrigger className="bg-background">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {uniqueVideoExtensions.map((ext) => (
                    <SelectItem key={ext} value={ext}>
                      {ext}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="video-quality" className="font-bold">Quality</Label>
              <Select value={videoQuality} onValueChange={setVideoQuality}>
                <SelectTrigger className="bg-background">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {uniqueQualities.map((quality) => (
                    <SelectItem key={quality} value={quality}>
                      {quality}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <Button onClick={handleDownloadVideo} disabled={isDownloading} className="w-full font-medium">
            <Download className="w-4 h-4 mr-2" />
            Download Video
          </Button>
        </CardContent>
      </Card>

      {/* Audio Download */}
      <Card className="transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 font-serif">
            <Video className="w-5 h-5 text-primary" />
            Download Audio
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-2">
            <div className="flex flex-col gap-2">
              <Label htmlFor="audio-ext" className="font-bold">Extension</Label>
              <Select value={audioExt} onValueChange={setAudioExt}>
                <SelectTrigger className="bg-background">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {uniqueAudioExtensions.map((ext) => (
                    <SelectItem key={ext} value={ext}>
                      {ext}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="video-quality" className="font-bold">Quality</Label>
              <Select value={audioQuality} onValueChange={setAudioQuality}>
                <SelectTrigger className="bg-background">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {uniqueAudioQualities.map((quality) => (
                    <SelectItem key={quality} value={quality}>
                      {quality}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <Button onClick={handleDownloadAudio} disabled={isDownloading} className="w-full font-medium">
            <Download className="w-4 h-4 mr-2" />
            Download Audio
          </Button>
        </CardContent>
      </Card>

      {/* Subtitles Download */}
      <Card className="transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 font-serif">
            <FileText className="w-5 h-5 text-primary" />
            Download Subtitles
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4>Available Subtitles</h4>
            {/* <ul>
              {subtitles.map((sub, idx) => (
                <li key={idx}>
                  Language: {sub.lang}, Extension: {sub.ext}
                  <button onClick={() => handleSubtitleDownload(sub.url, sub.lang, sub.ext)}>
                    Download
                  </button>
                </li>
              ))}
            </ul> */}
          </div>
          {/* <Button onClick={() => handleDownload("subtitles")} disabled={isDownloading} className="w-full font-medium">
            <Download className="w-4 h-4 mr-2" />
            Download Subtitles
          </Button> */}
        </CardContent>
      </Card>

      {/* Time Trimming Section */}
      <Card className="md:col-span-3 transition-all duration-200 hover:shadow-lg">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 font-serif">
            <Clock className="w-5 h-5 text-primary" />
            Trim Video/Audio (Optional)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-2">
              <Label htmlFor="start-time">Start Time (HH:MM:SS)</Label>
              <Input
                className="bg-background"
                id="start-time"
                placeholder="00:00:00"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                pattern="[0-9]{2}:[0-9]{2}:[0-9]{2}"
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="end-time">End Time (HH:MM:SS)</Label>
              <Input
                className="bg-background"
                id="end-time"
                placeholder="00:05:30"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                pattern="[0-9]{2}:[0-9]{2}:[0-9]{2}"
              />
            </div>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Leave empty to download the full video/audio. Format: HH:MM:SS (e.g., 01:30:45)
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
