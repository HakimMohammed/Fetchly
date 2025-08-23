import Link from "next/link";

function Footer() {
    return (
        <footer className="absolute inset-x-0 bottom-0 border-t py-4 mt-4">
            <div className="container mx-auto px-4 text-center text-muted-foreground">
                <p>&copy; 2025 FetchLy. Built By <Link href="https://github.com/HakimMohammed">Me</Link>.</p>
            </div>
        </footer>
    )
}

export default Footer;