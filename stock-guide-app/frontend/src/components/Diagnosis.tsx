/**
 * 기업 건강진단서 화면
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Heart, Activity } from 'lucide-react';
import { getCompanyDiagnosis, addToWatchlist, DiagnosisData } from '../api/client';

export const Diagnosis: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const navigate = useNavigate();

  const [diagnosis, setDiagnosis] = useState<DiagnosisData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (ticker) {
      loadDiagnosis();
    }
  }, [ticker]);

  const loadDiagnosis = async () => {
    if (!ticker) return;

    setIsLoading(true);
    setError(null);

    try {
      const data = await getCompanyDiagnosis(ticker);
      setDiagnosis(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '건강진단서를 불러오는 데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddToWatchlist = async () => {
    if (!ticker) return;

    try {
      await addToWatchlist(ticker, ticker, '');
      alert('관심 목록에 추가되었습니다!');
    } catch (err: any) {
      alert(err.response?.data?.detail || '추가 실패');
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

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{ticker} 건강진단서</h1>
            <p className="text-gray-600 mt-1">AI가 분석한 종합 건강 상태</p>
          </div>
          <button
            onClick={handleAddToWatchlist}
            className="btn-primary flex items-center gap-2"
          >
            <Heart size={20} />
            찜하기
          </button>
        </div>
      </div>

      {/* 진단서 내용 */}
      <div className="max-w-4xl mx-auto">
        {isLoading ? (
          <div className="card">
            <div className="flex items-center gap-3 mb-4">
              <Activity className="animate-spin" size={24} />
              <span className="text-lg">AI가 건강진단서를 작성하고 있습니다...</span>
            </div>
            <div className="space-y-3">
              <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
              <div className="h-4 bg-gray-200 rounded animate-pulse w-5/6"></div>
              <div className="h-4 bg-gray-200 rounded animate-pulse w-4/6"></div>
            </div>
          </div>
        ) : error ? (
          <div className="card bg-red-50 border border-red-200">
            <p className="text-red-700">{error}</p>
            <button onClick={loadDiagnosis} className="btn-primary mt-4">
              다시 시도
            </button>
          </div>
        ) : diagnosis ? (
          <div className="card">
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap leading-relaxed">
                {diagnosis.diagnosis}
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <p className="text-sm text-gray-500">
                사용된 분석 도구: {diagnosis.tools_used.join(', ')}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                생성 시각: {new Date(diagnosis.generated_at).toLocaleString('ko-KR')}
              </p>
            </div>

            <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                ⚠️ <strong>면책 조항:</strong> 이 정보는 참고용이며, 최종 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다.
              </p>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};
