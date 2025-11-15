import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import HistoryPage from './pages/HistoryPage';
import SmartFormPage from './pages/SmartFormPage';
import ProjectInput from './components/ProjectInput';
import AIResultDisplay from './components/AIResultDisplay';
import AIConfigTest from './components/AIConfigTest';
import AIDebugTest from './components/AIDebugTest';
import { ProjectRequirement, AnalysisResult } from './types';
import { AIAdvisorService } from './services/AIAdvisorService';

// AI 顾问页面组件
const AdvisorPage = () => {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async (requirement: ProjectRequirement, enableAI: boolean) => {
    setIsLoading(true);
    
    try {
      // 模拟网络请求延迟,提供更真实的用户体验
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // 调用 AI 分析服务,传递 useAI 参数
      const analysis = await AIAdvisorService.analyzeProject(requirement, enableAI);
      setResult(analysis);
    } catch (error) {
      console.error('分析失败:', error);
      // 可以在这里添加错误处理 UI
      alert('分析失败,请重试');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
  };

  return (
    <Layout>
      {!result ? (
        <ProjectInput onAnalyze={handleAnalyze} isLoading={isLoading} />
      ) : (
        <AIResultDisplay result={result} onReset={handleReset} />
      )}
    </Layout>
  );
};

// 404 Not Found Page
const NotFoundPage = () => (
  <Layout>
    <div className="container mx-auto px-4 py-20 text-center">
      <div className="inline-block p-6 bg-slate-800/30 backdrop-blur-sm rounded-3xl mb-6">
        <span className="text-9xl opacity-50">🔍</span>
      </div>
      <h1 className="text-6xl md:text-8xl font-bold text-slate-300 mb-4">404</h1>
      <p className="text-slate-400 text-xl mb-8">抱歉，您访问的页面不存在</p>
      <a
        href="/"
        className="inline-block px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transform hover:-translate-y-1 transition-all duration-300"
      >
        返回首页 →
      </a>
    </div>
  </Layout>
);

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/advisor" element={<AdvisorPage />} />
      <Route path="/ai-config" element={<Layout><AIConfigTest /></Layout>} />
      <Route path="/ai-debug" element={<Layout><AIDebugTest /></Layout>} />
      <Route path="/smart-form" element={<SmartFormPage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default App;
