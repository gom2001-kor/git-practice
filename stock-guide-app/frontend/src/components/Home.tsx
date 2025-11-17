/**
 * 홈 화면 - 오늘의 키워드 + 빠른 검색
 */
import React, { useEffect, useState } from 'react';
import { TrendingUp, Search } from 'lucide-react';
import { getDailyKeyword, DailyKeyword } from '../api/client';
import { useNavigate } from 'react-router-dom';

export const Home: React.FC = () => {
  const [keyword, setKeyword] = useState<DailyKeyword | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadDailyKeyword();
  }, []);

  const loadDailyKeyword = async () => {
    try {
      const data = await getDailyKeyword();
      setKeyword(data);
    } catch (error) {
      console.error('Failed to load daily keyword:', error);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 p-6">
      {/* 헤더 */}
      <header className="max-w-4xl mx-auto mb-8">
        <h1 className="text-3xl font-bold text-primary-700">주식투자 가이드</h1>
        <p className="text-gray-600 mt-2">주린이를 위한 AI 기반 투자 가이드</p>
      </header>

      {/* 오늘의 키워드 */}
      <div className="max-w-4xl mx-auto mb-8">
        <div className="card bg-gradient-to-r from-primary-600 to-blue-600 text-white">
          <div className="flex items-center gap-3 mb-4">
            <TrendingUp size={28} />
            <h2 className="text-xl font-bold">오늘의 산업 키워드</h2>
          </div>

          {keyword ? (
            <>
              <h3 className="text-2xl font-bold mb-3">{keyword.keyword}</h3>
              <p className="text-white/90 leading-relaxed">{keyword.description}</p>
              <div className="mt-4 pt-4 border-t border-white/20">
                <span className="text-sm text-white/80">
                  감성: {keyword.sentiment === '긍정' ? '✅' : '⚠️'} {keyword.sentiment}
                </span>
              </div>
            </>
          ) : (
            <div className="animate-pulse">
              <div className="h-8 bg-white/20 rounded w-1/3 mb-3"></div>
              <div className="h-4 bg-white/20 rounded w-full mb-2"></div>
              <div className="h-4 bg-white/20 rounded w-2/3"></div>
            </div>
          )}
        </div>
      </div>

      {/* 빠른 검색 */}
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <form onSubmit={handleSearch} className="flex gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="기업명 또는 종목 코드 입력 (예: Apple, AAPL)"
                className="input-field pl-10"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <button type="submit" className="btn-primary">
              검색
            </button>
          </form>

          <div className="mt-6">
            <h3 className="text-sm font-semibold text-gray-600 mb-3">인기 종목</h3>
            <div className="flex flex-wrap gap-2">
              {['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', '005930.KS'].map((ticker) => (
                <button
                  key={ticker}
                  onClick={() => navigate(`/diagnosis/${ticker}`)}
                  className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm font-medium transition-colors"
                >
                  {ticker}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 하단 네비게이션 */}
      <nav className="max-w-4xl mx-auto mt-8 flex justify-center gap-4">
        <button
          onClick={() => navigate('/watchlist')}
          className="btn-secondary"
        >
          내 관심 목록 보기
        </button>
      </nav>
    </div>
  );
};
