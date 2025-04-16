# 🎥 YouTube Downloader API – FastAPI Based REST Service

A **production-grade RESTful API** built with **FastAPI** that enables users to download YouTube videos or extract audio files in different formats and qualities. It supports automatic fallback mechanisms, background task handling, and metadata retrieval. The project is built to scale with plans for advanced features like Celery task queues, Docker deployment, OAuth2 authentication, rate limiting, logging, and cloud storage support.

---

## 🌐 Live Status
> ❗ Not deployed yet — Local-only in current phase.

---

## 🧽 Table of Contents
- [🔍 Project Overview](#-project-overview)
- [⚙️ Tech Stack](#-tech-stack)
- [🚀 Features Implemented](#-features-implemented)
- [🌤 API Endpoints](#-api-endpoints)
- [🛠 How It Works](#-how-it-works)
- [💾 File Storage](#-file-storage)
- [📊 Planned Enhancements](#-planned-enhancements)
- [📁 Project Structure](#-project-structure)
- [📦 Installation](#-installation)
- [🧺 Example Usage (curl)](#-example-curl-requests)
- [🔐 Security Measures](#-security-measures)
- [📝 License & Contribution](#-license--contribution)

---

## 🔍 Project Overview
This FastAPI-based application provides endpoints to:
- Download Videos and Audio: Users can download videos and audio in different formats like mp4, mkv, mp3, and webm.
- Quality Selection: Users can specify the quality of videos (360p, 480p, 720p, 1080p, 4k).
- Metadata Fetching: Users can get metadata for a video, such as title, duration, views, etc.
- Automatic Fallback: If a download fails using yt-dlp, the system will fall back to pytube for the download.
- Handle downloads asynchronously using background tasks.
- Cache metadata responses to reduce redundancy.

> 🧪 Designed for modularity, performance, and extensibility.

**Planned Enhancements:**
- Playlist downloads
- Video trimming
- Webhooks for completion notifications
- CI/CD with GitHub Actions
- OAuth2/API Key security
- Rate limits per user tier (free/premium)
- Deployment to AWS EC2 / Lambda / Kubernetes
- Structured logging with Loguru
- Metrics with Prometheus & Grafana
- Cloud storage with AWS S3
- Database logging with PostgreSQL + Alembic

---

## ⚙️ Tech Stack
| Layer                 | Tech / Tool                              |
| ---------------------| ---------------------------------------- |
| Backend Framework     | FastAPI                                  |
| Video Downloader      | yt-dlp                                   |
| Fallback Downloader   | pytube                                   |
| Background Processing | FastAPI's `BackgroundTasks`, Celery (Planned) |
| Caching (metadata)    | Python `functools.lru_cache`             |
| File Storage          | Local directory (`downloads/`), AWS S3 (Planned) |
| Logging               | Standard logging, Loguru (Planned)       |
| Task Queue            | Celery + Redis (Planned)                 |
| Authentication        | API Key / OAuth2 (Planned)               |
| Monitoring & Metrics  | Prometheus, Grafana (Planned)            |
| Deployment            | Docker, Gunicorn, Nginx (Planned)        |
| Hosting               | AWS EC2 / Kubernetes / Lambda (Planned)  |
| Database              | PostgreSQL / SQLite (Planned)            |
| Migrations            | Alembic (Planned)                        |
| Configuration         | `.env` file for secrets/config (Planned) |

---

## 🚀 Features Implemented
### ✅ Video Downloading
- Accepts YouTube URLs.
- Supports video (`mp4`, `webm`, `mkv`) and audio (`mp3`) formats.
- Allows quality selection (360p to 4K).
- Sanitized filenames, saved under `downloads/`.
- Background download using FastAPI’s `BackgroundTasks`.

### ✅ Metadata Extraction
- Extracts: `title`, `duration`, `views`, `likes`, `channel`, `thumbnail`, `published_date`.
- Uses `yt-dlp`, falls back to `pytube`.
- Cached responses with `@lru_cache`.

### ✅ Fallback Handling
- If `yt-dlp` fails, `pytube` automatically steps in.

### ✅ Background Tasking
- Download jobs are run asynchronously using `BackgroundTasks`.
- Will shift to Celery + Redis for scalable task queues.

---

## 🌤 API Endpoints
### 🎥 `POST /download`
**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=abcd1234",
  "format": "mp4",
  "quality": "720p"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Download started"
}
```

### 📊 `GET /metadata`
**Request:**
```
GET /metadata?url=https://www.youtube.com/watch?v=abcd1234
```
**Response:**
```json
{
  "title": "Sample Video",
  "duration": "5m30s",
  "views": 123456,
  "likes": 8000,
  "channel": "Sample Channel",
  "thumbnail_url": "https://img.youtube.com/vi/abcd1234/hqdefault.jpg",
  "published_date": "2024-04-03"
}
```

### 📂 `GET /history` *(Planned)*
- Will show past download jobs.
- Includes timestamps, file names, formats.
- Will be backed by SQLite/PostgreSQL.

---

## 🛠 How It Works
### 1. **Download Flow**
- Accepts input JSON.
- Builds a `yt-dlp` command for specific format/quality.
- If failed, tries `pytube`.
- Task runs in background.
- File saved in `downloads/`.

### 2. **Metadata Flow**
- Calls `yt-dlp --dump-json`.
- If it fails, parses using `pytube.YouTube`.
- Cached response to minimize repetitive calls.

### 3. **Quality Matching**
- Uses `yt-dlp` format strings.
- Best effort match for requested quality.

---

## 💾 File Storage
- Files stored at:
```
downloads/download_<timestamp>.<format>
```
- Names are sanitized and timestamped.
- S3/GCS support in future roadmap.

---

## 📊 Planned Enhancements
| Feature                          | Status | Description |
|----------------------------------|--------|-------------|
| `/history` endpoint              | 🔜     | List past downloads             |
| OAuth2 / API key auth            | 🔜     | Secure endpoints                |
| Rate limiting                    | 🔜     | Prevent abuse (5/day)           |
| Celery + Redis                   | 🔜     | Queue background tasks          |
| Loguru Logging                   | 🔜     | Pretty structured logs          |
| Dockerization                    | 🔜     | `Dockerfile`, `docker-compose`  |
| CI/CD (GitHub Actions)           | 🔜     | Automate deployment             |
| Prometheus + Grafana             | 🔜     | Metrics and monitoring          |
| AWS S3                           | 🔜     | Replace local file storage      |
| Playlist & Trimming Support      | 🔜     | Download playlists / segments   |
| Webhook                          | 🔜     | Notify client after download    |
| AWS Lambda / EC2 / K8s hosting   | 🔜     | Cloud deployment options        |
| PostgreSQL + Alembic             | 🔜     | Database and schema migration   |

---

## 📁 Project Structure
### ✅ Current Structure
```
Fastapi_Youtube_Downloader/
│
├── main.py                  # FastAPI application
├── downloads/               # Folder where all downloaded videos/audios are stored
├── requirements.txt         # Python package dependencies
├── routes.py                # Implementation of Routes
├── schemas.py               # Pydantic models for request body
├── services.py              # Core functionality for APIs
├── utils.py                 # Utility function for downloads directory, for build format selector and for format duration
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation (this file)
```

---

## 📦 Installation
### 1. Clone the repository
```bash
git clone https://github.com/Divyam07and10/Fastapi_Youtube_Downloader.git
cd Fastapi_Youtube_Downloader
```

### 2. Setup virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the development server
```bash
uvicorn main:app --reload
```

> App runs on http://localhost:8000

---

## 🧺 Example curl Requests
### Download a video
```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=abcd1234", "format": "mp4", "quality": "720p"}'
```

### Get metadata
```bash
curl "http://localhost:8000/metadata?url=https://www.youtube.com/watch?v=abcd1234"
```

---

## 🔐 Security Measures
- URL validation to only allow YouTube domains
- Input validation for format and quality fields
- Directory sanitization to prevent path traversal
- Planned OAuth2 / API Key authentication
- Planned rate limiting per IP/token

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


# FastAPI YouTube Downloader

A full-featured, YouTube Downloader API built using FastAPI. It supports video/audio downloads, metadata extraction, background processing via Celery, Redis-based rate limiting, and more.

---

## 🚀 Features

- ✅ Download video/audio from YouTube via `/download`
- ✅ Extract video/playlist metadata via `/metadata`
- ✅ Retrieve download history via `/history`
- ✅ Supports video (`mp4`, `webm`, `mkv`) and audio (`mp3`) formats.
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
Fastapi-Youtube-Downloader/
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
Each IP is limited to **10- downloads per day**. Tracked via Redis.

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

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Start Redis**
```bash
redis-server
```

3. **Run Celery worker**
```bash
celery -A app.tasks.worker.celery worker --loglevel=info
```

4. **Run FastAPI app**
```bash
uvicorn app.main:app --reload
```

5. **Set up PostgreSQL** and create tables:
```bash
alembic upgrade head
```

6. **Create `.env` file**
```
API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379
```

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
