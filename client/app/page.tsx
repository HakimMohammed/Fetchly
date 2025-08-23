"use client"

import { DownloadOptions } from "@/components/download-options"
import Footer from "@/components/footer"
import Header from "@/components/header"
import { ProgressIndicator } from "@/components/progress-indicator"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { VideoMetadataCard } from "@/components/video-metadata-card"
import { ytService } from "@/services/yt.service"
import { utils } from "@/utils"
import { Download, Link, Sparkles } from "lucide-react"
import { useState } from "react"

export default function VideoDownloader() {
  const [url, setUrl] = useState("")
  const [metadata, setMetadata] = useState<MetaData | null>(null)
  const [videos, setVideos] = useState<Stream[]>([])
  const [audios, setAudios] = useState<Stream[]>([])
  const [subtitles, setSubtitles] = useState<Subtitle[]>([])
  const [status, setStatus] = useState<"idle" | "processing" | "downloading" | "complete" | "error">("idle")
  const [progress, setProgress] = useState(0)

  const handleProcess = async () => {
    if (!url.trim()) return

    setStatus("processing")
    setProgress(0)

    const metaData: MetaData = await ytService.getMetaData(url)
    setMetadata(metaData)
    setVideos(metaData.streams.video)
    setAudios(metaData.streams.audio)
    setSubtitles(metaData.subtitles)

    setStatus("idle")

    // Simulate processing with progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)
  }

  const handleDownload = (type: string, options: any) => {
    setStatus("downloading")
    setProgress(0)

    // Simulate download progress
    const downloadInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(downloadInterval)
          setStatus("complete")
          setTimeout(() => setStatus("idle"), 3000)
          return 100
        }
        return prev + 5
      })
    }, 100)

    console.log(`Downloading ${type} with options:`, options)
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container my-48 mx-auto px-4 py-8 max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium mb-4">
            <Sparkles className="w-4 h-4" />
            Modern Video Downloader
          </div>
          <h2 className="text-4xl md:text-5xl font-serif font-black mb-4 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
            Download Videos, Audio & Subtitles
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Paste any video URL and download in your preferred format and quality. Support for trimming, multiple
            formats, and subtitle extraction.
          </p>
        </div>

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
              disabled={!url.trim() || status === "processing"}
              className="px-6 font-medium cursor-pointer"
            >
              {status === "processing" ? "Processing..." : "Process"}
            </Button>
          </div>
          <p className="text-sm text-muted-foreground text-center">
            Paste any video URL above and click Process to get started. Our system will analyze and prepare your video.
          </p>
        </div>

        {/* Progress Indicator */}
        <ProgressIndicator status={status} progress={progress} />

        {/* Video Metadata */}
        {metadata && (
          <div className="mb-8">
            <h3 className="text-2xl font-serif font-bold mb-4">Video Information</h3>
            <VideoMetadataCard metadata={metadata} />
          </div>
        )}

        {/* Download Options */}
        {metadata && (
          <div className="mb-8">
            <h3 className="text-2xl font-serif font-bold mb-4">Download Options</h3>
            <DownloadOptions duration={metadata.duration} subtitles={subtitles} url={url} videos={videos} audios={audios} />
          </div>
        )}

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-6 mt-16">
          <Card className="text-center p-6 transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Download className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-serif font-bold text-lg mb-2">Multiple Formats</h3>
            <p className="text-muted-foreground text-sm">
              Download videos in various qualities from 360p to 4K, audio in MP3/M4A/WAV, and subtitles in SRT/VTT
              formats.
            </p>
          </Card>

          <Card className="text-center p-6 transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-serif font-bold text-lg mb-2">Smart Trimming</h3>
            <p className="text-muted-foreground text-sm">
              Extract specific portions of videos or audio by setting custom start and end times with precision.
            </p>
          </Card>

          <Card className="text-center p-6 transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Link className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-serif font-bold text-lg mb-2">Universal Support</h3>
            <p className="text-muted-foreground text-sm">
              Works with YouTube, Vimeo, TikTok, Instagram, Twitter, and hundreds of other video platforms.
            </p>
          </Card>
        </div>
      </main>

      <Footer />
    </div>
  )
}
