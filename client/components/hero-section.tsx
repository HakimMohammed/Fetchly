import { Sparkles } from "lucide-react"

export default function HeroSection() {
    return (
        <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium mb-4">
                <Sparkles className="w-4 h-4" />
                Modern Video Downloader
            </div>
            <h2 className="text-4xl md:text-5xl font-serif font-black mb-4 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
                Download Videos or Audio
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Paste any video URL and download in your preferred format and quality. Supports trimming and popular
                formats.
            </p>
        </div>
    )
}