// Here we put the theme and language to the localStorage
const element = document.body;
element.dataset.bsTheme = localStorage.getItem("theme");
element.dataset.bsTranslation = localStorage.getItem("lang");

// Here we put the name of the current page to the localStorage
const page = document.location.pathname;
localStorage.setItem("currentPage", page.substring(1, page.length));

// Here we have the function that switches the page between dark mode and light mode
function switchTheme() {
  const element = document.body;
  element.dataset.bsTheme =
    element.dataset.bsTheme == "light" ? "dark" : "light";
  localStorage.setItem("theme", element.dataset.bsTheme);
}

// Here we have the function that switch the language of the page between pt-br and en.
// I don't finished this function yet.
// The function just switche the value of language on localstorage
function switchLanguage() {
  let lang = document.body;
  lang.dataset.bsTranslation =
    lang.dataset.bsTranslation == "pt-br" ? "en" : "pt-br";
  localStorage.setItem("lang", lang.dataset.bsTranslation);
}

// Here its just a plan that i have to make the translation of the pages
// I don't no if this will work yet i have to try it first
let ptBr = {
  "#navText1": "Início",
  "#navText2": "Contato",
  "#navText": "Sobre",
  introText: "Introdução",
};

let en = {
  "#navText1": "Home",
  "#navText2": "Contat",
  "#navText": "About",
  introText: "Introduction",
};

// Function that switches the icon of the color modes
const spn = document.querySelector("#themeIcon span");
spn.textContent =
  localStorage.getItem("theme") === "light" ? "dark_mode" : "light_mode";

function switchIconTheme() {
  spn.textContent =
    localStorage.getItem("theme") === "light" ? "dark_mode" : "light_mode";
}
