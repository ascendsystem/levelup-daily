"""Central AdSense configuration, rendering and ads.txt helpers.

No account-specific identifiers or Google snippets are generated unless the
publisher ID has been explicitly confirmed by the site owner.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

POSITIONS = {
    "home_mid",
    "home_after_headlines",
    "category_mid",
    "article_after_first_section",
    "article_mid",
}
MODES = {"off", "review", "active"}
PUBLISHER_RE = re.compile(r"^ca-pub-(\d{16})$")
UNIT_RE = re.compile(r"^\d{5,20}$")
ADSENSE_SCRIPT = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
ADS_TXT_CONTACT = "f08c47fec0942fa0"


def settings(site: dict) -> dict:
    value = site.get("adsense", {})
    return value if isinstance(value, dict) else {}


def mode(site: dict) -> str:
    return str(settings(site).get("mode", "off")).strip().lower()


def publisher_id(site: dict) -> str | None:
    config = settings(site)
    if config.get("publisher_id_confirmed") is not True:
        return None
    value = str(site.get("adsense_publisher_id", "")).strip()
    return value if PUBLISHER_RE.fullmatch(value) else None


def validate_config(site: dict, root: Path) -> None:
    config = settings(site)
    current_mode = mode(site)
    if current_mode not in MODES:
        raise ValueError("site.json: adsense.mode debe ser off, review o active.")

    units = config.get("units", {})
    if not isinstance(units, dict):
        raise ValueError("site.json: adsense.units debe ser un objeto de IDs de unidades.")
    unknown = set(units) - POSITIONS
    if unknown:
        raise ValueError("site.json: ubicaciones AdSense desconocidas: " + ", ".join(sorted(unknown)))
    for position, unit_id in units.items():
        if unit_id and not UNIT_RE.fullmatch(str(unit_id).strip()):
            raise ValueError(f"site.json: ID de unidad no válido en {position}; copia el ID real de AdSense.")

    if current_mode == "off":
        return
    if publisher_id(site) is None:
        raise ValueError("AdSense está en modo review/active, pero falta confirmar un ID ca-pub real de 16 dígitos en site.json.")

    if current_mode == "active":
        if not any(str(value).strip() for value in units.values()):
            raise ValueError("AdSense active requiere al menos un ID de unidad real configurado.")
        privacy = config.get("privacy", {})
        if not isinstance(privacy, dict) or privacy.get("certified_tcf_cmp_confirmed") is not True:
            raise ValueError("No se activa AdSense: confirma primero en la cuenta una CMP certificada por Google con integración TCF para EEE/Reino Unido/Suiza.")
        if privacy.get("preferences_entrypoint_confirmed") is not True:
            raise ValueError("No se activa AdSense: configura y comprueba el control para reabrir/revocar preferencias de privacidad.")
        cmp_file = str(privacy.get("integration_file", "content/adsense-cmp.html"))
        cmp_path = root / cmp_file
        if not cmp_path.is_file():
            raise ValueError(f"Falta el archivo de integración CMP configurado: {cmp_file}")
        markup = cmp_path.read_text(encoding="utf-8").strip()
        if not markup or "PENDIENTE" in markup.upper() or "<script" not in markup.lower():
            raise ValueError("No se activa AdSense: falta pegar y comprobar el código real de la CMP en su archivo de integración.")
        preferences_file = str(privacy.get("preferences_file", "content/adsense-cmp-preferences.html"))
        preferences_path = root / preferences_file
        if not preferences_path.is_file():
            raise ValueError(f"Falta el controlador para reabrir la CMP configurado: {preferences_file}")
        preferences_markup = preferences_path.read_text(encoding="utf-8").strip()
        if not preferences_markup or "PENDIENTE" in preferences_markup.upper() or "<script" not in preferences_markup.lower():
            raise ValueError("No se activa AdSense: falta configurar el control de preferencias de la CMP.")


def global_tag(site: dict) -> str:
    current_mode = mode(site)
    client = publisher_id(site)
    if current_mode not in {"review", "active"} or not client:
        return ""
    return (f'<script async src="{ADSENSE_SCRIPT}?client={html.escape(client, quote=True)}" '
            'crossorigin="anonymous"></script>')


def cmp_markup(site: dict, root: Path) -> str:
    if mode(site) != "active":
        return ""
    privacy = settings(site).get("privacy", {})
    file_name = str(privacy.get("integration_file", "content/adsense-cmp.html"))
    path = root / file_name
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def cmp_preferences_markup(site: dict, root: Path) -> str:
    if mode(site) != "active":
        return ""
    privacy = settings(site).get("privacy", {})
    file_name = str(privacy.get("preferences_file", "content/adsense-cmp-preferences.html"))
    path = root / file_name
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def recovery_markup(site: dict, root: Path) -> str:
    """Include only account-provided recovery snippets, unchanged, in active mode."""
    if mode(site) != "active" or not publisher_id(site):
        return ""
    files = (
        root / "content" / "adsense-recovery-tag.html",
        root / "content" / "adsense-error-protection.html",
    )
    parts = []
    for path in files:
        if not path.is_file():
            continue
        markup = path.read_text(encoding="utf-8").strip()
        if markup and "PENDIENTE" not in markup.upper() and "<script" in markup.lower():
            parts.append(markup)
    return "\n".join(parts)


def render_slot(site: dict, position: str) -> str:
    if position not in POSITIONS:
        raise ValueError(f"Ubicación publicitaria desconocida: {position}")
    config = settings(site)
    client = publisher_id(site)
    unit_id = str(config.get("units", {}).get(position, "")).strip()
    if mode(site) != "active" or not client or not UNIT_RE.fullmatch(unit_id):
        return '<div class="ad-slot" aria-hidden="true" data-ad-reserved="true"></div>'
    safe_client = html.escape(client, quote=True)
    safe_unit = html.escape(unit_id, quote=True)
    safe_position = html.escape(position, quote=True)
    return (f'<div class="ad-slot" data-ad-position="{safe_position}" data-adsense-active="true">'
            f'<ins class="adsbygoogle" style="display:block" data-ad-client="{safe_client}" '
            f'data-ad-slot="{safe_unit}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
            '<script>(window.adsbygoogle = window.adsbygoogle || []).push({});</script></div>')


def sync_ads_txt(root: Path, site: dict) -> str:
    """Add the Google seller record when configured; preserve every existing line."""
    current_mode = mode(site)
    if current_mode == "off":
        return "unchanged (AdSense off)"
    client = publisher_id(site)
    if not client:
        raise ValueError("No se modifica ads.txt: no hay publisher ID confirmado.")
    seller_id = client.removeprefix("ca-")
    record = f"google.com, {seller_id}, DIRECT, {ADS_TXT_CONTACT}"
    path = root / "ads.txt"
    existing = path.read_text(encoding="utf-8-sig") if path.is_file() else ""
    lines = existing.splitlines()
    same_publisher = [line.strip() for line in lines
                      if re.match(rf"^google\.com\s*,\s*{re.escape(seller_id)}\s*,", line.strip(), re.I)]
    if same_publisher:
        if same_publisher == [record]:
            return "unchanged"
        raise ValueError("ads.txt ya contiene este publisher ID con otra línea. No se ha sobrescrito ningún dato; revísalo manualmente.")
    if record in (line.strip() for line in lines):
        return "unchanged"
    prefix = existing
    if prefix and not prefix.endswith(("\n", "\r")):
        prefix += "\n"
    path.write_text(prefix + record + "\n", encoding="utf-8", newline="")
    return "created" if not existing else "updated"
