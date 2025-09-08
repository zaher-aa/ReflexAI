import React from 'react';
import { AnalysisResult } from '../types';

interface AnalysisSummaryProps {
  results: AnalysisResult;
}

const AnalysisSummary: React.FC<AnalysisSummaryProps> = ({ results }) => {
  const formatTime = (seconds: number) => {
    if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
    return `${seconds.toFixed(2)}s`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800 border-green-200';
      case 'processing': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'failed': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Analysis Summary</h3>
        <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(results.status)}`}>
          {results.status.charAt(0).toUpperCase() + results.status.slice(1)}
        </div>
      </div>

      {results.status === 'failed' && results.error_message && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
          <h4 className="text-red-800 font-medium mb-2">Analysis Failed</h4>
          <p className="text-red-700 text-sm">{results.error_message}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Basic Analysis Info */}
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">
            {results.textStatistics?.word_count || 'N/A'}
          </div>
          <div className="text-sm text-gray-600">Words Analyzed</div>
        </div>

        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">
            {results.keyness?.total_keywords || 'N/A'}
          </div>
          <div className="text-sm text-gray-600">Key Terms Found</div>
        </div>

        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">
            {results.semanticClustering?.total_clusters || results.semanticClusters?.length || 'N/A'}
          </div>
          <div className="text-sm text-gray-600">Semantic Clusters</div>
        </div>

        <div className="text-center">
          <div className="text-2xl font-bold text-indigo-600">
            {results.metadata ? formatTime(results.metadata.processing_time_seconds) : 'N/A'}
          </div>
          <div className="text-sm text-gray-600">Processing Time</div>
        </div>
      </div>

      {/* Feature Status */}
      <div className="mt-6 pt-4 border-t border-blue-200">
        <h4 className="font-medium text-gray-700 mb-3">Analysis Components</h4>
        <div className="flex flex-wrap gap-2">
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            results.keyness ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            ✓ Keyness Analysis
          </span>
          
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            results.semanticClusters?.length ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            ✓ Semantic Clustering
          </span>
          
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            results.sentiment ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            ✓ Sentiment Analysis
          </span>
          
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            results.textStatistics ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            ✓ Text Statistics
          </span>
          
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            results.aiInsights ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'
          }`}>
            {results.aiInsights ? '✓ AI Insights' : '○ AI Insights (N/A)'}
          </span>
        </div>
      </div>

      {/* Quick Insights */}
      {results.status === 'completed' && (
        <div className="mt-4 pt-4 border-t border-blue-200">
          <h4 className="font-medium text-gray-700 mb-2">Quick Insights</h4>
          <div className="text-sm text-gray-600 space-y-1">
            {results.textStatistics && (
              <p>
                • <strong>Vocabulary Richness:</strong> {(results.textStatistics.vocabulary_richness * 100).toFixed(1)}% 
                ({results.textStatistics.unique_words} unique words)
              </p>
            )}
            
            {results.sentiment && (
              <p>
                • <strong>Overall Sentiment:</strong> {
                  results.sentiment.overall > 0.1 ? 'Positive' :
                  results.sentiment.overall < -0.1 ? 'Negative' : 'Neutral'
                } ({(results.sentiment.overall * 100).toFixed(1)}%)
              </p>
            )}
            
            {results.textStatistics?.readability_score && (
              <p>
                • <strong>Readability:</strong> {results.textStatistics.readability_score.toFixed(1)} 
                (Flesch Reading Ease)
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisSummary;