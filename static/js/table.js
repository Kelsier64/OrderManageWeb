const rows = document.querySelectorAll(".detail .trs");
const data = {};
const users = new Set();
const releaseDates = new Set();

rows.forEach(row => {
    const cells = row.querySelectorAll("td");
    const user = cells[0].textContent.trim();
    const platform = cells[2].textContent.trim();
    const product = cells[3].textContent.trim();
    const releaseDate = cells[4].textContent.trim();
    const quantity = parseInt(cells[6].textContent.trim());

    if (!data[platform]) {
        data[platform] = {};
    }

    if (!data[platform][product]) {
        data[platform][product] = {};
    }

    if (!data[platform][product][releaseDate]) {
        data[platform][product][releaseDate] = {};
    }

    if (!data[platform][product][releaseDate][user]) {
        data[platform][product][releaseDate][user] = 0;
    }

    data[platform][product][releaseDate][user] += quantity;
    users.add(user);
    releaseDates.add(releaseDate);
});

const summaryHead = document.getElementById("summaryHead");
const headRow = document.createElement("tr");

const platformHeader = document.createElement("th");
platformHeader.textContent = "平台";
headRow.appendChild(platformHeader);

const productHeader = document.createElement("th");
productHeader.textContent = "品名";
headRow.appendChild(productHeader);

const releaseDateHeader = document.createElement("th");
releaseDateHeader.textContent = "上市日期";
headRow.appendChild(releaseDateHeader);

users.forEach(user => {
    const userHeader = document.createElement("th");
    userHeader.textContent = `${user}`;
    headRow.appendChild(userHeader);
});

const totalHeader = document.createElement("th");
totalHeader.textContent = "合計";
headRow.appendChild(totalHeader);

summaryHead.appendChild(headRow);

const summaryBody = document.getElementById("summaryBody");

for (const platform in data) {
    for (const product in data[platform]) {
        for (const releaseDate in data[platform][product]) {
            const row = document.createElement("tr");
            row.classList.add("newTr");
            row.classList.add(platform);

            const platformCell = document.createElement("td");
            const productCell = document.createElement("td");
            const releaseDateCell = document.createElement("td");

            platformCell.textContent = platform;
            productCell.textContent = product;
            releaseDateCell.textContent = releaseDate;

            row.appendChild(platformCell);
            row.appendChild(productCell);
            row.appendChild(releaseDateCell);

            let total = 0;

            users.forEach(user => {
                const userCell = document.createElement("td");
                const quantity = data[platform][product][releaseDate][user] || 0;
                userCell.textContent = quantity;
                row.appendChild(userCell);
                total += quantity;
            });

            const totalCell = document.createElement("td");
            totalCell.textContent = total;
            row.appendChild(totalCell);

            summaryBody.appendChild(row);
        }
    }
}
document.getElementById('table-select').addEventListener('change', function () {
    const detailTable = document.getElementById("detailTable");
    const summaryTable = document.getElementById("summaryTable");
    const detailSelect = document.querySelectorAll('.detailSelect');
    detailTable.classList.add('hidden');
    summaryTable.classList.add('hidden');
    if (this.value === "detail") {
        detailTable.classList.remove('hidden');
        summaryTable.classList.add('hidden');
        detailSelect.forEach(i => {
            i.classList.remove('hidden');
        });

    } else {
        detailTable.classList.add('hidden');
        summaryTable.classList.remove('hidden');
        detailSelect.forEach(i => {
            i.classList.add('hidden');
        });
    }
});



function populatePlatformOptions() {
    const platformSelect = document.getElementById('platform-select');
    const platforms = new Set();

    // Gather unique platform values from the table rows
    const rows = document.querySelectorAll('#detailTable .trs');
    rows.forEach(row => {
        platforms.add(row.cells[2].textContent);
    });

    // Create and append options to the platform select element
    platforms.forEach(platform => {
        const option = document.createElement('option');
        option.value = platform;
        option.textContent = platform;
        platformSelect.appendChild(option);
    });
}

function populateStoreOptions() {
    const storeSelect = document.getElementById('store-select');
    const stores = new Set();

    // Gather unique store values from the table rows
    const rows = document.querySelectorAll('#detailTable .trs');
    rows.forEach(row => {
        stores.add(row.cells[0].textContent);
    });

    // Create and append options to the store select element
    stores.forEach(store => {
        const option = document.createElement('option');
        option.value = store;
        option.textContent = store;
        storeSelect.appendChild(option);
    });
}
document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('sort-select');
    const platformSelect = document.getElementById('platform-select');
    const storeSelect = document.getElementById('store-select');
    sortTable();
    sortSelect.addEventListener('change', function() {
        sortTable();
    });

    platformSelect.addEventListener('change', function() {
        filterTable();
    });

    storeSelect.addEventListener('change', function() {
        filterTable();
    });

    // Populate platform and store select options
    populatePlatformOptions();
    populateStoreOptions();
});

function sortTable() {
    const table = document.getElementById('detailTable');
    const rows = Array.from(table.rows).slice(1); // Exclude the header row
    const sortSelect = document.getElementById('sort-select');
    const sortOrder = sortSelect.value;

    rows.sort((a, b) => {
        const dateA = new Date(a.cells[1].textContent);
        const dateB = new Date(b.cells[1].textContent);

        if (sortOrder === 'asc') {
            return dateA - dateB;
        } else {
            return dateB - dateA;
        }

    });

    rows.forEach(row => table.appendChild(row));
}



function filterTable() {
    const platformSelect = document.getElementById('platform-select');
    const storeSelect = document.getElementById('store-select');
    const selectedPlatform = platformSelect.value;
    const selectedStore = storeSelect.value;
    const trs = document.querySelectorAll('.trs');
    const newTr = document.querySelectorAll('.newTr');
    trs.forEach(tr => {
        const hasPlatform = selectedPlatform === 'all' || tr.classList.contains(selectedPlatform);
        const hasStore = selectedStore === 'all' || tr.classList.contains(selectedStore);

        if (hasPlatform && hasStore) {
            tr.classList.remove('hidden');
        } else {
            tr.classList.add('hidden');
        }
    });
    newTr.forEach(tr => {
        const hasPlatform = selectedPlatform === 'all' || tr.classList.contains(selectedPlatform);
        if (hasPlatform) {
            tr.classList.remove('hidden');
        } else {
            tr.classList.add('hidden');
        }
    });

}