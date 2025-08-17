export interface AnalysisResult {
  id: string;
  timestamp: string;
  keyness: KeynessResult;
  semanticClusters: SemanticCluster[];
  sentiment: SentimentResult;
}

export interface KeynessResult {
  keywords: Array<{
    word: string;
    score: number;
    frequency: number;
  }>;
}

export interface SemanticCluster {
  id: number;
  label: string;
  words: string[];
  size: number;
}

export interface SentimentResult {
  overall: number;
  positive: number;
  negative: number;
  neutral: number;
}

export interface FileUploadResponse {
  success: boolean;
  message: string;
  analysisId?: string;
}