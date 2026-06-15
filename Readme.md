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

The main idea is simple:

Website content → Scraper → FastAPI → PostgreSQL + pgvector → Embeddings → Retrieval → LLM Answer

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
