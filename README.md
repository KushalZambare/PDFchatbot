# PDF Bot - Your Intelligent Document Assistant

PDF Bot is a Streamlit-based application that allows you to upload a PDF and interact with its contents using a variety of AI-powered features. These include text extraction, advanced search (with both keyword-based and semantic search), translation, text-to-speech (TTS), summarization, Q&A, quiz generation, and real-time collaboration.

## Features

- **PDF Text Extraction:**  
  Extract text from PDFs using PyPDF2 and optional OCR (with `pdf2image` and `pytesseract`) for scanned documents.

- **Document Navigation & Annotation:**  
  Navigate pages, annotate text snippets, and view revision history.

- **Advanced Search:**  
  Search within the document using:
  - **Keyword-based Search:** Traditional text matching with highlighted results.
  - **Semantic Search:** Leverages OpenAI embeddings and cosine similarity for context-aware results.

- **Translation & Text-to-Speech:**  
  Translate text to various languages and generate audio output using `gTTS`.

- **AI-Powered Summarization:**  
  Generate concise summaries of either the entire document or individual pages using OpenAI GPT-3.5 Turbo.

- **Q&A & Quiz Generation:**  
  Ask questions about the document and generate quizzes with answers based on its content.

- **Real-Time Collaboration:**  
  Collaborate with others via WebSocket-enabled chat and shared annotations.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/pdf-bot.git
   cd pdf-bot
