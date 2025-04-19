# URL Shortener with FastAPI

A modern URL shortening service built with FastAPI, MongoDB, and Jinja2 templates.

![URL Shortener](src/static/logo.webp)

## Features

- ✂️ Shorten long URLs to easy-to-share links
- 📊 Track access counts and last accessed date
- 🚀 Fast and responsive API
- 🎨 Clean and modern UI
- 📱 Mobile-friendly design
- 🔄 Serverless-ready for Vercel deployment

## Tech Stack

- **Backend**: FastAPI
- **Database**: MongoDB with Beanie ODM
- **Frontend**: Jinja2 Templates, HTML, CSS, JavaScript
- **Deployment**: Vercel-ready

## Prerequisites

- Python 3.13+
- MongoDB database (e.g., MongoDB Atlas)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/url-shortener-fastapi.git
   cd url-shortener-fastapi
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the `src` directory with the following content:
   ```
   DATABASE_USER=your_mongodb_username
   DATABASE_PASSWORD=your_mongodb_password
   DATABASE_NAME=your_database_name
   DATABASE_HOST=your_mongodb_host
   DATABASE_PORT=27017
   DEVELOPMENT=True
   ```

## Running Locally

Start the development server:

```bash
python main.py
```

The application will be available at http://localhost:8000

## Usage

1. Open your browser and navigate to http://localhost:8000
2. Enter a URL you want to shorten
3. Click "¡Acortar URL!"
4. Copy your shortened URL to share

## API Endpoints

- `GET /` - Main page
- `POST /api/v1/shorten` - Shorten a URL
- `GET /{token}` - Redirect to the original URL

## Deployment to Vercel

This project is configured for deployment on Vercel:

1. Install Vercel CLI:

   ```bash
   npm install -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

## Project Structure

```
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
├── vercel.json          # Vercel configuration
└── src/
    ├── app/             # Application code
    │   ├── api/         # API routes and controllers
    │   ├── database/    # Database models and connection
    │   └── shared/      # Shared utilities and constants
    └── static/          # Static assets
        ├── icons/       # App icons
        └── templates/   # HTML templates
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Author

[JuanjoLopez19](https://github.com/JuanjoLopez19) - [Portfolio](https://juanjolopez19.github.io)
