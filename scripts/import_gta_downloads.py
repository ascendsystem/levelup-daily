#!/usr/bin/env python3
"""Copy selected user GTA VI photos and attach them only to matching new guides."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / "Downloads" / "imagenes gta"
OFFICIAL_MEDIA = "https://www.rockstargames.com/VI/media"


def display_name(value):
    return value.replace("_", " ").replace("  ", " ").strip()


def describe_source(relative):
    parts = Path(relative).parts
    if parts[0] == "Postcards":
        place = display_name(parts[1])
        place = place.replace("National Park", "National Park")
        return f"Postal promocional de {place} en GTA VI."
    if parts[0] == "Places":
        place = display_name(parts[1])
        return f"Escena promocional de GTA VI ambientada en {place}."
    if parts[0] == "People":
        person = display_name(parts[1])
        if person.casefold() == "jason and lucia":
            person = "Jason y Lucia"
        return f"Imagen promocional de {person} en GTA VI."
    group = display_name(parts[0])
    if "Jason and Lucia" in group:
        group = "Jason y Lucia"
    return f"Material promocional de GTA VI: {group}."
PLAN = {
 "gta-6-index-misiones-objetivos": ("Places/Vice City/Vice_City_13.jpg", "Places/Vice City/Vice_City_09.jpg"),
 "gta-6-repetir-misiones-guardados-manuales": ("People/Jason and Lucia/Jason_and_Lucia_17.jpg", "People/Jason and Lucia/Jason_and_Lucia_16.jpg"),
 "gta-6-viaje-rapido-transporte": ("Places/Leonida Keys/Leonida_Keys_05.jpg", "Places/Vice City/Vice_City_10.jpg"),
 "gta-6-perfil-criminal-consecuencias": ("People/Jason and Lucia/Jason_and_Lucia_18.jpg", "People/Jason Duval/Jason_Duval_07.jpg"),
 "gta-6-nivel-busqueda-seis-estrellas": ("People/Lucia Caminos/Lucia_Caminos_14.jpg", "People/Jason Duval/Jason_Duval_16.jpg"),
 "gta-6-waink-it-app-coches": ("People/Jason Duval/Jason_Duval_08.jpg", "People/Jason Duval/Jason_Duval_09.jpg"),
 "gta-6-robar-coches-herramientas": ("People/Jason and Lucia/Jason_and_Lucia_19.jpg", "People/Jason and Lucia/Jason_and_Lucia_20.jpg"),
 "gta-6-vender-registrar-coches": ("Places/Ambrosia/Ambrosia_05.jpg", "Places/Vice City/Vice_City_17.jpg"),
 "gta-6-snap-gun-como-se-consigue": ("People/Jason Duval/Jason_Duval_15.jpg", "People/Jason Duval/Jason_Duval_12.jpg"),
 "gta-6-postgame-despues-creditos": ("People/Jason and Lucia/Jason_and_Lucia_05.jpg", "Places/Grassrivers/Grassrivers_08.jpg"),
 "gta-6-controles-clasicos-configurar": ("People/Jason and Lucia/Jason_and_Lucia_04.jpg", "Places/Vice City/Vice_City_18.jpg"),
 "gta-6-primera-persona-camara": ("People/Jason Duval/Jason_Duval_19.jpg", "People/Jason and Lucia/Jason_and_Lucia_11.jpg"),
 "gta-6-coches-rapidos-estadisticas": ("People/Jason and Lucia/Jason_and_Lucia_09.jpg", "Places/Port Gellhorn/Port_Gellhorn_03.jpg"),
 "gta-6-vehiculos-ultimate-edition": ("People/Jason Duval/Jason_Duval_18.jpg", "Places/Vice City/Vice_City_20.jpg"),
 "gta-6-barcos-acuaticos-confirmados": ("Places/Leonida Keys/Leonida_Keys_02.jpg", "Places/Leonida Keys/Leonida_Keys_03.jpg"),
 "gta-6-duracion-historia-cuanto-se-tarda": ("People/Jason and Lucia/Jason_and_Lucia_13.jpg", "People/Jason and Lucia/Jason_and_Lucia_08.jpg"),
 "gta-6-jason-duval-biografia": ("People/Jason Duval/Jason_Duval_02.jpg", "People/Jason Duval/Jason_Duval_10.jpg"),
 "gta-6-lucia-caminos-biografia": ("People/Lucia Caminos/Lucia_Caminos_10.jpg", "People/Lucia Caminos/Lucia_Caminos_13.jpg"),
 "gta-6-cal-hampton-quien-es": ("Cal_Hampton/Cal_Hampton_landscape.jpg", "People/Cal Hampton/Cal_Hampton_03.jpg"),
 "gta-6-boobie-ike-quien-es": ("Boobie_Ike/Boobie_Ike_landscape.jpg", "People/Boobie Ike/Boobie_Ike_02.jpg"),
 "gta-6-drequan-priest-only-raw": ("DreQuan_Priest/DreQuan_Priest_landscape.jpg", "People/DreQuan Priest/DreQuan_Priest_02.jpg"),
 "gta-6-real-dimez-bae-luxe-roxy": ("People/Real Dimez/Real_Dimez_04.jpg", "People/Real Dimez/Real_Dimez_02.jpg"),
 "gta-6-raul-bautista-personaje": ("Raul_Bautista/Raul_Bautista_landscape.jpg", "People/Raul Bautista/Raul_Bautista_02.jpg"),
 "gta-6-brian-heder-personaje": ("Brian_Heder/Brian_Heder_landscape.jpg", "People/Brian Heder/Brian_Heder_02.jpg"),
 "gta-6-leonida-keys-zona": ("Postcards/Leonida_Keys/Leonida_Keys_Postcard_landscape.jpg", "Places/Leonida Keys/Leonida_Keys_06.jpg"),
 "gta-6-port-gellhorn-zona": ("Postcards/Port_Gellhorn/Port_Gellhorn_Postcard_landscape.jpg", "Places/Port Gellhorn/Port_Gellhorn_06.jpg"),
 "gta-6-grassrivers-zona": ("Postcards/Grassrivers/Grassrivers_Postcard_landscape.jpg", "Places/Grassrivers/Grassrivers_02.jpg"),
 "gta-6-ambrosia-zona": ("Postcards/Ambrosia/Ambrosia_Postcard_landscape.jpg", "Places/Ambrosia/Ambrosia_03.jpg"),
 "gta-6-mount-kalaga-zona": ("Postcards/Mount_Kalaga_National_Park/Mount_Kalaga_National_Park_Postcard_landscape.jpg", "Places/Mount Kalaga National Park/Mount_Kalaga_National_Park_04.jpg"),
 "gta-6-vida-cotidiana-detalles-mundo": ("Places/Vice City/Vice_City_03.jpg", "Places/Vice City/Vice_City_12.jpg"),
 "gta-6-analisis-reviews-lanzamiento": ("Places/Vice City/Vice_City_11.jpg", "People/Jason and Lucia/Jason_and_Lucia_07.jpg"),
 "gta-6-redes-sociales-telefono-satira": ("People/Jason Duval/Jason_Duval_05.jpg", "Places/Vice City/Vice_City_07.jpg"),
 "gta-6-jason-lucia-relacion-analisis": ("People/Jason and Lucia/Jason_and_Lucia_03.jpg", "People/Jason and Lucia/Jason_and_Lucia_14.jpg"),
 "gta-6-detalles-analisis-lanzamiento": ("Jason_and_Lucia_01_With_Logos/Jason_and_Lucia_01_With_Logos_landscape.jpg", "Places/Vice City/Vice_City_14.jpg"),
}


def phash(path):
    import numpy as np
    pixels = np.asarray(Image.open(path).convert("L").resize((32, 32)), dtype=float)
    n = 32
    k = np.arange(n)
    dct = np.cos((2 * k[:, None] + 1) * k[None, :] * 3.141592653589793 / (2 * n))
    dct[:, 0] *= 1 / (2 ** 0.5)
    dct *= (2 / n) ** 0.5
    values = (dct @ pixels @ dct.T)[:8, :8].flatten()
    median = np.median(values[1:])
    result = 0
    for value in values:
        result = (result << 1) | int(value > median)
    return result


def main():
    if not DOWNLOADS.is_dir():
        raise SystemExit(f"No encuentro la carpeta: {DOWNLOADS}")
    articles_path = ROOT / "content/gta-deep-dive-articles.json"
    articles = json.loads(articles_path.read_text(encoding="utf-8"))
    by_slug = {article["slug"]: article for article in articles}
    if set(PLAN) - set(by_slug):
        raise SystemExit("El plan incluye artículos que no están en el lote nuevo.")

    from image_audit import phash as project_phash
    assigned = set()
    # Reject reuse of an already-published source visual as well as duplicate selections.
    existing_hashes = []
    json_sources = ["articles.json", "additional-articles.json", "gta-launch-guides.json", "gta-update-23-nov.json", "gta-music-23-nov.json"]
    for name in json_sources:
        items = json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))
        for item in items:
            for ext in ("webp", "jpg", "jpeg", "png"):
                p = ROOT / "assets/images/covers" / f"{item.get('cover','')}.{ext}"
                if p.is_file() and project_phash(p) is not None: existing_hashes.append(int(project_phash(p), 16))
            for media in item.get("inline_media", []):
                p = ROOT / media.get("image", "")
                if p.is_file() and project_phash(p) is not None: existing_hashes.append(int(project_phash(p), 16))
    inline = json.loads((ROOT / "content/inline-media.json").read_text(encoding="utf-8"))
    ranked = json.loads((ROOT / "content/ranked-entries.json").read_text(encoding="utf-8"))
    for media_list in inline.values():
        for media in media_list:
            p = ROOT / media.get("image", "")
            if p.is_file() and project_phash(p) is not None: existing_hashes.append(int(project_phash(p), 16))
    for entries in ranked.values():
        for entry in entries:
            p = ROOT / entry.get("image", "")
            if p.is_file() and project_phash(p) is not None: existing_hashes.append(int(project_phash(p), 16))
    if np_is_missing():
        raise SystemExit("Se necesita NumPy instalado para verificar duplicados perceptuales.")

    selected = []
    conflicts = []
    for slug, pair in PLAN.items():
        for usage, relative in zip(("cover", "inside"), pair):
            source = DOWNLOADS / relative
            if not source.is_file():
                raise SystemExit(f"No encuentro la imagen seleccionada: {source}")
            binary_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            visual_hash = phash(source)
            if binary_hash in assigned:
                conflicts.append(f"archivo repetido en el plan: {slug} {usage} → {relative}")
            if any((visual_hash ^ previous).bit_count() <= 2 for previous in selected):
                conflicts.append(f"duplicado visual dentro de las nuevas selecciones: {slug} {usage} → {relative}")
            if any((visual_hash ^ previous).bit_count() <= 2 for previous in existing_hashes):
                conflicts.append(f"ya está asignada a un artículo existente: {slug} {usage} → {relative}")
            assigned.add(binary_hash)
            selected.append(visual_hash)
    if conflicts:
        raise SystemExit("Revisa estas selecciones antes de copiar:\n- " + "\n- ".join(conflicts))

    for slug, pair in PLAN.items():
        article = by_slug[slug]
        article["image_credit"] = "Rockstar Games · archivo proporcionado por el usuario"
        article["image_source"] = OFFICIAL_MEDIA
        article["image_rights_status"] = "Permiso comercial pendiente de confirmar antes de publicar con anuncios"
        article["image_caption"] = describe_source(pair[0])
        article["image_alt"] = describe_source(pair[0])
        article["cover_image"] = "assets/images/user-gta/" + slug + "-portada.webp"
        article["image_source_file"] = "imagenes gta/" + pair[0]
        media = []
        for usage, relative in zip(("cover", "inside"), pair):
            if usage == "cover":
                destination = ROOT / article["cover_image"]
            else:
                destination_rel = "assets/images/user-gta/" + slug + "-interior.webp"
                destination = ROOT / destination_rel
                media.append({"after_section": min(2, max(1, len(article["sections"]))),
                    "image": destination_rel, "alt": describe_source(relative),
                    "caption": describe_source(relative),
                    "credit": "Rockstar Games · archivo proporcionado por el usuario", "source": OFFICIAL_MEDIA,
                    "source_file": "imagenes gta/" + relative,
                    "rights_status": "Permiso comercial pendiente de confirmar antes de publicar con anuncios"})
            destination.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(DOWNLOADS / relative) as image:
                image = ImageOps.exif_transpose(image).convert("RGB")
                image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
                image.save(destination, "WEBP", quality=88, method=6)
        article["inline_media"] = media
        article.pop("cover_photo_needed", None)
        article.pop("inline_photo_needed", None)

    # The user-submitted Little Sam theory has no specific evidence image in this selection.
    little_sam = by_slug["gta-6-easter-egg-little-sam"]
    little_sam["cover_photo_needed"] = "FOTO PORTADA — evidencia visual concreta del supuesto easter egg Little Sam, con contexto de dónde aparece."
    little_sam["inline_photo_needed"] = "FOTO INTERIOR — detalle ampliado del supuesto easter egg y una vista del contexto para distinguir evidencia de teoría."
    articles_path.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imágenes GTA VI asignadas a {len(PLAN)} artículos nuevos: {len(selected)} archivos únicos.")
    print("Se conservaron las imágenes de los artículos que ya existían. Little Sam permanece pendiente de evidencia visual específica.")


def np_is_missing():
    try:
        import numpy
        return False
    except Exception:
        return True


if __name__ == "__main__":
    main()
