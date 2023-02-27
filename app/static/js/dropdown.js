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

// Delete account link
const confirmation = () => {
    if (window.confirm("Are you sure you want to delete your account?")) {
        deleteUser();
    }
}

async function deleteUser() {
    const URL = "http://127.0.0.1:5000/profile/delete_user";
    const response = await fetch(URL, {method:"DELETE"});
    const data = await response.json();
    alert("Your account has been removed from the server.")
    window.location.href = data.next_URL;
}