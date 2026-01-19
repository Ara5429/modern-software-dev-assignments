# Mood Tracking Notes - Frontend

Vue 3 frontend for the mood tracking notes application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Features

- **Notes Management**: Create, read, update, and delete notes
- **Mood Tracking**: Track your mood with 5 options (happy, neutral, sad, angry, tired)
- **Tags**: Organize notes with tags
- **Weekly Mood Chart**: Visualize your mood trends over the past week
- **Action Items**: Track tasks and action items

## Tech Stack

- Vue 3 (Composition API)
- Vite
- Tailwind CSS
- Chart.js
- Axios

## Project Structure

```
src/
├── components/
│   ├── NotesList.vue      # Notes CRUD component
│   ├── MoodTracker.vue     # Mood tracking component
│   └── MoodChart.vue       # Weekly mood chart
├── App.vue                 # Main app component
├── main.js                 # App entry point
├── api.js                  # API client
└── style.css               # Global styles with Tailwind
```
