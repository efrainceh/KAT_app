document.body.onload = function () {

    var count = 1;
    let kat_id = document.getElementById("kat_id").innerHTML
    const myInterval = setInterval(checkRunState, 10000);

    async function checkRunState() {

        const URL = ` http://localhost:8080/run/runcode/${kat_id}`;
        // const URL = `http://127.0.0.1:5000/run/runcode/${kat_id}`;
        const response = await fetch(URL);
        const data = await response.json();
        
        if (data.run_state == 0) {

            clearInterval(myInterval);
            window.location.href = data.next_URL;

        }

        // Increase the number of dots shown on the website so that the user knows
        // the program is still going
        count += 2;
        changeDots(count);

    }

}

const changeDots = (n) => {

    multiplier = (n % 13) + 1;
    let str = " . "
    dots = document.getElementById("dots");
    dots.innerHTML = str.repeat(multiplier);

}
