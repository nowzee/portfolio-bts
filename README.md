# Portfolio BTS – Louis PERROUX

Version statique (GitHub Pages) du portfolio [0xinsomnia.me](https://0xinsomnia.me/),
adaptée pour le BTS SIO option SLAM (ESNA Bretagne).

## Pages

- `index.html` — Accueil (whoami, compétences, projets)
- `parcours.html` — Formation, expériences, réalisations, certifications & CTF
- `competences.html` — Tableau de compétences + bouton de téléchargement Excel
- `veille.html` — Veille cybersécurité (filtres CVE / Malware / Ransomware / APT / Outil / Actualité)
- `blog.html` — Blog & writeups CTF
- `blog/alice_in_ransomland.html` — Writeup ECW 2025
- `blog/ghost_in_the_git.html` — Writeup MIDNIGHT FLAG 2026

## Structure

```
portfolio-bts/
├── *.html                # pages principales
├── blog/                 # writeups rendus depuis content/blog/*.md
├── content/blog/         # sources markdown (édition)
├── render_blog.py        # script de re-génération du blog
└── assets/
    ├── css/style.css
    ├── js/main.js
    ├── img/              # toutes les images
    ├── favicon.svg
    └── files/            # tableau-competences.xlsx (à déposer)
```

## Mettre à jour le blog

Modifier les fichiers dans `content/blog/`, puis relancer :

```bash
pip install markdown
python render_blog.py
```

## Tableau de compétences

Dépose ton fichier Excel dans `assets/files/tableau-competences.xlsx`
(et éventuellement `tableau-competences.pdf`). Les boutons de la page
`competences.html` pointent déjà vers ces chemins.

## Déploiement GitHub Pages

Le repo est déjà en place : https://nowzee.github.io/portfolio-bts/

Pour publier les modifications :

```bash
git add .
git commit -m "update portfolio"
git push
```

GitHub Pages se met à jour automatiquement (~30 s).

## Aperçu local

```bash
python -m http.server 8000
# puis http://localhost:8000
```
