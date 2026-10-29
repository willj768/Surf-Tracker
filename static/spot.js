const name = new URLSearchParams(window.location.search).get("name");
const results = document.getElementById("results");

let beachInfo = {};

async function loadBeachInfo() {
  try {
    const res = await fetch("/static/beach_info.json");
    if (!res.ok) throw new Error(`status ${res.status}`);
    beachInfo = await res.json();
  } catch (err) {
    console.error("Couldn't load beach information:", err);
  }
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function setBackground(name) {
  const url = `/static/images/${slugify(name)}.jpg`;
  const img = new Image();
  img.onload = () => document.body.style.setProperty("--bg", `url("${url}")`);
  img.onerror = () => {};
  img.src = url;
}

function showChart(name) {
  results.innerHTML = "";
  const img = document.createElement("img");
  img.src = `/chart/${encodeURIComponent(name)}`;
  img.alt = `Surf score chart for ${name}`;
  img.onerror = () => {
    img.remove();
    results.textContent = "No chart available for this beach.";
  };
  results.appendChild(img);
}

function showMap(spot) {
  const map = L.map("map", { scrollWheelZoom: false });

  // Frame roughly all of Devon and Cornwall
  map.fitBounds([[49.9, -6.4], [51.3, -2.8]]);

  L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    attribution: "Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community",
    maxZoom: 18,
  }
).addTo(map);

  L.circleMarker([spot.lat, spot.lon], {
    radius: 9,
    color: "white",
    weight: 2,
    fillColor: "#1e90ff",
    fillOpacity: 1,
  })
    .addTo(map)
    .bindTooltip(spot.name, { permanent: true, direction: "top" });
}

async function loadSpot() {
  try {
    const res = await fetch(`/spot/${encodeURIComponent(name)}`);
    if (!res.ok) throw new Error(`status ${res.status}`);
    const spot = await res.json();

    document.getElementById("spot-name").textContent = spot.name;
    const info = beachInfo[spot.name.toLowerCase()];

    document.getElementById("spot-description").textContent =
      info?.description || spot.description || "No description yet.";

    const credit = document.getElementById("photo-credit");

    if (info?.photoCredit) {
      const photo = info.photoCredit;

      credit.hidden = false;
      credit.replaceChildren();

      const photoLink = document.createElement("a");
      photoLink.href = photo.url;
      photoLink.target = "_blank";
      photoLink.rel = "noopener";
      photoLink.textContent = photo.text;

      credit.append("Photo: ", photoLink);

      if (photo.photographer) {
        credit.append(` by ${photo.photographer}`);
      }

      if (photo.license && photo.licenseUrl) {
        const licenseLink = document.createElement("a");
        licenseLink.href = photo.licenseUrl;
        licenseLink.target = "_blank";
        licenseLink.rel = "noopener";
        licenseLink.textContent = photo.license;

        credit.append(", licensed under ", licenseLink);
      }

      credit.append(".");

      if (photo.modification) {
        credit.append(` ${photo.modification}.`);
      }
    } else if (credit) {
      credit.hidden = true;
    }

    showMap(spot);
  } catch (err) {
    console.error(err);
    document.getElementById("spot-name").textContent = name;
    document.getElementById("spot-description").textContent =
      "Couldn't load details for this beach.";
    document.getElementById("map").remove();
  }
}

async function load() {
  if (!name) {
    document.getElementById("spot-name").textContent =
      "No beach selected";
    return;
  }

  document.title = `${name} - Surf Tracker`;

  await loadBeachInfo();

  setBackground(name);
  showChart(name);
  loadSpot();
}

load();