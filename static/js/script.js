const menuNav = document.querySelector("body > header > nav")
const menuNavContent = document.querySelector("body > header > nav > ul")

function burgerMenu() {
    menuNavContent.classList.toggle("menu-open")
}
menuNav.addEventListener("click", burgerMenu)
