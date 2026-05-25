# AI Document Processing Pipeline

An asynchronous document processing system built using FastAPI, Celery, Redis, PostgreSQL, and Docker.

This project demonstrates how modern backend systems handle heavy processing tasks like PDF extraction, AI summarization, and email notifications using distributed background workers.

Instead of processing large files directly inside API requests, the system pushes tasks into Redis queues and executes them asynchronously using Celery workers. This architecture improves scalability, reliability, and overall API performance.

---

# Features

- Upload PDF documents through FastAPI APIs
- Store document metadata in PostgreSQL
- Process PDFs asynchronously using Celery workers
- Extract text from uploaded PDFs
- Generate AI-based summaries
- Queue-based architecture using Redis
- Email notification system with retry support
- Dockerized multi-service backend setup
- Status tracking for document workflows

---

# System Architecture

```text
Client
   ↓
FastAPI API
   ↓
PostgreSQL
   ↓
Redis Queue
   ↓
Celery Worker
   ↓
PDF Processing
   ↓
AI Summary Generation
   ↓
Notification Queue
   ↓
Email Service
```

# Tech Stack
## Backend
    - FastAPI
    - Python
    - SQLAlchemy
    - PostgreSQL
## Async Processing
    - Celery
    - Redis
## AI / NLP
    - pypdf
    - Local AI service layer
## DevOps
    - Docker
    - Docker Compose

# workflow


1. Upload PDF

The user uploads a PDF document through the /upload API endpoint.

2. Store Metadata

The API stores:

- filename
- file path
- user email
- processing status

inside PostgreSQL.

3. Queue Background Task

The API pushes a task into Redis using Celery.

4. Background Processing

Celery workers:

- extract PDF text
- generate summaries
- update document status

without blocking the API server.

5. Notification System

After processing completes, a separate notification task sends an email to the user.

## Environment Setup
```
DATABASE_URL=postgresql://admin:password@postgres:5432/document_pipeline

REDIS_URL=redis://redis:6379/0

SMTP_HOST=sandbox.smtp.mailtrap.io
SMTP_PORT=2525

SMTP_USER=your_username
SMTP_PASSWORD=your_password
```

# Installation
## Clone Repository
```git clone 

cd ai-document-pipeline
```
## Run Using Docker
```
docker compose up --build
```
# Services
Service	    Port
FastAPI	    8000
PostgreSQL	5432
Redis	    6379
# API Endpoint
## Upload PDF
POST /upload
Form    Data
Field	Type
email	string
file	PDF file
## Future Improvements
- JWT authentication
- User dashboard
- File storage using AWS S3
- Vector database integration
- Real AI summarization using Ollama/OpenAI
-WebSocket-based live status updates
- Dead-letter queues
- Kubernetes deployment

## Learning Outcomes

This project helped in understanding:

- asynchronous backend architecture
- distributed task processing
- Redis queues
- Celery workers
- API scalability
- Docker-based deployments
- event-driven workflows
- retry systems
- backend service separation