const box = document.getElementById("search");
const list = document.getElementById("suggestions");
let timer = null;
let activeIndex = -1;

function clearList() {
  list.innerHTML = "";
  activeIndex = -1;
}

function selectName(name) {
  window.location.href = `/static/spot.html?name=${encodeURIComponent(name)}`;
}

function render(names) {
  clearList();
  names.forEach(name => {
    const li = document.createElement("li");
    li.textContent = name;
    li.addEventListener("click", () => selectName(name));
    list.appendChild(li);
  });
}

function setActive(index) {
  const items = list.children;
  if (!items.length) return;
  if (activeIndex >= 0) items[activeIndex].classList.remove("active");
  activeIndex = (index + items.length) % items.length;
  items[activeIndex].classList.add("active");
}

box.addEventListener("input", () => {
  clearTimeout(timer);
  const text = box.value.trim();
  if (!text) { clearList(); return; }

  timer = setTimeout(async () => {
    const res = await fetch(`/search?q=${encodeURIComponent(text)}`);
    const names = await res.json();
    if (box.value.trim() !== text) return;
    render(names);
  }, 200);
});

box.addEventListener("keydown", (e) => {
  if (e.key === "ArrowDown") {
    e.preventDefault();
    setActive(activeIndex + 1);
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    setActive(activeIndex === -1 ? list.children.length - 1 : activeIndex - 1);
  } else if (e.key === "Enter" && activeIndex >= 0) {
    e.preventDefault();
    selectName(list.children[activeIndex].textContent);
  } else if (e.key === "Escape") {
    clearList();
  }
});