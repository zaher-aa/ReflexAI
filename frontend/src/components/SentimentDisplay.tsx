import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { SentimentResult } from '../types';

ChartJS.register(ArcElement, Tooltip, Legend);

interface SentimentDisplayProps {
  sentiment: SentimentResult;
}

const SentimentDisplay: React.FC<SentimentDisplayProps> = ({ sentiment }) => {
  const data = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [{
      data: [sentiment.positive, sentiment.negative, sentiment.neutral],
      backgroundColor: ['#10B981', '#EF4444', '#6B7280'],
      borderWidth: 0
    }]
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Sentiment Analysis</h3>
      <div className="max-w-xs mx-auto">
        <Doughnut data={data} />
      </div>
      <div className="mt-4 text-center">
        <p className="text-2xl font-bold">
          Overall Score: {sentiment.overall.toFixed(2)}
        </p>
      </div>
    </div>
  );
};

export default SentimentDisplay;