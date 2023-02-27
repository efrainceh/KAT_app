// Dropdownd functionality
const dropbtn = document.getElementById("dropbtn");
const dropdown = document.getElementById("profile-dropdown");

const toggleDropdown = () => {
    dropdown.classList.toggle("show");
}

dropbtn.addEventListener("click", function(e) {
    e.stopPropagation();
    toggleDropdown();
});

document.addEventListener("click", function(e) {
    if (dropdown.classList.contains("show")) {
        toggleDropdown();
    }
});

