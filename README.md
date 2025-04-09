# 

# ⚡ LINGOGPT

This project is a full-stack application that uses:

- 🐍 A **Python server** (located in `server/`)
- 🌐 A **React TS frontend** (located in `client/`)
- 🛠 Simple setup and start scripts to make running the app easy

---

## 🚀 Getting Started

### 1. Install Dependencies

Run the `install.sh` script to install all required packages for both the **backend** and **frontend**.

```bash
  ./install.sh
```

This will:

- ✅ Activate your Python virtual environment (`server/venv/`)
- ✅ Install Python dependencies from `server/requirements.txt`
- ✅ Install frontend dependencies via `npm install` in the `client/` directory

---

### 2. Start the Application

Once dependencies are installed, launch the full application with:

```bash
./start.sh
```

This script will:

- 🧠 Activate the Python virtual environment
- 🐍 Start the Python backend server (`server/main.py`) in the background
- 💻 Navigate to the React frontend (`client/`) and run `npm run dev`

You’ll now be able to interact with the app via your browser at:

```
http://localhost:5174
```

---


## 🖥️ Development Tips

### Virtual Environment

Create your Python virtual environment:

```bash
python -m venv server/venv
```

Activate it:

- On **Linux/macOS**:
  ```bash
  source server/venv/bin/activate
  ```
- On **Windows**:
  ```bash
  server\venv\Scripts\activate
  ```

### Windows Users

If you're using **Windows**, run the `.sh` scripts with:

- [Git Bash](https://gitforwindows.org/)
- [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install)

If you prefer PowerShell, use the equivalent `.ps1` versions if provided.

---

## ✅ Example Workflow

```bash
# First-time setup
python -m venv server/venv
./install.sh

# Each time you want to start the app
./start.sh
```
n issue or submit a PR to improve the project!