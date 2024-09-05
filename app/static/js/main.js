function toggleInputFields() {
    const action = document.getElementById('action').value;
    const matchDictInput = document.getElementById('matchDict');

    if (action === 'update') {
        matchDictInput.style.display = 'block';
    } else {
        matchDictInput.style.display = 'none';
    }
}

function manageEntry() {
    const url = document.getElementById('sheetUrl').value;
    const entryDict = document.getElementById('entryDict').value;
    const matchDict = document.getElementById('matchDict').value;
    const action = document.getElementById('action').value;
    let parsedEntry, parsedMatch;

    try {
        parsedEntry = JSON.parse(entryDict);
        if (action === 'update') {
            parsedMatch = JSON.parse(matchDict);
        }
    } catch (error) {
        alert('Invalid JSON format. Please enter a valid dictionary.');
        return;
    }

    const bodyData = {
        spreadsheet_url: url,
        action: action,
        entry_dict: action === 'update' ? { match_dict: parsedMatch, update_dict: parsedEntry } : parsedEntry
    };

    fetch('/manage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
    })
    .then(response => response.json())
    .then(data => alert(data.message || data.error))
    .catch(error => alert('An error occurred: ' + error));
}

function fetchEntries() {
    const url = document.getElementById('sheetUrl').value;
    fetch('/read', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ spreadsheet_url: url })
    })
    .then(response => response.json())
    .then(data => {
        let table = '<table>';
        table += '<tr>';
        const headers = data.formatted_data.split('\n')[0].split('\t');
        headers.forEach(header => {
            table += `<th>${header}</th>`;
        });
        table += '</tr>';

        const rows = data.formatted_data.split('\n').slice(1);
        rows.forEach(row => {
            table += '<tr>';
            row.split('\t').forEach(cell => {
                table += `<td>${cell}</td>`;
            });
            table += '</tr>';
        });
        table += '</table>';
        document.getElementById('output').innerHTML = table;
    })
    .catch(error => alert('An error occurred: ' + error));
}
