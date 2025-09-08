import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import { KeynessResult } from '../types';

interface EnhancedKeynessChartProps {
  data: KeynessResult;
  onExport?: (type: 'png' | 'pdf') => void;
}

interface KeynessData {
  word: string;
  score: number;
  frequency: number;
  effectSize: number;
  category: 'positive' | 'negative';
}

const EnhancedKeynessChart: React.FC<EnhancedKeynessChartProps> = ({ 
  data, 
  onExport 
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!data.keywords.length || !svgRef.current) return;

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove();

    const margin = { top: 60, right: 150, bottom: 60, left: 120 };
    const width = 800 - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;

    const svg = d3.select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Process data to match the keyness comparison format
    const processedData: KeynessData[] = data.keywords
      .slice(0, 20) // Show top 20 keywords
      .map((keyword) => ({
        word: keyword.word,
        score: keyword.score,
        frequency: keyword.frequency,
        effectSize: keyword.effect_size || keyword.raw_score || keyword.score,
        category: ((keyword.effect_size || keyword.raw_score || keyword.score) > 0 ? 'positive' : 'negative') as 'positive' | 'negative'
      }))
      .sort((a, b) => Math.abs(b.effectSize) - Math.abs(a.effectSize)); // Sort by absolute value but keep sign
    
    // Debug logging
    console.log('Keyness data received:', data.keywords.slice(0, 5));
    console.log('Processed data:', processedData.slice(0, 5));
    console.log('Negative items:', processedData.filter(d => d.category === 'negative'));

    // Scales
    const yScale = d3.scaleBand()
      .domain(processedData.map(d => d.word))
      .range([0, height])
      .padding(0.1);

    const maxAbsValue = d3.max(processedData, d => Math.abs(d.effectSize)) || 1;
    const xScale = d3.scaleLinear()
      .domain([-maxAbsValue * 1.1, maxAbsValue * 1.1])
      .range([0, width]);

    const colorScale = d3.scaleOrdinal()
      .domain(['positive', 'negative'])
      .range(['#2563eb', '#dc2626']); // Blue for positive, red for negative

    // Add title
    svg.append("text")
      .attr("x", (width + margin.left + margin.right) / 2)
      .attr("y", 30)
      .attr("text-anchor", "middle")
      .attr("font-size", "16px")
      .attr("font-weight", "bold")
      .attr("fill", "#333")
      .text("Keyness Comparison: Effect Size");

    // Add center line (zero line)
    g.append("line")
      .attr("x1", xScale(0))
      .attr("x2", xScale(0))
      .attr("y1", 0)
      .attr("y2", height)
      .attr("stroke", "#666")
      .attr("stroke-width", 2);

    // Create bars
    const bars = g.selectAll(".bar")
      .data(processedData)
      .enter()
      .append("g")
      .attr("class", "bar");

    bars.append("rect")
      .attr("y", d => yScale(d.word)!)
      .attr("height", yScale.bandwidth())
      .attr("x", d => d.effectSize >= 0 ? xScale(0) : xScale(d.effectSize))
      .attr("width", d => Math.abs(xScale(d.effectSize) - xScale(0)))
      .attr("fill", d => colorScale(d.category) as string)
      .attr("fill-opacity", 0.8)
      .attr("stroke", d => colorScale(d.category) as string)
      .attr("stroke-width", 1);

    // Add word labels
    g.selectAll(".word-label")
      .data(processedData)
      .enter()
      .append("text")
      .attr("class", "word-label")
      .attr("y", d => yScale(d.word)! + yScale.bandwidth() / 2)
      .attr("x", -10)
      .attr("text-anchor", "end")
      .attr("dominant-baseline", "middle")
      .attr("font-size", "11px")
      .attr("fill", "#333")
      .text(d => d.word);

    // Add effect size labels
    g.selectAll(".effect-label")
      .data(processedData)
      .enter()
      .append("text")
      .attr("class", "effect-label")
      .attr("y", d => yScale(d.word)! + yScale.bandwidth() / 2)
      .attr("x", d => {
        const barEnd = d.effectSize >= 0 ? xScale(d.effectSize) : xScale(d.effectSize);
        return barEnd + (d.effectSize >= 0 ? 5 : -5);
      })
      .attr("text-anchor", d => d.effectSize >= 0 ? "start" : "end")
      .attr("dominant-baseline", "middle")
      .attr("font-size", "10px")
      .attr("fill", "#666")
      .text(d => `${d.effectSize.toFixed(2)} (n=${d.frequency})`);

    // Add x-axis
    const xAxis = d3.axisBottom(xScale)
      .tickSize(-height)
      .tickFormat(d => d3.format(".1f")(d as number));

    g.append("g")
      .attr("class", "x-axis")
      .attr("transform", `translate(0,${height})`)
      .call(xAxis)
      .selectAll(".tick line")
      .attr("stroke", "#e0e0e0")
      .attr("stroke-dasharray", "3,3");

    // Style axis
    g.select(".x-axis .domain")
      .attr("stroke", "#ccc");

    g.selectAll(".x-axis text")
      .attr("fill", "#666")
      .attr("font-size", "11px");

    // Add axis labels
    svg.append("text")
      .attr("x", (width + margin.left + margin.right) / 2)
      .attr("y", height + margin.top + 45)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("fill", "#666")
      .text("Effect Size");

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -(height + margin.top) / 2)
      .attr("y", 15)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("fill", "#666")
      .text("Keywords");

    // Add legend
    const legend = svg.append("g")
      .attr("class", "legend")
      .attr("transform", `translate(${width + margin.left + 20}, ${margin.top + 50})`);

    const legendData = [
      { label: "Positive Effect", color: "#2563eb" },
      { label: "Negative Effect", color: "#dc2626" }
    ];

    const legendItems = legend.selectAll(".legend-item")
      .data(legendData)
      .enter()
      .append("g")
      .attr("class", "legend-item")
      .attr("transform", (d, i) => `translate(0, ${i * 25})`);

    legendItems.append("rect")
      .attr("width", 15)
      .attr("height", 15)
      .attr("fill", d => d.color);

    legendItems.append("text")
      .attr("x", 20)
      .attr("y", 12)
      .attr("font-size", "12px")
      .attr("fill", "#333")
      .text(d => d.label);

    // Add tooltips on hover
    bars.on("mouseover", function(event, d) {
      // Create tooltip
      const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
        .style("position", "absolute")
        .style("background", "rgba(0,0,0,0.8)")
        .style("color", "white")
        .style("padding", "8px")
        .style("border-radius", "4px")
        .style("font-size", "12px")
        .style("pointer-events", "none");

      tooltip.transition()
        .duration(200)
        .style("opacity", 1);

      tooltip.html(`
        <strong>${d.word}</strong><br/>
        Effect Size: ${d.effectSize.toFixed(3)}<br/>
        Frequency: ${d.frequency}<br/>
        Score: ${d.score.toFixed(3)}
      `)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");

      // Highlight bar
      d3.select(this).select("rect")
        .attr("fill-opacity", 1)
        .attr("stroke-width", 2);
    })
    .on("mouseout", function() {
      // Remove tooltip
      d3.selectAll(".tooltip").remove();

      // Reset bar
      d3.select(this).select("rect")
        .attr("fill-opacity", 0.8)
        .attr("stroke-width", 1);
    });

  }, [data]);

  const exportChart = (type: 'png' | 'pdf') => {
    if (onExport) {
      onExport(type);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Keyness Analysis</h3>
        <div className="flex gap-2">
          <button
            onClick={() => exportChart('png')}
            className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
          >
            Export PNG
          </button>
          <button
            onClick={() => exportChart('pdf')}
            className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
          >
            Export PDF
          </button>
        </div>
      </div>

      <svg ref={svgRef} className="w-full h-auto border rounded"></svg>

      <div className="mt-4 text-sm text-gray-600">
        <p><strong>Interpretation:</strong> Positive effects (blue) indicate words more frequent in your text compared to reference corpus. Negative effects (red) indicate words less frequent in your text.</p>
      </div>
    </div>
  );
};

export default EnhancedKeynessChart;