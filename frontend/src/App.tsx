import React, { useState } from "react";
import ReactMarkdown from 'react-markdown';
import FileUpload from "./components/FileUpload";
import KeynessChart from "./components/KeynessChart";
import EnhancedKeynessChart from "./components/EnhancedKeynessChart";
import SemanticClusters from "./components/SemanticClusters";
import InteractiveSemanticClusters from "./components/InteractiveSemanticClusters";
import SentimentDisplay from "./components/SentimentDisplay";
import TextStatistics from "./components/TextStatistics";
import AnalysisSummary from "./components/AnalysisSummary";
import PrivacyNotice from "./components/PrivacyNotice";
import PrivacyPolicy from "./components/PrivacyPolicy";
import { ExportUtils } from "./components/ExportUtils";
import { uploadFile, getResults, downloadResults } from "./services/api";
import { AnalysisResult } from "./types";

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'enhanced' | 'basic'>('enhanced');
  const [privacyAccepted, setPrivacyAccepted] = useState(false);
  const [showPrivacyPolicy, setShowPrivacyPolicy] = useState(false);

  const handleFileUpload = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);
    setUploadProgress(0);

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Upload file
      const uploadResponse = await uploadFile(file);

      if (uploadResponse.success && uploadResponse.analysisId) {
        setUploadProgress(95);

        // Get the analysis results
        const analysisResults = await getResults(uploadResponse.analysisId);
        setUploadProgress(100);

        // Wait a moment to show completion
        setTimeout(() => {
          setResults(analysisResults);
          setIsAnalyzing(false);
          setUploadProgress(0);
        }, 500);
      } else {
        throw new Error(uploadResponse.message || "Upload failed");
      }
    } catch (err: any) {
      setError(err.message || "Failed to analyze text. Please try again.");
      console.error(err);
      setIsAnalyzing(false);
      setUploadProgress(0);
    }
  };

  const handleDownload = async () => {
    if (!results) return;

    try {
      const blob = await downloadResults(results.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `analysis-${results.id}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
      setError("Failed to download results.");
    }
  };

  const handleExportAll = async () => {
    try {
      await ExportUtils.exportAllVisualizations();
    } catch (err) {
      console.error("Export failed:", err);
      setError("Failed to export visualizations.");
    }
  };

  const handleVisualizationExport = async (type: 'png' | 'pdf', chartType: string) => {
    try {
      const filename = `${chartType}-${results?.id || 'analysis'}.${type}`;
      if (type === 'png') {
        await ExportUtils.exportToPNG(chartType, filename);
      } else {
        await ExportUtils.exportToPDF(chartType, filename);
      }
    } catch (err) {
      console.error(`${type.toUpperCase()} export failed:`, err);
      setError(`Failed to export ${type.toUpperCase()}.`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {!privacyAccepted && (
        <PrivacyNotice onAccept={() => setPrivacyAccepted(true)} />
      )}

      {showPrivacyPolicy && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-40 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Privacy Policy</h2>
                <button
                  onClick={() => setShowPrivacyPolicy(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              <PrivacyPolicy />
            </div>
          </div>
        </div>
      )}

      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                ReflexAI Text Analysis
              </h1>
              <p className="mt-2 text-gray-600">
                Privacy-focused writing insights for creative writers
              </p>
            </div>
            <button
              onClick={() => setShowPrivacyPolicy(true)}
              className="text-sm text-blue-600 hover:text-blue-800 underline"
            >
              Privacy Policy
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {!results ? (
          <div className="max-w-2xl mx-auto">
            <FileUpload
              onFileSelect={handleFileUpload}
              isUploading={isAnalyzing}
              uploadProgress={uploadProgress}
            />
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
              <div className="flex items-center space-x-4">
                <div className="flex border rounded overflow-hidden">
                  <button
                    onClick={() => setViewMode('enhanced')}
                    className={`px-3 py-1 text-sm ${viewMode === 'enhanced' ? 'bg-blue-500 text-white' : 'bg-white text-gray-700'}`}
                  >
                    Enhanced
                  </button>
                  <button
                    onClick={() => setViewMode('basic')}
                    className={`px-3 py-1 text-sm ${viewMode === 'basic' ? 'bg-blue-500 text-white' : 'bg-white text-gray-700'}`}
                  >
                    Basic
                  </button>
                </div>
                <button
                  onClick={handleExportAll}
                  className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                >
                  Export All
                </button>
                <button
                  onClick={handleDownload}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Download Data
                </button>
                <button
                  onClick={() => setResults(null)}
                  className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
                >
                  New Analysis
                </button>
              </div>
            </div>

            {/* Analysis Summary */}
            <AnalysisSummary results={results} />

            {/* AI Insights Section (if available) */}
            {results.aiInsights && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-3">AI Insights</h3>
                <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                  <ReactMarkdown>
                    {results.aiInsights.ai_insights}
                  </ReactMarkdown>
                </div>
                <p className="text-xs text-gray-500 mt-3">
                  Generated by {results.aiInsights.model}
                </p>
              </div>
            )}

            {/* Keyness Analysis */}
            {results.keyness && (
              <div data-export-id="keyness-chart">
                {viewMode === 'enhanced' ? (
                  <EnhancedKeynessChart 
                    data={results.keyness} 
                    onExport={(type) => handleVisualizationExport(type, 'keyness-chart')}
                  />
                ) : (
                  <KeynessChart data={results.keyness} />
                )}
              </div>
            )}

            {/* Semantic Clusters */}
            {results.semanticClusters && results.semanticClusters.length > 0 && (
              <div data-export-id="semantic-clusters">
                {viewMode === 'enhanced' ? (
                  <InteractiveSemanticClusters 
                    clusters={results.semanticClusters}
                    onExport={(type) => handleVisualizationExport(type, 'semantic-clusters')}
                  />
                ) : (
                  <SemanticClusters clusters={results.semanticClusters} />
                )}
              </div>
            )}

            {/* Sentiment Analysis */}
            {results.sentiment && (
              <div data-export-id="sentiment-analysis">
                <SentimentDisplay sentiment={results.sentiment} />
              </div>
            )}

            {/* Text Statistics */}
            {results.textStatistics && (
              <div data-export-id="text-statistics">
                <TextStatistics 
                  statistics={results.textStatistics}
                  metadata={results.metadata}
                  onExport={(type) => handleVisualizationExport(type, 'text-statistics')}
                />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
