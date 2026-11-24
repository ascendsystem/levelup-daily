"""Check generated AdSense markup, page coverage and reserved placements."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

from adsense import ADSENSE_SCRIPT, mode, publisher_id

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, expected_client: str | None):
        super().__init__(convert_charrefs=True)
        self.expected_client = expected_client
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.errors: list[str] = []
        self.loaders = 0
        self.units = 0
        self.slots = 0

    def handle_starttag(self, tag, raw_attrs):
        attrs = {str(key): str(value or "") for key, value in raw_attrs}
        classes = set(attrs.get("class", "").split())
        ancestors = self.stack

        if "ad-slot" in classes:
            self.slots += 1

        if tag == "script" and ADSENSE_SCRIPT in attrs.get("src", ""):
            self.loaders += 1
            if not self.expected_client or f"client={self.expected_client}" not in attrs["src"]:
                self.errors.append("el cargador de AdSense no coincide con el ID de editor confirmado")

        if tag == "ins" and "adsbygoogle" in classes:
            self.units += 1
            enclosing_slot = any(
                parent_tag == "div"
                and "ad-slot" in parent_attrs.get("class", "").split()
                and parent_attrs.get("data-adsense-active") == "true"
                for parent_tag, parent_attrs in ancestors
            )
            if not enclosing_slot:
                self.errors.append("una unidad adsbygoogle está fuera de un espacio centralizado")
            if any(parent_tag in {"a", "nav", "button", "form"} for parent_tag, _ in ancestors):
                self.errors.append("una unidad publicitaria está dentro o junto a un elemento interactivo")
            if not self.expected_client or attrs.get("data-ad-client") != self.expected_client:
                self.errors.append("una unidad publicitaria usa un publisher ID inesperado")
            if not re.fullmatch(r"\d{5,20}", attrs.get("data-ad-slot", "")):
                self.errors.append("una unidad publicitaria carece de un ID de unidad válido")
            if attrs.get("data-ad-format") != "auto" or attrs.get("data-full-width-responsive") != "true":
                self.errors.append("una unidad no usa el formato adaptable establecido")

        if tag not in self.VOID:
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return


def public_site(site: dict) -> bool:
    from urllib.parse import urlparse
    base = str(site.get("base_url", "")).rstrip("/")
    parsed = urlparse(base)
    return bool(parsed.scheme == "https" and parsed.netloc and "." in parsed.netloc
                and not any(token in base.lower() for token in ("tu-usuario", "example.com", "localhost", "pendiente")))


def audit_generated_site(root: Path = ROOT, site: dict | None = None) -> dict:
    if site is None:
        site = json.loads((root / "site.json").read_text(encoding="utf-8"))
    current_mode = mode(site)
    client = publisher_id(site)
    should_load = public_site(site) and current_mode in {"review", "active"}
    errors: list[str] = []
    html_pages = sorted(root.rglob("*.html"))
    restricted = {
        "404.html", "buscar/index.html", "sobre-nosotros/index.html", "contacto/index.html",
        "aviso-legal/index.html", "politica-de-cookies/index.html",
        "politica-de-privacidad/index.html", "politica-editorial/index.html",
    }
    total_units = total_loaders = total_slots = 0

    for page in html_pages:
        relative = page.relative_to(root).as_posix()
        parts = relative.split("/")
        source = page.read_text(encoding="utf-8")
        is_eligible = (relative == "index.html"
                       or 'class="page-wrap listing-page"' in source
                       or 'class="page-wrap article-page"' in source)
        parser = PageParser(client)
        parser.feed(source)
        total_units += parser.units
        total_loaders += parser.loaders
        total_slots += parser.slots
        if parser.errors:
            errors.extend(f"{relative}: {error}" for error in parser.errors)
        if parser.loaders > 1:
            errors.append(f"{relative}: cargador de AdSense repetido {parser.loaders} veces")
        expected_loader = should_load and is_eligible
        if parser.loaders != int(expected_loader):
            errors.append(f"{relative}: se esperaba {int(expected_loader)} cargador(es), hay {parser.loaders}")
        if (relative in restricted or not is_eligible) and parser.units:
            errors.append(f"{relative}: hay anuncios en una página excluida o no editorial")
        if current_mode != "active" and parser.units:
            errors.append(f"{relative}: se publicaron unidades cuando el modo no está active")

    if current_mode == "active" and total_units == 0:
        errors.append("modo active sin unidades publicitarias en las páginas generadas")
    if current_mode != "active" and total_units:
        errors.append("hay unidades activas con AdSense en modo off/review")

    ads_txt = root / "ads.txt"
    if should_load and ads_txt.is_file() and client:
        expected = f"google.com, {client.removeprefix('ca-')}, DIRECT, f08c47fec0942fa0"
        if expected not in {line.strip() for line in ads_txt.read_text(encoding="utf-8-sig").splitlines()}:
            errors.append("ads.txt no incluye la línea del publisher ID confirmado")
    elif should_load and client and not ads_txt.is_file():
        errors.append("falta ads.txt con publisher ID confirmado en la raíz del sitio")

    return {"errors": errors, "pages": len(html_pages), "units": total_units,
            "loaders": total_loaders, "slots": total_slots, "mode": current_mode,
            "has_publisher_id": bool(client), "ads_txt_present": ads_txt.is_file()}


def main() -> int:
    report = audit_generated_site()
    print(f"AdSense preflight: {report['pages']} HTML; modo={report['mode']}; "
          f"cargadores={report['loaders']}; unidades={report['units']}; espacios={report['slots']}; "
          f"ads.txt={'sí' if report['ads_txt_present'] else 'no'}.")
    if report["errors"]:
        for error in report["errors"]:
            print("ERROR: " + error)
        return 1
    print("Comprobación de marcado y ubicaciones superada. La revisión visual y el Centro de políticas siguen requiriendo la cuenta de Google.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
