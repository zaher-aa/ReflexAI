import React, { useState, useEffect } from 'react';

interface PrivacyNoticeProps {
  onAccept: () => void;
}

const PrivacyNotice: React.FC<PrivacyNoticeProps> = ({ onAccept }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check if user has already accepted privacy policy
    const hasAccepted = localStorage.getItem('reflexai-privacy-accepted');
    if (!hasAccepted) {
      setIsVisible(true);
    } else {
      onAccept(); // Auto-accept if previously accepted
    }
  }, [onAccept]);

  const handleAccept = () => {
    localStorage.setItem('reflexai-privacy-accepted', 'true');
    localStorage.setItem('reflexai-privacy-accepted-date', new Date().toISOString());
    setIsVisible(false);
    onAccept();
  };

  const handleViewDetails = () => {
    // Could open a modal or navigate to privacy policy page
    window.open('#privacy-policy', '_blank');
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Privacy-First Text Analysis</h2>
              <p className="text-gray-600">Your creative work stays private</p>
            </div>
          </div>

          <div className="space-y-4 mb-6">
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <h3 className="font-semibold text-green-800 mb-2">🔒 What We Do</h3>
              <ul className="text-green-700 space-y-1">
                <li>✓ Analyze your text locally on this server</li>
                <li>✓ Automatically delete files after processing</li>
                <li>✓ Use local AI models (no cloud services)</li>
                <li>✓ Provide detailed writing insights</li>
              </ul>
            </div>

            <div className="bg-red-50 p-4 rounded-lg border border-red-200">
              <h3 className="font-semibold text-red-800 mb-2">🚫 What We Don't Do</h3>
              <ul className="text-red-700 space-y-1">
                <li>✗ Store your text permanently</li>
                <li>✗ Send data to external services</li>
                <li>✗ Create user accounts or track users</li>
                <li>✗ Share your work with anyone</li>
              </ul>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <h3 className="font-semibold text-blue-800 mb-2">⚡ How It Works</h3>
              <ol className="text-blue-700 space-y-1">
                <li>1. Upload your text file (max 50MB)</li>
                <li>2. Analysis processes on local server</li>
                <li>3. View your results and export them</li>
                <li>4. Files automatically deleted within 1 hour</li>
              </ol>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg mb-6">
            <p className="text-sm text-gray-700">
              <strong>Technical Details:</strong> This application runs locally and does not require 
              internet connectivity for analysis. Optional AI insights use Ollama (local model) 
              rather than cloud-based AI services. All processing happens on this server.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleAccept}
              className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 font-medium"
            >
              Accept & Start Analyzing
            </button>
            <button
              onClick={handleViewDetails}
              className="flex-1 border border-gray-300 py-3 px-6 rounded-lg hover:bg-gray-50 font-medium"
            >
              View Full Privacy Policy
            </button>
          </div>

          <p className="text-xs text-gray-500 text-center mt-4">
            By continuing, you acknowledge this privacy-focused approach to text analysis.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PrivacyNotice;