async function searchHolidays() {
    const country = document.getElementById('country').value;
    const month = document.getElementById('month').value;
    const resultsDiv = document.getElementById('results');

    if (!country) {
        resultsDiv.innerHTML = '<div class="error">Please enter a country code</div>';
        return;
    }

    try {
        const response = await fetch('/holidays', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({country, month})
        });

        const holidays = await response.json();

        if (response.ok) {
            displayHolidays(holidays);
        } else {
            resultsDiv.innerHTML = `<div class="error">Error: ${holidays.error}</div>`;
        }
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

function displayHolidays(holidays) {
    const resultsDiv = document.getElementById('results');

    if (holidays.length === 0) {
        resultsDiv.innerHTML = '<div class="error">No holidays found</div>';
        return;
    }

    resultsDiv.innerHTML = holidays.map(holiday => `
                <div class="holiday-card">
                    <div class="holiday-name">${holiday.name}</div>
                    <div class="holiday-date">${formatDate(holiday.date)}</div>
                    <div class="holiday-type">${holiday.type}</div>
                    ${formatGreetings(holiday.greetings)}
                </div>
            `).join('');
}

function formatDate(dateString) {
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatGreetings(greetings) {
    if (!greetings || Object.keys(greetings).length === 0) {
        return '';
    }

    const languageNames = {
        en: 'English',
        ar: 'Arabic',
        he: 'Hebrew',
        ru: 'Russian',
        fr: 'French'
    };

    return `
                <div class="greetings">
                    ${Object.entries(greetings)
        .filter(([_, greeting]) => greeting)
        .map(([lang, greeting]) => `
                            <div class="greeting">
                                <strong>${languageNames[lang]}:</strong> ${greeting}
                            </div>
                        `).join('')}
                </div>
            `;
}