# Spazio Restaurant – AI Customer Service Assistant

An AI-powered customer service chatbot developed for Spazio Restaurant using Python, Flask, Gemini API, SQLite, Retrieval-Augmented Generation (RAG), Sentence Transformers and FAISS.

The assistant helps customers access restaurant information, explore menu prices, understand services and get answers to frequently asked questions in multiple languages.

## Project Overview

Spazio Assistant is designed to improve customer communication by providing quick and consistent responses to common restaurant-related questions.

The project combines structured database queries with Retrieval-Augmented Generation (RAG) to provide relevant, context-based answers.

## Features

- **Multilingual communication:** Supports English, Malayalam and Hindi, with automatic language detection.
- **Menu price lookup:** Retrieves menu items, portion sizes and prices from SQLite.
- **Order calculations:** Calculates item totals based on quantity and portion size.
- **Restaurant information:** Answers questions about outlets, opening hours, payments and services.
- **RAG-based knowledge retrieval:** Searches restaurant documentation for relevant information using embeddings and FAISS.
- **Customer support:** Provides restaurant contact information when human assistance is required.
- **Responsive web interface:** Provides a simple and accessible chatbot interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Gemini API | AI language model |
| OpenAI Python SDK | API communication |
| SQLite | Structured restaurant data |
| Sentence Transformers | Text embedding generation |
| FAISS | Vector similarity search |
| NumPy | Numerical operations |
| HTML, CSS, JavaScript | Frontend interface |

## RAG Architecture

The RAG implementation uses restaurant-specific Markdown documents as its knowledge source.

The process works as follows:

1. Restaurant documents are loaded from `data/knowledge_base/`.
2. Documents are divided into overlapping text chunks.
3. Sentence Transformers generates embeddings using `all-MiniLM-L6-v2`.
4. FAISS stores the embeddings in a vector index.
5. When a customer asks a question, the question is converted into an embedding.
6. FAISS retrieves the three most relevant knowledge chunks.
7. Retrieved information is provided to the AI assistant to generate a contextual response.

### Knowledge Base

The knowledge base contains documentation covering:

- Restaurant profile and history
- Outlet information
- Ordering and delivery
- Catering and bulk orders
- Food quality and safety
- Customer service policies
- AI assistant rules

### Structured Database vs RAG

The project uses two complementary information retrieval approaches:

- **SQLite:** Used for structured information such as menu items, portion sizes, prices and calculations.
- **RAG with FAISS:** Used for retrieving relevant information from restaurant documentation and policies.

This separation helps the assistant retrieve exact menu information while using contextual documentation for broader customer questions.

## Project Structure

```text
spazio-customer-service-agent/
│
├── app.py
├── agent.py
├── tools.py
├── rag.py
├── database.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── data/
│   ├── restaurant_info.csv
│   ├── menu_corrected_from_official_pdf.csv
│   └── knowledge_base/
│       ├── restaurant_profile.md
│       ├── outlets.md
│       ├── ordering_and_delivery.md
│       ├── catering_and_bulk_orders.md
│       ├── food_quality_and_safety.md
│       ├── customer_service_policies.md
│       └── ai_assistant_rules.md
│
├── vector_store/
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    ├── script.js
    └── images/
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd spazio-customer-service-agent
```

### 2. Create a virtual environment

```bash
py -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add your Gemini API configuration:

```env
LLM_API_URL=YOUR_GEMINI_API_ENDPOINT
MODEL_NAME=YOUR_GEMINI_MODEL
API_KEY=YOUR_GEMINI_API_KEY
```

Never publish your actual API key.

### 5. Initialise the database

```bash
py database.py
```

### 6. Build the RAG knowledge base

```bash
py rag.py
```

This generates the FAISS index and metadata files inside `vector_store/`.

### 7. Start the application

```bash
py app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## Testing

The project includes Python test files for checking different components:

- `test_agent.py`
- `test_api.py`
- `test_database.py`
- `test_gemini.py`
- `test_menu.py`
- `test_tools.py`

Run an individual test using:

```bash
py test_menu.py
```

## Security

- API keys are stored in environment variables.
- `.env` files are excluded from Git.
- Local SQLite databases are excluded from Git.
- Python virtual environments and cache files are excluded.
- The FAISS vector index is generated locally from the knowledge-base documents.

## Future Improvements

- WhatsApp integration for customer communication.
- Improved multilingual menu-item recognition.
- Live order status and availability integration.
- Restaurant management dashboard.
- Enhanced customer feedback and analytics.

## Project Purpose

This project demonstrates the practical application of AI-powered customer service, function calling, structured database retrieval and Retrieval-Augmented Generation in a real restaurant business environment.

Developed for Spazio Restaurant as an academic AI project.
