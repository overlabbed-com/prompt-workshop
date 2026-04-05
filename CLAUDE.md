# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Is Prompt Workshop

Prompt Workshop is an open-source prompt engineering toolkit with time series forecasting. It's a self-improving system that measures, forecasts, and optimizes prompt performance across different roles and use cases.

## Features

- **Multiple Profiles**: Support for coding, support, analysis, creative, and technical prompts
- **PQI Scoring**: Composite quality index with profile-specific weights
- **Heuristic Analysis**: Pattern matching for tool announcements, verbose responses, menu patterns
- **Time Series Forecasting**: Cisco TSFM integration for 24-hour predictions
- **Attribution Engine**: Measure impact of prompt changes
- **Auto-Activation**: Starts working after 50 feedback entries

## Repository Structure

```
prompt-workshop/
├── src/
│   └── prompt_workshop/     # Main package
│       ├── __init__.py
│       ├── profile_registry.py
│       ├── pqi_calculator.py
│       ├── heuristics_analyzer.py
│       ├── forecasting.py
│       └── callbacks/
│           ├── litellm_handler.py
│           └── langchain_handler.py
├── pyproject.toml
└── README.md
```

## Development Commands

### Setup
```bash
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest tests/ -v
```

### Running a Single Test
```bash
pytest tests/test_pqi.py -v
```

### Code Formatting
```bash
black src/
ruff check src/
```

## Architecture

### Profile Registry

Manages prompt profiles with configuration for:
- Coding prompts
- Support prompts
- Analysis prompts
- Creative prompts
- Technical prompts

### PQI Calculator

Calculates the **Prompt Quality Index (PQI)** — a composite score with profile-specific weights:

```python
from prompt_workshop import ProfileRegistry, PQICalculator

registry = ProfileRegistry()
coding_profile = registry.get_profile("coding")

calculator = PQICalculator("coding")
metrics = {
    "tool_call_success": 0.97,
    "announcement_rate": 0.08,
    "avg_token_count": 3200,
    "verbose_no_tools_rate": 0.03,
    "menu_pattern_rate": 0.02,
    "error_rate": 0.02,
}
pqi, components = calculator.calculate(metrics)
```

### Heuristics Analyzer

Detects problematic patterns in prompt responses:
- Tool announcement spam
- Verbose responses without tool calls
- Menu repetition patterns

```python
from prompt_workshop import HeuristicsAnalyzer

analyzer = HeuristicsAnalyzer("coding")
flags = analyzer.analyze(
    response_text="I will now call the tool...",
    token_count=2000,
    tool_call_count=1
)
```

### Time Series Forecasting

Integrates with **Cisco TSFM** for 24-hour PQI predictions:
- Trend analysis
- Seasonality detection
- Anomaly warnings
- Optimization recommendations

### Callback Handlers

**LiteLLM Webhook**:
```yaml
callbacks:
  - prompt_workshop.PromptWorkshopCallbackHandler
```

**LangChain**:
```python
from prompt_workshop import LangChainCallbackHandler
handler = LangChainCallbackHandler(profile="analysis", prompt_name="research-assistant")
```

## Dependencies

### Core
- `requests` — HTTP client
- `numpy` — Numerical computations

### Development
- `pytest` — Testing framework
- `pytest-cov` — Coverage reporting
- `black` — Code formatting
- `ruff` — Linting

## Code Style

- Python 3.10+
- Line length: 100 (black, ruff)
- Type hints preferred

## Acknowledgments

Uses [Cisco Time Series Model](https://github.com/splunk/cisco-time-series-model) (Apache-2.0 license)

## License

MIT License
