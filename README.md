# Weather Dashboard

A beautiful, dynamic weather dashboard built with Django that adapts its UI based on current weather conditions.

## Features

- **Dynamic Weather-Based UI**: The dashboard changes its appearance based on weather conditions:
  - ☀️ **Sunny**: Bright, cheerful purple and pink gradients with golden accents
  - ☁️ **Cloudy**: Moody, dark gray tones with soft overlays
  - 🌧️ **Rainy**: Deep, dramatic purple and indigo hues
  - ❄️ **Snowy**: Clean, crisp white and light gray palette

- **Real-time Weather Data**: Powered by the Open-Meteo API (no API key required)
- **Location Search**: Search for any city worldwide
- **7-Day Forecast**: View weather predictions for the upcoming week
- **Responsive Design**: Beautiful on desktop and mobile devices
- **Production-Grade UI**: Custom-styled with glassmorphism effects, animations, and smooth transitions

## Tech Stack

- **Backend**: Django 6.0+
- **API**: Open-Meteo (free, no API key required)
- **Styling**: Custom CSS with glassmorphism, gradients, and animations
- **Typography**: Playfair Display (headings) & Outfit (body text)
- **Dependency Management**: `uv`
- **Code Quality**: Ruff (linting & formatting)

## Development

### Setup

```bash
# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Start development server
uv run python manage.py runserver
```

### Development Commands

```bash
# Add a dependency
uv add <package>

# Run tests
uv run python manage.py test

# Lint and format code
uv run ruff check --fix
uv run ruff format
```

### API Integration

The dashboard uses two Open-Meteo API endpoints:

1. **Geocoding**: Converts city names to coordinates
   - `https://geocoding-api.open-meteo.com/v1/search`

2. **Weather Forecast**: Retrieves weather data
   - `https://api.open-meteo.com/v1/forecast`

Both APIs are free and require no authentication.

## Project Structure

```
weather-dashboard/
├── config/              # Django project configuration
├── weather/             # Weather app
│   ├── views.py         # Weather data fetching and display logic
│   ├── urls.py          # URL routing
│   └── templates/       # App-specific templates
├── templates/           # Global templates
│   └── dashboard.html   # Main weather dashboard
└── manage.py            # Django management script
```

## Design Highlights

### Dynamic Theming
The dashboard automatically adapts its appearance based on weather conditions using:
- Custom gradients for each weather type
- Glassmorphism card effects with backdrop blur
- Unique color palettes (sunny, cloudy, rainy, snowy)
- Text shadows and overlays for depth
- Floating animations for weather icons

### Typography
- **Playfair Display**: Elegant serif font for headings
- **Outfit**: Modern sans-serif for body text

### Animations
- Smooth fade-in transitions
- Floating weather icons
- Hover effects on cards
- Search box focus states

## License

This project is open source and available for educational and personal use.
