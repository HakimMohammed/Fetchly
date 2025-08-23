"use client"

import { Progress } from "@/components/ui/progress"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, CheckCircle, AlertCircle } from "lucide-react"

interface ProgressIndicatorProps {
  status: "idle" | "processing" | "downloading" | "complete" | "error"
  progress?: number
  message?: string
}

export function ProgressIndicator({ status, progress = 0, message }: ProgressIndicatorProps) {
  if (status === "idle") return null

  const getStatusIcon = () => {
    switch (status) {
      case "processing":
      case "downloading":
        return <Loader2 className="w-5 h-5 animate-spin text-primary" />
      case "complete":
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case "error":
        return <AlertCircle className="w-5 h-5 text-destructive" />
      default:
        return null
    }
  }

  const getStatusMessage = () => {
    if (message) return message

    switch (status) {
      case "processing":
        return "Processing video..."
      case "downloading":
        return "Downloading..."
      case "complete":
        return "Download complete!"
      case "error":
        return "An error occurred"
      default:
        return ""
    }
  }

  return (
    <Card className="transition-all duration-200">
      <CardContent className="p-6">
        <div className="flex items-center gap-3 mb-4">
          {getStatusIcon()}
          <span className="font-medium">{getStatusMessage()}</span>
        </div>
        {(status === "processing" || status === "downloading") && <Progress value={progress} className="w-full" />}
      </CardContent>
    </Card>
  )
}
