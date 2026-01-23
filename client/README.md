# ASTU Route AI - Next.js Version

This is the Next.js version of ASTU Route AI, an intelligent campus navigation system for Adama Science and Technology University.

## Features

- 🗺️ Interactive Campus Map with real-time navigation
- 🤖 AI-powered Assistant for campus information
- 📍 Location Search and Directory
- 🎨 Modern, responsive design with Tailwind CSS
- ⚡ Built with Next.js 15 and React 19

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Install dependencies:

```bash
npm install
```

2. Set up environment variables:

Create a `.env.local` file in the root directory and add your Gemini API key:

```
NEXT_PUBLIC_GEMINI_API_KEY=your_api_key_here
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
client-next/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── Navbar.tsx
│   ├── Hero.tsx
│   ├── MapDisplay.tsx
│   ├── MapWrapper.tsx
│   ├── AIAssistant.tsx
│   └── Footer.tsx
├── services/              # API services
│   └── geminiService.ts
├── constants.tsx          # Campus data
├── types.ts              # TypeScript types
├── next.config.ts        # Next.js configuration
├── tailwind.config.ts    # Tailwind CSS configuration
└── tsconfig.json         # TypeScript configuration
```

## Key Technologies

- **Next.js 15**: React framework with App Router
- **React 19**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Leaflet & React-Leaflet**: Interactive maps
- **Google Generative AI**: AI assistant
- **Lucide React**: Icon library

## Environment Variables

- `NEXT_PUBLIC_GEMINI_API_KEY`: Your Google Gemini API key for the AI assistant

## Features Overview

### Home Page
- Hero section with search functionality
- Quick navigation to different sections

### Campus Map
- Interactive map powered by Leaflet
- Location markers with categories
- Filter by facility type
- Route visualization

### AI Assistant
- Chat interface for campus information
- Powered by Google Gemini AI
- Contextual responses about campus facilities

### Directory
- Complete listing of all campus facilities
- Searchable and categorized
- Click to view on map

## License

This project is part of the ASTU Route AI initiative.
