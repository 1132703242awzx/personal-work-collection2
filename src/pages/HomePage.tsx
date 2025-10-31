import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

const HomePage = () => {
  const features = [
    {
      icon: '🎯',
      title: 'AI 智能分析',
      description: '基于先进的 AI 算法，精准分析项目需求',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: '⚡',
      title: '快速生成',
      description: '秒级生成专业的开发建议和技术方案',
      color: 'from-purple-500 to-pink-500',
    },
    {
      icon: '🔧',
      title: '技术栈推荐',
      description: '根据项目特点推荐最适合的技术栈',
      color: 'from-orange-500 to-red-500',
    },
    {
      icon: '📊',
      title: '项目分析',
      description: '深入分析项目复杂度和技术难点',
      color: 'from-green-500 to-emerald-500',
    },
  ];

  const stats = [
    { value: '10K+', label: '分析项目' },
    { value: '95%', label: '准确率' },
    { value: '50+', label: '技术栈' },
    { value: '24/7', label: '在线服务' },
  ];

  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-20 animate-fadeIn">
          <div className="inline-block mb-6 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full">
            <span className="text-blue-400 text-sm font-semibold">
              ✨ 新一代 AI 开发助手
            </span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent leading-tight">
            智能开发顾问系统
          </h1>
          
          <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            输入项目需求，获取 AI 驱动的专业开发建议、技术栈推荐和详细实施方案
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              to="/smart-form"
              className="group px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transform hover:-translate-y-1 transition-all duration-300 flex items-center space-x-2"
            >
              <span>🚀 智能表单</span>
              <span className="group-hover:translate-x-1 transition-transform">
                →
              </span>
            </Link>
            
            <Link
              to="/advisor"
              className="px-8 py-4 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl font-semibold text-slate-300 hover:bg-slate-700/50 hover:border-slate-600 transform hover:-translate-y-1 transition-all duration-300"
            >
              传统模式
            </Link>
            
            <Link
              to="/about"
              className="px-8 py-4 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl font-semibold text-slate-300 hover:bg-slate-700/50 hover:border-slate-600 transform hover:-translate-y-1 transition-all duration-300"
            >
              了解更多
            </Link>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20 animate-fadeIn animation-delay-200">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl hover:bg-slate-800/50 hover:border-slate-600/50 transition-all duration-300"
            >
              <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-2">
                {stat.value}
              </div>
              <div className="text-slate-400 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Features Grid */}
        <div className="mb-20">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-white">
            核心功能
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6 animate-fadeIn animation-delay-400">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group p-8 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 hover:border-slate-600/50 transform hover:-translate-y-2 transition-all duration-300"
              >
                <div
                  className={`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform duration-300`}
                >
                  {feature.icon}
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-3">
                  {feature.title}
                </h3>
                
                <p className="text-slate-400 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="mb-20">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-white">
            如何使用
          </h2>
          
          <div className="max-w-4xl mx-auto space-y-8">
            {[
              {
                step: '01',
                title: '输入项目需求',
                description: '详细描述你的项目类型、功能需求和技术偏好',
                color: 'from-blue-500 to-cyan-500',
              },
              {
                step: '02',
                title: 'AI 智能分析',
                description: 'AI 系统分析需求，生成最优技术方案',
                color: 'from-purple-500 to-pink-500',
              },
              {
                step: '03',
                title: '获取专业建议',
                description: '查看详细的技术栈推荐、AI 提示词和实施建议',
                color: 'from-orange-500 to-red-500',
              },
            ].map((item, index) => (
              <div
                key={index}
                className="flex items-start space-x-6 p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 transition-all duration-300 animate-fadeIn"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div
                  className={`flex-shrink-0 w-16 h-16 bg-gradient-to-br ${item.color} rounded-xl flex items-center justify-center text-white font-bold text-xl`}
                >
                  {item.step}
                </div>
                
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    {item.title}
                  </h3>
                  <p className="text-slate-400">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center p-12 bg-gradient-to-r from-blue-500/10 to-purple-500/10 backdrop-blur-sm border border-blue-500/20 rounded-3xl animate-fadeIn">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-white">
            准备开始了吗？
          </h2>
          <p className="text-slate-300 mb-8 text-lg">
            立即体验 AI 驱动的智能开发建议
          </p>
          <Link
            to="/advisor"
            className="inline-block px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-white shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transform hover:-translate-y-1 transition-all duration-300"
          >
            开始使用 AI 顾问 →
          </Link>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;
