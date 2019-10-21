$(document).ready(function() {
    const spinner = $('#spinner');
    $("#form").submit(function(event) {
        event.preventDefault();
        const username_input = $("#username");
        const username = username_input.val();
        if(username === ""){
            return;
        }
        const res =  $('#res');
        res.hide();
        $("#table tbody").empty();
        spinner.show();
        fetch('/', {
            method: 'post',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({'username': username})
        }).then(function(response) {
            return response.json();
        }).then(function(json) {
            username_input.val("");
            let count = 0;
            for (const [key, value] of Object.entries(json['following'])) {
                count++;
                const channel = key;
                const follow_date = value;
                $("#table tbody").append("<tr>\n" +
                                             `<td>${channel}</td>\n` +
                                             `<td>${follow_date}</td>\n` +
                                         "</tr>");
            }
            if(count < 100){
                sortTable(1);
            }
            res.show();
            spinner.hide();
        });
    });
});

function downloadCSV(csv, filename) {
    /*
        Source code:
        https://www.codexworld.com/export-html-table-data-to-csv-using-javascript/
    */
    let csvFile;
    let downloadLink;
    csvFile = new Blob([csv], {type: "text/csv"});
    downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

function exportTableToCSV(filename) {
    /*
        Source code:
        https://www.codexworld.com/export-html-table-data-to-csv-using-javascript/
    */
    let csv = [];
    let rows = document.querySelectorAll("table tr");
    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll("td, th");
        for (let j = 0; j < cols.length; j++)
            row.push(cols[j].innerText);
        csv.push(row.join(","));
    }
    downloadCSV(csv.join("\n"), filename);
}

function sortTable(n) {
    /*
        Source code:
        https://www.w3schools.com/howto/howto_js_sort_table.asp
    */
    let table, rows, switching, i, x, y, shouldSwitch, dir, switchCount = 0;
    table = document.getElementById("table");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir === "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount ++;
        } else {
            if (switchCount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}