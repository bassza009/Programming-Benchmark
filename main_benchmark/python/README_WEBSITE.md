# Simple Python Landing Page Website

A beautiful, responsive landing page built with Python's built-in HTTP server.

## Features

- ✨ Modern, responsive design
- ⚡ No external dependencies (uses Python standard library)
- 🎨 Beautiful gradient styling
- 📱 Mobile-friendly layout
- 🚀 Easy to run and customize

## Getting Started

### Requirements

- Python 3.7+

### Installation

No external dependencies needed! Just Python.

### Running the Website

```bash
python3 app.py
```

Then open your browser and navigate to:
```
http://localhost:8000
```

You should see the landing page.

### Customization

Edit `app.py` to customize:
- Port number (change `PORT = 8000`)
- Page title and heading
- Features section content
- Colors and styles in the CSS
- Add more routes by extending the `LandingPageHandler` class

## File Structure

```
.
├── app.py                 # Main Python web server
└── README_WEBSITE.md      # This file
```

## How It Works

The server uses Python's built-in `http.server` module to:
1. Listen for HTTP requests on port 8000
2. Serve the HTML landing page when accessing the root path (`/`)
3. Support custom request handling through the `LandingPageHandler` class

## Stopping the Server

Press `Ctrl+C` in your terminal to stop the server.

## Future Enhancements

- Add static file serving (CSS, images)
- Add form processing
- Upgrade to Flask/Django for more features
- Add dynamic content rendering
