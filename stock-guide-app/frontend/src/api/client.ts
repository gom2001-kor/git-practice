/**
 * API Client
 * Axios 기반 백엔드 통신
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 (로딩 상태 등)
apiClient.interceptors.request.use(
  (config) => {
    // TODO: JWT 토큰 추가
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 인터셉터 (에러 핸들링)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ===== API Functions =====

export interface StockPriceData {
  ticker: string;
  current_price: number;
  change_percent: number;
  volume: number;
  timestamp: string;
}

export interface DiagnosisData {
  ticker: string;
  diagnosis: string;
  tools_used: string[];
  generated_at: string;
}

export interface WatchlistItem {
  id: number;
  ticker: string;
  company_name: string;
  memo?: string;
  current_price?: number;
  change_percent?: number;
  added_at: string;
}

export interface DailyKeyword {
  keyword: string;
  description: string;
  sentiment: string;
  generated_at: string;
}

/**
 * 주식 분석 (ReAct 에이전트)
 */
export const analyzeStock = async (ticker: string, question?: string) => {
  const response = await apiClient.post('/api/v1/stock/analyze', {
    ticker,
    question,
  });
  return response.data;
};

/**
 * 기업 건강진단서
 */
export const getCompanyDiagnosis = async (ticker: string): Promise<DiagnosisData> => {
  const response = await apiClient.get(`/api/v1/stock/diagnosis/${ticker}`);
  return response.data;
};

/**
 * 실시간 주가
 */
export const getStockPrice = async (ticker: string): Promise<StockPriceData> => {
  const response = await apiClient.get(`/api/v1/stock/price/${ticker}`);
  return response.data;
};

/**
 * 뉴스 검색
 */
export const searchNews = async (query: string, days: number = 7) => {
  const response = await apiClient.get('/api/v1/stock/news', {
    params: { query, days },
  });
  return response.data;
};

/**
 * 오늘의 키워드
 */
export const getDailyKeyword = async (): Promise<DailyKeyword> => {
  const response = await apiClient.get('/api/v1/stock/daily-keyword');
  return response.data;
};

/**
 * 관심 목록 조회
 */
export const getWatchlist = async (): Promise<WatchlistItem[]> => {
  const response = await apiClient.get('/api/v1/watchlist/');
  return response.data;
};

/**
 * 관심 목록 추가
 */
export const addToWatchlist = async (ticker: string, companyName: string, memo?: string) => {
  const response = await apiClient.post('/api/v1/watchlist/', {
    ticker,
    company_name: companyName,
    memo,
  });
  return response.data;
};

/**
 * 관심 목록 업데이트
 */
export const updateWatchlistItem = async (itemId: number, memo: string) => {
  const response = await apiClient.patch(`/api/v1/watchlist/${itemId}`, {
    memo,
  });
  return response.data;
};

/**
 * 관심 목록 삭제
 */
export const deleteFromWatchlist = async (itemId: number) => {
  const response = await apiClient.delete(`/api/v1/watchlist/${itemId}`);
  return response.data;
};
