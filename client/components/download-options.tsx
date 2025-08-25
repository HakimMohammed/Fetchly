"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ytService } from "@/services/yt.service"
import type { DownloadRequest } from "@/types"
import { utils } from "@/utils"
import { Clock, Download } from "lucide-react"
import { useEffect, useState } from "react"

interface DownloadOptionsProps {
  url: string,
  duration: number
}

function isValidTimeRange(startTime: string, endTime: string, duration: string): boolean {
  const isHMS = (v: string) => /^\d{2}:\d{2}:\d{2}$/.test(v);
  const s = isHMS(startTime) ? startTime : "00:00:00";
  const e = isHMS(endTime) ? endTime : duration;
  const start = utils.parseTime(s);
  const end = utils.parseTime(e);
  const max = utils.parseTime(duration);
  return start < end && end <= max;
}

export function DownloadOptions({ duration, url }: DownloadOptionsProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [mediaType, setMediaType] = useState<"video" | "audio">("video");

  // Time trimming
  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState(utils.getFullTime(duration));

  // Precompute range validity for disabling buttons
  const fullDur = utils.getFullTime(duration);
  const isRangeValid = isValidTimeRange(startTime, endTime, fullDur);

  useEffect(() => {
    // no-op: defaults are set above
  }, []);

  const handleDownload = async () => {
    const fullDur = utils.getFullTime(duration);
    if (!isValidTimeRange(startTime, endTime, fullDur)) {
      alert("Invalid time range.");
      return;
    }
    setIsDownloading(true);
    setDownloadProgress(0);
    try {
      const downloadRequest: DownloadRequest = {
        url,
        media_type: mediaType,
        start_time: startTime !== "00:00:00" ? startTime : undefined,
        end_time: endTime !== fullDur ? endTime : undefined
      };
      await ytService.downloadWithProgress(downloadRequest, setDownloadProgress);
    } finally {
      setIsDownloading(false);
      setDownloadProgress(0);
    }
  };

  return (
    <div className="grid gap-6 md:grid-cols-1">
      {/* Simple selection: media type + time range */}
      <Card className="transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 font-serif">
            Quick Download
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-2">
            <div className="flex flex-col gap-2">
              <Label className="font-bold">Type</Label>
              <Select value={mediaType} onValueChange={(v) => setMediaType(v as any)}>
                <SelectTrigger className="bg-background">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="video">Video</SelectItem>
                  <SelectItem value="audio">Audio</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          {isDownloading && (
            <div className="space-y-2">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-primary h-2 rounded-full transition-all duration-300" style={{ width: `${downloadProgress}%` }} />
              </div>
              <p className="text-sm text-center">{downloadProgress}%</p>
            </div>
          )}
          <Button
            onClick={handleDownload}
            disabled={isDownloading || !isRangeValid}
            className="w-full font-medium"
          >
            <Download className="w-4 h-4 mr-2" />
            {isDownloading ? "Downloading..." : "Download"}
          </Button>
        </CardContent>
      </Card>

      {/* Time Trimming Section */}
      <Card className="transition-all duration-200 hover:shadow-lg">
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