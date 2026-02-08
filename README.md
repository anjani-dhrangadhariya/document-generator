🧪 Clinical Factsheet AI (Demo)
A Technical Proof of Concept for Automated Medical Writing.

This repository demonstrates how to integrate LangChain, OpenRouter, Docker, and Streamlit to automate the tedious process of extracting data from dense unstructured text summaries.

🎯 Purpose
The goal of this project is to showcase:

Asynchronous Document Processing: Efficiently handling PDF/DOCX parsing.

LLM Prompt Engineering: Using structured prompts to extract specific clinical fields (Study Phase, Design, BMI requirements, etc.).

Dynamic Document Templating: Mapping AI outputs to a professional Word document template in real-time.

🛠️ Tech Stack
Frontend: Streamlit (Python-based web UI)

Orchestration: LangChain (Chains & Prompt Templates)

LLM: OpenRouter (accessing GPT-4/GPT-4o)

Configuration: Pydantic Settings (Type-safe env management)

Infrastructure: Docker & Docker Compose

⚡ Quick Start (The "One-Command" Demo)
If you have Docker installed, you can see this in action immediately:

Clone & Set API Key:

Bash
git clone <repo-url>
echo "OPENROUTER_API_KEY=your_key_here" > .env
Launch:

Bash
docker-compose up --build
Explore: Open http://localhost:8501 and upload a dummy clinical summary.

🔍 Why this Architecture?
Separation of Concerns: The Extractor handles the "brain" (LLM), while the Generator handles the "body" (formatting).

Environment Integrity: Using Docker ensures that file paths, OS dependencies, and Python versions never conflict.

Scalability: The pipeline is built to be "field-agnostic"—adding a new clinical field to extract only requires a new prompt and a placeholder in the Word template.
