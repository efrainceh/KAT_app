function deleteTableRow(deleteButton) {
    var rowIndex = deleteButton.parentNode.parentNode.rowIndex;
    var runID = document.getElementById("table-runs").rows[rowIndex].cells[0].innerHTML;
    deleteInDB(runID, rowIndex);
}

async function deleteInDB(id, rowIndex) {
    const URL = `http://127.0.0.1:5000/profile/delete_run/${id}`;
    const response = await fetch(URL, {method:"DELETE"});
    if (response.ok) {
        document.getElementById("table-runs").deleteRow(rowIndex);
    }
}

function showFigure(row) {
    var rowIndex = row.parentNode.rowIndex;
    var runID = document.getElementById("table-runs").rows[rowIndex].cells[0].innerHTML;
    getFigure(runID);
}

async function getFigure(id) {
    const URL = `http://127.0.0.1:5000/result/image_url/${id}`;
    const response = await fetch(URL);
    const data = await response.json();
    document.getElementById("run-img").src = data.img_URL;
}







 
