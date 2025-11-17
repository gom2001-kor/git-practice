/**
 * 관심 목록 화면
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Trash2, Edit2 } from 'lucide-react';
import { getWatchlist, deleteFromWatchlist, WatchlistItem } from '../api/client';

export const Watchlist: React.FC = () => {
  const navigate = useNavigate();
  const [items, setItems] = useState<WatchlistItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadWatchlist();
  }, []);

  const loadWatchlist = async () => {
    setIsLoading(true);
    try {
      const data = await getWatchlist();
      setItems(data);
    } catch (error) {
      console.error('Failed to load watchlist:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (itemId: number) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;

    try {
      await deleteFromWatchlist(itemId);
      setItems(items.filter((item) => item.id !== itemId));
    } catch (error) {
      alert('삭제에 실패했습니다.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* 헤더 */}
      <div className="max-w-4xl mx-auto mb-6">
        <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4">
          <ArrowLeft size={20} />
          <span>뒤로</span>
        </button>

        <h1 className="text-2xl font-bold text-gray-900">내 관심 목록</h1>
        <p className="text-gray-600 mt-1">찜한 종목들을 한눈에 확인하세요</p>
      </div>

      {/* 관심 목록 */}
      <div className="max-w-4xl mx-auto space-y-4">
        {isLoading ? (
          <div className="card">
            <p>로딩 중...</p>
          </div>
        ) : items.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-500 mb-4">아직 관심 목록이 비어있습니다.</p>
            <button onClick={() => navigate('/')} className="btn-primary">
              종목 검색하기
            </button>
          </div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-bold text-gray-900">{item.ticker}</h3>
                    <span className="text-sm text-gray-600">{item.company_name}</span>
                  </div>

                  {item.current_price && (
                    <div className="flex items-center gap-4 mb-2">
                      <span className="text-xl font-semibold">
                        ${item.current_price.toFixed(2)}
                      </span>
                      <span
                        className={`text-sm font-medium ${
                          (item.change_percent || 0) >= 0 ? 'text-success' : 'text-danger'
                        }`}
                      >
                        {(item.change_percent || 0) >= 0 ? '▲' : '▼'}{' '}
                        {Math.abs(item.change_percent || 0).toFixed(2)}%
                      </span>
                    </div>
                  )}

                  {item.memo && (
                    <p className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                      📝 {item.memo}
                    </p>
                  )}

                  <p className="text-xs text-gray-500 mt-2">
                    추가일: {new Date(item.added_at).toLocaleDateString('ko-KR')}
                  </p>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => navigate(`/diagnosis/${item.ticker}`)}
                    className="btn-secondary text-sm"
                  >
                    진단서 보기
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <Trash2 size={20} />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
