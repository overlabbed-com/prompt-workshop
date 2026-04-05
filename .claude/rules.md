# Prompt Workshop-Specific Governance Rules

These rules augment the root `.claude/rules/` governance framework. They NEVER weaken those policies.

## Project Context

Prompt Workshop is an open-source prompt engineering toolkit with time series forecasting. Measures, forecasts, and optimizes prompt performance across different roles.

**Key constraints:**
- PQI (Prompt Quality Index) scoring with profile-specific weights
- Heuristic analysis for pattern detection
- Cisco TSFM integration for 24-hour predictions
- LiteLLM and LangChain callback handlers
- Auto-activation after 50 feedback entries

## Security Requirements

### API Key Handling
- **NEVER hardcode API keys** in source code
- All LLM API keys come from environment variables
- Callback handlers MUST sanitize logs (no prompt/response leakage)
- Webhook URLs validated before use (no internal network access)

### Data Privacy
- Prompt feedback data anonymized before storage
- No PII in heuristic analysis outputs
- Time series data aggregated before forecasting

### External Requests
- All LLM API calls use HTTPS only
- TLS certificate verification enabled
- Rate limiting respected (configurable per provider)

## Development Workflow

### Adding a New Profile
1. Create profile config in `profiles/<name>.yaml`
2. Define PQI weight schema for the profile
3. Implement heuristic detectors specific to profile
4. Add unit tests for PQI calculation
5. Document profile purpose and use cases

### Adding a New Heuristic Detector
1. Implement detector in `heuristics/<detector>.py`
2. Define trigger conditions and severity levels
3. Add test cases with sample responses
4. Register detector in `HeuristicsAnalyzer`
5. Document false positive mitigation

### Adding a New Callback Handler
1. Implement handler extending base class
2. Handle lifecycle events (start, success, error)
3. Extract metrics (token count, latency, tool calls)
4. Sanitize sensitive data before storage
5. Write integration test with mock LLM

## PQI Calculation

### Profile-Specific Weights

| Profile | Tool Success | Announcement | Tokens | Verbose | Error |
|---------|-------------|--------------|--------|---------|-------|
| **coding** | 40% | 10% | 15% | 15% | 20% |
| **support** | 30% | 15% | 10% | 20% | 25% |
| **analysis** | 25% | 10% | 20% | 15% | 30% |
| **creative** | 20% | 15% | 10% | 10% | 15% |
| **technical** | 35% | 10% | 15% | 15% | 25% |

### PQI Formula
```
PQI = Σ(weight_i × normalized_metric_i) × 100
```

Where:
- `tool_call_success`: 0-1 scale (higher = better)
- `announcement_rate`: 0-1 scale (lower = better, inverted)
- `avg_token_count`: normalized against profile baseline
- `verbose_no_tools_rate`: 0-1 scale (lower = better, inverted)
- `error_rate`: 0-1 scale (lower = better, inverted)

## Heuristic Detection

### Built-in Detectors

| Detector | Triggers On | Severity |
|----------|-------------|----------|
| `tool_announcement` | "I will now call..." patterns | Medium |
| `verbose_no_tools` | High token count, zero tool calls | High |
| `menu_repetition` | Same menu offered 3+ times | Medium |
| `error_suppression` | Caught exceptions not logged | High |
| `tool_call_fail` | Tool called but error returned | Critical |

### Custom Detector Registration
```python
from prompt_worksheet import HeuristicsAnalyzer

analyzer = HeuristicsAnalyzer("coding")
analyzer.register_detector(MyCustomDetector())
```

## Time Series Forecasting

### Cisco TSFM Integration
- Input: Daily PQI measurements per profile
- Output: 24-hour forecast with confidence intervals
- Retraining: Automatic when data drift detected

### Forecast Triggers
- PQI drops below profile threshold → alert
- Seasonal pattern detected → adjust baseline
- Anomaly detected → investigate root cause

## Testing Requirements

### Unit Tests
- PQI calculation accuracy (known inputs → expected outputs)
- Heuristic detector trigger conditions
- Profile weight normalization

### Integration Tests
- LiteLLM callback end-to-end
- LangChain callback end-to-end
- Time series forecast generation

### Performance Tests
- PQI calculation: <1ms per measurement
- Heuristic analysis: <10ms per response
- Forecast generation: <100ms

## Configuration

### Environment Variables
| Variable | Purpose | Required |
|----------|---------|----------|
| `PQI_BASELINE_CODING` | Token baseline for coding profile | No |
| `PQI_BASELINE_SUPPORT` | Token baseline for support profile | No |
| `TSFM_MODEL_PATH` | Path to Cisco TSFM model | No |
| `FEEDBACK_THRESHOLD` | Entries before auto-activation | No (default: 50) |

### Profile Schema
```yaml
name: coding
description: Code generation and debugging
weights:
  tool_call_success: 0.40
  announcement_rate: 0.10
  avg_token_count: 0.15
  verbose_no_tools_rate: 0.15
  error_rate: 0.20
thresholds:
  pqi_warning: 70
  pqi_critical: 50
heuristics:
  - tool_announcement
  - verbose_no_tools
  - menu_repetition
```

## Failure Modes

| Symptom | Root Cause | Remediation |
|---------|-----------|-------------|
| PQI spikes unexpectedly | Baseline drift | Recalculate baseline with rolling window |
| Heuristic false positives | Overly broad pattern | Tighten regex, add whitelist |
| Forecast fails | Insufficient data | Require minimum 30 days before forecasting |
| Callback handler errors | LLM response format change | Update parser, add schema validation |

## Attribution Engine

### Measuring Impact
- A/B test prompts with controlled variables
- Track PQI delta before/after changes
- Attribute improvement to specific modifications

### Attribution Schema
```json
{
  "prompt_id": "coding-debugger-v2",
  "before_pqi": 72.3,
  "after_pqi": 78.1,
  "delta": 5.8,
  "changes": ["added_tool_definition", "reduced_temperature"],
  "confidence": 0.85
}
```
