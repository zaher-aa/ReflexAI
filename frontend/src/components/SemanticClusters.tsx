import React from 'react';
import { SemanticCluster } from '../types';

interface SemanticClustersProps {
  clusters: SemanticCluster[];
}

const SemanticClusters: React.FC<SemanticClustersProps> = ({ clusters }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Semantic Clusters</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {clusters.map((cluster) => (
          <div key={cluster.id} className="border rounded-lg p-4">
            <h4 className="font-medium text-primary mb-2">
              Cluster {cluster.id}: {cluster.label}
            </h4>
            <div className="flex flex-wrap gap-2">
              {cluster.words.map((word, idx) => (
                <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                  {word}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SemanticClusters;