# TrueTx GitHub Bootstrap

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
