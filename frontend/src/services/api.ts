import axios from 'axios';
import { AnalysisResult, FileUploadResponse } from '../types';

const API_BASE = '/api';

export const uploadFile = async (file: File): Promise<FileUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  
  return response.data;
};

export const analyzeText = async (text: string): Promise<AnalysisResult> => {
  const response = await axios.post(`${API_BASE}/analyze`, { text });
  return response.data;
};

export const getResults = async (analysisId: string): Promise<AnalysisResult> => {
  const response = await axios.get(`${API_BASE}/results/${analysisId}`);
  return response.data;
};

export const downloadResults = async (analysisId: string): Promise<Blob> => {
  const response = await axios.get(`${API_BASE}/download/${analysisId}`, {
    responseType: 'blob'
  });
  return response.data;
};