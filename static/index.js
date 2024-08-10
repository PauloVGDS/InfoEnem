
const page = document.location.pathname;
localStorage.setItem("currentPage", page.substring(1, page.length));

function switchTheme() {
  const element = document.body;
  const spn = document.querySelector("#themeIcon span");

  element.dataset.bsTheme =
    element.dataset.bsTheme == "light" ? "dark" : "light";

  spn.textContent =
    localStorage.getItem("theme") === "light" ? "light_mode" : "dark_mode";

  localStorage.setItem("theme", element.dataset.bsTheme);
}

document.addEventListener("DOMContentLoaded", () => {
  const spn = document.querySelector("#themeIcon span");
  spn.textContent =
    localStorage.getItem("theme") == "light" ? "dark_mode" : "light_mode";

  const element = document.body;
  element.dataset.bsTheme = 
    localStorage.getItem("theme");

});
