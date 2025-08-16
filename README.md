# Multi-Agent Board Emulation System

A minimal prototype demonstrating a multi-agent collaboration system for cancer case board reviews using Python, agent-based architecture, and Gemini LLM.

## Overview

This system simulates a tumor board where three medical specialists collaborate on cancer cases:

- **Oncologist**: Focuses on treatment plans and prognosis
- **Radiologist**: Provides imaging insights and metastasis assessment
- **Pathologist**: Analyzes biopsy results and tissue characteristics

## Features

- **Agent-Based Architecture**: Clean separation of concerns with specialized medical agents
- **LLM Integration**: Uses Gemini LLM for intelligent case analysis
- **Biomni Compatibility**: Integrates with Biomni framework when available
- **Fallback Support**: Works independently if Biomni is not installed
- **Structured Output**: Generates comprehensive case reviews and final decisions

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Gemini API Key

```bash
# On Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# On macOS/Linux
export GEMINI_API_KEY="your_api_key_here"
```

**Get your API key from**: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run the Simulation

```bash
python board_emulation.py
```

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Oncologist    │    │   Radiologist   │    │   Pathologist   │
│   Agent         │    │   Agent         │    │   Agent         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Tumor Board   │
                    │   Coordinator   │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Final Decision │
                    │   & Report      │
                    └─────────────────┘
```

## Code Structure

- **`MedicalAgent`**: Abstract base class for all medical specialists
- **`Oncologist`**: Specializes in treatment planning and prognosis
- **`Radiologist`**: Focuses on imaging interpretation
- **`Pathologist`**: Analyzes tissue and biopsy results
- **`TumorBoard`**: Coordinates all agents and generates final decisions
- **`PatientCase`**: Data structure for patient information

## Sample Output

```
🏥 Multi-Agent Tumor Board Emulation System
==================================================

============================================================
TUMOR BOARD REVIEW - Patient CASE-2024-001
============================================================

Oncologist Analysis:
----------------------------------------
Recommendation: [AI-generated treatment recommendation]

Radiologist Analysis:
----------------------------------------
Recommendation: [AI-generated imaging insights]

Pathologist Analysis:
----------------------------------------
Recommendation: [AI-generated pathological analysis]

============================================================
FINAL BOARD DECISION
============================================================
[AI-generated consolidated treatment plan]

============================================================
SIMULATION COMPLETE
============================================================
```

## Customization

### Adding New Agents

1. Create a new class inheriting from `MedicalAgent`
2. Implement the `analyze_case()` method
3. Add the agent to the `TumorBoard.agents` list

### Modifying Case Data

Edit the `create_sample_case()` function to include different patient scenarios.

### Changing LLM Models

Modify the `llm_model` parameter in agent constructors or update the default in `get_llm()`.

## Dependencies

- **Python 3.8+**
- **langchain-openai**: LLM integration framework
- **google-generativeai**: Google's Gemini API client
- **python-dotenv**: Environment variable management (optional)

## Troubleshooting

### API Key Issues

- Ensure `GEMINI_API_KEY` environment variable is set
- Verify the API key is valid and has sufficient quota

### Import Errors

- Install required packages: `pip install -r requirements.txt`
- Check Python version compatibility

### Network Issues

- Verify internet connection
- Check firewall/proxy settings

## Future Enhancements

- **Multi-case Support**: Process multiple patients in sequence
- **Agent Memory**: Persistent learning across cases
- **Web Interface**: Browser-based case review system
- **Integration**: Connect with real medical databases
- **Validation**: Medical accuracy verification systems

## License

This project is for educational and research purposes. Please ensure compliance with relevant medical and data privacy regulations when using in clinical settings.

## Contributing

Contributions are welcome! Please focus on:

- Code quality and documentation
- Medical accuracy improvements
- Performance optimizations
- Additional agent types
