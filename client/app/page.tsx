"use client"

import { DownloadOptions } from "@/components/download-options"
import Features from "@/components/feature-section"
import Footer from "@/components/footer"
import Header from "@/components/header"
import HeroSection from "@/components/hero-section"
import LoadingCard from "@/components/loading-card"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Toaster } from "@/components/ui/toaster"
import { VideoMetadataCard } from "@/components/video-metadata-card"
import { Status } from "@/enums"
import { handleError } from "@/lib/error-handler"
import { ytService } from "@/services/yt.service"
import type { VideoInfo } from "@/types"
import { utils } from "@/utils"
import { Download, Link, Sparkles } from "lucide-react"
import { useState } from "react"

export default function VideoDownloader() {

  const [url, setUrl] = useState("")
  const [mediaInfo, setMediaInfo] = useState<VideoInfo | null>(null)
  const [status, setStatus] = useState<Status>(Status.Idle)

  const handleProcess = async () => {
    if (!url.trim()) return
    setStatus(Status.Processing)

    try {
      const videoInfo: VideoInfo = await ytService.getMetaData(url)
      setMediaInfo(videoInfo)
      
      setStatus(Status.Idle)
    } catch (error) {
      handleError(error, "Failed to process video URL")
      setStatus(Status.Error)
    }
  }

  const isValidUrl = (urlString: string): boolean => {
    return utils.isValidUrl(urlString);
  }

  return (
    <div className="min-h-screen bg-background">
      {
        status === Status.Processing && <LoadingCard text="Processing URL ..." className="z-50" />
      }
      <Header />
      <main className="container my-48 mx-auto px-4 py-8 max-w-6xl">

        {/* Hero Section */}
        <HeroSection />

        <div className="flex flex-col gap-4 mb-8">
          <div className="flex items-center gap-2 font-serif">
            <span className="flex gap-1 font-bold">
              <Link className="w-5 h-5 text-primary" />
              Enter Video URL
            </span>
            <Input
              placeholder="https://youtube.com/watch?v=... or any video URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 border-ring"
              onKeyDown={(e) => e.key === "Enter" && handleProcess()}
            />
            <Button
              onClick={handleProcess}
              disabled={!url.trim() || !isValidUrl(url) || status === "processing"}
              className="px-6 font-medium cursor-pointer"
            >
              {status === "processing" ? "Processing..." : "Process"}
            </Button>
          </div>
          <p className="text-sm text-muted-foreground text-center">
            Paste any video URL above and click Process to get started. Our system will analyze and prepare your video.
          </p>
        </div>

        {/* Video Metadata */}
        {mediaInfo && (
          <div className="mb-8">
            <h3 className="text-2xl font-serif font-bold mb-4">Video Information</h3>
            <VideoMetadataCard videoInfo={mediaInfo} />
          </div>
        )}

        {/* Download Options */}
        {mediaInfo && (
          <div className="mb-8">
            <h3 className="text-2xl font-serif font-bold mb-4">Download Options</h3>
            <DownloadOptions
              duration={mediaInfo.duration}
              url={url}
            />
          </div>
        )}
        <Features />
      </main>

      <Footer />
      <Toaster />
    </div>
  )
}