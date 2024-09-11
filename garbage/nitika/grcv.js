document.getElementById('generate-btn').addEventListener('click', function() {
    const dataInput = document.getElementById('data-input').value;
    const parsedData = parseData(dataInput);

    if (parsedData) {
        createGraph(parsedData);
    } else {
        alert('Invalid data format. Please enter data in the format: x1,y1;x2,y2;...');
    }
});

function parseData(input) {
    try {
        const pairs = input.split(';');
        const labels = [];
        const data = [];

        pairs.forEach(pair => {
            const [x, y] = pair.split(',').map(Number);
            labels.push(x);
            data.push(y);
        });

        return { labels, data };
    } catch (e) {
        return null;
    }
}

function createGraph({ labels, data }) {
    const ctx = document.getElementById('graphCanvas').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Data',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
