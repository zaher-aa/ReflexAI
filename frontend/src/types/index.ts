export type AnalysisStatus = "pending" | "processing" | "completed" | "failed";

export interface KeywordItem {
  word: string;
  score: number;
  frequency: number;
  rank: number;
  effect_size?: number;
  raw_score?: number;
  confidence?: number;
}

export interface KeynessResult {
  keywords: KeywordItem[];
  total_keywords: number;
  processing_time_ms?: number;
  reference_corpus?: string;
}

export interface WordCoordinate {
  word: string;
  x: number;
  y: number;
  cluster_id: number;
}

export interface SemanticCluster {
  id: number;
  label: string;
  words: string[];
  size: number;
  centroid?: Record<string, number>;
  coherence_score?: number;
  word_coordinates?: WordCoordinate[];
}

export interface SemanticClusteringResult {
  clusters: SemanticCluster[];
  total_clusters: number;
  processing_time_ms?: number;
  algorithm?: string;
  similarity_threshold?: number;
}

export interface SentimentResult {
  overall: number;
  positive: number;
  negative: number;
  neutral: number;
  compound?: number;
  confidence?: number;
  sentence_sentiments?: Array<Record<string, number>>;
}

export interface TextStatistics {
  character_count: number;
  word_count: number;
  sentence_count: number;
  paragraph_count: number;
  avg_sentence_length: number;
  avg_word_length: number;
  unique_words: number;
  vocabulary_richness: number;
  readability_score?: number;
}

export interface ProcessingMetadata {
  start_time: string;
  end_time: string;
  processing_time_seconds: number;
  file_size_bytes?: number;
  model_versions?: Record<string, string>;
  parameters?: Record<string, any>;
}

export interface AnalysisResult {
  id: string;
  timestamp: string;
  status: AnalysisStatus;
  keyness?: KeynessResult;
  semanticClusters?: SemanticCluster[]; // For backward compatibility
  semanticClustering?: SemanticClusteringResult;
  sentiment?: SentimentResult;
  textStatistics?: TextStatistics;
  aiInsights?: {
    ai_insights: string;
    model: string;
  };
  metadata?: ProcessingMetadata;
  error_message?: string;
}

export interface FileUploadResponse {
  success: boolean;
  message: string;
  analysisId?: string;
  progress?: number;
}