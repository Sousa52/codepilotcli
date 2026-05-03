import sys
import os
import subprocess
import requests
import threading
import itertools
import time

from colorama import Fore, Style, init

init()

# File utilities

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def get_git_diff():
    result = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        text=True
    )
    return result.stdout


def get_project_files():
    files_content = []

    for root, dirs, files in os.walk("."):
        # skip heavy / irrelevant folders
        if "venv" in root or ".git" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()

                    files_content.append(f"\n--- {path} ---\n{content}")

                except:
                    pass

    return "\n".join(files_content)

# AI call (shared)

spinner_state = {"stop": False}


def spinner():
    for frame in itertools.cycle(["|", "/", "-", "\\"]):
        if spinner_state["stop"]:
            break
        sys.stdout.write("\r" + Fore.YELLOW + "Thinking " + frame + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.1)


def stop_spinner_clean(thread):
    spinner_state["stop"] = True
    thread.join()
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


def ask_ai(prompt):
    spinner_state["stop"] = False

    thread = threading.Thread(target=spinner)
    thread.start()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        stop_spinner_clean(thread)

        if response.status_code != 200:
            return Fore.RED + f"HTTP Error {response.status_code}" + Style.RESET_ALL

        try:
            data = response.json()
        except ValueError:
            return Fore.RED + "Invalid JSON response from Ollama." + Style.RESET_ALL

        if data.get("response"):
            return data["response"].strip()

        if data.get("error"):
            return Fore.RED + f"AI Error: {data['error']}" + Style.RESET_ALL

        return Fore.RED + "Unexpected response from AI model." + Style.RESET_ALL

    except requests.exceptions.ConnectionError:
        stop_spinner_clean(thread)
        return Fore.RED + "Cannot connect to Ollama. Run: ollama serve" + Style.RESET_ALL

    except requests.exceptions.Timeout:
        stop_spinner_clean(thread)
        return Fore.RED + "Request timed out. Model is too slow." + Style.RESET_ALL

    except Exception as e:
        stop_spinner_clean(thread)
        return Fore.RED + f"Unexpected error: {str(e)}" + Style.RESET_ALL
    
# Features

def format_output(title, content):
    return (
        Fore.CYAN + "\n====================\n" +
        f"{title}\n" +
        "====================\n\n" +
        Style.RESET_ALL +
        content +
        Fore.CYAN + "\n\n====================\n" +
        Style.RESET_ALL
    )

def explain_code(file_path):
    code = read_file(file_path)

    if code is None:
        return

    prompt = f"""
You are a senior software engineer.

Explain this code simply and clearly:

{code}
"""

    return format_output("🧠 CODE EXPLANATION", ask_ai(prompt))


def generate_commit_message(diff):
    prompt = f"""
You are an expert software engineer.

Write a clear, concise git commit message for this change:

{diff}

Rules:
- Use imperative tone (Fix, Add, Remove, Improve)
- Keep it under 1 sentence
"""

    return format_output("🧾 COMMIT MESSAGE", ask_ai(prompt))


def summarize_project():
    project_code = get_project_files()

    if not project_code.strip():
        return format_output("📦 PROJECT SUMMARY", "No Python files found.")

    prompt = f"""
You are a senior software engineer.

Explain what this project does in simple terms.

Here is the full codebase:

{project_code}
"""

    return format_output("📦 PROJECT SUMMARY", ask_ai(prompt))

# CLI entry point

def main():
    if len(sys.argv) < 2:
        print("\nCodePilot CLI")
        print("====================")
        print("Usage: codepilot <command> [args]\n")
        print("Commands:")
        print("  explain <file>     Explain a Python file")
        print("  commit             Generate git commit message")
        print("  summarize          Summarize entire project\n")
        return

    command = sys.argv[1]

    # explain file
    if command == "explain":
        if len(sys.argv) < 3:
            print("Usage: codepilot explain <file>")
            return

        file_path = sys.argv[2]
        result = explain_code(file_path)
        print(result)

    # git commit message
    elif command == "commit":
        diff = get_git_diff()

        if not diff.strip():
            print("No changes detected.")
            return

        result = generate_commit_message(diff)
        print(result)

    # summarize project
    elif command == "summarize":
        result = summarize_project()
        print(result)

    else:
        print(f"Unknown command: {command}")
        print("Use: codepilot explain | commit | summarize")


if __name__ == "__main__":
    main()