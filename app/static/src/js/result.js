$(document).ready(function () {
    // console.log('ready')

})

/**
 * chartJs
 */
const radarData = {
    labels: [
        // [radar[3][0].substr(0,4), radar[3][0].substr(4)],
        radar[3][0],
        // [radar[1][0].substr(0,3), radar[1][0].substr(3)],
        radar[1][0].split(''),
        // [radar[0][0].substr(0,4), radar[0][0].substr(4)],
        radar[0][0],
        // [radar[2][0].substr(0,5), radar[2][0].substr(5)],
        radar[2][0].split('')
    ],
    datasets: [{
        data: [radar[3][3], radar[1][3], radar[0][3], radar[2][3]],
        fill: true,
        backgroundColor: 'rgba(76,175,80, 0.2)',
        borderColor: 'rgb(76,175,80)',
        pointBackgroundColor: 'rgba(76,175,80,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: 'rgba(255,255,255,1)',
        pointHoverBorderColor: 'rgb(76,175,80)',
        pointBorderWidth: 1,
        pointRadius: 7,
        pointHoverRadius: 10,
        pointStyle: 'circle',
        hidden: false
    }]
};

const radarConfig = {
    type: 'radar',
    data: radarData,
    options: {
        elements: {
            line: {
                borderWidth: 3
            }
        },
        // 額外項目
        plugins: {
            // 圖例
            legend: {
                // 顯示標籤
                display: false,
                labels: {
                    color: 'rgba(29, 66, 30, 1)'
                }
            },
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(161,192,224,0.5)',
                titleFont: {
                    size: 20
                },
                titleColor: 'black',
                bodyFont: {
                    size: 20
                },
                bodyColor: 'black',
                usePointStyle: true,
                displayColors: true
            },
        },
        scales: {
            r: {
                beginAtZero: true,
                min: 0,
                max: 100,
                ticks: {
                    font: {
                        size: 20
                    },
                    color: 'rgba(29, 66, 30, 1)',
                    maxTicksLimit: 10,
                },
                pointLabels: {
                    color: 'rgba(29, 66, 30, 1)',
                    font: {
                        size: 20,
                        weight: 700
                    }
                },
                angleLines: {
                    color: 'rgba(29, 66, 30, 0.5)'
                },
                grid: {
                    color: 'rgba(29, 66, 30, 1)'
                },
            }
        }
    }
};

var myRadar = new Chart(
    document.getElementById('myRadar'),
    radarConfig
);