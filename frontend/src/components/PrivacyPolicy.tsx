import React, { useState } from 'react';

interface PrivacyPolicyProps {
  onAccept?: () => void;
  onDecline?: () => void;
  showButtons?: boolean;
}

const PrivacyPolicy: React.FC<PrivacyPolicyProps> = ({ 
  onAccept, 
  onDecline, 
  showButtons = false 
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Privacy & Data Handling</h3>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-blue-500 hover:text-blue-700 text-sm"
        >
          {isExpanded ? 'Collapse' : 'Read Full Policy'}
        </button>
      </div>

      <div className="text-sm text-gray-700 space-y-3">
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <h4 className="font-semibold text-green-800 mb-2">🔒 Privacy-First Design</h4>
          <ul className="space-y-1 text-green-700">
            <li>• Your text files are automatically deleted after analysis</li>
            <li>• No data is permanently stored on our servers</li>
            <li>• Analysis happens locally - your text never leaves this application</li>
            <li>• Optional AI insights use local Ollama model (not cloud services)</li>
          </ul>
        </div>

        {isExpanded && (
          <div className="space-y-4 mt-4">
            <div>
              <h4 className="font-semibold mb-2">Data Processing</h4>
              <p>
                ReflexAI processes your uploaded text files to provide writing analytics including:
                keyness analysis, semantic clustering, and sentiment analysis. All processing occurs 
                on the server where this application is hosted.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">File Storage & Deletion</h4>
              <p>
                Uploaded files are temporarily stored in a secure directory during processing. 
                Files are automatically deleted immediately after analysis completion or after 
                1 hour maximum, whichever comes first. This ensures your creative work remains private.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">AI Processing (Optional)</h4>
              <p>
                If enabled, AI insights are generated using a local Ollama language model running 
                on the same server. Your text is not sent to any external AI services or cloud providers. 
                The AI model processes only a brief excerpt of your text for thematic analysis.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Data Not Collected</h4>
              <ul className="list-disc list-inside space-y-1">
                <li>Personal identification information</li>
                <li>User accounts or login data</li>
                <li>IP addresses or tracking data</li>
                <li>Permanent copies of your text</li>
                <li>Usage analytics beyond basic error logging</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Your Rights</h4>
              <p>
                Since no personal data is permanently stored, there are no user accounts 
                or persistent data to manage. Each analysis session is independent and 
                temporary.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">File Size & Security</h4>
              <p>
                Files are limited to 50MB maximum. Only UTF-8 encoded text files (.txt) 
                are accepted. Files are processed in isolated temporary directories with 
                automatic cleanup.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Open Source</h4>
              <p>
                ReflexAI is open source software. You can review the code, run it locally, 
                or deploy your own instance for complete control over your data processing.
              </p>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <h4 className="font-semibold text-blue-800 mb-2">Technical Implementation</h4>
              <div className="text-blue-700 text-xs space-y-1">
                <p><strong>Automatic Deletion:</strong> DELETE_AFTER_ANALYSIS=true (configurable)</p>
                <p><strong>Max File Age:</strong> 3600 seconds (1 hour)</p>
                <p><strong>Cleanup Interval:</strong> 1800 seconds (30 minutes)</p>
                <p><strong>Processing Location:</strong> Local server, no cloud services</p>
              </div>
            </div>
          </div>
        )}

        {showButtons && (
          <div className="flex space-x-4 pt-4 border-t">
            <button
              onClick={onAccept}
              className="flex-1 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
            >
              Accept & Continue
            </button>
            <button
              onClick={onDecline}
              className="flex-1 border border-gray-300 py-2 px-4 rounded hover:bg-gray-50"
            >
              Decline
            </button>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t text-xs text-gray-500">
        <p>
          Last updated: {new Date().toLocaleDateString()} | 
          This policy applies to ReflexAI text analysis tool for creative writers.
        </p>
      </div>
    </div>
  );
};

export default PrivacyPolicy;