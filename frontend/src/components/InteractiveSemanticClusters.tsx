import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import { SemanticCluster } from '../types';

interface InteractiveSemanticClustersProps {
  clusters: SemanticCluster[];
  onExport?: (type: 'png' | 'pdf') => void;
}

interface ClusterNode {
  id: string;
  label: string;
  words: string[];
  x: number;
  y: number;
  radius: number;
  color: string;
}

const InteractiveSemanticClusters: React.FC<InteractiveSemanticClustersProps> = ({ 
  clusters, 
  onExport 
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedCluster, setSelectedCluster] = useState<ClusterNode | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; content: string } | null>(null);

  useEffect(() => {
    if (!clusters.length || !svgRef.current) return;

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove();

    // Get container dimensions
    const container = svgRef.current.parentElement;
    const containerWidth = container?.clientWidth || 800;
    
    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const width = Math.max(400, Math.min(containerWidth - 40, 900)) - margin.left - margin.right;
    const height = Math.max(300, width * 0.75) - margin.top - margin.bottom;

    const svg = d3.select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Color scale
    const colorScale = d3.scaleOrdinal()
      .domain(clusters.map(c => c.id.toString()))
      .range(d3.schemeCategory10);

    // Create cluster nodes with better positioning logic
    const nodes: ClusterNode[] = clusters.map((cluster, index) => {
      const maxRadius = Math.min(width, height) * 0.25; // Reduced from 0.3
      const clusterRadius = Math.max(15, Math.min(35, cluster.size * 1.5)); // Smaller clusters
      
      let x, y;
      
      if (clusters.length <= 2) {
        // For 1-2 clusters, place horizontally
        x = (width / (clusters.length + 1)) * (index + 1);
        y = height / 2;
      } else if (clusters.length <= 4) {
        // For 3-4 clusters, use a grid layout
        const cols = Math.ceil(Math.sqrt(clusters.length));
        const rows = Math.ceil(clusters.length / cols);
        const col = index % cols;
        const row = Math.floor(index / cols);
        x = (width / (cols + 1)) * (col + 1);
        y = (height / (rows + 1)) * (row + 1);
      } else {
        // For more clusters, use circular layout with better spacing
        const angle = (index / clusters.length) * 2 * Math.PI;
        const centerX = width / 2;
        const centerY = height / 2;
        x = centerX + maxRadius * Math.cos(angle);
        y = centerY + maxRadius * Math.sin(angle);
      }
      
      return {
        id: cluster.id.toString(),
        label: cluster.label,
        words: cluster.words,
        x,
        y,
        radius: clusterRadius,
        color: colorScale(cluster.id.toString()) as string
      };
    });

    // Create force simulation with adjusted forces
    const simulation = d3.forceSimulation(nodes as any)
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("charge", d3.forceManyBody().strength(-200)) // Reduced repulsion
      .force("collision", d3.forceCollide().radius(d => (d as ClusterNode).radius + 15)) // More padding
      .force("bounds", () => {
        // Keep nodes within bounds
        nodes.forEach(node => {
          const n = node as any;
          n.x = Math.max(n.radius + 10, Math.min(width - n.radius - 10, n.x));
          n.y = Math.max(n.radius + 10, Math.min(height - n.radius - 10, n.y));
        });
      })
      .stop();

    // Run simulation with more iterations for better layout
    for (let i = 0; i < 150; ++i) simulation.tick();

    // Draw connections between related clusters
    const links = g.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(nodes.slice(0, -1).map((d, i) => ({ 
        source: d, 
        target: nodes[i + 1] || nodes[0] 
      })))
      .enter()
      .append("line")
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y)
      .attr("stroke", "#e0e0e0")
      .attr("stroke-width", 1)
      .attr("stroke-dasharray", "3,3");

    // Create cluster circles
    const clusterCircles = g.append("g")
      .attr("class", "clusters")
      .selectAll("circle")
      .data(nodes)
      .enter()
      .append("circle")
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("r", d => d.radius)
      .attr("fill", d => d.color)
      .attr("fill-opacity", 0.7)
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .style("cursor", "pointer");

    // Add cluster labels
    const clusterLabels = g.append("g")
      .attr("class", "cluster-labels")
      .selectAll("text")
      .data(nodes)
      .enter()
      .append("text")
      .attr("x", d => d.x)
      .attr("y", d => d.y)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .attr("fill", "#333")
      .attr("font-size", "12px")
      .attr("font-weight", "bold")
      .text(d => `Cluster ${d.id}`)
      .style("pointer-events", "none");

    // Add word clouds around clusters with better positioning
    nodes.forEach(node => {
      const wordGroup = g.append("g")
        .attr("class", `words-${node.id}`)
        .style("opacity", 0);

      const displayWords = node.words.slice(0, 6); // Fewer words to prevent crowding
      displayWords.forEach((word, i) => {
        const wordAngle = (i / displayWords.length) * 2 * Math.PI;
        const wordRadius = node.radius + 30; // More spacing from cluster
        const wordX = node.x + wordRadius * Math.cos(wordAngle);
        const wordY = node.y + wordRadius * Math.sin(wordAngle);

        // Ensure words stay within bounds
        const clampedX = Math.max(20, Math.min(width - 20, wordX));
        const clampedY = Math.max(20, Math.min(height - 20, wordY));

        wordGroup.append("text")
          .attr("x", clampedX)
          .attr("y", clampedY)
          .attr("text-anchor", "middle")
          .attr("dominant-baseline", "middle")
          .attr("fill", node.color)
          .attr("font-size", "9px") // Slightly smaller font
          .attr("font-weight", "500")
          .text(word.length > 8 ? word.substring(0, 8) + '...' : word); // Truncate long words
      });
    });

    // Add interactions
    clusterCircles
      .on("mouseover", function(event, d) {
        // Highlight cluster
        d3.select(this)
          .attr("fill-opacity", 0.9)
          .attr("stroke-width", 3);

        // Show word cloud
        g.select(`.words-${d.id}`)
          .transition()
          .duration(200)
          .style("opacity", 1);

        // Show tooltip
        const tooltipContent = `${d.label}\n${d.words.length} words`;
        setTooltip({
          x: event.pageX + 10,
          y: event.pageY - 10,
          content: tooltipContent
        });
      })
      .on("mouseout", function(event, d) {
        // Reset cluster
        d3.select(this)
          .attr("fill-opacity", 0.7)
          .attr("stroke-width", 2);

        // Hide word cloud
        g.select(`.words-${d.id}`)
          .transition()
          .duration(200)
          .style("opacity", 0);

        setTooltip(null);
      })
      .on("click", function(event, d) {
        setSelectedCluster(d);
      });

    // Add title
    svg.append("text")
      .attr("x", (width + margin.left + margin.right) / 2)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .attr("font-size", "16px")
      .attr("font-weight", "bold")
      .attr("fill", "#333")
      .text("Interactive Semantic Cluster Visualization");

  }, [clusters]);

  const exportVisualization = (type: 'png' | 'pdf') => {
    if (onExport) {
      onExport(type);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Semantic Clusters</h3>
        <div className="flex gap-2">
          <button
            onClick={() => exportVisualization('png')}
            className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
          >
            Export PNG
          </button>
          <button
            onClick={() => exportVisualization('pdf')}
            className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
          >
            Export PDF
          </button>
        </div>
      </div>

      <div className="relative w-full max-w-4xl mx-auto">
        <svg ref={svgRef} className="w-full h-auto border rounded bg-gray-50"></svg>
        
        {tooltip && (
          <div
            className="absolute bg-black text-white p-2 rounded text-sm pointer-events-none z-10"
            style={{ left: tooltip.x, top: tooltip.y }}
          >
            <pre className="whitespace-pre-wrap">{tooltip.content}</pre>
          </div>
        )}
      </div>

      {selectedCluster && (
        <div className="mt-4 p-4 bg-gray-50 rounded">
          <h4 className="font-semibold text-lg mb-2">
            Cluster {selectedCluster.id}: {selectedCluster.label}
          </h4>
          <div className="flex flex-wrap gap-2">
            {selectedCluster.words.map((word, idx) => (
              <span
                key={idx}
                className="px-2 py-1 rounded text-sm"
                style={{ 
                  backgroundColor: selectedCluster.color + '20',
                  color: selectedCluster.color,
                  border: `1px solid ${selectedCluster.color}40`
                }}
              >
                {word}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 text-sm text-gray-600">
        <p>💡 <strong>Tip:</strong> Hover over clusters to see related words, click to select and view details.</p>
      </div>
    </div>
  );
};

export default InteractiveSemanticClusters;