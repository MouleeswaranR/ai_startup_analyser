# 🏢 AI Company — Multi-Agent Startup Engine

AI Company is an automated startup generation floor powered by **CrewAI** and **Groq**. 

Describe a startup idea, and 5 specialized AI agents work together as a corporate team to generate a complete business package.

## 🚀 Key Features

- **Multi-Agent Orchestration**: 5 distinct agents (CEO, Research, Dev, Marketing, Support) collaborate on your idea.
- **Ultra-Fast Inference**: Powered by Groq (LLaMA 3.1) for near-instant results.
- **Human-Made UI**: A clean, professional, light-themed dashboard inspired by modern SaaS (Linear/Vercel).
- **Comprehensive Deliverables**:
  - Business Strategy & Roadmap
  - Market & Competitor Analysis (Formatted Tables)
  - Technical Architecture & Landing Page Code
  - Social Media & SEO Content
  - Customer FAQ & Email Templates (No Placeholders)

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI Framework**: CrewAI
- **LLM**: Groq (llama-3.1-8b-instant)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gowtham-v-data/AI-Company.git
   cd AI-Company
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file from `.env.example`
   - Add your `GROQ_API_KEY`

4. Run the application:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

5. Open your browser:
   Visit `http://localhost:8000`

## 👔 The AI Team

- **CEO**: Defines vision, revenue models, and roadmaps.
- **Research Analyst**: Conducts deep market and competitor research.
- **Developer**: Designs tech stacks and builds the MVP prototype.
- **Marketing Lead**: Creates high-conversion social and blog content.
- **Support Lead**: Sets up the customer experience infrastructure.

---
Built with ❤️ by AI Company Team
