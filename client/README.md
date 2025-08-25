# Fetchly Client

A modern, responsive web application for downloading videos and audio from various platforms.

## Features

-   🎥 Download videos in multiple formats and qualities (360p to 4K)
-   🎵 Extract audio in various formats (MP3, M4A, WAV, etc.)
-   ✂️ Smart trimming functionality
-   🌐 Support for multiple platforms (YouTube, Vimeo, TikTok, etc.)
-   🌙 Dark/Light theme support
-   📱 Fully responsive design
-   ⚡ Fast and optimized performance

## Tech Stack

-   **Framework**: Next.js 15 with React 19
-   **Styling**: Tailwind CSS v4
-   **UI Components**: Radix UI primitives
-   **Icons**: Lucide React
-   **HTTP Client**: Axios
-   **Fonts**: Google Fonts (Open Sans, Montserrat)
-   **Theme**: next-themes
-   **TypeScript**: Full type safety

## Getting Started

### Prerequisites

-   Node.js 18+
-   pnpm (recommended) or npm

### Installation

1. Clone the repository:

```bash
git clone https://github.com/HakimMohammed/fetchly.git
cd fetchly/client
```

2. Install dependencies:

```bash
pnpm install
```

3. Set up environment variables:

```bash
cp .env.example .env.local
```

4. Configure your environment variables in `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Fetchly
NEXT_PUBLIC_APP_VERSION=0.1.0
```

5. Start the development server:

```bash
pnpm dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

-   `pnpm dev` - Start development server
-   `pnpm build` - Build for production
-   `pnpm start` - Start production server
-   `pnpm lint` - Run ESLint
-   `pnpm lint:fix` - Run ESLint with auto-fix
-   `pnpm type-check` - Run TypeScript type checking
-   `pnpm clean` - Clean build artifacts

## Project Structure

```
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   └── ...               # Feature components
├── lib/                  # Utility libraries
│   ├── axios.ts          # HTTP client configuration
│   ├── constants.ts      # App constants
│   ├── error-handler.ts  # Error handling utilities
│   └── utils.ts          # Utility functions
├── services/             # API services
│   └── yt.service.ts     # Video service API
├── types/                # TypeScript type definitions
│   └── index.ts          # Global types
├── utils/                # Utility functions
│   └── index.ts          # Common utilities
└── public/               # Static assets
```

## Environment Variables

| Variable                   | Description         | Default                 |
| -------------------------- | ------------------- | ----------------------- |
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL     | `http://localhost:8000` |
| `NEXT_PUBLIC_APP_NAME`     | Application name    | `Fetchly`               |
| `NEXT_PUBLIC_APP_VERSION`  | Application version | `0.1.0`                 |

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@fetchly.app or create an issue on GitHub.
