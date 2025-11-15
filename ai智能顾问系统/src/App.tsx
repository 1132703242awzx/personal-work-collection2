import { useState } from 'react';
import ProjectInput from './components/ProjectInput';
import ResultDisplay from './components/ResultDisplay';
import { ProjectRequirement, AnalysisResult } from './types';
import { AIAdvisorService } from './services/AIAdvisorService';
import './App.css';

function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async (requirement: ProjectRequirement) => {
    setIsLoading(true);
    
    try {
      // 模拟网络请求延迟,提供更真实的用户体验
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // 调用 AI 分析服务
      const analysis = await AIAdvisorService.analyzeProject(requirement);
      setResult(analysis);
    } catch (error) {
      console.error('分析失败:', error);
      // 可以在这里添加错误处理 UI
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1> 智能开发顾问系统</h1>
          <p className="subtitle">AI-Powered Development Advisor</p>
          <p className="description">
            输入您的项目需求，获取专业的 AI 提示词、技术栈推荐和详细的开发建议
          </p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {!result ? (
            <ProjectInput onAnalyze={handleAnalyze} isLoading={isLoading} />
          ) : (
            <ResultDisplay result={result} onReset={handleReset} />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p> 2025 智能开发顾问系统 | Powered by React + TypeScript</p>
      </footer>
    </div>
  );
}

export default App;