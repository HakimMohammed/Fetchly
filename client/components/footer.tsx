import Link from "next/link";

function Footer() {
    return (
        <>
            {/* Spacer to prevent content from being covered by the fixed footer */}
            <div aria-hidden className="h-16" />
            <footer className="fixed inset-x-0 bottom-0 border-t bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60 py-4">
                <div className="container mx-auto px-4 text-center text-muted-foreground">
                    <p>
                        &copy; 2025 FetchLy. Built By {" "}
                        <Link href="https://github.com/HakimMohammed" className="underline underline-offset-4">
                            Me
                        </Link>
                        .
                    </p>
                </div>
            </footer>
        </>
    )
}

export default Footer;