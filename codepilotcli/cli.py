import sys
import requests
import subprocess
import os

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

def ask_ai(prompt):
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

        data = response.json()

        if "response" in data:
            return data["response"]

        if "error" in data:
            return f"AI Error: {data['error']}"

        return f"Unexpected response: {data}"

    except Exception as e:
        return f"Request failed: {str(e)}"

# Features

def explain_code(file_path):
    code = read_file(file_path)

    if code is None:
        return

    prompt = f"""
You are a senior software engineer.

Explain this code simply and clearly:

{code}
"""

    return ask_ai(prompt)


def generate_commit_message(diff):
    prompt = f"""
You are an expert software engineer.

Write a clear, concise git commit message for this change:

{diff}

Rules:
- Use imperative tone (Fix, Add, Remove, Improve)
- Keep it under 1 sentence
"""

    return ask_ai(prompt)


def summarize_project():
    project_code = get_project_files()

    if not project_code.strip():
        return "No Python files found."

    prompt = f"""
You are a senior software engineer.

Explain what this project does in simple terms.

Here is the full codebase:

{project_code}
"""

    return ask_ai(prompt)

# CLI entry point

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ai explain <file>")
        print("  ai commit")
        print("  ai summarize")
        return

    command = sys.argv[1]

    # explain file
    if command == "explain":
        if len(sys.argv) < 3:
            print("Usage: ai explain <file>")
            return

        file_path = sys.argv[2]
        result = explain_code(file_path)
        print("\n" + result)

    # git commit message
    elif command == "commit":
        diff = get_git_diff()

        if not diff.strip():
            print("No changes detected.")
            return

        result = generate_commit_message(diff)
        print("\nSuggested commit message:\n")
        print(result)

    # summarize project
    elif command == "summarize":
        result = summarize_project()
        print("\nProject Summary:\n")
        print(result)

    else:
        print("Unknown command")
        print("Use:")
        print("  ai explain <file>")
        print("  ai commit")
        print("  ai summarize")


if __name__ == "__main__":
    main()