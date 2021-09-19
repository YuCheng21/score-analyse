$(document).ready(function () {
    // console.log('ready')

})

/**
 * Theme Color
 */
const style = getComputedStyle(document.body);
const theme = {};
theme.primary = style.getPropertyValue('--bs-primary');
theme.secondary = style.getPropertyValue('--bs-secondary');
theme.success = style.getPropertyValue('--bs-success');
theme.info = style.getPropertyValue('--bs-info');
theme.warning = style.getPropertyValue('--bs-warning');
theme.danger = style.getPropertyValue('--bs-danger');
theme.light = style.getPropertyValue('--bs-light');
theme.dark = style.getPropertyValue('--bs-dark');

/**
 * chartJs
 */

// 資料標籤
const labels = [
    // [radar[3][0].substr(0,4), radar[3][0].substr(4)],
    radar[3][0],
    // [radar[1][0].substr(0,3), radar[1][0].substr(3)],
    radar[1][0].split(''),
    // [radar[0][0].substr(0,4), radar[0][0].substr(4)],
    radar[0][0],
    // [radar[2][0].substr(0,5), radar[2][0].substr(5)],
    radar[2][0].split('')
]

// 資料值
const data = [
    radar[3][3],
    radar[1][3],
    radar[0][3],
    radar[2][3]
]

// 資料集設定
const dataset = [
    {
        data: data,
        fill: true,
        backgroundColor: `${theme.primary}20`,
        borderColor: `${theme.primary}`,
        pointBackgroundColor: `${theme.primary}`,
        pointBorderColor: `${theme.light}`,
        pointHoverBackgroundColor: `${theme.warning}`,
        pointHoverBorderColor: `${theme.primary}`,
        pointBorderWidth: 1,
        pointRadius: 7,
        pointHoverRadius: 10,
        pointStyle: 'circle',
        hidden: false
    }
]

// 雷達圖資料設定
const radarData = {
    labels: labels,
    datasets: dataset
};

// 雷達圖屬性設定
const radarOptions = {
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
                color: `${theme.primary}`
            }
        },
        tooltip: {
            enabled: true,
            backgroundColor: `${theme.warning}50`,
            titleFont: {
                size: 20
            },
            titleColor: `${theme.dark}`,
            bodyFont: {
                size: 20
            },
            bodyColor: `${theme.dark}`,
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
                color: `${theme.dark}`,
                maxTicksLimit: 10,
            },
            pointLabels: {
                color: `${theme.dark}`,
                font: {
                    size: 20,
                    weight: 700
                }
            },
            angleLines: {
                color: `${theme.primary}`
            },
            grid: {
                color: `${theme.primary}`
            },
        }
    }
}

// 圖表總資訊
const chartInfo = {
    type: 'radar',
    data: radarData,
    options: radarOptions
};

// 建立圖表
const myRadar = new Chart(
    document.getElementById('myRadar'),
    chartInfo
);
