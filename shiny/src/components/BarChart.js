import React, {useEffect} from 'react';
import Chart from 'chart.js';

let barChart;

const BarChart = ({data}) => {
    useEffect(()=>{
        if (barChart) {
            barChart.destroy();
        }
        const ctx = "bar-chart";
        barChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['10대', '20대', '30대', '40대', '50대', '60대'],
                datasets: [{
                    // label: '나이별예상분포',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                title: {
                    display: true,
                    text: '나이별예상분포'
                },
                legend: {
                    display: false
                },
                maintainAspectRatio: false
            }
        })
    }, [data]);
    
    return (
        <canvas id="bar-chart"></canvas>
    )
}


export default BarChart;
