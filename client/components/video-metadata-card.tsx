"use client"

import { Badge } from "@/components/ui/badge"
import { CardContent } from "@/components/ui/card"
import { Clock, Eye } from "lucide-react"

interface VideoMetadataCardProps {
  metadata: MetaData
}

export function VideoMetadataCard({ metadata }: VideoMetadataCardProps) {
  return (
    <div className="overflow-hidden transition-all duration-200 shadow-lg rounded-lg">
      <div className="relative">
        <img src={metadata.thumbnail || "/placeholder.svg"} alt={metadata.title} className="object-cover" />
        <Badge className="absolute bottom-2 right-2 bg-black/70 text-white hover:bg-black/70">
          <Clock className="w-3 h-3 mr-1" />
          {metadata.duration_string}
        </Badge>
      </div>
      <CardContent className="p-4">
        <h3 className="font-serif font-bold text-lg leading-tight mb-2 line-clamp-2">{metadata.title}</h3>
        <p className="text-sm text-muted-foreground mb-1">{metadata.channel}</p>
        {metadata.views && (
          <div className="flex items-center text-sm text-muted-foreground">
            <Eye className="w-3 h-3 mr-1" />
            {metadata.views} views
          </div>
        )}
      </CardContent>
    </div>
  )
}
