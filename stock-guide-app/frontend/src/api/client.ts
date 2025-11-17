/**
 * API Client
 * Axios 기반 백엔드 통신 + 데모 모드 지원
 */
import axios from 'axios';
import * as mockData from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'demo';
const DEMO_MODE = API_BASE_URL === 'demo';

console.log('🔧 API Mode:', DEMO_MODE ? 'DEMO (No Backend)' : `Backend: ${API_BASE_URL}`);

export const apiClient = axios.create({
  baseURL: DEMO_MODE ? '' : API_BASE_URL,
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
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return mockData.mockAnalysisResult(ticker, question || '분석 요청');
  }

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
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    return mockData.mockDiagnosis(ticker);
  }

  const response = await apiClient.get(`/api/v1/stock/diagnosis/${ticker}`);
  return response.data;
};

/**
 * 실시간 주가
 */
export const getStockPrice = async (ticker: string): Promise<StockPriceData> => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.mockStockPrice(ticker);
  }

  const response = await apiClient.get(`/api/v1/stock/price/${ticker}`);
  return response.data;
};

/**
 * 뉴스 검색
 */
export const searchNews = async (query: string, days: number = 7) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return { articles: [], overall_sentiment: 0 };
  }

  const response = await apiClient.get('/api/v1/stock/news', {
    params: { query, days },
  });
  return response.data;
};

/**
 * 오늘의 키워드
 */
export const getDailyKeyword = async (): Promise<DailyKeyword> => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.mockDailyKeyword;
  }

  const response = await apiClient.get('/api/v1/stock/daily-keyword');
  return response.data;
};

/**
 * 관심 목록 조회
 */
export const getWatchlist = async (): Promise<WatchlistItem[]> => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.mockWatchlist;
  }

  const response = await apiClient.get('/api/v1/watchlist/');
  return response.data;
};

/**
 * 관심 목록 추가
 */
export const addToWatchlist = async (ticker: string, companyName: string, memo?: string) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return {
      message: '데모 모드: 관심 목록 추가 시뮬레이션 (실제로는 저장되지 않습니다)',
      success: true
    };
  }

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
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return { message: '데모 모드: 업데이트 시뮬레이션', success: true };
  }

  const response = await apiClient.patch(`/api/v1/watchlist/${itemId}`, {
    memo,
  });
  return response.data;
};

/**
 * 관심 목록 삭제
 */
export const deleteFromWatchlist = async (itemId: number) => {
  if (DEMO_MODE) {
    await new Promise(resolve => setTimeout(resolve, 500));
    return { message: '데모 모드: 삭제 시뮬레이션', success: true };
  }

  const response = await apiClient.delete(`/api/v1/watchlist/${itemId}`);
  return response.data;
};
