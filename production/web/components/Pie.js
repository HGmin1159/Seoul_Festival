import React, {useEffect} from 'react';
import Chart from 'chart.js';

let pieChart;

const Pie = ({man}) => {
    useEffect(()=>{
        if (pieChart) {
            pieChart.destroy();
        }
        const ctx = 'pie-chart';
        pieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: [man, 1-man],
                    backgroundColor: ['lightblue', 'pink']
                }],
                labels: [
                    '남',
                    '여'
                ]
            },
            options: {
                legend: {
                    reverse: true
                },
                maintainAspectRatio: false
            }
        })
    }, [man])
    
    return (
        <canvas id='pie-chart'></canvas>
    )
}


export default Pie;