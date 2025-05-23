#!/usr/bin/env python3
# scripts/genera_articoli.py

import feedparser
import datetime
import os
import re
from transformers import pipeline

# 1) Imposta qui i feed RSS di politica
FEEDS = [
    "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
    "https://www.repubblica.it/rss/politica/rss2.0.xml"
]

# 2) Inizializza il generatore di testo (GPT-2 italiano)
generator = pipeline("text-generation", model="GroNLP/gpt2-small-italian")

def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = s.strip().lower()
    return re.sub(r"[-\s]+", "-", s)

def genera_post(entry):
    titolo = entry.title
    slug = slugify(titolo)
    oggi = datetime.date.today().isoformat()
    filename = f"content/politica/{oggi}-{slug}.md"

    # Se esiste già, salta
    if os.path.exists(filename):
        return

    # Prepara il prompt e genera il testo
    prompt = f"Scrivi un articolo di cronaca politica in italiano, neutrale e informativo, basato sul titolo: \"{titolo}\".\nArticolo:"
    result = generator(prompt, max_length=300, do_sample=True)
    testo = result[0]["generated_text"]

    # Scrive il file Markdown per Hugo
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: \"{titolo}\"\n")
        f.write(f"date: {now}\n")
        f.write("draft: false\n")
        f.write("categories: [\"Politica\"]\n")
        f.write("---\n\n")
        f.write(testo)

def main():
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            genera_post(entry)

if __name__ == "__main__":
    main()
