/**
 * Mock Data for Demo Mode
 * 백엔드 없이도 앱을 실행할 수 있도록 데모 데이터 제공
 */

export const DEMO_MODE = !import.meta.env.VITE_API_URL || import.meta.env.VITE_API_URL === 'demo';

export const mockDailyKeyword = {
  keyword: "AI 반도체",
  description: "인공지능 학습에 필요한 고성능 칩 기술이 급성장하고 있습니다. 특히 생성형 AI(ChatGPT, Midjourney 등)의 확산으로 GPU 수요가 폭발적으로 증가하고 있으며, 관련 기업들의 주가도 연일 상승세를 보이고 있습니다.",
  sentiment: "긍정",
  generated_at: new Date().toISOString()
};

export const mockStockPrice = (ticker: string) => ({
  ticker,
  current_price: 178.50 + Math.random() * 10,
  change_percent: (Math.random() - 0.5) * 5,
  volume: Math.floor(50000000 + Math.random() * 10000000),
  timestamp: new Date().toISOString()
});

export const mockDiagnosis = (ticker: string) => ({
  ticker,
  diagnosis: `${ticker} 기업 건강진단서 (데모 모드)

✅ 좋은 점
• 현재 주가가 52주 최고가 대비 적정 수준입니다
• 영업이익률이 업계 평균 이상으로 건강합니다
• 전문가들의 평가가 대체로 긍정적입니다
• 재무 안정성이 양호한 편입니다

⚠️ 주의할 점
• 최근 거래량 변동이 있습니다
• 업종 전반의 불확실성이 존재합니다

💡 초보자를 위한 설명
이 기업은 전반적으로 안정적인 재무 상태를 보이고 있습니다.
다만 투자 결정 전 더 많은 정보를 확인하시는 것을 추천드립니다.

⚠️ 면책 조항: 이 정보는 데모 모드입니다. 실제 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다.

📌 실제 데이터를 보려면:
1. 백엔드 서버를 실행하거나
2. Netlify에서 환경변수 VITE_API_URL을 설정하세요`,
  tools_used: ["demo_mode"],
  generated_at: new Date().toISOString()
});

export const mockWatchlist = [
  {
    id: 1,
    ticker: "AAPL",
    company_name: "Apple Inc.",
    memo: "M3 칩 출시 후 매수 고려",
    current_price: 178.50,
    change_percent: 1.2,
    added_at: new Date(Date.now() - 86400000 * 3).toISOString()
  },
  {
    id: 2,
    ticker: "NVDA",
    company_name: "NVIDIA Corporation",
    memo: "AI 붐 수혜주",
    current_price: 495.20,
    change_percent: 3.5,
    added_at: new Date(Date.now() - 86400000 * 7).toISOString()
  },
  {
    id: 3,
    ticker: "MSFT",
    company_name: "Microsoft Corporation",
    memo: "OpenAI 파트너십 주목",
    current_price: 378.90,
    change_percent: -0.8,
    added_at: new Date(Date.now() - 86400000 * 1).toISOString()
  }
];

export const mockAnalysisResult = (ticker: string, question: string) => ({
  answer: `${ticker}에 대한 분석 결과 (데모 모드)

질문: "${question}"

현재 이 기능은 데모 모드로 작동 중입니다.
실제 AI 분석 결과를 보려면 백엔드 서버를 실행하거나
Netlify 환경변수를 설정해주세요.

📌 실제 기능:
- GPT-4 기반 ReAct 에이전트가 5개의 도구를 사용하여 분석
- 실시간 주가, 재무제표, 애널리스트 의견, 뉴스 종합
- 초보자가 이해하기 쉬운 언어로 번역

자세한 내용은 QUICK_START.md를 참고하세요.`,
  tools_used: ["demo_mode"],
  success: true
});
