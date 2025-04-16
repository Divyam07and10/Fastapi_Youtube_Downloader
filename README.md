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


Here's the updated README.md reflecting the new project structure and codebase:

```markdown
# 🎥 YouTube Downloader API – FastAPI Based REST Service

A **production-grade RESTful API** built with **FastAPI** that enables users to download YouTube videos or extract audio files in different formats and qualities. Implements rate limiting, background processing, and Redis caching. Built with modular architecture for scalability.

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
- Download Videos/Audio in multiple formats (mp4, mkv, mp3, webm)
- Select video quality (360p to 4K)
- Rate limiting (100 downloads/day per IP)
- Redis-backed request tracking
- PostgreSQL database for download history
- Metadata caching with LRU strategy
- Celery background task processing
- API key authentication
- Automatic fallback (yt-dlp → pytube)

**Planned Enhancements:**
- Docker deployment
- AWS S3 storage integration
- OAuth2 authentication
- Prometheus monitoring
- Video trimming/stitching
- Playlist support

---

## ⚙️ Tech Stack
| Layer                 | Tech / Tool                              |
|-----------------------|------------------------------------------|
| Backend Framework     | FastAPI                                  |
| Database              | PostgreSQL                               |
| Cache/Queue           | Redis                                    |
| Task Queue            | Celery                                   |
| Video Processing      | yt-dlp + pytube (fallback)               |
| Auth                  | API Key Authentication                   |
| Rate Limiting         | Redis-based counter                      |
| File Storage          | Local storage (downloads/)               |
| Validation            | Pydantic models                          |
| ORM                   | SQLAlchemy Async                         |
| Monitoring            | Built-in metrics (Planned: Prometheus)   |

---

## 🚀 Features Implemented
### ✅ Core Features
- YouTube URL validation & sanitization
- Rate limiting (100/day per IP)
- Background processing with Celery
- Download history tracking
- Metadata caching (1 hour TTL)
- API key authentication
- Multiple format/quality support
- Automatic fallback mechanism
- Redis-backed rate limiting
- Async database operations

### ✅ Safety Features
- Input validation for all endpoints
- Path sanitization for file storage
- Environment-based configuration
- Secure credential handling (.env)
- SQL injection prevention
- Rate limiting abuse protection

---

## 🌤 API Endpoints
| Endpoint              | Method | Description                     |
|-----------------------|--------|---------------------------------|
| `/download`           | POST   | Initiate video/audio download   |
| `/metadata`           | GET    | Get video metadata              |
| `/history`            | GET    | View download history           |
| `/metrics`            | GET    | System metrics (Planned)        |

**Sample Download Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=abcd1234",
  "format": "mp4",
  "quality": "720p"
}
```

**Sample Metadata Response:**
```json
{
  "title": "Sample Video",
  "duration": "5m30s", 
  "views": 123456,
  "channel": "Sample Channel",
  "thumbnail_url": "https://img.youtube.com/vi/abcd1234/hqdefault.jpg",
  "published_date": "2024-04-03"
}
```

---

## 📁 Project Structure
```bash
Fastapi_Youtube_Downloader/
├── app/                   # Core application logic
│   ├── api/               # API endpoint handlers
│   │   ├── download.py    # Download routes
│   │   ├── history.py     # History routes
│   │   └── metadata.py    # Metadata routes
│   ├── core/              # Configuration & utilities
│   │   ├── config.py      # Environment configuration
│   │   ├── rate_limit.py  # Redis rate limiting
│   │   └── security.py    # API key validation
│   ├── db/                # Database configuration
│   │   ├── database.py    # Async DB connection
│   │   └── models.py      # SQLAlchemy models
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   ├── tasks/             # Celery tasks
│   └── utils/             # Helpers & validators
├── downloads/             # Downloaded files storage
├── requirements.txt       # Dependency list
├── .env                   # Environment variables
├── README.md              # Project documentation
└── celery_worker.py       # Celery entry point
```

---

## 📦 Installation

### 1. Prerequisites
- Python 3.10+
- Redis server
- PostgreSQL
- FFmpeg

### 2. Setup Environment
```bash
git clone https://github.com/Divyam07and10/Fastapi_Youtube_Downloader.git
cd Fastapi_Youtube_Downloader
python -m venv yt
source yt/bin/activate  # Linux/MacOS
# .\yt\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
1. Create `.env` file from `.env.example`
2. Set database credentials and API keys
3. Configure Redis connection details

### 5. Database Setup
```bash
alembic upgrade head  # After setting up Alembic (planned)
```

### 6. Run Application
```bash
# Start FastAPI
uvicorn app.main:app --reload

# Start Celery worker
celery -A app.tasks.worker.celery_app worker --loglevel=info
```

---

## 🔐 Security Features
- API key authentication for all endpoints
- Redis-based rate limiting (100 requests/day/IP)
- Input sanitization for URLs and file paths
- Environment-separated credentials
- Async database operations
- Request validation middleware
- HTTPS support (Planned)
- JWT token authentication (Planned)

---

## 🧺 Example Requests
**Download Video:**
```bash
curl -X POST http://localhost:8000/download \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/dQw4w9WgXcQ", "format": "mp4", "quality": "1080p"}'
```

**Get Metadata:**
```bash
curl -H "X-API-Key: your_api_key" \
  "http://localhost:8000/metadata?url=https://youtu.be/dQw4w9WgXcQ"
```

---

## 📜 License
MIT License - See [LICENSE](LICENSE) for details.

---

## 👨💻 Roadmap
- [ ] Docker containerization
- [ ] AWS S3 storage integration
- [ ] Prometheus/Grafana monitoring
- [ ] OAuth2 authentication
- [ ] Video trimming capabilities
- [ ] Playlist download support

---

## 🤝 Contribution
1. Fork the repository
2. Create feature branch (`git checkout -b feature/foo`)
3. Commit changes (`git commit -am 'Add foo'`)
4. Push to branch (`git push origin feature/foo`)
5. Create new Pull Request

```

This updated README:
1. Matches the actual project structure
2. Reflects current implementation status
3. Provides accurate setup instructions
4. Shows working API examples
5. Maintains consistency with codebase features
6. Highlights security measures
7. Includes proper environment setup guidance
