# Prompt Workshop

Open-source prompt engineering toolkit with time series forecasting.

A self-improving prompt engineering system that measures, forecasts, and optimizes prompt performance across different roles and use cases.

## Features

- **Multiple Profiles**: Support for coding, support, analysis, creative, and technical prompts
- **PQI Scoring**: Composite quality index with profile-specific weights
- **Heuristic Analysis**: Pattern matching for tool announcements, verbose responses, menu patterns
- **Time Series Forecasting**: Cisco TSFM integration for 24-hour predictions
- **Attribution Engine**: Measure impact of prompt changes
- **Auto-Activation**: Starts working after 50 feedback entries

## Installation

```bash
pip install prompt-workshop
```

## Quick Start

```python
from prompt_workshop import ProfileRegistry, PQICalculator, HeuristicsAnalyzer

# Get a profile
registry = ProfileRegistry()
coding_profile = registry.get_profile("coding")

# Calculate PQI
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
print(f"PQI: {pqi:.1f}")

# Analyze heuristics
analyzer = HeuristicsAnalyzer("coding")
flags = analyzer.analyze(response_text="I will now call the tool...", token_count=2000, tool_call_count=1)
print(f"Flags: {flags}")
```

## Integration

### LiteLLM Webhook
```yaml
callbacks:
  - prompt_workshop.PromptWorkshopCallbackHandler
```

### LangChain
```python
from prompt_workshop import LangChainCallbackHandler
handler = LangChainCallbackHandler(profile="analysis", prompt_name="research-assistant")
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Uses [Cisco Time Series Model](https://github.com/splunk/cisco-time-series-model) (Apache-2.0 license)
