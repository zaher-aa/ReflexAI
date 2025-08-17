import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import KeynessChart from './components/KeynessChart';
import SemanticClusters from './components/SemanticClusters';
import SentimentDisplay from './components/SentimentDisplay';
import { uploadFile, getResults, downloadResults } from './services/api';
import { AnalysisResult } from './types';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);
    
    try {
      // Use the upload API endpoint
      const uploadResponse = await uploadFile(file);
      
      if (uploadResponse.success && uploadResponse.analysisId) {
        // Get the analysis results
        const analysisResults = await getResults(uploadResponse.analysisId);
        setResults(analysisResults);
      } else {
        throw new Error(uploadResponse.message || 'Upload failed');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to analyze text. Please try again.');
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDownload = async () => {
    if (!results) return;
    
    try {
      const blob = await downloadResults(results.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analysis-${results.id}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      setError('Failed to download results.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Text Analysis Tool
          </h1>
          <p className="mt-2 text-gray-600">
            Discover insights in your creative writing
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {!results ? (
          <div className="max-w-2xl mx-auto">
            <FileUpload onFileSelect={handleFileUpload} isUploading={isAnalyzing} />
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded text-red-600">
                {error}
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold">Analysis Results</h2>
              <div className="space-x-4">
                <button
                  onClick={handleDownload}
                  className="px-4 py-2 bg-primary text-white rounded hover:bg-indigo-600"
                >
                  Download Results
                </button>
                <button
                  onClick={() => setResults(null)}
                  className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                >
                  New Analysis
                </button>
              </div>
            </div>
            
            <KeynessChart data={results.keyness} />
            <SemanticClusters clusters={results.semanticClusters} />
            <SentimentDisplay sentiment={results.sentiment} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
