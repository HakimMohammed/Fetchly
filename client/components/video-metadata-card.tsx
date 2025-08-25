"use client"

import { Badge } from "@/components/ui/badge"
import { CardContent } from "@/components/ui/card"
import type { VideoInfo } from "@/types"
import { Clock, Eye } from "lucide-react"

interface VideoMetadataCardProps {
  videoInfo: VideoInfo
}

export function VideoMetadataCard({ videoInfo }: VideoMetadataCardProps) {
  return (
    <div className="overflow-hidden transition-all duration-200 shadow-lg rounded-lg">
      <div className="relative">
        <img src={videoInfo.thumbnail || "/placeholder.svg"} alt={videoInfo.title} className="object-cover" />
        <Badge className="absolute bottom-2 right-2 bg-black/70 text-white hover:bg-black/70">
          <Clock className="w-3 h-3 mr-1" />
          {videoInfo.duration_string}
        </Badge>
      </div>
      <CardContent className="p-4">
        <h3 className="font-serif font-bold text-lg leading-tight mb-2 line-clamp-2">{videoInfo.title}</h3>
        {videoInfo.views && (
          <div className="flex items-center text-sm text-muted-foreground">
            <Eye className="w-3 h-3 mr-1" />
            {videoInfo.views} views
          </div>
        )}
      </CardContent>
    </div>
  )
}
