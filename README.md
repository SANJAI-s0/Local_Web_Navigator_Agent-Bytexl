# Bytexplore

An AI-powered web navigation agent that interprets natural language instructions and autonomously performs browsing tasks on your local computer. This project uses a local large language model (Ollama) for parsing instructions, Playwright for browser automation, Tkinter for a graphical user interface (GUI), and supports voice input, task memory (via `memory.json`), error handling, and result exports (JSON/CSV). All operations are designed to run locally, minimizing cloud dependencies.

---

## Project Overview

This agent allows users to input commands like "search for laptops under 50k and list top 5," and it handles navigation, data extraction, and output generation. The interface is now a web-based application using Flask, accessible via a browser, replacing the previous Tkinter GUI. Task history is stored in `memory.json` for task chaining, replacing the earlier SQLite database approach.

### Core Features

- **Instruction Parsing**: Uses Ollama (local LLM) to break down commands into actionable steps.
- **Browser Control**: Automates headless Chrome via Playwright for navigation, typing, form submission, and data extraction.
- **Task Execution**: Supports multi-step tasks like searching, extracting results, and exporting data.
- **Output**: Displays results in a web interface and exports to `results.json` and `results.csv`.
- **Local Setup**: Runs offline after setup (internet needed for web tasks and initial model download); the Flask app runs locally on port 5000.

### Additional Features

- Multi-step reasoning and task chaining using `memory.json`
- Error handling with retry logic
- Web-based UI (Flask) for user interaction, accessible at `http://localhost:5000`
- Voice input support (requires microphone and internet for speech recognition)
- Compatible with Python 3.10+ (tested on 3.12.8 with Flask 3.0.3)

---

## Prerequisites

- **Operating System**: Windows 11 (tested on Asus Vivobook X1500EA)
- **Python**: Version 3.10 or higher (recommended 3.12.8)
- **Ollama**: Version 0.12.3 or later (from [ollama.ai](https://ollama.ai))
- **Flask**: Version 3.0.3 (for web interface)
- **Memory**: Minimum 4 GB RAM (8 GB recommended)
- **Storage**: ~10 GB free space for models and dependencies
- **Internet**: Required for initial setup, model download, web tasks, and Flask server
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

```bash
ollama pull <model>
```

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
python -m webagent.main
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
│   ├── main.py
│   └── templates/
│       └── index.html  # Flask HTML template
├── data/
│   ├── memory.json
│   ├── results.json
│   └── results.csv
├── requirements.txt
├── README.md
└── .gitignore
```
Search. 
---

## Usage Examples

Enter commands like:

**Basic search commands:**
"Search for laptops under 50000 INR"
"Find best smartphones in 2025"
"Look for latest programming books"

**E-commerce specific:**
"Search for wireless headphones on Amazon and list top 5 results"
"Find best deals on smart watches under 10000 INR"
"Show me the latest deals on gaming laptops"

**Information extraction:**
"Extract the top 5 news headlines from timesofindia.com"
"Get the latest technology news from example.com"
"Find and list the main points from Wikipedia's AI article"

**Form filling tasks:**
"Fill the contact form on example.com with my details"
"Search for Python programming courses and fill the inquiry form"

**Multi-step commands:**
"Search for budget smartphones, extract their prices and save to CSV"
"Find laptop deals, list specifications and export to JSON"

**Voice command examples:**
"Hey, search for best budget smartphones"
"Find me deals on wireless earbuds"

**Technical searches:**
"Search for latest AI research papers"
"Find information about machine learning algorithms"

**Comparison tasks:**
"Compare prices of iPhone 15 and Samsung Galaxy S23"
"Show me different models of smart TVs with their specifications"

**Local service searches:**
"Find best restaurants near me"
"Search for electronics repair shops in Bangalore"

**Educational queries:**
"Find online courses for data science"
"Search for best programming tutorials for beginners"

View results in GUI or check output files:

- `results.json` - Structured output
- `results.csv` - CSV format
- `memory.json` - Task history

---
## Customization Options

- **Model Selection**: Modify `agent.py` to use different models based on system specs
- **Browser Actions**: Extend `browser_controller.py` for additional websites
- **UI Modifications**: Customize `templates/index.html` for different interface layouts or add static CSS/JS in a `static` folder
---
Read me.
## Troubleshooting

| Issue | Solution |
|--------|-----------|
| **Port Conflict** | If Ollama fails to start, check if port 11435 is in use; for Flask, ensure port 5000 is free |
| **Memory Issues** | Use `tinyllama` instead of `phi3` on low-memory systems |
| **Voice Input Errors** | Ensure microphone is properly configured and internet is available |
| **Flask Not Loading** | Verify `templates/index.html` exists and dependencies are installed |

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
