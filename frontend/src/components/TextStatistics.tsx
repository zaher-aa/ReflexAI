import React from 'react';
import { TextStatistics as TextStatsType, ProcessingMetadata } from '../types';

interface TextStatisticsProps {
  statistics?: TextStatsType;
  metadata?: ProcessingMetadata;
  onExport?: (type: 'png' | 'pdf') => void;
}

const TextStatistics: React.FC<TextStatisticsProps> = ({ 
  statistics, 
  metadata,
  onExport 
}) => {
  if (!statistics) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Text Statistics</h3>
        <p className="text-gray-500">Statistics not available</p>
      </div>
    );
  }

  const formatNumber = (num: number) => num.toLocaleString();
  const formatFloat = (num: number) => num.toFixed(2);
  const formatPercent = (num: number) => `${(num * 100).toFixed(1)}%`;

  const getReadabilityLevel = (score: number) => {
    if (score >= 90) return { label: "Very Easy", color: "text-green-600" };
    if (score >= 80) return { label: "Easy", color: "text-green-500" };
    if (score >= 70) return { label: "Fairly Easy", color: "text-yellow-500" };
    if (score >= 60) return { label: "Standard", color: "text-orange-500" };
    if (score >= 50) return { label: "Fairly Difficult", color: "text-orange-600" };
    if (score >= 30) return { label: "Difficult", color: "text-red-500" };
    return { label: "Very Difficult", color: "text-red-600" };
  };

  const readability = statistics.readability_score ? getReadabilityLevel(statistics.readability_score) : null;

  return (
    <div className="bg-white p-6 rounded-lg shadow" data-export-id="text-statistics">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold">Text Statistics</h3>
        {onExport && (
          <div className="flex gap-2">
            <button
              onClick={() => onExport('png')}
              className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
            >
              Export PNG
            </button>
            <button
              onClick={() => onExport('pdf')}
              className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
            >
              Export PDF
            </button>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Basic Counts */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-700 border-b pb-2">Content Overview</h4>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Characters:</span>
              <span className="font-medium">{formatNumber(statistics.character_count)}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Words:</span>
              <span className="font-medium">{formatNumber(statistics.word_count)}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Sentences:</span>
              <span className="font-medium">{formatNumber(statistics.sentence_count)}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Paragraphs:</span>
              <span className="font-medium">{formatNumber(statistics.paragraph_count)}</span>
            </div>
          </div>
        </div>

        {/* Averages & Complexity */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-700 border-b pb-2">Writing Complexity</h4>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Avg. Sentence Length:</span>
              <span className="font-medium">{formatFloat(statistics.avg_sentence_length)} words</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Avg. Word Length:</span>
              <span className="font-medium">{formatFloat(statistics.avg_word_length)} chars</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Unique Words:</span>
              <span className="font-medium">{formatNumber(statistics.unique_words)}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Vocabulary Richness:</span>
              <span className="font-medium">{formatPercent(statistics.vocabulary_richness)}</span>
            </div>
          </div>
        </div>

        {/* Readability */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-700 border-b pb-2">Readability</h4>
          
          {statistics.readability_score !== undefined && readability ? (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Flesch Score:</span>
                <span className="font-medium">{formatFloat(statistics.readability_score)}</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-600">Reading Level:</span>
                <span className={`font-medium ${readability.color}`}>
                  {readability.label}
                </span>
              </div>
              
              <div className="mt-4">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-2 rounded-full"
                    style={{ 
                      width: `${Math.max(0, Math.min(100, statistics.readability_score))}%` 
                    }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Difficult</span>
                  <span>Easy</span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">Readability score not available</p>
          )}
        </div>
      </div>

      {/* Processing Information */}
      {metadata && (
        <div className="mt-6 pt-6 border-t">
          <h4 className="font-semibold text-gray-700 mb-3">Processing Details</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Processing Time:</span>
              <span className="font-medium">{formatFloat(metadata.processing_time_seconds)}s</span>
            </div>
            
            {metadata.file_size_bytes && (
              <div className="flex justify-between">
                <span className="text-gray-600">File Size:</span>
                <span className="font-medium">
                  {metadata.file_size_bytes < 1024 ? 
                    `${metadata.file_size_bytes} bytes` :
                    metadata.file_size_bytes < 1024 * 1024 ?
                      `${(metadata.file_size_bytes / 1024).toFixed(1)} KB` :
                      `${(metadata.file_size_bytes / (1024 * 1024)).toFixed(1)} MB`
                  }
                </span>
              </div>
            )}
            
            {metadata.model_versions && Object.keys(metadata.model_versions).length > 0 && (
              <div className="col-span-full">
                <span className="text-gray-600">Models Used:</span>
                <div className="mt-1 space-y-1">
                  {Object.entries(metadata.model_versions).map(([model, version]) => (
                    <div key={model} className="text-xs text-gray-500">
                      {model}: {version || 'unknown'}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="mt-4 text-sm text-gray-600">
        <p><strong>Vocabulary Richness:</strong> Ratio of unique words to total words. Higher values indicate more diverse vocabulary.</p>
        <p><strong>Flesch Reading Ease:</strong> Higher scores (90-100) indicate easier reading, lower scores (0-30) indicate more difficult text.</p>
      </div>
    </div>
  );
};

export default TextStatistics;