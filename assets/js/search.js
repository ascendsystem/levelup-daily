(function () {
  "use strict";
  const form = document.querySelector("#results-search");
  const input = document.querySelector("#results-q");
  const status = document.querySelector("#search-status");
  const results = document.querySelector("#search-results");
  if (!form || !input || !status || !results) return;

  const params = new URLSearchParams(window.location.search);
  input.value = params.get("q") || "";
  const indexUrl = "../assets/data/search-index.json";
  const inlineIndex = document.querySelector("#search-data");
  const loadIndex = inlineIndex
    ? Promise.resolve().then(function () { return JSON.parse(inlineIndex.textContent); })
    : fetch(indexUrl).then(function (response) {
      if (!response.ok) throw new Error("No se pudo cargar el índice.");
      return response.json();
    });
  const localLink = function (route) {
    return "../" + route + (route.endsWith("/") ? "index.html" : "");
  };
  const normalize = function (value) {
    return (value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  };
  const matches = function (text, token) {
    if (token.length >= 3) return text.includes(token);
    return new RegExp("(?:^|[^a-z0-9])" + token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?=$|[^a-z0-9])").test(text);
  };

  function addResult(item) {
    const article = document.createElement("article");
    article.className = "story-card";
    const imageLink = document.createElement("a");
    imageLink.className = "card-image";
    imageLink.href = localLink(item.url);
    if (item.image) {
      const image = document.createElement("img");
      image.src = "../" + item.image;
      image.alt = "Imagen relacionada con " + item.title;
      image.loading = "lazy";
      image.width = 1200;
      image.height = 720;
      imageLink.appendChild(image);
    } else {
      const placeholder = document.createElement("div");
      placeholder.className = "photo-request photo-request-card";
      const kicker = document.createElement("span");
      kicker.className = "photo-request-kicker";
      kicker.textContent = "FOTO PENDIENTE";
      const label = document.createElement("strong");
      label.textContent = item.coverRequest || "Foto relacionada con " + item.title;
      placeholder.append(kicker, label);
      imageLink.appendChild(placeholder);
    }
    const body = document.createElement("div");
    body.className = "card-body";
    const category = document.createElement("a");
    category.className = "category-label";
    category.href = localLink(item.categoryUrl);
    category.textContent = item.category;
    const heading = document.createElement("h3");
    const title = document.createElement("a");
    title.href = localLink(item.url);
    title.textContent = item.title;
    heading.appendChild(title);
    const description = document.createElement("p");
    description.textContent = item.description;
    const meta = document.createElement("div");
    meta.className = "card-meta";
    const time = document.createElement("time");
    time.dateTime = item.updated;
    time.textContent = new Date(item.updated + "T12:00:00").toLocaleDateString("es-ES");
    const read = document.createElement("span");
    read.textContent = item.readTime + " min";
    meta.append(time, read);
    body.append(category, heading, description, meta);
    article.append(imageLink, body);
    results.appendChild(article);
  }

  function render(items) {
    results.replaceChildren();
    const query = normalize(input.value);
    if (!query) {
      status.textContent = "Escribe un tema, juego o serie para buscar.";
      return;
    }
    const tokens = query.split(/\s+/).filter(Boolean);
    const ranked = items.map(function (item) {
      const title = normalize(item.title);
      const category = normalize(item.category);
      const text = normalize(item.text);
      const score = tokens.reduce(function (total, token) {
        return total + (matches(title, token) ? 5 : 0) + (matches(category, token) ? 3 : 0) + (matches(text, token) ? 1 : 0);
      }, 0);
      return { item, score };
    }).filter(function (entry) { return entry.score > 0; })
      .sort(function (a, b) { return b.score - a.score || b.item.updated.localeCompare(a.item.updated); })
      .slice(0, 30);
    ranked.forEach(function (entry) { addResult(entry.item); });
    status.textContent = ranked.length ? ranked.length + (ranked.length === 1 ? " resultado" : " resultados") + " para «" + input.value.trim() + "»" : "No encontramos resultados para «" + input.value.trim() + "». Prueba con otro término o una categoría.";
    if (!ranked.length) {
      const empty = document.createElement("p");
      empty.className = "search-results-empty";
      empty.textContent = "Prueba términos como GTA VI, mapa, anime, PS5 o PC gaming.";
      results.appendChild(empty);
    }
  }

  loadIndex.then(function (items) {
    render(items);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const query = input.value.trim();
      const url = new URL(window.location.href);
      if (query) url.searchParams.set("q", query);
      else url.searchParams.delete("q");
      if (window.location.protocol !== "file:") {
        history.pushState({}, "", url);
      }
      render(items);
    });
    window.addEventListener("popstate", function () {
      input.value = new URLSearchParams(window.location.search).get("q") || "";
      render(items);
    });
  }).catch(function () {
    status.textContent = "No se pudo cargar el índice de búsqueda. Vuelve a cargar la página o usa las categorías.";
  });
})();
