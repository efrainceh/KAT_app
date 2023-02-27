document.body.onload = function () {
    let kat_id = document.getElementById("kat_id").innerHTML
    var count = 1;
    const myInterval = setInterval(checkRunState, 20000);
    async function checkRunState() {
        const URL = `http://127.0.0.1:5000/run/runcode/${kat_id}`;
        const response = await fetch(URL);
        const data = await response.json();
        count += 2;
        changeDots(count);
        if (data.runcode == 0) {
            clearInterval(myInterval);
            window.location.href = data.next_URL;
        }
    }
}

const changeDots = (n) => {
    multiplier = (n % 13) + 1;
    let str = " . "
    dots = document.getElementById("dots");
    dots.innerHTML = str.repeat(multiplier);
}
