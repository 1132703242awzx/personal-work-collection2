import React, { useState } from 'react';
import { AnalysisResult } from '../types';
import './ResultDisplay.css';

interface ResultDisplayProps {
  result: AnalysisResult;
  onReset: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onReset }) => {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);

  const copyToClipboard = (text: string, section: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(section);
    setTimeout(() => setCopiedSection(null), 2000);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'must-have':
        return 'priority-must';
      case 'recommended':
        return 'priority-recommended';
      default:
        return 'priority-optional';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'must-have':
        return '必需';
      case 'recommended':
        return '推荐';
      default:
        return '可选';
    }
  };

  return (
    <div className="result-display">
      <div className="result-header">
        <h2> 智能分析结果</h2>
        <button onClick={onReset} className="btn-reset">
           重新分析
        </button>
      </div>

      {/* AI 提示词部分 */}
      <section className="result-section">
        <div className="section-header">
          <h3> AI 提示词</h3>
          <button
            onClick={() => copyToClipboard(result.aiPrompt.prompt, 'prompt')}
            className="btn-copy"
          >
            {copiedSection === 'prompt' ? ' 已复制' : ' 复制'}
          </button>
        </div>
        <div className="prompt-box">
          <pre>{result.aiPrompt.prompt}</pre>
        </div>
        <div className="context-box">
          <h4> 上下文信息</h4>
          <p>{result.aiPrompt.context}</p>
        </div>
        <div className="suggestions-box">
          <h4> 建议要点</h4>
          <ul>
            {result.aiPrompt.suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      </section>

      {/* 技术栈推荐 */}
      <section className="result-section">
        <div className="section-header">
          <h3> 推荐技术栈</h3>
        </div>
        <div className="tech-stack-grid">
          {result.techStack.map((tech, index) => (
            <div key={index} className="tech-card">
              <div className="tech-header">
                <span className="tech-category">{tech.category}</span>
                <span className={`tech-priority ${getPriorityColor(tech.priority)}`}>
                  {getPriorityLabel(tech.priority)}
                </span>
              </div>
              <h4 className="tech-name">{tech.name}</h4>
              {tech.version && <p className="tech-version">版本: {tech.version}</p>}
              <p className="tech-reason">{tech.reason}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 开发建议 */}
      <section className="result-section">
        <div className="section-header">
          <h3> 开发路线图</h3>
        </div>
        <div className="timeline">
          {result.developmentAdvice.map((advice, index) => (
            <div key={index} className="timeline-item">
              <div className="timeline-marker">{index + 1}</div>
              <div className="timeline-content">
                <h4>{advice.phase}</h4>
                {advice.estimatedTime && (
                  <p className="timeline-time"> 预计时间: {advice.estimatedTime}</p>
                )}
                <ul className="task-list">
                  {advice.tasks.map((task, taskIndex) => (
                    <li key={taskIndex}>{task}</li>
                  ))}
                </ul>
                {advice.resources && advice.resources.length > 0 && (
                  <div className="resources">
                    <strong>需要资源: </strong>
                    {advice.resources.join('、')}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 额外注意事项 */}
      {result.additionalNotes && result.additionalNotes.length > 0 && (
        <section className="result-section notes-section">
          <div className="section-header">
            <h3> 重要提示</h3>
          </div>
          <div className="notes-grid">
            {result.additionalNotes.map((note, index) => (
              <div key={index} className="note-card">
                {note}
              </div>
            ))}
          </div>
        </section>
      )}

      <div className="action-footer">
        <button onClick={() => window.print()} className="btn-secondary">
           打印报告
        </button>
        <button
          onClick={() => {
            const fullReport = `
AI 提示词:
${result.aiPrompt.prompt}

技术栈推荐:
${result.techStack.map(t => `- ${t.name}: ${t.reason}`).join('\n')}

开发建议:
${result.developmentAdvice.map(a => `${a.phase}:\n${a.tasks.map(t => `  - ${t}`).join('\n')}`).join('\n\n')}
            `.trim();
            copyToClipboard(fullReport, 'full');
          }}
          className="btn-primary"
        >
          {copiedSection === 'full' ? ' 已复制完整报告' : ' 复制完整报告'}
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay;
