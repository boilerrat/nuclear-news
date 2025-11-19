# Nuclear Industry Intelligence System

A CrewAI-based multi-agent system for aggregating, analyzing, and synthesizing information from the nuclear industry with a specialized focus on radiation safety and protection.

## Overview

The Nuclear Industry Intelligence System automates the discovery and synthesis of information from diverse sources including peer-reviewed journals, regulatory bodies, industry publications, and technical conferences. The system employs specialized AI agents that collaborate through a sequential workflow to transform raw information into comprehensive, well-formatted reports.

## Features

- **Multi-Agent Architecture**: Specialized agents for research, analysis, synthesis, and formatting
- **Comprehensive Source Coverage**: Discovers information from academic journals, regulatory bodies, industry publications, and conferences
- **Domain Expertise**: Focused on radiation safety and protection with proper technical terminology
- **Crawl4AI Integration**: Advanced web scraping with clean markdown output optimized for analysis
- **Structured Workflow**: Sequential process ensuring quality at each stage
- **Configurable**: YAML-based configuration for agents and tasks

## System Architecture

The system employs four specialized agents:

1. **Research Agent**: Discovers relevant information from diverse sources using web search and scraping
2. **Analysis Agent**: Evaluates content for relevance, significance, and quality
3. **Synthesis Agent**: Transforms analyzed information into coherent narratives
4. **Report Formatting Agent**: Formats final reports for distribution

## Installation

### Prerequisites

- Python 3.10 or later
- OpenAI API key
- Serper API key (for web search)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd nuclear-news
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `SERPER_API_KEY`: Your Serper API key for web search

## Usage

### Basic Usage

Run the system with a topic:

```bash
python -m nuclear_intelligence.main "ALARA implementation advances"
```

### Command-Line Options

```bash
python -m nuclear_intelligence.main <topic> [options]

Arguments:
  topic                 Topic or area of focus for intelligence gathering

Options:
  --time-window TEXT    Time window for information discovery (default: "past month")
  --output-dir PATH     Directory for output files (default: outputs/)
```

### Examples

```bash
# Search for recent dosimetry advances
python -m nuclear_intelligence.main "dosimetry advances" --time-window "past week"

# Search for regulatory updates
python -m nuclear_intelligence.main "NRC regulatory updates" --time-window "past month"

# Custom output directory
python -m nuclear_intelligence.main "contamination control" --output-dir ./reports
```

### Programmatic Usage

```python
from nuclear_intelligence.crew import NuclearIntelligenceCrew

# Initialize crew
crew = NuclearIntelligenceCrew()

# Execute workflow
result = crew.kickoff(
    topic="ALARA implementation",
    time_window="past month"
)
```

## Project Structure

```
nuclear-news/
├── src/
│   └── nuclear_intelligence/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── crew.py              # Main crew implementation
│       ├── config/
│       │   ├── agents.yaml      # Agent definitions
│       │   └── tasks.yaml       # Task definitions
│       └── tools/
│           └── crawl4ai_tool.py # Custom Crawl4AI tool
├── outputs/                     # Generated reports
├── tests/                       # Test files
├── pyproject.toml              # Project configuration
├── .env.example                # Environment variable template
└── README.md                   # This file
```

## Configuration

### Agents

Agent definitions are in `src/nuclear_intelligence/config/agents.yaml`. Each agent includes:
- Role: The agent's function
- Goal: Specific objectives
- Backstory: Expertise and perspective
- Tools: Assigned tools for the agent

### Tasks

Task definitions are in `src/nuclear_intelligence/config/tasks.yaml`. Tasks specify:
- Description: What the agent should accomplish
- Expected output: Format and content requirements
- Agent assignment: Which agent performs the task
- Context: Dependencies on previous tasks

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

The project uses:
- `black` for code formatting
- `ruff` for linting
- `mypy` for type checking

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type check
mypy src/
```

## Technology Stack

- **CrewAI**: Multi-agent orchestration framework
- **Crawl4AI**: Advanced web scraping with markdown output
- **OpenAI**: Language models for agent reasoning
- **Serper**: Web search API
- **Pydantic**: Data validation and schema definition

## Domain Focus

The system concentrates on the nuclear industry with emphasis on:
- Radiation detection and measurement technologies
- Dosimetry methods and instrumentation
- Contamination control procedures
- Shielding design and optimization
- Regulatory compliance and licensing
- Occupational health physics practices
- Environmental monitoring and assessment
- Emergency preparedness and response
- Decommissioning and waste management
- ALARA (As Low As Reasonably Achievable) implementation

## Quality Assurance

The system implements multiple quality assurance measures:
- Human review processes for output validation
- Automated quality checks for structure and content
- Continuous improvement based on feedback
- Technical accuracy validation

## Contributing

When contributing to this project, please follow the guidelines in `nuclear_intelligence_cursor_rules.md` and `nuclear_intelligence_technical_spec.md`.

## License

[Specify license]

## Support

For issues, questions, or contributions, please [specify contact method or issue tracker].


