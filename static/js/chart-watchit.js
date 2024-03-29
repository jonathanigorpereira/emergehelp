$(document).ready(function () {
    const config = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "Informações sobre os batimentos cardíacos do usuário",
                backgroundColor: 'rgb(135, 206, 250)',
                borderColor: 'rgb(135, 206, 250)',
                data: [],
                fill: false,
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Dados transmitidos em tempo real'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Horário'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Batimentos'
                    },
                    ticks: {
                        min: 50,
                        max: 140,
                        stepSize: 10,
                        reverse: false,
                      },
                }]
            }
        }
    };

    const context = document.getElementById('canvas').getContext('2d');

    const lineChart = new Chart(context, config);

    const source = new EventSource("/chart-data");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (config.data.labels.length === 20) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }
        config.data.labels.push(data.time);
        config.data.datasets[0].data.push(data.value);
        lineChart.update();
    }
});


