/**
 * Demo Mode Banner
 * 데모 모드일 때 상단에 표시되는 배너
 */
import React from 'react';
import { AlertCircle } from 'lucide-react';

const DEMO_MODE = !import.meta.env.VITE_API_URL || import.meta.env.VITE_API_URL === 'demo';

export const DemoModeBanner: React.FC = () => {
  if (!DEMO_MODE) return null;

  return (
    <div className="bg-yellow-50 border-b border-yellow-200 px-4 py-3">
      <div className="max-w-4xl mx-auto flex items-start gap-3">
        <AlertCircle className="text-yellow-600 flex-shrink-0 mt-0.5" size={20} />
        <div className="flex-1">
          <p className="text-sm text-yellow-800">
            <strong>데모 모드로 실행 중입니다.</strong> 표시되는 데이터는 샘플입니다.
            실제 주가 및 AI 분석을 보려면{' '}
            <a
              href="https://github.com/your-repo/stock-guide-app#readme"
              target="_blank"
              rel="noopener noreferrer"
              className="underline font-semibold"
            >
              백엔드 서버를 실행
            </a>
            하거나{' '}
            <a
              href="https://github.com/your-repo/stock-guide-app/blob/main/stock-guide-app/QUICK_START.md"
              target="_blank"
              rel="noopener noreferrer"
              className="underline font-semibold"
            >
              QUICK_START.md
            </a>
            를 참고하세요.
          </p>
        </div>
      </div>
    </div>
  );
};
