# Keel Backend

The Keel backend is a modular, multi-agent system in which specialized AI agents collaborate through a shared reasoning log.

```
backend/
├── agents/                         # Agent code
│   ├── agent_definitions.py        # Agent instructions and constants
│   ├── agent_strategies.py         # Selection and termination strategies
│   └── agent_manager.py            # Agent creation and management
├── plugins/                        # Semantic Kernel plugins
│   ├── schedule_plugin.py          # Equipment schedule data
│   ├── risk_plugin.py              # Risk calculation
│   ├── logging_plugin.py           # Agent thinking and event logging
│   ├── report_file_plugin.py       # Report generation and local storage
│   ├── political_risk_json_plugin.py # Political risk data processing
│   ├── web_search_plugin.py        # Grounded web search for the risk agents
│   └── citation_handler_plugin.py  # Citation tracking from web search
├── managers/                       # High-level managers
│   ├── chatbot_manager.py          # Chat interactions
│   ├── workflow_manager.py         # Automated schedule analysis
│   └── scheduler.py                # Scheduled runs
├── api/                            # FastAPI app, endpoints, standalone server
├── config/                         # Settings and environment configuration
├── sql/                            # SQLite schema and sample data
├── utils/                          # Database helpers and Streamlit components
├── main.py                         # Entry point
├── setup_database.py               # Builds the local database
├── streamlit_app.py                # Developer UI
└── requirements.txt
```

## Core Components

### Specialized Agents

1. **Scheduler Agent** (`SCHEDULER_AGENT`)
   - Analyzes equipment schedule data and computes variances
   - Determines initial risk levels and prepares context for the risk agents

2. **Political / Tariff / Logistics Risk Agents**
   - Each owns one risk domain and runs grounded web search
   - Judge whether an event is material to a specific shipment
   - Return sourced assessments with citations

3. **Reporting Agent** (`REPORTING_AGENT`)
   - Consolidates findings, removes duplicates, ranks by impact
   - Generates a formatted Word report saved locally

4. **Assistant Agent** (`ASSISTANT_AGENT`)
   - Handles conversation flow and general queries

### Plugins

- **EquipmentSchedulePlugin** - retrieves and compares schedule data
- **RiskCalculationPlugin** - risk percentages and categorization
- **LoggingPlugin** - agent thinking and event logs (auditable trail)
- **ReportFilePlugin** - Word document generation and local storage
- **WebSearchPlugin** - grounded web search with citations
- **PoliticalRiskJsonPlugin** - structures risk analysis for storage

### Managers

- **ChatbotManager** - orchestrates agents for chat sessions, routes queries, manages state, and handles error recovery and rate limiting

## Running

```bash
# Build the database once
python setup_database.py

# Developer interface
streamlit run streamlit_app.py
```

## Interaction Patterns

Schedule / risk questions:
```
User Query -> SCHEDULER_AGENT -> REPORTING_AGENT -> Response
```

Political / tariff / logistics analysis:
```
User Query -> SCHEDULER_AGENT -> [RISK]_AGENT -> REPORTING_AGENT -> Response
```

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-sonnet-4-6
DB_PATH=keel.db
REPORT_STORAGE_PATH=reports
```
