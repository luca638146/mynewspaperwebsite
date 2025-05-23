name: auto-publish

on:
  schedule:
    - cron: '0 5,17 * * *'  # Esegue alle 7 e alle 19 ora italiana (UTC+2)
  workflow_dispatch:

jobs:
  build-site:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install openai feedparser transformers torch

      - name: Ensure posts directory exists
        run: mkdir -p content/posts

      - name: Genera articolo AI
        run: python scripts/genera_articoli.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      - name: List files in posts
        run: ls -l content/posts/

      - name: Commit new article
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add content/posts/*.md || echo "Nessun file da aggiungere"
          git diff --cached --quiet || (git commit -m "📝 Nuovo articolo generato automaticamente" && git push)
