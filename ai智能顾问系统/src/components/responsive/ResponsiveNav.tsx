/**
 * 响应式导航栏组件
 * 移动端显示汉堡菜单,桌面端显示完整导航
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface NavItem {
  label: string;
  href?: string;
  onClick?: () => void;
  icon?: React.ReactNode;
}

interface ResponsiveNavProps {
  logo?: React.ReactNode;
  items: NavItem[];
  rightContent?: React.ReactNode;
  className?: string;
}

export default function ResponsiveNav({
  logo,
  items,
  rightContent,
  className = ''
}: ResponsiveNavProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // 监听滚动,添加背景
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // 移动端菜单打开时禁止背景滚动
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isMenuOpen]);

  const handleItemClick = (item: NavItem) => {
    if (item.onClick) {
      item.onClick();
    }
    setIsMenuOpen(false);
  };

  return (
    <>
      {/* 主导航栏 */}
      <nav className={`
        fixed top-0 left-0 right-0 z-50
        transition-all duration-300
        ${scrolled 
          ? 'bg-slate-900/95 backdrop-blur-md shadow-lg' 
          : 'bg-transparent'
        }
        ${className}
      `}>
        <div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14 md:h-16 lg:h-20">
            
            {/* Logo */}
            <div className="flex-shrink-0">
              {logo || (
                <div className="text-white font-bold text-lg md:text-xl lg:text-2xl">
                  Logo
                </div>
              )}
            </div>

            {/* 桌面端导航 - 隐藏在移动端 */}
            <div className="hidden md:flex items-center space-x-1 lg:space-x-2">
              {items.map((item, index) => (
                <button
                  key={index}
                  onClick={() => handleItemClick(item)}
                  className="
                    px-3 lg:px-4 py-2
                    text-sm lg:text-base
                    text-gray-300 hover:text-white
                    hover:bg-slate-800
                    rounded-lg
                    transition-all
                    min-h-[44px]
                    flex items-center gap-2
                  "
                >
                  {item.icon}
                  {item.label}
                </button>
              ))}
            </div>

            {/* 右侧内容 */}
            <div className="hidden md:flex items-center gap-3">
              {rightContent}
            </div>

            {/* 移动端汉堡菜单按钮 */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="
                md:hidden
                w-11 h-11
                flex items-center justify-center
                text-white
                hover:bg-slate-800
                rounded-lg
                transition-colors
              "
              aria-label="Toggle menu"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>
      </nav>

      {/* 移动端侧边菜单 */}
      <AnimatePresence>
        {isMenuOpen && (
          <>
            {/* 背景遮罩 */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMenuOpen(false)}
              className="
                fixed inset-0 z-40
                bg-black/60 backdrop-blur-sm
                md:hidden
              "
            />

            {/* 菜单内容 */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'tween', duration: 0.3 }}
              className="
                fixed top-0 right-0 bottom-0 z-50
                w-4/5 max-w-sm
                bg-slate-900
                shadow-2xl
                overflow-y-auto
                md:hidden
              "
            >
              {/* 菜单头部 */}
              <div className="flex items-center justify-between p-4 border-b border-slate-700">
                <div className="text-white font-bold text-lg">
                  菜单
                </div>
                <button
                  onClick={() => setIsMenuOpen(false)}
                  className="
                    w-11 h-11
                    flex items-center justify-center
                    text-white
                    hover:bg-slate-800
                    rounded-lg
                    transition-colors
                  "
                >
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* 菜单项 */}
              <div className="p-4 space-y-2">
                {items.map((item, index) => (
                  <motion.button
                    key={index}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => handleItemClick(item)}
                    className="
                      w-full
                      px-4 py-3
                      text-left
                      text-base
                      text-gray-300 hover:text-white
                      hover:bg-slate-800
                      rounded-lg
                      transition-all
                      min-h-[52px]
                      flex items-center gap-3
                    "
                  >
                    {item.icon}
                    {item.label}
                  </motion.button>
                ))}

                {/* 移动端右侧内容 */}
                {rightContent && (
                  <div className="pt-4 border-t border-slate-700 mt-4">
                    {rightContent}
                  </div>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

// 导航间距占位符(避免内容被导航遮挡)
export function NavSpacer() {
  return <div className="h-14 md:h-16 lg:h-20" />;
}
