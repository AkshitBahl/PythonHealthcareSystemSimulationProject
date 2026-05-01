#!/usr/bin/env python3
"""
Healthcare System Simulator - Launcher
======================================
This script launches both the FastAPI backend and the Next.js frontend
in a single command as requested.

Requirements:
- Python 3.10+
- Node.js & npm
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path


def check_and_install_python_deps():
    """Install Python dependencies if fastapi or uvicorn are missing."""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("[Python] Dependencies already installed.")
    except ImportError:
        print("[Python] Installing dependencies from requirements.txt...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("[Python] Dependencies installed successfully.")


def check_and_install_node_deps(frontend_dir: Path):
    """Install Node.js dependencies if node_modules does not exist."""
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("[Node] node_modules not found. Running npm install...")
        subprocess.check_call(["npm", "install"], cwd=frontend_dir)
        print("[Node] Dependencies installed successfully.")
    else:
        print("[Node] Dependencies already installed.")


def run_services():
    """Run the backend and frontend processes simultaneously."""
    root_dir = Path(__file__).parent.absolute()
    frontend_dir = root_dir / "frontend"

    # 1. Dependency checks
    check_and_install_python_deps()
    if frontend_dir.exists():
        check_and_install_node_deps(frontend_dir)
    else:
        print("ERROR: frontend directory not found. Please ensure it is created.")
        sys.exit(1)

    # 2. Define commands
    backend_cmd = [sys.executable, "-m", "uvicorn", "backend.app:app", "--reload", "--port", "8000"]
    frontend_cmd = ["npm", "run", "dev"]

    frontend_proc = None
    backend_proc = None

    try:
        # 3. Start Backend
        print("\n\033[94m➤ Starting FastAPI backend (Port 8000)...\033[0m")
        backend_proc = subprocess.Popen(
            backend_cmd,
            cwd=root_dir,
        )

        # 4. Start Frontend
        print("\033[94m➤ Starting Next.js frontend (Port 3000)...\033[0m")
        frontend_proc = subprocess.Popen(
            frontend_cmd,
            cwd=frontend_dir,
        )

        # 5. Open Browser (wait 5 sec for Next.js to start)
        print("\033[92m➤ Waiting for frontend to compile...\033[0m")
        time.sleep(5)
        webbrowser.open("http://localhost:3000")

        input("\n\033[92m[Services Running] Press Enter or Ctrl+C to terminate both servers...\033[0m\n")

    except KeyboardInterrupt:
        pass
    finally:
        print("\n\033[93m➤ Stopping services...\033[0m")
        if frontend_proc:
            frontend_proc.terminate()
            frontend_proc.wait()
            print("[Next.js] Stopped")
        if backend_proc:
            backend_proc.terminate()
            backend_proc.wait()
            print("[FastAPI] Stopped")

        print("\033[92m➤ All services stopped safely.\033[0m")


if __name__ == "__main__":
    run_services()
