# FastAPI YouTube Downloader

A full-featured, YouTube Downloader API built using FastAPI. It supports video/audio downloads, metadata extraction, playlist support, background processing via Celery, Redis-based rate limiting, and more.

---

## 🚀 Features

- ✅ Download video/audio from YouTube via `/download`
- ✅ Extract video/playlist metadata via `/metadata`
- ✅ Retrieve download history via `/history`
- ✅ Supports video (mp4, webm, mkv) and audio (mp3) formats
- ✅ Metadata caching
- ✅ IP-based rate limiting (10 downloads/day/IP via Redis)
- ✅ Background task processing with Celery
- ✅ API key authentication
- ✅ Async SQLAlchemy + PostgreSQL for download history

---

## 🧱 Tech Stack

- **FastAPI** - Web framework
- **yt-dlp** - Core YouTube downloader
- **Celery** - Background task queue
- **Redis** - For Celery broker & IP rate limiting
- **PostgreSQL** - Download history database
- **Async SQLAlchemy** - ORM
- **Pydantic** - Data validation

---

## 📂 Directory Structure

```bash
Fastapi_Youtube_Downloader/
├── app/  # Contains FastAPI application code
│   ├── api/  # Handles API endpoints for download, history, and metadata
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   ├── download.py  # Contains the download-related route handlers
│   │   ├── history.py  # Contains the history-related route handlers
│   │   └── metadata.py  # Contains the metadata-related route handlers
│   ├── core/  # Contains configuration and core utilities like rate limiting and security
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   ├── config.py  # Configuration settings and environment variable parsing
│   │   ├── rate_limit.py  # Implements rate-limiting logic for download requests
│   │   └── security.py  # Handles security features like OAuth2 and password hashing
│   ├── db/  # Contains database-related code and models
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   ├── database.py  # Database connection setup and session management
│   │   └── models.py  # Defines database models like DownloadHistory
│   ├── schemas/  # Contains Pydantic models for request/response validation
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   ├── download.py  # Pydantic models for download-related validation
│   │   ├── history.py  # Pydantic models for history-related validation
│   │   └── metadata.py  # Pydantic models for metadata-related validation
│   ├── services/  # Contains business logic for downloading and metadata processing
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   ├── downloader.py  # Business logic for video downloading and retries
│   │   └── metadata.py  # Logic for fetching and processing video metadata
│   ├── tasks/  # Handles background tasks like video downloads with Celery
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   └── worker.py  # Celery worker for processing background download tasks
│   ├── utils/  # Contains helper functions and validators
│   │   ├── __init__.py  # Marks the directory as a Python package
│   │   ├── helpers.py  # General helper functions used across the application
│   │   └── validators.py  # Utility functions for validating input data
│   ├── __init__.py  # Marks the directory as a Python package
│   └── main.py  # The main entry point for the FastAPI application
├── downloads/  # Stores downloaded video/audio files
├── yt/  # Virtual environment directory (ignored in version control)
├── .env  # Environment variables (database credentials, configuration settings)
├── .gitignore  # Specifies ignored files (e.g., virtual environment, downloads)
├── requirements.txt  # Python dependencies for the project
└── README.md  # Project documentation and setup instructions
```

---

## 🔐 Authentication

Use an API key in the header:

```http
GET /download
x-api-key: your_api_key_here
```

---

## 📦 Rate Limiting

Each IP is limited to **100 downloads per day**. Tracked via Redis.

---

## 🧪 API Endpoints

### `POST /download`

Download a video/audio or playlist.

```json
{
  "url": "https://youtube.com/watch?v=xyz",
  "format": "mp4",
  "quality": "720p"
}
```

- Background download via Celery.
- Returns task ID for tracking.

### `GET /metadata`

Get video or playlist metadata.

```json
{
  "url": "https://youtube.com/watch?v=xyz"
}
```

### `GET /history`

Get download history.

---

## 🐘 Database

Using async SQLAlchemy with PostgreSQL.

- Stores download records.
- Metadata is cached but not stored.

---

## 🛠 Setup & Run

### 1. **Install dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Setup virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`
```

### 3. **Start Redis**

```bash
redis-server
```

### 4. **Run Celery worker**

```bash
celery -A app.tasks.worker.celery worker --loglevel=info
```

### 5. **Run FastAPI app**

```bash
uvicorn app.main:app --reload
```

> App runs on http://localhost:8000

### 6. **Run FastAPI app on any alernative port**

```bash
uvicorn app.main:app --reload --port port_number
like for eg, uvicorn app.main:app --reload --port 8001
```

> App runs on http://localhost:8001 in the example taken

---

## ✅ Example cURL

```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key" \
  -d '{"url": "https://youtu.be/dQw4w9WgXcQ", "format": "mp4"}'
```

---

## 📌 Notes

- All downloads are saved in the `downloads/` folder.
- Supports playlists with individual and ZIP output.
- Metadata includes: title, duration, uploader, views, etc.

---

### 💬 Want to contribute?
- Fork and open a PR!
- Discuss via GitHub Issues or email.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author
Crafted with ❤️ using FastAPI, yt-dlp, and Python.

---

This is the full content for your `README.md` file. It explains the purpose of the project, installation instructions, how to use it, and gives details about the available endpoints.

---

For questions or help, feel free to ask!
