# Keel: Supply Chain Delivery Risk Intelligence

<p align="center">
  <img src="docs/images/keel_logo.png" alt="Keel Logo" height="180px">
</p>

## Overview

Keel is an agentic AI system that helps teams protect the long-lead equipment their projects depend on. It continuously watches equipment delivery schedules and works out, on its own, whether events in the world (geopolitical instability, tariff changes, labor action, or logistics disruptions) threaten a specific shipment, then surfaces early, explainable warnings.

Instead of replacing people, Keel acts as a tireless assistant: it reasons about whether each event actually affects a given delivery, rates the severity, and produces structured, cited insight. Users can ask natural language questions and get visual, sourced answers grounded in current data.

Keel analyzes:

- **Schedule variances** - delivery timeline risk from planned versus forecast dates
- **Political factors** - geopolitical risk near factories, borders, and routes
- **Tariff changes** - trade policy shifts that affect procurement
- **Logistics disruptions** - port congestion and shipping-lane issues

## Multi-Agent Flow

Keel uses Semantic Kernel to orchestrate a group of specialized agents. Selection and termination strategies decide which agent responds next and when a conversation is complete.

### Agents

- **ASSISTANT_AGENT** - general queries, greetings, and fallback responses
- **SCHEDULER_AGENT** - analyzes equipment schedule data and computes delivery risk
- **POLITICAL_RISK_AGENT** - evaluates political risk using grounded web search
- **TARIFF_RISK_AGENT** - assesses trade and tariff exposure
- **LOGISTICS_RISK_AGENT** - assesses shipping and port disruption
- **REPORTING_AGENT** - consolidates findings into a single cited report

### Example flows

General query:
```
User Query -> ASSISTANT_AGENT -> End
```

Schedule risk:
```
User Query -> SCHEDULER_AGENT -> REPORTING_AGENT -> End
```

Political risk:
```
User Query -> SCHEDULER_AGENT -> POLITICAL_RISK_AGENT -> REPORTING_AGENT -> End
```

For political, tariff, or logistics questions, the scheduler first extracts country, route, and equipment context. That structured data is passed to the relevant specialist agent, which runs grounded web searches, judges whether each result is material to the shipment, and returns an assessment with citations. The reporting agent then combines everything into a final report.

### Reasoning and resilience

- **Dynamic routing** - the orchestrator promotes only the items worth investigating and selects the risk lenses that fit each one
- **Ambiguity handling** - when evidence is thin or sources disagree, agents lower their confidence and state what they could not confirm rather than inventing an answer
- **Error recovery** - failed tool calls retry, fall back to another source, or degrade to an "unverified" note; a circuit breaker prevents endless retries
- **Transparent reasoning** - every agent logs its thinking steps, which power the Thinking Logs view and the human review step

## Technology

**Backend**
- **Claude (Anthropic API)** - large language models for reasoning and generation
- **Semantic Kernel** - orchestration framework for the multi-agent workflow
- **Anthropic web search** - grounded, cited web search for the risk agents
- **SQLite** - local database for schedules, equipment metadata, logs, and reports
- **FastAPI** - REST API layer
- **Streamlit** - developer interface for testing and debugging
- **Spire.Doc.Free** - Word document generation

**Frontend**
- **React** and **Next.js** - interactive, component-based UI
- **Tailwind CSS** - styling
- **React Simple Maps** - risk visualization

## Business Impact

- **Prevent costly delays** - spot delivery risk before it hits the schedule
- **Early warning** - timely alerts on emerging political, tariff, and logistics issues
- **Shareable documentation** - structured reports for procurement teams
- **Data-driven decisions** - choices backed by cited risk analysis
- **Human in control** - people approve the decisions that carry cost

## Quick Start

### Prerequisites

- Python 3.11
- An Anthropic API key
- Node.js (for the frontend)

### Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

### Environment Setup

Create `backend/.env` (see `backend/.env.example`):

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-sonnet-4-6
DB_PATH=keel.db
REPORT_STORAGE_PATH=reports
```

### Build the database

```bash
cd backend
python setup_database.py     # creates keel.db with schema and sample data
```

### Run

Developer interface (simplest):
```bash
cd backend
streamlit run streamlit_app.py
```

Full stack:
```bash
# API
cd backend/api
python api_server.py

# Frontend (in another terminal)
cd frontend
npm run dev
```

## Project Structure

```
frontend/                     # Next.js app (pages, components, hooks, styles)
backend/
├── agents/                   # Agent definitions, creation, and strategies
├── api/                      # FastAPI app, endpoints, standalone server
├── config/                   # Settings and environment configuration
├── managers/                 # Chatbot, workflow, and scheduler managers
├── plugins/                  # Semantic Kernel plugins (schedule, risk, logging,
│                             #   report generation, web search, citations)
├── sql/                      # SQLite schema and sample data
├── utils/                    # Database helpers and Streamlit components
├── main.py                   # Entry point
├── setup_database.py         # Builds the local database
├── streamlit_app.py          # Developer UI
└── requirements.txt
```

## License

Licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.md) file for details.
