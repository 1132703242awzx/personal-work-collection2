import { useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

interface HistoryItem {
  id: string;
  projectName: string;
  category: string;
  description: string;
  timestamp: string;
  complexity: string;
  techCount: number;
}

const HistoryPage = () => {
  // 模拟历史记录数据
  const [historyItems] = useState<HistoryItem[]>([
    {
      id: '1',
      projectName: '智能客服系统',
      category: 'Web应用',
      description: '基于 AI 的智能客服平台，支持多渠道接入',
      timestamp: '2025-10-23 15:30',
      complexity: '中等',
      techCount: 8,
    },
    {
      id: '2',
      projectName: '电商移动应用',
      category: '移动应用',
      description: '跨平台电商 APP，包含商品展示、购物车、支付功能',
      timestamp: '2025-10-22 10:15',
      complexity: '较高',
      techCount: 12,
    },
    {
      id: '3',
      projectName: '数据可视化大屏',
      category: '数据分析',
      description: '实时数据监控和可视化大屏系统',
      timestamp: '2025-10-20 09:45',
      complexity: '中等',
      techCount: 6,
    },
  ]);

  const [filter, setFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredItems = historyItems.filter(item => {
    const matchesSearch = item.projectName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filter === 'all' || item.category === filter;
    return matchesSearch && matchesFilter;
  });

  const categories = ['全部', 'Web应用', '移动应用', '数据分析', '人工智能', '企业系统'];

  const getComplexityColor = (complexity: string) => {
    const colors: Record<string, string> = {
      '简单': 'from-green-500 to-emerald-500',
      '中等': 'from-blue-500 to-cyan-500',
      '较高': 'from-orange-500 to-yellow-500',
      '复杂': 'from-red-500 to-pink-500',
    };
    return colors[complexity] || 'from-slate-500 to-slate-600';
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12 animate-fadeIn">
          <div className="inline-block p-4 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl mb-4">
            <span className="text-6xl">📚</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            历史记录
          </h1>
          <p className="text-slate-400 text-lg">
            查看和管理您的项目分析历史
          </p>
        </div>

        {/* Search and Filter */}
        <div className="mb-8 space-y-4 animate-fadeIn animation-delay-100">
          {/* Search Bar */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索项目名称或描述..."
              className="w-full px-6 py-4 pl-14 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:shadow-lg focus:shadow-blue-500/20 transition-all duration-300"
            />
            <svg
              className="absolute left-5 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>

          {/* Category Filter */}
          <div className="flex flex-wrap gap-2">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setFilter(cat === '全部' ? 'all' : cat)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                  (filter === 'all' && cat === '全部') || filter === cat
                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-slate-800/50 text-slate-400 border border-slate-700/50 hover:border-slate-600/50'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* History Grid */}
        {filteredItems.length === 0 ? (
          <div className="text-center py-20">
            <div className="inline-block p-6 bg-slate-800/30 backdrop-blur-sm rounded-3xl mb-6">
              <span className="text-8xl opacity-50">🔍</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-400 mb-2">
              没有找到相关记录
            </h3>
            <p className="text-slate-500 mb-6">
              试试其他搜索关键词或筛选条件
            </p>
            <Link
              to="/advisor"
              className="inline-block px-6 py-3 bg-blue-500 text-white rounded-xl font-semibold hover:bg-blue-600 transition-colors"
            >
              开始新的分析 →
            </Link>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredItems.map((item, index) => (
              <div
                key={item.id}
                className="group bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl overflow-hidden hover:bg-slate-800/50 hover:border-slate-600/50 transform hover:-translate-y-2 transition-all duration-300 animate-fadeIn"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Card Header */}
                <div className="p-6 border-b border-slate-700/50">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-xl font-bold text-white group-hover:text-blue-400 transition-colors">
                      {item.projectName}
                    </h3>
                    <button
                      className="text-slate-500 hover:text-red-400 transition-colors"
                      onClick={() => alert('删除功能')}
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fillRule="evenodd"
                          d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                  </div>

                  <div className="flex items-center space-x-2 mb-3">
                    <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded-md text-xs font-semibold border border-blue-500/30">
                      {item.category}
                    </span>
                    <span
                      className={`px-2 py-1 bg-gradient-to-r ${getComplexityColor(
                        item.complexity
                      )} rounded-md text-xs font-semibold text-white`}
                    >
                      {item.complexity}
                    </span>
                  </div>

                  <p className="text-sm text-slate-400 line-clamp-2 leading-relaxed">
                    {item.description}
                  </p>
                </div>

                {/* Card Footer */}
                <div className="p-6 bg-slate-900/30">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4 text-xs text-slate-500">
                      <div className="flex items-center space-x-1">
                        <span>🕐</span>
                        <span>{item.timestamp}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span>🔧</span>
                        <span>{item.techCount} 项技术</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <button
                      onClick={() => alert('查看详情功能')}
                      className="flex-1 px-4 py-2 bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 rounded-lg text-blue-400 hover:bg-blue-500/30 hover:border-blue-500/50 transition-all duration-300 text-sm font-semibold"
                    >
                      查看详情
                    </button>
                    <button
                      onClick={() => alert('再次使用功能')}
                      className="flex-1 px-4 py-2 bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 rounded-lg text-purple-400 hover:bg-purple-500/30 hover:border-purple-500/50 transition-all duration-300 text-sm font-semibold"
                    >
                      再次使用
                    </button>
                  </div>
                </div>

                {/* Hover Gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-purple-500/0 group-hover:from-blue-500/5 group-hover:to-purple-500/5 transition-all duration-300 pointer-events-none rounded-2xl"></div>
              </div>
            ))}
          </div>
        )}

        {/* Statistics */}
        <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-6 animate-fadeIn">
          <div className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl">
            <div className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-2">
              {historyItems.length}
            </div>
            <div className="text-slate-400 text-sm">总分析数</div>
          </div>
          <div className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl">
            <div className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent mb-2">
              {historyItems.filter(i => i.category === 'Web应用').length}
            </div>
            <div className="text-slate-400 text-sm">Web 项目</div>
          </div>
          <div className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl">
            <div className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent mb-2">
              {historyItems.filter(i => i.category === '移动应用').length}
            </div>
            <div className="text-slate-400 text-sm">移动项目</div>
          </div>
          <div className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl">
            <div className="text-3xl font-bold bg-gradient-to-r from-pink-400 to-purple-500 bg-clip-text text-transparent mb-2">
              本月
            </div>
            <div className="text-slate-400 text-sm">最近活跃</div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HistoryPage;
