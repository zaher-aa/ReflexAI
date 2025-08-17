import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { KeynessResult } from '../types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface KeynessChartProps {
  data: KeynessResult;
}

const KeynessChart: React.FC<KeynessChartProps> = ({ data }) => {
  const chartData = {
    labels: data.keywords.slice(0, 20).map(k => k.word),
    datasets: [{
      label: 'Keyness Score',
      data: data.keywords.slice(0, 20).map(k => k.score),
      backgroundColor: 'rgba(79, 70, 229, 0.8)',
      borderColor: 'rgba(79, 70, 229, 1)',
      borderWidth: 1
    }]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Top Keywords by Distinctiveness'
      }
    },
    scales: {
      x: { ticks: { autoSkip: false, maxRotation: 45, minRotation: 45 } },
      y: { beginAtZero: true }
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default KeynessChart;