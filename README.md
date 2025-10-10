# Bytexplore

An AI-powered web navigation agent that interprets natural language instructions and autonomously performs browsing tasks on your local computer. This project uses a local large language model (Ollama) for parsing instructions, Playwright for browser automation, Tkinter for a graphical user interface (GUI), and supports voice input, task memory (via `memory.json`), error handling, and result exports (JSON/CSV). All operations are designed to run locally, minimizing cloud dependencies.

---

## Project Overview

This agent allows users to input commands like "search for laptops under 50k and list top 5," and it handles navigation, data extraction, and output generation without requiring internet connectivity beyond the initial setup and web tasks. Task history is stored in `memory.json` for task chaining, replacing the earlier SQLite database approach.

### Core Features

- **Instruction Parsing**: Uses Ollama (local LLM) to break down commands into actionable steps
- **Browser Control**: Automates headless Chrome via Playwright for navigation, typing, form submission, and data extraction
- **Task Execution**: Supports multi-step tasks like searching, extracting results, and exporting data
- **Output**: Displays results in a GUI and exports to `results.json` and `results.csv`
- **Local Setup**: Runs offline after setup (internet needed for web tasks and initial model download)

### Additional Features

- Multi-step reasoning and task chaining using `memory.json`
- Error handling with retry logic
- Simple GUI (Tkinter) for user interaction
- Voice input support (requires microphone and internet for speech recognition)
- Compatible with Python 3.10+ (tested on 3.12.8)

---

## Prerequisites

- **Operating System**: Windows 11 (tested on Asus Vivobook X1500EA)
- **Python**: Version 3.10 or higher (recommended 3.12.8)
- **Ollama**: Version 0.12.3 or later (from [ollama.ai](https://ollama.ai))
- **Memory**: Minimum 4 GB RAM (8 GB recommended)
- **Storage**: ~10 GB free space for models and dependencies
- **Internet**: Required for initial setup, model download, and web tasks
- **Microphone**: Optional, for voice input (requires PyAudio and portaudio dependencies)

---

## Setup Instructions

### Step 1: Clone the Repository
```powershell
git clone https://github.com/SANJAI-s0/Bytexplore.git
cd Bytexplore
```

### Step 2: Set Up Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
playwright install
```

For voice input support:
```powershell
choco install portaudio
pip install pyaudio
```

### Step 4: Install and Configure Ollama

1. Download and install Ollama from [ollama.ai](https://ollama.ai)
2. Start the Ollama server on port 11435:

```powershell
$env:OLLAMA_HOST="127.0.0.1:11435"
ollama serve
```

3. Download the appropriate model based on your RAM:

- For 4GB RAM: `ollama run tinyllama`
- For 8GB+ RAM: `ollama run phi3`

### Step 5: Adjust Virtual Memory (For Low RAM Systems)

- Open System Properties: `sysdm.cpl`
- Set custom page file size:
  - Initial: 8000 MB
  - Maximum: 16000 MB

### Step 6: Run the Application
```powershell
.\.venv\Scripts\activate
$env:OLLAMA_HOST="127.0.0.1:11435"
python webagent\main.py
```

### Step 7: Run Tests (Optional)
```powershell
python -m pytest tests/
```

---

## Project Structure
```bash
Bytexplore/
├── webagent/
│   ├── __init__.py
│   ├── agent.py
│   ├── browser_controller.py
│   └── main.py
├── tests/
│   ├── test_agent.py
│   └── test_browser_controller.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Usage Examples

Enter commands like:

```text
"search for laptops under 50k and list top 5"
"extract headlines from example.com"
```

View results in GUI or check output files:

- `results.json` - Structured output
- `results.csv` - CSV format
- `memory.json` - Task history

---

## Customization Options

- **Model Selection**: Modify `agent.py` to use different models based on system specs
- **Browser Actions**: Extend `browser_controller.py` for additional websites
- **UI Modifications**: Customize `main.py` for different interface layouts

---

## Troubleshooting

| Issue | Solution |
|--------|-----------|
| **Port Conflict** | If Ollama fails to start, check if port 11435 is already in use |
| **Memory Issues** | Use `tinyllama` instead of `phi3` on low-memory systems |
| **Voice Input Errors** | Ensure microphone is properly configured and internet is available |

---

## Team Roles

| Role | Member | Responsibility |
|------|---------|----------------|
| **Project Lead** | Jacob Antony | Overall coordination and submission |
| **Core Developer** | Sanjai | Logic implementation and browser automation |
| **UI Designer** | Madhumitha | Interface development |
| **Documentation** | Gayathri | README and setup guides |
| **Testing** | Ghobika | Quality assurance and test cases |

---

## License

**MIT License** — Free to modify and distribute.

---

> This consolidated version includes all the essential setup, configuration, and usage details for end-to-end local execution.