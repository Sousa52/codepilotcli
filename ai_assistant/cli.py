import sys
import requests
import subprocess

# File utilities

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_git_diff():
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )
    return result.stdout

# AI call (shared)

def ask_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

# Features

def explain_code(file_path):
    code = read_file(file_path)

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

# CLI entry point

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ai explain <file>")
        print("  ai commit")
        return

    command = sys.argv[1]

    # ai explain <file>
    if command == "explain":
        if len(sys.argv) < 3:
            print("Usage: ai explain <file>")
            return

        file_path = sys.argv[2]
        result = explain_code(file_path)
        print("\n" + result)

    # ai commit
    elif command == "commit":
        diff = get_git_diff()

        if not diff.strip():
            print("No changes detected.")
            return

        result = generate_commit_message(diff)
        print("\nSuggested commit message:\n")
        print(result)

    else:
        print("Unknown command")
        print("Use: ai explain <file> | ai commit")


if __name__ == "__main__":
    main()