import { ThemeToggle } from "@/components/theme-toggle";
import { Download } from "lucide-react";

function Header() {
    return (
        <header className=" backdrop-blur-sm sticky top-0 z-50">
            <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                        <Download className="w-4 h-4 text-primary-foreground" />
                    </div>
                    <h1 className="text-xl font-serif font-bold">FetchLy</h1>
                </div>
                <ThemeToggle />
            </div>
        </header>
    )
}

export default Header;