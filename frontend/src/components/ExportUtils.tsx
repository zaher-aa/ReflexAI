import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

export class ExportUtils {
  static async exportToPNG(elementId: string, filename: string = 'visualization.png'): Promise<void> {
    try {
      const element = document.getElementById(elementId) || document.querySelector(`[data-export-id="${elementId}"]`);
      if (!element) {
        throw new Error('Element not found for export');
      }

      const canvas = await html2canvas(element as HTMLElement, {
        backgroundColor: '#ffffff',
        scale: 2, // High resolution
        logging: false,
        useCORS: true
      });

      // Create download link
      const link = document.createElement('a');
      link.download = filename;
      link.href = canvas.toDataURL('image/png');
      link.click();
    } catch (error) {
      console.error('PNG export failed:', error);
      throw error;
    }
  }

  static async exportToPDF(elementId: string, filename: string = 'visualization.pdf'): Promise<void> {
    try {
      const element = document.getElementById(elementId) || document.querySelector(`[data-export-id="${elementId}"]`);
      if (!element) {
        throw new Error('Element not found for export');
      }

      const canvas = await html2canvas(element as HTMLElement, {
        backgroundColor: '#ffffff',
        scale: 2,
        logging: false,
        useCORS: true
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
        unit: 'px',
        format: [canvas.width, canvas.height]
      });

      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
      pdf.save(filename);
    } catch (error) {
      console.error('PDF export failed:', error);
      throw error;
    }
  }

  static async exportAllVisualizations(): Promise<void> {
    try {
      // Export keyness chart
      const keynessElement = document.querySelector('[data-export-id="keyness-chart"]');
      if (keynessElement) {
        await this.exportToPNG('keyness-chart', 'keyness-analysis.png');
        await this.exportToPDF('keyness-chart', 'keyness-analysis.pdf');
      }

      // Export semantic clusters
      const clustersElement = document.querySelector('[data-export-id="semantic-clusters"]');
      if (clustersElement) {
        await this.exportToPNG('semantic-clusters', 'semantic-clusters.png');
        await this.exportToPDF('semantic-clusters', 'semantic-clusters.pdf');
      }

      // Export sentiment analysis
      const sentimentElement = document.querySelector('[data-export-id="sentiment-analysis"]');
      if (sentimentElement) {
        await this.exportToPNG('sentiment-analysis', 'sentiment-analysis.png');
        await this.exportToPDF('sentiment-analysis', 'sentiment-analysis.pdf');
      }

      console.log('All visualizations exported successfully');
    } catch (error) {
      console.error('Batch export failed:', error);
      throw error;
    }
  }
}