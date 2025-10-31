import Layout from '../components/Layout';

const AboutPage = () => {
  const features = [
    {
      icon: '🤖',
      title: 'AI 驱动',
      description: '采用先进的 AI 算法，智能分析项目需求',
    },
    {
      icon: '⚡',
      title: '快速响应',
      description: '秒级生成专业的技术方案和开发建议',
    },
    {
      icon: '🎯',
      title: '精准推荐',
      description: '基于项目特点推荐最合适的技术栈',
    },
    {
      icon: '📊',
      title: '数据分析',
      description: '深度分析项目复杂度和开发周期',
    },
  ];

  const team = [
    {
      name: 'AI 分析引擎',
      role: '核心技术',
      avatar: '🧠',
      description: '基于深度学习的项目分析系统',
    },
    {
      name: 'React 19',
      role: '前端框架',
      avatar: '⚛️',
      description: '最新版本的 React 框架',
    },
    {
      name: 'TypeScript',
      role: '类型系统',
      avatar: '📘',
      description: '提供完整的类型安全保障',
    },
    {
      name: 'Tailwind CSS',
      role: '样式方案',
      avatar: '🎨',
      description: '现代化的原子化 CSS 框架',
    },
  ];

  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-20 animate-fadeIn">
          <div className="inline-block p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-4">
            <span className="text-6xl">ℹ️</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            关于我们
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            一个专注于为开发者提供智能项目分析和技术建议的 AI 系统
          </p>
        </div>

        {/* Mission Statement */}
        <div className="mb-20 animate-fadeIn animation-delay-100">
          <div className="max-w-4xl mx-auto p-8 md:p-12 bg-gradient-to-br from-blue-500/10 to-purple-500/10 backdrop-blur-sm border border-blue-500/20 rounded-3xl">
            <h2 className="text-3xl font-bold text-white mb-6 text-center">
              我们的使命
            </h2>
            <p className="text-slate-300 text-lg leading-relaxed text-center mb-6">
              让每个开发者都能获得专业的 AI 技术顾问服务，
              通过智能分析提升项目规划效率，
              帮助团队选择最优的技术方案，
              加速软件开发进程。
            </p>
            <div className="flex justify-center">
              <div className="inline-flex items-center space-x-2 px-6 py-3 bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 rounded-xl">
                <span className="text-2xl">🚀</span>
                <span className="text-blue-400 font-semibold">
                  让开发更简单，让决策更智能
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-white text-center mb-12 animate-fadeIn">
            核心优势
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 hover:border-slate-600/50 transform hover:-translate-y-2 transition-all duration-300 animate-fadeIn"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Technology Stack */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-white text-center mb-12 animate-fadeIn">
            技术栈
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {team.map((member, index) => (
              <div
                key={index}
                className="text-center p-8 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 hover:border-slate-600/50 transform hover:-translate-y-2 transition-all duration-300 animate-fadeIn"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-4xl transform hover:scale-110 transition-transform duration-300">
                  {member.avatar}
                </div>
                <h3 className="text-xl font-bold text-white mb-1">
                  {member.name}
                </h3>
                <p className="text-blue-400 text-sm mb-3">{member.role}</p>
                <p className="text-slate-400 text-sm">{member.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="mb-20 animate-fadeIn">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { value: '10K+', label: '分析项目', icon: '📊' },
              { value: '95%', label: '准确率', icon: '🎯' },
              { value: '50+', label: '支持技术', icon: '🔧' },
              { value: '24/7', label: '在线服务', icon: '⚡' },
            ].map((stat, index) => (
              <div
                key={index}
                className="text-center p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl hover:bg-slate-800/50 hover:border-slate-600/50 transition-all duration-300"
              >
                <div className="text-4xl mb-2">{stat.icon}</div>
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-slate-400 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Timeline */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-white text-center mb-12 animate-fadeIn">
            发展历程
          </h2>
          <div className="max-w-3xl mx-auto space-y-8">
            {[
              {
                date: '2025.01',
                title: '项目启动',
                description: '开始研发 AI 开发顾问系统',
                color: 'from-blue-500 to-cyan-500',
              },
              {
                date: '2025.06',
                title: '技术突破',
                description: '完成核心 AI 分析引擎开发',
                color: 'from-purple-500 to-pink-500',
              },
              {
                date: '2025.10',
                title: '正式上线',
                description: '系统正式发布，服务全球开发者',
                color: 'from-green-500 to-emerald-500',
              },
            ].map((item, index) => (
              <div
                key={index}
                className="flex items-start space-x-6 animate-fadeIn"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div
                  className={`flex-shrink-0 w-16 h-16 bg-gradient-to-br ${item.color} rounded-xl flex items-center justify-center text-white font-bold shadow-lg`}
                >
                  {item.date.split('.')[1]}月
                </div>
                <div className="flex-1 p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 transition-all duration-300">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-xl font-bold text-white">
                      {item.title}
                    </h3>
                    <span className="text-sm text-slate-500">{item.date}</span>
                  </div>
                  <p className="text-slate-400">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Contact CTA */}
        <div className="text-center p-12 bg-gradient-to-r from-blue-500/10 to-purple-500/10 backdrop-blur-sm border border-blue-500/20 rounded-3xl animate-fadeIn">
          <h2 className="text-3xl font-bold text-white mb-4">
            加入我们的社区
          </h2>
          <p className="text-slate-300 mb-8 text-lg">
            与全球开发者一起，探索 AI 驱动的开发新模式
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-4 bg-blue-500 text-white rounded-xl font-semibold hover:bg-blue-600 shadow-lg shadow-blue-500/50 transform hover:-translate-y-1 transition-all duration-300">
              💬 加入 Discord
            </button>
            <button className="px-8 py-4 bg-slate-800/50 backdrop-blur-sm border border-slate-700 text-slate-300 rounded-xl font-semibold hover:bg-slate-700/50 hover:border-slate-600 transform hover:-translate-y-1 transition-all duration-300">
              📧 联系我们
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AboutPage;
