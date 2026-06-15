# Custom AI Chatbot

A full-stack AI chatbot foundation built with FastAPI, PostgreSQL, pgvector, Scrapy, Nginx, Docker, and OpenAI.

This project allows you to crawl your own website, store the content as knowledge base chunks, generate vector embeddings, retrieve relevant content with semantic search, and answer user questions using an LLM.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Run the Project](#run-the-project)
- [Collect Website Content](#collect-website-content)
- [Generate Embeddings](#generate-embeddings)
- [Test the Chat Endpoint](#test-the-chat-endpoint)
- [Notes](#notes)

---

## Project Overview

This project is a reusable foundation for building your own AI assistant.

You can customize it for:

- Company websites
- Documentation assistants
- Personal websites
- Customer support bots
- Internal knowledge bases
- AI agent foundations

Architecture:

Website → Scraper → FastAPI → PostgreSQL + pgvector → Embeddings → Retrieval → LLM → Answer

---

## Project Structure

```txt
custom_ai_chatbot/
├── api/
├── client/
├── nginx/
├── scraper/
├── secrets/
├── utils/
├── docker-compose.yml
└── endpoints.http
```

### api/

Contains the FastAPI backend, database models, schemas, routers, services, AI logic, embedding generation, retrieval, and RAG pipeline.

### scraper/

Contains the Scrapy project used to crawl your website and send extracted content to the FastAPI knowledge base endpoint.

### nginx/

Contains the Nginx reverse proxy configuration.

### secrets/

Contains environment variable files.

Each service contains a `.env.sample` file.

Create a real `.env` file from the sample file and replace fake values with real values.

### utils/

Contains utility shell scripts such as database backup and restore scripts.

### client/

Contains the frontend application.

---

## Requirements

### Docker

https://docs.docker.com/get-docker/

### Python

https://www.python.org/downloads/

### Node.js

https://nodejs.org/

### Git

https://git-scm.com/downloads

### OpenAI API Key

https://platform.openai.com/

---

## Environment Variables

Inside the `secrets/` folder, each service contains a `.env.sample` file.

Create a real `.env` file from each sample file.

Example:

```bash
cp secrets/api/.env.sample secrets/api/.env
cp secrets/db/.env.sample secrets/db/.env
cp secrets/scraper/.env.sample secrets/scraper/.env
```

Replace all placeholder values with real values.

Example:

```env
OPEN_AI_KEY=your-real-openai-api-key
```

Do not commit real `.env` files to GitHub.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/mmmohajer/custom_ai_chatbot.git
```

Enter the project:

```bash
cd custom_ai_chatbot
```

Create a virtual environment:

```bash
python3 -m venv venv
```

or

```bash
python -m venv venv
```

Activate the virtual environment.

macOS / Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r api/requirements.txt
```

```bash
pip install -r scraper/requirements.txt
```

Install frontend dependencies:

```bash
cd client
npm install
cd ..
```

---

## Run the Project

From the project root:

```bash
docker compose up --build -d
```

This starts:

- Nginx
- FastAPI
- PostgreSQL + pgvector
- Scraper
- Frontend

API URL:

```txt
http://localhost/api/
```

---

## Collect Website Content

Open:

```txt
scraper/app/app/spiders/website.py
```

Update:

```python
allowed_domains = ["yourdomain.com"]
start_urls = ["https://yourdomain.com"]
```

Update internal URL validation as well.

Enter the scraper container:

```bash
docker exec -it <scraper-container-name> bash
```

Run the spider:

```bash
scrapy crawl website
```

The scraper will crawl the website and send page content to the knowledge base API.

---

## Generate Embeddings

After content has been stored in PostgreSQL, generate embeddings.

Enter the API container:

```bash
docker exec -it <api-container-name> bash
```

Run:

```bash
python -m app.aibot.commands.main generate-missing-embeddings
```

This command:

- Finds chunks without embeddings
- Generates embeddings using OpenAI
- Stores vectors in pgvector

After this step the knowledge base is ready for semantic search.

---

## Test the Chat Endpoint

Use `endpoints.http` to test the API.

Example:

```http
POST http://localhost/api/aibot/knowledge-base/chat/
Content-Type: application/json

{
  "message": "What services do you offer?",
  "similarity_threshold": 0.3,
  "top_k": 5
}
```

The response includes:

- Question
- Answer
- Sources
- Similarity scores

---

## Notes

This project is designed as a foundation that you can extend with:

- Authentication
- Payments
- Notifications
- Admin dashboard
- Scheduled scraping
- Multi-website support
- User-specific knowledge bases
- Advanced AI agent workflows
