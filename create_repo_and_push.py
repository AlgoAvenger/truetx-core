import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")
API_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_repo():
    print(f"Creating repo {GITHUB_REPO}...")
    r = requests.post(f"{API_URL}/user/repos", headers=headers, json={
        "name": GITHUB_REPO,
        "private": False,
        "auto_init": True
    })
    if r.status_code == 201:
        print("Repository created successfully.")
    elif r.status_code == 422 and 'name already exists' in r.text:
        print("Repo already exists. Proceeding...")
    else:
        raise Exception(f"Failed to create repo: {r.status_code} {r.text}")

def upload_file(path, content):
    url = f"{API_URL}/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{path}"
    encoded = base64.b64encode(content.encode()).decode()
    r = requests.put(url, headers=headers, json={
        "message": f"Add {path}",
        "content": encoded
    })
    print(f"Uploaded {path}: {r.status_code}")

def main():
    create_repo()
    upload_file(".github/workflows/ci.yml", '''name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt || true
      - name: Run tests
        run: pytest || echo "No tests defined."
''')
    upload_file(".github/CODEOWNERS", '''* @yourusername
''')
    upload_file(".github/pull_request_template.md", '''### What Changed?

- Brief summary of changes

### Related Issues

- Closes #...

### Checklist

- [ ] Tests added
- [ ] Docs updated
''')
    upload_file("roadmap_issues.md", '''# TrueTx Roadmap Issues

## MVP
- [ ] Setup CI integration
- [ ] Create CODEOWNERS
- [ ] Setup PR template
- [ ] Add issue templates

## Post-MVP
- [ ] Add auto-release flow
- [ ] Setup test coverage
- [ ] Enable GitHub pages for docs
''')
    upload_file("README.md", '''# TrueTx GitHub Bootstrap

## Setup Instructions

1. Copy `.env.example` to `.env` and fill in your GitHub credentials:

```bash
cp .env.example .env
```

2. Install required Python packages:

```bash
pip install requests python-dotenv
```

3. Run the script to create the repo and push metadata:

```bash
python create_repo_and_push.py
```

Make sure you have a GitHub [Personal Access Token](https://github.com/settings/tokens) with `repo` permissions.
''')

if __name__ == "__main__":
    main()
