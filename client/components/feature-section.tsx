import {Card} from "@/components/ui/card"
import { Download, Link, Sparkles } from "lucide-react"

export default function Features() {
    return (
        <div className="grid md:grid-cols-3 gap-6 mt-16">
          <Card className="text-center p-6 transition-all duration-200 hover:shadow-lg hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Download className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-serif font-bold text-lg mb-2">Multiple Formats</h3>
            <p className="text-muted-foreground text-sm">
              Download videos in various qualities from 360p to 4K, audio in MP3/M4A/WAV.
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
    )
}