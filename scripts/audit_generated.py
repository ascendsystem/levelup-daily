#!/usr/bin/env python3
"""Reproducible checks for generated HTML, local links, images, and SEO mode."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.images = []
        self.article_images = 0
        self.figure_classes = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "img":
            self.images.append((attrs.get("src", ""), attrs.get("alt")))
            if any(cls in {"article-cover", "article-inline-image", "ranked-guide-image"} for cls in self.figure_classes):
                self.article_images += 1
        if tag == "figure":
            self.figure_classes.append(attrs.get("class", ""))
        if tag in {"a", "link", "script", "source"}:
            key = "href" if tag in {"a", "link"} else "src"
            value = attrs.get(key)
            if tag == "source":
                value = attrs.get("srcset", "").split(",")[0].strip().split(" ")[0]
            if value:
                self.links.append((tag, value))

    def handle_endtag(self, tag):
        if tag == "figure" and self.figure_classes:
            self.figure_classes.pop()


def article_sources():
    files = [
        "articles.json", "additional-articles.json", "gta-launch-guides.json",
        "gta-update-23-nov.json", "gta-music-23-nov.json", "gta-deep-dive-articles.json",
    ]
    articles = []
    for name in files:
        articles.extend(json.loads((ROOT / "content" / name).read_text(encoding="utf-8")))
    return articles


def is_public_site():
    url = str(json.loads((ROOT / "site.json").read_text(encoding="utf-8")).get("base_url", ""))
    parsed = urlparse(url)
    return bool(parsed.scheme == "https" and parsed.netloc and "." in parsed.netloc and not any(x in url.lower() for x in ("tu-usuario", "example.com", "localhost", "pendiente")))


def local_target(source_page: Path, url: str):
    parsed = urlparse(unquote(url))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    target = (source_page.parent / parsed.path).resolve()
    if parsed.path.endswith("/") or (target.exists() and target.is_dir()):
        target /= "index.html"
    return target


def main():
    errors = []
    articles = article_sources()
    new_articles = json.loads((ROOT / "content" / "gta-deep-dive-articles.json").read_text(encoding="utf-8"))
    if len(new_articles) != 35:
        errors.append(f"La ampliación contiene {len(new_articles)} artículos; se esperaban 35.")
    if any(not a.get("sources") for a in new_articles):
        errors.append("Hay artículos nuevos sin enlaces a fuentes.")
    seo_titles = [a.get("seo_title", a["title"] + " | LEVELUP DAILY") for a in new_articles]
    meta_descriptions = [a.get("description", "") for a in new_articles]
    if len(seo_titles) != len(set(seo_titles)):
        errors.append("Los artículos nuevos tienen títulos SEO duplicados.")
    if len(meta_descriptions) != len(set(meta_descriptions)):
        errors.append("Los artículos nuevos tienen meta descriptions duplicadas.")
    slugs = [a["slug"] for a in articles]
    titles = [re.sub(r"\s+", " ", a["title"].strip().casefold()) for a in articles]
    if len(slugs) != len(set(slugs)):
        errors.append("Los artículos contienen slugs duplicados.")
    if len(titles) != len(set(titles)):
        errors.append("Los artículos contienen títulos idénticos.")

    counts = []
    for article in articles:
        page = ROOT / article["category"] / article["slug"] / "index.html"
        if not page.is_file():
            errors.append(f"Falta la página de {article['slug']}.")
            continue
        raw = page.read_text(encoding="utf-8")
        parsed = PageParser()
        parsed.feed(raw)
        counts.append(len(parsed.images))
        if parsed.h1 != 1:
            errors.append(f"{article['slug']}: tiene {parsed.h1} elementos H1; se esperaba uno.")
        if "assets/images/editorial/" in raw or "covers/editorial-" in raw:
            errors.append(f"{article['slug']}: aún referencia una imagen de ejemplo generada.")
        if any(alt is None for _, alt in parsed.images):
            errors.append(f"{article['slug']}: hay imágenes sin texto alternativo.")
        if "tu-usuario.github.io" in raw:
            errors.append(f"{article['slug']}: contiene la URL de ejemplo.")
        if is_public_site():
            if '<meta name="robots" content="index,follow,max-image-preview:large">' not in raw or "<link rel=\"canonical\"" not in raw:
                errors.append(f"{article['slug']}: faltan las señales SEO públicas.")
        elif '<meta name="robots" content="noindex,nofollow">' not in raw or "<link rel=\"canonical\"" in raw:
            errors.append(f"{article['slug']}: no está marcado correctamente como build local.")
        for src, _alt in parsed.images:
            target = local_target(page, src)
            if target and not target.is_file():
                errors.append(f"Imagen ausente en {article['slug']}: {src}")

    html_pages = [p for p in ROOT.rglob("*.html") if not any(part in {".git", "tmp"} for part in p.parts)]
    broken_links = 0
    for page in html_pages:
        parsed = PageParser()
        try:
            parsed.feed(page.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            errors.append(f"No se pudo leer el HTML UTF-8: {page.relative_to(ROOT)}")
            continue
        for tag, href in parsed.links:
            target = local_target(page, href)
            if target and not target.is_file():
                broken_links += 1
                errors.append(f"Enlace local roto en {page.relative_to(ROOT)}: {href}")

    credit = json.loads((ROOT / "assets/images/image-credits.json").read_text(encoding="utf-8"))
    duplicates = credit["duplicate_audit"]
    cross_files = duplicates.get("cross_article_file_reuse_existing", [])
    cross_hashes = duplicates.get("cross_article_sha256_reuse_existing", [])

    print(f"Artículos: {len(articles)}; páginas HTML comprobadas: {len(html_pages)}")
    print(f"Imágenes por artículo: mínimo {min(counts) if counts else 0}; mediana {sorted(counts)[len(counts)//2] if counts else 0}; máximo {max(counts) if counts else 0}")
    print(f"Imágenes asignadas inventariadas: {credit['published_assets']}; enlaces locales rotos: {broken_links}")
    print(f"Reutilizaciones heredadas entre artículos: {len(cross_files)} archivos, {len(cross_hashes)} SHA-256 compartidos")
    print(f"Modo SEO: {'público' if is_public_site() else 'local noindex'}")
    if errors:
        print(f"ERRORES: {len(errors)}")
        for error in errors[:100]:
            print("- " + error)
        return 1
    print("Resultado: todos los controles automáticos pasaron.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
