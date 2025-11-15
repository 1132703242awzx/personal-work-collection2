interface TechStackCardProps {
  name: string;
  version?: string;
  description: string;
  category: string;
  icon?: string;
  recommended?: boolean;
  difficulty?: 'easy' | 'medium' | 'hard';
}

const TechStackCard = ({
  name,
  version,
  description,
  category,
  icon,
  recommended = false,
  difficulty = 'medium',
}: TechStackCardProps) => {
  const difficultyColors = {
    easy: 'from-green-500 to-emerald-500',
    medium: 'from-blue-500 to-cyan-500',
    hard: 'from-orange-500 to-red-500',
  };

  const difficultyLabels = {
    easy: '简单',
    medium: '中等',
    hard: '困难',
  };

  const categoryColors: Record<string, string> = {
    前端框架: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    后端框架: 'bg-green-500/20 text-green-400 border-green-500/30',
    数据库: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
    工具: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
    其他: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
  };

  return (
    <div className="group relative">
      {/* Recommended Badge */}
      {recommended && (
        <div className="absolute -top-3 -right-3 z-10">
          <div className="px-3 py-1 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full text-xs font-bold text-white shadow-lg shadow-yellow-500/50 animate-pulse">
            ⭐ 推荐
          </div>
        </div>
      )}

      <div className="h-full p-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl hover:bg-slate-800/50 hover:border-slate-600/50 transform hover:-translate-y-2 transition-all duration-300">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            {icon && (
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300">
                {icon}
              </div>
            )}
            <div>
              <h3 className="text-xl font-bold text-white group-hover:text-blue-400 transition-colors">
                {name}
              </h3>
              {version && (
                <span className="text-sm text-slate-500">v{version}</span>
              )}
            </div>
          </div>

          {/* Difficulty Badge */}
          <div
            className={`px-2 py-1 bg-gradient-to-r ${difficultyColors[difficulty]} rounded-lg text-xs font-semibold text-white`}
          >
            {difficultyLabels[difficulty]}
          </div>
        </div>

        {/* Description */}
        <p className="text-slate-400 text-sm leading-relaxed mb-4">
          {description}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <span
            className={`px-3 py-1 rounded-full text-xs font-semibold border ${
              categoryColors[category] || categoryColors['其他']
            }`}
          >
            {category}
          </span>

          <button className="text-blue-400 hover:text-blue-300 text-sm font-semibold transition-colors">
            查看详情 →
          </button>
        </div>

        {/* Hover Effect */}
        <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-blue-500/0 to-purple-500/0 group-hover:from-blue-500/5 group-hover:to-purple-500/5 transition-all duration-300 pointer-events-none"></div>
      </div>
    </div>
  );
};

export default TechStackCard;
