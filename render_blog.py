"""
Render markdown blog posts to standalone HTML for GitHub Pages.
Translates kicker/lead-style metadata as-is. Run once after edits.
"""
import markdown
import os
import re

POSTS = [
    {
        "src": "content/blog/alice_ransomland.md",
        "out": "blog/alice_in_ransomland.html",
        "default_title": "Alice_In_Rans0ml4nd",
    },
    {
        "src": "content/blog/Gh0st_1n_7h3_G1t.md",
        "out": "blog/ghost_in_the_git.html",
        "default_title": "Gh0st_1n_7h3_G1t",
    },
]

PAGE_TPL = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} – Blog – Insomnia</title>
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/atom-one-dark.min.css">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="../index.html" aria-label="Accueil">Insomnia</a>
      <nav class="nav" aria-label="Navigation principale">
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav-list" aria-label="Menu">☰</button>
        <ul id="nav-list" class="nav-list">
          <li><a href="../index.html">Accueil</a></li>
          <li><a href="../parcours.html">Parcours</a></li>
          <li><a href="../competences.html">Compétences</a></li>
          <li><a href="../veille.html">Veille</a></li>
          <li><a href="../blog.html">Blog</a></li>
          <li><a href="mailto:insomnia@0xinsomnia.me">Contact</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="content" class="section">
    <div class="container narrow">
      <p class="kicker">{kicker}</p>
      <h1 class="section-title">{title}</h1>
      <p class="lead">{lead}</p>
      {banner_html}
      <article class="reveal in-view markdown-content">
        {content}
        <p><a class="link" href="../blog.html">← Retour au blog</a></p>
      </article>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-left">
        <p class="footer-note">Made with <span class="heart" aria-hidden="true">❤️</span> by <strong>Insomnia</strong> • <span id="year"></span></p>
      </div>
      <div class="footer-right">
        <ul class="footer-social">
          <li><a class="social-link" href="https://github.com/nowzee" target="_blank" rel="noopener" aria-label="GitHub"><svg viewBox="0 0 24 24" class="icon"><path fill="currentColor" d="M12 .5C5.73.5.99 5.24.99 11.52c0 4.86 3.16 8.98 7.55 10.43.55.1.76-.24.76-.54 0-.27-.01-1.17-.02-2.12-3.07.67-3.72-1.31-3.72-1.31-.5-1.26-1.23-1.6-1.23-1.6-.99-.68.08-.66.08-.66 1.1.08 1.68 1.13 1.68 1.13.98 1.68 2.58 1.19 3.21.9.1-.71.38-1.19.69-1.46-2.45-.28-5.02-1.22-5.02-5.43 0-1.2.43-2.18 1.13-2.95-.11-.28-.49-1.41.11-2.94 0 0 .92-.3 3.02 1.13a10.5 10.5 0 0 1 5.5 0c2.1-1.43 3.02-1.13 3.02-1.13.6 1.53.22 2.66.11 2.94.7.77 1.13 1.75 1.13 2.95 0 4.22-2.58 5.15-5.03 5.42.39.33.73.98.73 1.98 0 1.43-.01 2.58-.01 2.94 0 .3.2.64.77.53 4.38-1.45 7.54-5.56 7.54-10.42C23 5.24 18.27.5 12 .5Z"/></svg></a></li>
          <li><a class="social-link" href="mailto:insomnia@0xinsomnia.me" aria-label="Email"><svg viewBox="0 0 24 24" class="icon"><path fill="currentColor" d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5L4 8V6l8 5 8-5v2Z"/></svg></a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="../assets/js/main.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/powershell.min.js"></script>
  <script>hljs.highlightAll();</script>
</body>
</html>
"""

def parse_post(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    parts = raw.split("---", 2)
    meta = {}
    if len(parts) >= 3:
        for line in parts[1].strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        body = parts[2].strip()
    else:
        body = raw
    return meta, body

def fix_image_paths(html):
    # Markdown images that reference static/img/... -> ../assets/img/...
    html = re.sub(r'src="(?:/?static/)?img/', 'src="../assets/img/', html)
    html = re.sub(r"src='(?:/?static/)?img/", "src='../assets/img/", html)
    return html

for post in POSTS:
    src = post["src"]
    if not os.path.exists(src):
        print("missing:", src); continue
    meta, body = parse_post(src)
    html_body = markdown.markdown(body, extensions=["fenced_code", "tables", "nl2br"])
    html_body = fix_image_paths(html_body)

    title = meta.get("title", post["default_title"])
    kicker = meta.get("kicker", "$ writeup")
    lead = meta.get("lead", "")
    banner = meta.get("banner", "")
    if banner:
        banner_path = banner
        # Strip a leading "img/" or "static/img/"
        banner_path = re.sub(r"^(?:static/)?img/", "", banner_path)
        banner_html = (
            f'<figure class="post-banner">'
            f'<img src="../assets/img/{banner_path}" alt="{title}" loading="lazy">'
            f'</figure>'
        )
    else:
        banner_html = ""

    out_html = PAGE_TPL.format(
        title=title, kicker=kicker, lead=lead,
        banner_html=banner_html, content=html_body,
    )
    os.makedirs(os.path.dirname(post["out"]), exist_ok=True)
    with open(post["out"], "w", encoding="utf-8") as f:
        f.write(out_html)
    print("rendered:", post["out"])
