# Portfolio BTS

Portfolio statique pour GitHub Pages, en français, dans le cadre du BTS.

## Structure

```
portfolio-bts/
├── index.html              # Accueil
├── veille.html             # Veille technologique cyber
├── competences.html        # Tableau de compétences + bouton Excel
└── assets/
    ├── css/style.css
    ├── js/main.js
    ├── img/                # Images
    └── files/              # Mettre ici tableau-competences.xlsx (et .pdf)
```

## Personnalisation rapide

1. Remplace `Prénom Nom` dans les 3 fichiers HTML.
2. Remplace l'URL GitHub dans le `<footer>` et l'email `contact@example.com`.
3. Dépose ton fichier Excel : `assets/files/tableau-competences.xlsx`
   (le bouton de téléchargement pointe déjà vers ce chemin).
4. Mets à jour les cartes de la page Veille (`veille.html`) au fil des semaines.

## Déploiement GitHub Pages

1. Crée un repo GitHub (par ex. `portfolio-bts`).
2. Pousse le contenu du dossier à la racine du repo.
3. Sur GitHub : **Settings → Pages → Source: Deploy from a branch → main / (root)**.
4. Le site sera disponible à `https://<ton-user>.github.io/portfolio-bts/`.

Pour un domaine racine `<ton-user>.github.io`, nomme le repo `<ton-user>.github.io`.

## Aperçu local

Ouvre simplement `index.html` dans le navigateur, ou lance un mini-serveur :

```bash
python -m http.server 8000
```

puis va sur http://localhost:8000.
