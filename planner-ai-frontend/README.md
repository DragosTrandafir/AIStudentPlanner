# Planner AI Frontend

A modern Next.js application for AI-powered student planning and task management.

## Overview

This frontend application provides an intuitive calendar interface for students to manage their academic tasks, subjects, and exams. It integrates with an AI backend to generate optimized study plans and reschedule tasks based on user feedback.

## Features

- **📅 Interactive Calendar**: Month, week, and day views with FullCalendar integration
- **🤖 AI-Powered Planning**: Generate study plans using advanced AI algorithms
- **📝 Task Management**: Create and manage assignments, projects, and exams
- **🔄 Smart Rescheduling**: Adjust plans based on user feedback and progress
- **🌙 Dark/Light Themes**: Customizable interface with theme persistence
- **📱 Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **🔐 Secure Authentication**: JWT-based user authentication and session management

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS v4 with custom CSS variables
- **UI Components**: Headless UI, Heroicons, Lucide React
- **Calendar**: FullCalendar React for calendar functionality
- **Date Handling**: date-fns, react-datepicker, react-date-range
- **State Management**: React hooks with Context API

## Quick Start

### Prerequisites

- Node.js 18.x or higher
- npm 8.x or higher
- Backend API running on `http://localhost:8000`

### Installation

1. **Clone and navigate:**
   ```bash
   cd planner-ai-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   ```
   http://localhost:3000
   ```

## Project Structure

```
├── app/                 # Next.js App Router
│   ├── globals.css     # Global styles
│   ├── layout.tsx      # Root layout with theme provider
│   └── page.tsx        # Main application entry
├── components/         # React components by feature
│   ├── authenticate/   # Login/Register components
│   ├── calendar/       # Calendar view components
│   ├── modals/         # Modal dialogs
│   └── sidebar/        # Navigation sidebar
├── lib/                # API integration functions
├── styles/            # CSS stylesheets
├── types/             # TypeScript type definitions
└── utils/             # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with a FastAPI backend for:

- User authentication and management
- Subject and task CRUD operations
- AI plan generation and rescheduling
- Feedback submission for plan optimization

## Documentation

Comprehensive documentation is available in `/documentation/frontend_documentation/`:

- [Frontend Overview](documentation/frontend_documentation/frontend_overview.md)
- [Components Guide](documentation/frontend_documentation/components.md)
- [API Integration](documentation/frontend_documentation/api_integration.md)
- [Styling & Theming](documentation/frontend_documentation/styling_theming.md)
- [Types & Utilities](documentation/frontend_documentation/types_utilities.md)
- [Setup & Development](documentation/frontend_documentation/setup_development.md)

## Development

### Code Quality

- **TypeScript**: Strict type checking enabled
- **ESLint**: Code linting and formatting
- **Prettier**: Consistent code formatting

### Theming

The app supports light and dark themes with CSS variables for consistent styling across components.

### Responsive Design

Built mobile-first with responsive breakpoints for tablet and desktop views.

## Deployment

### Production Build

```bash
npm run build
npm start
```

### Vercel Deployment

Optimized for Vercel with automatic deployments from GitHub.

## Contributing

1. Follow the existing code style and TypeScript conventions
2. Add proper type definitions for new features
3. Update documentation for significant changes
4. Test across different themes and screen sizes

## License

This project is part of the AI Student Planner system.
