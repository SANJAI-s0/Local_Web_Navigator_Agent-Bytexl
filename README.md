# Local_Web_Navigator_Agent-Bytexl

An AI-powered web navigation agent that interprets natural language instructions and autonomously performs browsing tasks on your local computer. This project uses a local large language model (Ollama) for parsing instructions, Playwright for browser automation, Tkinter for a graphical user interface (GUI), and supports voice input, task memory (via `memory.json`), error handling, and result exports (JSON/CSV). All operations are designed to run locally, minimizing cloud dependencies.

## Project Overview
This agent allows users to input commands like "search for laptops under 50k and list top 5," and it handles navigation, data extraction, and output generation without requiring internet connectivity beyond the initial setup and web tasks. Task history is stored in `memory.json` for task chaining, replacing the earlier SQLite database approach.

### Core Features
- **Instruction Parsing**: Uses Ollama (local LLM) to break down commands into actionable steps.
- **Browser Control**: Automates headless Chrome via Playwright for navigation, typing, form submission, and data extraction.
- **Task Execution**: Supports multi-step tasks like searching, extracting results, and exporting data.
- **Output**: Displays results in a GUI and exports to `results.json` and `results.csv`.
- **Local Setup**: Runs offline after setup (internet needed for web tasks and initial model download).

### Additional Features
- Multi-step reasoning and task chaining using `memory.json`.
- Error handling with retry logic.
- Simple GUI (Tkinter) for user interaction.
- Voice input support (requires microphone and internet for speech recognition).
- Compatible with Python 3.10+ (tested on 3.12.8).

## Prerequisites
- **Operating System**: Windows 11 (tested on Asus Vivobook X1500EA).
- **Python**: Version 3.10 or higher (recommended 3.12.8).
- **Ollama**: Version 0.12.3 or later (from [ollama.ai](https://ollama.ai)).
- **Memory**: Minimum 4 GB RAM (8 GB recommended); may require page file adjustment for low-memory systems.
- **Storage**: ~10 GB free space for models and dependencies.
- **Internet**: Required for initial setup, model download, and web tasks.
- **Microphone**: Optional, for voice input (requires PyAudio and portaudio dependencies).

## Setup Instructions

### Step 1: Clone the Repository
Clone the project from GitHub to your local machine:

```powershell
git clone https://github.com/SANJAI-s0/Local_Web_Navigator_Agent-Bytexl.git
cd Local_Web_Navigator_Agent-Bytexl
```

### Step 2: Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

- Verify Python version:
  ```powershell
  python --version
  ```
  - Ensure it outputs "Python 3.12.8" or a compatible version.

### Step 3: Install Dependencies
Install the required Python packages and Playwright browser binaries:

```powershell
pip install -r requirements.txt
playwright install
```

- **Note**: If voice input fails later, install PyAudio and portaudio:
  - Open PowerShell as Administrator:
    ```powershell
    choco install portaudio
    pip install pyaudio
    ```
  - Or use a prebuilt wheel:
    ```powershell
    pip install PyAudio-0.2.14-cp312-cp312-win_amd64.whl
    ```

### Step 4: Install and Configure Ollama
Ollama is used for local language model processing. Follow these steps:

1. **Install Ollama**:
   - Download and install Ollama from [ollama.ai](https://ollama.ai) for Windows.
   - Verify installation:
     ```powershell
     ollama --version
     ```
     - Expected output: "ollama version 0.12.3" or later.

2. **Start Ollama Server on Custom Port (11435)**:
   - Due to potential port 11434 conflicts, configure Ollama to use port 11435:
     ```powershell
     $env:OLLAMA_HOST="127.0.0.1:11435"
     ollama serve
     ```
   - Keep this terminal open. Verify the server is running:
     ```powershell
     netstat -aon | findstr :11435
     ```
     - Expected output: `TCP 127.0.0.1:11435 0.0.0.0:0 LISTENING <PID>`.

3. **Download a Model**:
   - Choose a model based on your system’s RAM:
     - **Recommended for 4 GB RAM**: `tinyllama` (~1.1 GB disk, ~2 GB RAM).
     - **For 8 GB+ RAM**: `phi3` (~2.2 GB disk, ~3.8 GB RAM).
   - Download and load the model:
     ```powershell
     $env:OLLAMA_HOST="127.0.0.1:11435"
     ollama run tinyllama
     ```
     - Type `exit` after the model loads. Verify:
       ```powershell
       ollama list
       ```
     - If using `phi3` and memory is insufficient (e.g., 2.9 GB available vs. 3.8 GB needed), increase the page file (see Step 5).

### Step 5: Adjust Virtual Memory (Optional for Low RAM)
If `phi3` fails due to insufficient memory:
- Open System Properties:
  ```powershell
  sysdm.cpl
  ```
- Go to **Advanced** tab > **Performance** > **Settings** > **Advanced** > **Virtual Memory** > **Change**.
- Uncheck "Automatically manage paging file size for all drives."
- Select **C:** drive, choose **Custom size**.
- Set **Initial size** to 8000 MB and **Maximum size** to 16000 MB.
- Click **Set**, then **OK**, and restart your computer.
- Verify after reboot:
  ```powershell
  systeminfo | findstr "Total Physical Memory"
  systeminfo | findstr "Virtual Memory"
  ```

### Step 6: Run the Application
Launch the application with the virtual environment activated:

```powershell
cd Z:\git_bytexl_hackathon\webagent
.\venv\Scripts\activate
$env:OLLAMA_HOST="127.0.0.1:11435"
python webagent\main.py
```

- A GUI window will appear. Enter a command (e.g., "search for laptops under 50k and list top 5") and click "Execute".
- Check `results.json`, `results.csv`, and `memory.json` for output.
- For voice input, click "Voice Input" and speak (requires internet for speech recognition).

### Step 7: Run Tests (Optional)
Run unit tests to verify functionality:

```powershell
cd Z:\git_bytexl_hackathon\webagent
.\venv\Scripts\activate
$env:OLLAMA_HOST="127.0.0.1:11435"
pytest tests/
```

- Expected output will show test results. Fix any import errors by ensuring `tests/test_agent.py` and `tests/test_browser_controller.py` import from `webagent.agent` and `webagent.browser_controller`.

## Project Structure
- `webagent/`
  - `__init__.py`: Marks `webagent` as a package.
  - `agent.py`: Core agent logic (parsing, execution, JSON memory).
  - `browser_controller.py`: Playwright-based browser wrappers.
  - `main.py`: GUI entry point and input processing.
- `tests/`
  - `test_agent.py`: Tests for agent functionality.
  - `test_browser_controller.py`: Tests for browser control.
- `requirements.txt`: Dependency list.
- `README.md`: This file.
- `memory.json`: Task history storage (auto-created).
- `results.json`, `results.csv`: Output files (auto-created).
- `.venv/`: Virtual environment directory.

## Task Allocation for our "The One" Team of 5 Members

### Jacob Antony: Project Lead and Team Management
**Responsibilities:**
- Oversee the overall project progress and coordinate with the team.
- Maintain and enhance webagent/agent.py (e.g., refine the parse_instruction and execute_plan methods for better accuracy and error handling).
- Ensure the integration of memory.json for task history works seamlessly.
- Address any syntax errors (e.g., the recent SyntaxError fix) and optimize for low-memory systems (e.g., switch between tinyllama and phi3 based on RAM availability).

### Member 2:  Core Logic Developer and Browser Automation
**Responsibilities:**
- Manage webagent/browser_controller.py to improve browser automation (e.g., add support for more websites by expanding map_selector).
- Enhance the Tkinter GUI in webagent/main.py (e.g., add buttons for saving/export options or a status bar).
- Debug browser-related issues (e.g., set headless=False for visual troubleshooting).

### Member 3: UI Developer and Designs
**Responsibilities:**
- Develop and maintain test cases in tests/test_agent.py and tests/test_browser_controller.py.
- Run pytest tests/ to ensure functionality after code changes.
- Identify and report bugs, especially related to memory constraints or Ollama integration.

### Member 4: Documentation and Support
**Responsibilities:**
- Maintain and update the README.md with new features, troubleshooting tips, or team contributions.
- Assist with setup documentation for team members (e.g., clarify Ollama port 11435 setup).
- Support deployment by documenting environment-specific steps (e.g., page file adjustment for low RAM).

### Member 5:  Testing, Quality Assurance and Additional Features
**Responsibilities:**
- Implement and test voice input functionality in webagent/main.py (e.g., ensure speech_recognition and PyAudio work).
- Explore additional features like offline voice recognition (e.g., integrating Vosk) or result visualization.
- Assist with dependency installation troubleshooting (e.g., PyAudio or portaudio issues).

## Usage
1. Run the application as described in Step 6.
2. Enter a command in the GUI (e.g., "search for laptops under 50k and list top 5").
3. View results in the GUI or exported files.
4. For debugging, set `headless=False` in `webagent/main.py`:
   ```python
   browser = BrowserController(headless=False)
   ```

## Customization
- Extend selectors in `webagent/agent.py` for additional websites.
- Add new actions in `webagent/browser_controller.py`.
- For offline voice input, replace `recognize_google` with Vosk (requires additional setup).

## Limitations
- Extraction may fail if website layouts change (update selectors).
- Voice input requires internet (Google API).
- Best suited for simple tasks; complex sites need custom logic.
- Low-memory systems (e.g., 4 GB RAM) may require `tinyllama` or page file adjustment.

## Troubleshooting
- **Port 11434 Conflict**: If `ollama serve` fails, ensure port 11434 is free:
  ```powershell
  netstat -aon | findstr :11434
  tasklist | findstr <PID>
  taskkill /PID <PID> /F
  ```
- **Memory Issues**: Increase page file or use `tinyllama` if `phi3` fails.
- **Parsing Errors**: Ensure Ollama server is running and the model is loaded before starting `main.py`.

## Contributing
Fork the repository, make changes, and submit a pull request. Issues and suggestions are welcome!

## License
MIT License (feel free to modify).
