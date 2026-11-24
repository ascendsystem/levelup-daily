(function () {
  "use strict";

  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");
  if (menuButton && nav) {
    menuButton.addEventListener("click", function () {
      const open = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(open));
      const menuLabel = menuButton.querySelector(".sr-only");
      if (menuLabel) menuLabel.textContent = open ? "Cerrar menú" : "Abrir menú";
      nav.classList.toggle("is-open", open);
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        menuButton.setAttribute("aria-expanded", "false");
        const menuLabel = menuButton.querySelector(".sr-only");
        if (menuLabel) menuLabel.textContent = "Abrir menú";
        nav.classList.remove("is-open");
      }
    });
  }

  const contactForm = document.querySelector("#contact-form");
  if (contactForm) {
    const validateButton = contactForm.querySelector("#contact-validate");
    const status = contactForm.querySelector("#contact-status");
    if (validateButton) validateButton.disabled = false;
    validateButton?.addEventListener("click", function () {
      if (!contactForm.reportValidity()) return;
      if (status) status.textContent = "Los campos son válidos, pero el mensaje no se ha enviado: falta configurar un servicio de recepción. No cierres esta página si quieres copiar el texto.";
    });
  }

  document.querySelectorAll("[data-progressive-grid]").forEach(function (grid) {
    const cards = Array.from(grid.querySelectorAll(".story-card"));
    const button = grid.parentElement.querySelector("[data-load-more]");
    let visible = 9;
    if (!button || cards.length <= visible) return;
    cards.slice(visible).forEach(function (card) { card.hidden = true; });
    button.hidden = false;
    button.addEventListener("click", function () {
      const next = Math.min(visible + 9, cards.length);
      cards.slice(visible, next).forEach(function (card) { card.hidden = false; });
      visible = next;
      if (visible >= cards.length) button.hidden = true;
    });
  });

  document.querySelectorAll("[data-reading-time]").forEach(function (label) {
    const content = document.querySelector(".article-content");
    if (!content) return;
    const count = (content.innerText || content.textContent || "").trim().split(/\s+/).filter(Boolean).length;
    const minutes = Math.max(1, Math.ceil(count / 210));
    label.textContent = "Lectura estimada: " + minutes + " min";
  });

  document.querySelectorAll("[data-share]").forEach(function (button) {
    button.addEventListener("click", async function () {
      const shareData = { title: document.title, text: document.querySelector(".article-dek")?.textContent || "", url: window.location.href };
      try {
        if (navigator.share) {
          await navigator.share(shareData);
          return;
        }
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(shareData.url);
          announce("Enlace copiado al portapapeles.");
          return;
        }
        window.prompt("Copia el enlace del artículo:", shareData.url);
      } catch (error) {
        if (error && error.name !== "AbortError") announce("No se pudo compartir el enlace.");
      }
    });
  });

  function announce(message) {
    let status = document.querySelector("#share-status");
    if (!status) {
      status = document.createElement("p");
      status.id = "share-status";
      status.setAttribute("role", "status");
      status.className = "search-status";
      document.querySelector(".article-tools")?.after(status);
    }
    status.textContent = message;
  }

  const banner = document.querySelector("#consent-banner");
  const dialog = document.querySelector("#consent-dialog");
  const consentKey = "levelupdaily-privacy-choice-v1";
  function readConsent() {
    try { return localStorage.getItem(consentKey); } catch (_) { return null; }
  }
  function storeConsent(choice) {
    try { localStorage.setItem(consentKey, JSON.stringify({ choice, analytics: false, ads: false, date: new Date().toISOString() })); } catch (_) {}
    if (banner) banner.hidden = true;
    if (dialog?.open) dialog.close();
  }
  if (banner && !readConsent()) banner.hidden = false;
  document.querySelectorAll("[data-open-consent]").forEach(function (button) {
    button.addEventListener("click", function () {
      if (!dialog) return;
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
    });
  });
  document.querySelectorAll("[data-close-consent]").forEach(function (button) {
    button.addEventListener("click", function () { if (dialog?.open) dialog.close(); });
  });
  document.querySelectorAll("[data-consent]").forEach(function (button) {
    button.addEventListener("click", function () {
      const choice = button.getAttribute("data-consent") === "reject" ? "rejected" : "saved";
      storeConsent(choice);
    });
  });
  dialog?.addEventListener("click", function (event) {
    if (event.target === dialog) dialog.close();
  });

  const topButton = document.querySelector(".to-top");
  if (topButton) {
    window.addEventListener("scroll", function () { topButton.classList.toggle("visible", window.scrollY > 650); }, { passive: true });
    topButton.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  function createAdBlockBait() {
    const bait = document.createElement("div");
    bait.className = "adsbox ad-banner ad-unit ad-placement text-ad";
    bait.setAttribute("aria-hidden", "true");
    bait.style.cssText = "position:absolute!important;left:-10000px!important;top:-10000px!important;width:12px!important;height:12px!important;overflow:hidden!important;pointer-events:none!important;";
    document.body.appendChild(bait);
    return bait;
  }

  function detectAdBlock() {
    return new Promise(function (resolve) {
      const bait = createAdBlockBait();
      window.setTimeout(function () {
        const style = window.getComputedStyle(bait);
        const blocked = !bait.isConnected || bait.offsetWidth < 2 || bait.offsetHeight < 2 || style.display === "none" || style.visibility === "hidden";
        bait.remove();
        resolve(blocked);
      }, 350);
    });
  }

  function showAdBlockGate() {
    if (document.querySelector("#adblock-gate")) return;
    const gate = document.createElement("dialog");
    gate.id = "adblock-gate";
    gate.className = "adblock-gate";
    gate.setAttribute("aria-labelledby", "adblock-title");
    gate.innerHTML = '<div class="adblock-gate-inner"><span class="eyebrow">LEVELUP DAILY</span><h2 id="adblock-title">Desactiva el bloqueador para seguir</h2><p>Para leer la web, pausa el bloqueador de anuncios para LEVELUP DAILY. Los espacios publicitarios están vacíos mientras se configura la cuenta de anuncios.</p><p class="adblock-help">Si usas una extensión, abre su icono en el navegador y permite este sitio. Si el bloqueo viene del propio navegador, desactiva la protección contra anuncios desde el icono del escudo.</p><button class="button button-primary" type="button" data-adblock-check>Ya lo he permitido · volver a comprobar</button><p class="adblock-status" role="status" aria-live="polite" data-adblock-status></p></div>';
    document.body.appendChild(gate);
    gate.addEventListener("cancel", function (event) { event.preventDefault(); });
    const button = gate.querySelector("[data-adblock-check]");
    const status = gate.querySelector("[data-adblock-status]");
    button.addEventListener("click", function () {
      button.disabled = true;
      button.textContent = "Comprobando…";
      status.textContent = "";
      detectAdBlock().then(function (blocked) {
        if (blocked) {
          button.disabled = false;
          button.textContent = "Ya lo he permitido · volver a comprobar";
          status.textContent = "El bloqueador sigue activo en este sitio. Paúsalo y vuelve a comprobar.";
          button.focus();
          return;
        }
        gate.close();
        gate.remove();
      });
    });
    if (typeof gate.showModal === "function") gate.showModal();
    else gate.setAttribute("open", "");
    button.focus();
  }

  const adsConfigured = document.querySelector('ins.adsbygoogle, [data-adsense-active="true"]');
  if (adsConfigured) {
    detectAdBlock().then(function (blocked) {
      if (blocked) showAdBlockGate();
    });
  }
})();
