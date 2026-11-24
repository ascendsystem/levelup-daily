"""Audit existing article image assignments without creating or replacing images."""
from __future__ import annotations

import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

try:
    from PIL import Image
except Exception:
    Image = None
try:
    import numpy as np
except Exception:
    np = None


def remember_legacy(root, articles, ranked, inline):
    meta = {}
    def add(path, credit=None, source=None, caption=None, source_file=None, rights_status=None):
        if path:
            meta[Path(path).as_posix()] = {"credit": credit, "source": source, "caption": caption,
                                           "source_file": source_file, "rights_status": rights_status}
    for article in articles:
        add(article.get("cover_image"), article.get("image_credit"), article.get("image_source"),
            article.get("image_caption"), article.get("image_source_file"), article.get("image_rights_status"))
        for ext in ("webp", "jpg", "jpeg", "png"):
            path = f"assets/images/covers/{article.get('cover', '')}.{ext}"
            if (root / path).is_file():
                add(path, article.get("image_credit"), article.get("image_source"), article.get("image_caption"))
        for media in article.get("inline_media", []):
            add(media.get("image"), media.get("credit"), media.get("source"), media.get("caption"),
                media.get("source_file"), media.get("rights_status"))
        for entry in ranked.get(article["slug"], []):
            add(entry.get("image"), entry.get("image_credit"), entry.get("image_source"), entry.get("image_caption"))
    for media_list in inline.values():
        for media in media_list:
            add(media.get("image"), media.get("credit"), media.get("source"), media.get("caption"))
    return meta


def phash(path):
    if Image is None or np is None or path.suffix.lower() == ".svg":
        return None
    try:
        pixels = np.asarray(Image.open(path).convert("L").resize((32, 32)), dtype=float)
        n = 32
        k = np.arange(n)
        dct = np.cos((2 * k[:, None] + 1) * k[None, :] * math.pi / (2 * n))
        dct[:, 0] *= 1 / math.sqrt(2)
        dct *= math.sqrt(2 / n)
        values = (dct @ pixels @ dct.T)[:8, :8].flatten()
        median = np.median(values[1:])
        result = 0
        for value in values:
            result = (result << 1) | int(value > median)
        return f"{result:016x}"
    except Exception:
        return None

def dimensions(path):
    if Image is None or path.suffix.lower() == ".svg":
        return None, None
    try:
        with Image.open(path) as image:
            return image.width, image.height
    except Exception:
        return None, None


def cover_file(root, article):
    custom = article.get("cover_image")
    if custom and (root / custom).is_file():
        return Path(custom).as_posix()
    for ext in ("webp", "jpg", "jpeg", "png"):
        candidate = f"assets/images/covers/{article.get('cover', '')}.{ext}"
        if (root / candidate).is_file():
            return candidate
    return None


def write_audit(root, articles, legacy_meta, stock, run_date):
    active = defaultdict(list)
    def add(path, article, route, usage):
        if path and (root / path).is_file():
            active[Path(path).as_posix()].append((article, route, usage))
    for article in articles:
        route = f"{article['category']}/{article['slug']}/"
        add(cover_file(root, article), article, route, "portada")
        for media in article.get("inline_media", []):
            add(media.get("image"), article, route, "interior")
        for position, entry in enumerate(article.get("ranked_items", []), 1):
            image = entry.get("image")
            if not image:
                filename = entry.get("filename") or re.sub(r"[^a-z0-9]+", "-", entry["title"].lower()).strip("-") + ".webp"
                image = "assets/images/inline/rankings/" + filename
            add(image, article, route, f"puesto {position}")

    pexels = {Path(photo["image"]).as_posix(): photo for photo in stock.get("photos", [])}
    files, exact, perceptual = [], defaultdict(list), defaultdict(list)
    for path in sorted((root / "assets/images").rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".svg", ".webp", ".jpg", ".jpeg", ".png", ".avif"}:
            continue
        rel = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        perceptual_hash = phash(path)
        width_px, height_px = dimensions(path)
        exact[digest].append(rel)
        if perceptual_hash:
            perceptual[perceptual_hash].append(rel)
        uses, photo, old = active.get(rel, []), pexels.get(rel), legacy_meta.get(rel, {})
        if uses:
            article_slugs = sorted({use[0]["slug"] for use in uses})
            article, route, _ = uses[0]
            source = "Pexels" if photo else old.get("credit") or article.get("image_credit") or "Procedencia no documentada localmente"
            source_url = photo.get("source") if photo else old.get("source") or article.get("image_source")
            license_name = "Pexels License" if photo else "No registrada en el proyecto; revisar antes de publicación comercial"
            if old.get("rights_status"):
                license_name = old["rights_status"]
            status = "assigned_pexels" if photo else "existing_assignment_preserved_rights_to_verify"
            record = {"asset_id": "img-" + digest[:16], "file": rel, "article_slug": article_slugs[0],
                "article_slugs": article_slugs, "article_routes": sorted({use[1] for use in uses}),
                "usage": [use[2] for use in uses], "category": article.get("category"), "source": source,
                "source_url": source_url, "source_file": old.get("source_file"),
                "creator": photo.get("author") if photo else old.get("credit") or article.get("image_credit"),
                "license": license_name, "license_url": stock.get("license_url") if photo else None,
                "download_date": None, "catalogued_date": run_date, "width_px": width_px, "height_px": height_px,
                "description": old.get("caption") or article.get("image_caption"),
                "keywords": [article["title"], *article.get("tags", [])], "sha256": digest,
                "perceptual_hash": perceptual_hash, "status": status}
        elif photo:
            record = {"asset_id": "img-" + digest[:16], "file": rel, "article_slug": None,
                "article_slugs": [], "article_routes": [], "usage": [], "category": "fotografía temática",
                "source": "Pexels", "source_url": photo["source"], "creator": photo["author"],
                "license": "Pexels License", "license_url": stock.get("license_url"), "download_date": None,
                "catalogued_date": run_date, "width_px": width_px, "height_px": height_px,
                "description": photo.get("description"),
                "keywords": [photo.get("description", ""), "Pexels"], "sha256": digest,
                "perceptual_hash": perceptual_hash, "status": "licensed_but_unassigned"}
        elif rel.endswith("logo.svg") or rel.endswith("favicon.svg"):
            record = {"asset_id": "img-" + digest[:16], "file": rel, "article_slug": None,
                "article_slugs": [], "article_routes": [], "usage": ["branding"], "category": "identidad del sitio",
                "source": "Proyecto LEVELUP DAILY", "source_url": None, "creator": "LEVELUP DAILY",
                "license": "Recurso local de identidad del proyecto", "license_url": None, "download_date": None,
                "catalogued_date": run_date, "width_px": width_px, "height_px": height_px,
                "description": "Logo o icono del sitio", "keywords": ["branding"],
                "sha256": digest, "perceptual_hash": perceptual_hash, "status": "branding_asset"}
        else:
            record = {"asset_id": "img-" + digest[:16], "file": rel, "article_slug": None,
                "article_slugs": [], "article_routes": [], "usage": [], "category": "archivo no asignado",
                "source": old.get("credit") or "Procedencia no documentada localmente", "source_url": old.get("source"),
                "creator": old.get("credit"), "license": "No verificada; revisar antes de publicar o monetizar",
                "license_url": None, "download_date": None, "catalogued_date": run_date,
                "width_px": width_px, "height_px": height_px,
                "description": old.get("caption") or "Archivo conservado, no asignado.",
                "keywords": ["archivo local", "derechos pendientes"], "sha256": digest,
                "perceptual_hash": perceptual_hash, "status": "unassigned_rights_review"}
        files.append(record)

    cross_file = [{"file": name, "articles": sorted({use[0]["slug"] for use in uses})}
                  for name, uses in active.items() if len({use[0]["slug"] for use in uses}) > 1]
    cross_sha = []
    for digest, names in exact.items():
        slugs = sorted({use[0]["slug"] for name in names for use in active.get(name, [])})
        if len(slugs) > 1:
            cross_sha.append({"sha256": digest, "files": names, "articles": slugs})
    duplicate_exact = [names for names in exact.values() if len(names) > 1]
    duplicate_phash = [names for names in perceptual.values() if len(names) > 1]
    credits = {"schema_version": "1.0", "catalogued_date": run_date,
        "hash_methods": {"exact": "SHA-256", "perceptual": "DCT pHash para imágenes raster compatibles; null para SVG"},
        "assignment_rule": "Se conservan las asignaciones existentes. No se sustituyen imágenes por ejemplos.",
        "published_assets": sum(bool(active.get(record["file"])) for record in files), "assets": files,
        "duplicate_audit": {"exact_sha256_groups_all_local_files": duplicate_exact,
            "perceptual_hash_groups_all_local_files": duplicate_phash,
            "cross_article_file_reuse_existing": cross_file, "cross_article_sha256_reuse_existing": cross_sha}}
    (root / "assets/images/image-credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows, rank_rows, pending = [], [], []
    for article in articles:
        route = f"{article['category']}/{article['slug']}/"
        cover = cover_file(root, article) or "FOTO PENDIENTE"
        media = [m.get("image") for m in article.get("inline_media", []) if m.get("image") and (root / m["image"]).is_file()]
        interior = "; ".join(media) or "FOTO PENDIENTE"
        source = legacy_meta.get(cover, {}).get("credit") or legacy_meta.get(cover, {}).get("source") or ("Pexels" if cover in pexels else "Fuente por verificar")
        state = "asignación existente conservada" if cover != "FOTO PENDIENTE" else "portada pendiente"
        rows.append(f"| {article['slug']} | {route} | {cover} | {interior} | {source} | {state} |")
        if cover == "FOTO PENDIENTE": pending.append((article["slug"], "portada"))
        if not media and not article.get("ranked_items"): pending.append((article["slug"], "interior"))
        for position, entry in enumerate(article.get("ranked_items", []), 1):
            image = entry.get("image") or "FOTO PENDIENTE"
            rank_rows.append(f"| {article['slug']} · {position:02d} {entry.get('title', '')} | {image} | Asignación existente conservada |")
    exact_duplicate_count = sum(len(names) - 1 for names in duplicate_exact)
    phash_duplicate_count = sum(len(names) - 1 for names in duplicate_phash)
    gta_download_assignments = sum(1 for record in files if str(record.get("source_file", "")).startswith("imagenes gta/"))
    assigned_raster = [record for record in files if active.get(record["file"]) and record.get("width_px") and record.get("height_px")]
    low_resolution = [record for record in assigned_raster if record["width_px"] < 640 or record["height_px"] < 360]
    minimum_size = (min(record["width_px"] for record in assigned_raster), min(record["height_px"] for record in assigned_raster)) if assigned_raster else (0, 0)
    report = ["# IMAGE-AUDIT — LEVELUP DAILY", "", f"Revisado: {run_date}. Se conservaron las asignaciones que ya tenía la web.", "",
        "## Resultado", "", f"- Artículos inventariados: {len(articles)}.",
        f"- Archivos asignados: {credits['published_assets']}.",
        f"- Imágenes de la carpeta GTA asignadas a los artículos nuevos: {gta_download_assignments}.",
        f"- Reutilización entre artículos en las asignaciones existentes: {len(cross_file)} archivos.",
        f"- Grupos SHA-256 compartidos entre artículos existentes: {len(cross_sha)}.",
        f"- El archivo local contiene {exact_duplicate_count} duplicados exactos y {phash_duplicate_count} coincidencias pHash.",
        f"- Resolución registrada: {len(assigned_raster)} imágenes asignadas; mínimos de ancho y alto por separado {minimum_size[0]} × {minimum_size[1]} px; {len(low_resolution)} por debajo de 640 × 360 px.",
        "- Las marcas de agua y los permisos comerciales requieren inspección manual; no se consideran verificados por el hash o la resolución.",
        f"- Espacios de portada/interior aún pendientes: {len(pending)}.",
        "- Los archivos y sus asignaciones no se sustituyen por ejemplos. Créditos, fuentes registradas, hashes y estados están en `assets/images/image-credits.json`.", "",
        "## Asignaciones existentes", "", "| Artículo | URL | Portada | Interior | Fuente registrada | Estado |", "|---|---|---|---|---|---|", *rows, "",
        "## Rankings existentes", "", "| Artículo y entrada | Imagen | Estado |", "|---|---|---|", *rank_rows, "",
        "## Carpetas de Descargas", "", f"Se seleccionaron {gta_download_assignments} imágenes de `Descargas/imagenes gta` para artículos nuevos tras revisar sus miniaturas y descartar reutilizaciones con páginas existentes. Las demás carpetas del usuario permanecen intactas y sin reasignar.",
        "Los campos de licencia y fecha de descarga que no consten en los datos originales quedan sin verificar; revisa los permisos antes de publicar o monetizar.", ""]
    (root / "IMAGE-AUDIT.md").write_text("\n".join(report), encoding="utf-8")
