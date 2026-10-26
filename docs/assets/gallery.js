/* USB_BSD / GitHub Pages gallery. No trackers, remote resources or execution of media. */
(() => {
  "use strict";

  const grid = document.getElementById("photo-grid");
  const status = document.getElementById("photo-status");
  const modal = document.getElementById("photo-dialog");
  const modalImage = document.getElementById("dialog-image");
  const modalTitle = document.getElementById("dialog-title");
  const modalCaption = document.getElementById("dialog-caption");
  const close = document.getElementById("dialog-close");
  if (!grid || !status || !modal || !modalImage || !modalTitle || !modalCaption || !close) return;

  const slots = [
    { id: "desktop", number: "01", category: "FREEBSD / GNOME", title: "Pulpit systemu", detail: "Widok sesji GNOME na stanowisku wdrożeniowym" },
    { id: "disk", number: "02", category: "STORAGE / USB", title: "Wolumin CHERUB_DATA", detail: "Widok nośnika w menedżerze plików" },
    { id: "validation", number: "03", category: "AUDYT / TERMINAL", title: "Walidacja montowania", detail: "Wynik rzeczywistej kontroli ext2fs i read-only" },
    { id: "station", number: "04", category: "HARDWARE / LAB", title: "Stacja robocza", detail: "Fotografia lokalnej konfiguracji sprzętowej" }
  ];

  const validSource = (src) => typeof src === "string" &&
    /^assets\/photos\/[a-z0-9][a-z0-9._-]*\.(?:webp|png|jpe?g)$/i.test(src) &&
    !src.includes("..");

  let opener = null;
  const label = (name, value) => {
    const n = document.createElement(name);
    n.textContent = value;
    return n;
  };

  function placeholder(slot) {
    const article = document.createElement("article");
    article.className = "gallery-card gallery-card--empty";
    const image = document.createElement("div");
    image.className = "gallery-card__media gallery-card__media--empty";
    image.setAttribute("aria-hidden", "true");
    image.append(label("span", slot.number));
    image.append(label("span", "PHOTO PENDING"));
    article.append(image);
    const body = document.createElement("div");
    body.className = "gallery-card__body";
    const group = label("span", slot.category);
    group.className = "gallery-card__category";
    const title = label("h3", slot.title);
    const desc = label("p", slot.detail);
    body.append(group, title, desc);
    article.append(body);
    return article;
  }

  function show(photo, button) {
    opener = button;
    modalImage.src = photo.src;
    modalImage.alt = photo.alt;
    modalTitle.textContent = photo.title;
    modalCaption.textContent = photo.caption;
    if (typeof modal.showModal === "function") modal.showModal();
  }

  function photoCard(photo) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "gallery-card gallery-card--photo";
    button.setAttribute("aria-label", "Otwórz zdjęcie: " + photo.title);

    const image = document.createElement("img");
    image.className = "gallery-card__media";
    image.src = photo.src;
    image.alt = photo.alt;
    image.loading = "lazy";
    image.decoding = "async";
    const body = document.createElement("div");
    body.className = "gallery-card__body";
    const group = label("span", photo.category || "DOKUMENTACJA");
    group.className = "gallery-card__category";
    body.append(group, label("h3", photo.title), label("p", photo.caption));
    button.append(image, body);
    button.addEventListener("click", () => show(photo, button));
    return button;
  }

  function render(photos) {
    const valid = photos.filter(photo =>
      photo && validSource(photo.src) &&
      typeof photo.title === "string" && typeof photo.alt === "string" &&
      typeof photo.caption === "string"
    ).slice(0, 24);
    const content = document.createDocumentFragment();
    const filled = new Set();

    for (const photo of valid) {
      filled.add(photo.slot);
      content.append(photoCard(photo));
    }
    for (const slot of slots) {
      if (!filled.has(slot.id)) content.append(placeholder(slot));
    }
    grid.replaceChildren(content);
    status.textContent = valid.length === 0 ?
      "Galeria jest przygotowana. Oczekuje na fotografie stanowiska." :
      "Opublikowane materiały: " + valid.length + ". Wybierz zdjęcie, aby je powiększyć.";
  }

  close.addEventListener("click", () => modal.close());
  modal.addEventListener("click", event => {
    if (event.target === modal) modal.close();
  });
  modal.addEventListener("close", () => {
    modalImage.removeAttribute("src");
    if (opener) opener.focus();
    opener = null;
  });

  fetch("data/gallery.json", { cache: "no-store" })
    .then(response => {
      if (!response.ok) throw new Error("Manifest unavailable");
      return response.json();
    })
    .then(data => {
      if (data.schemaVersion !== 1 || !Array.isArray(data.photos)) throw new Error("Invalid manifest");
      render(data.photos);
    })
    .catch(() => {
      status.textContent = "Zdjęcia jeszcze niedostępne. Repozytorium zawiera dokumentację techniczną.";
    });
})();
