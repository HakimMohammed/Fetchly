"use client"
import { ytService } from "@/services/yt.service"
import type { DownloadRequest } from "@/types"
import { utils } from "@/utils"
import { Clock, Download } from "lucide-react"
import { useEffect, useState } from "react"
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {Label} from "@/components/ui/label"
import {Select, SelectTrigger, SelectValue, SelectContent, SelectItem} from "@/components/ui/select"
import {Button} from "@/components/ui/button"
import LoadingCard from "./loading-card"
import {Input} from "@/components/ui/input"

interface DownloadOptionsProps {
  url: string,
  duration: number
}

export function DownloadOptions({ duration, url }: DownloadOptionsProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [mediaType, setMediaType] = useState<"video" | "audio">("video");

  // Time trimming
  const [startTime, setStartTime] = useState("00:00:00");
  const [endTime, setEndTime] = useState(utils.getFullTime(duration));

  // Precompute range validity for disabling buttons
  const fullDur = utils.getFullTime(duration);
  const isRangeValid = utils.isValidTimeRange(startTime, endTime, fullDur);

  useEffect(() => {
    // no-op: defaults are set above
  }, []);

  const handleDownload = async () => {
    const fullDur = utils.getFullTime(duration);
    if (!utils.isValidTimeRange(startTime, endTime, fullDur)) {
      alert("Invalid time range.");
      return;
    }
    setIsDownloading(true);
    try {
      const downloadRequest: DownloadRequest = {
        url,
        media_type: mediaType,
        start_time: startTime !== "00:00:00" ? startTime : undefined,
        end_time: endTime !== fullDur ? endTime : undefined
      };
      await ytService.download(downloadRequest);
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="grid gap-6 md:grid-cols-1">
      {/* Simple selection: media type + time range */}
      <Card className="transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex flex-col gap-4">
              <Label className="">Media Type</Label>
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
            <div className="flex flex-col gap-4">
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
            <div className="flex flex-col gap-4">
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
          
          {isDownloading && <LoadingCard text={`Downloading ${mediaType}...`} />}
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

      
    </div>
  )
}