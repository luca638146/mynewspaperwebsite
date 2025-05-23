import os
from datetime import datetime
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def genera_articolo(titolo):
    prompt = f"Scrivi un articolo giornalistico in italiano sul seguente argomento: {titolo}.\nL'articolo deve essere chiaro, informativo e lungo circa 300 parole."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.7,
    )
    testo = response.choices[0].message.content.strip()
    return testo

def crea_file_articolo(titolo, contenuto):
    data = datetime.now().strftime("%Y-%m-%d")
    slug = titolo.lower().replace(" ", "-").replace("'", "").replace(",", "")
    directory = "content/posts"
    os.makedirs(directory, exist_ok=True)
    filename = f"{directory}/{data}-{slug}.md"

    front_matter = f"""---
title: "{titolo}"
date: {data}T08:00:00+01:00
draft: false
---

"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(contenuto)

def main():
    tema = "L'intelligenza artificiale nel giornalismo moderno"
    try:
        articolo = genera_articolo(tema)
        crea_file_articolo(tema, articolo)
        print(f"✅ Articolo creato con tema: {tema}")
    except Exception as e:
        print(f"❌ Errore durante la generazione dell'articolo: {e}")

if __name__ == "__main__":
    main()
