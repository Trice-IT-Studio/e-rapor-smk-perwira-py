const search = document.querySelector('.input-group'),
    table_rows = document.querySelectorAll('tbody .searchable');

search.addEventListener('input', searchTable);

function searchTable() {
    table_rows.forEach((row) => {
        // Select specific cells or elements for searching
        let searchable_content = Array.from(row.querySelectorAll('td:not(.exclude)')) // Exclude unwanted elements (e.g., modals)
            .map(td => td.textContent.toLowerCase())
            .join(' '); // Combine text content for searching
        
        let search_data = search.value.toLowerCase();

        // Toggle the "hide" class based on the search
        row.classList.toggle('hide', searchable_content.indexOf(search_data) < 0);
    });
}
