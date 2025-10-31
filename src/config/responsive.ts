/**
 * 响应式设计配置
 * 定义断点、间距、字体大小等响应式规则
 */

// 断点定义 (与 Tailwind 默认断点一致)
export const breakpoints = {
  mobile: '0px',      // < 768px
  tablet: '768px',    // 768px - 1024px
  desktop: '1024px',  // > 1024px
  wide: '1280px',     // > 1280px (可选的超宽屏)
} as const;

// 容器最大宽度
export const containerMaxWidth = {
  mobile: '100%',
  tablet: '768px',
  desktop: '1024px',
  wide: '1280px',
} as const;

// 响应式间距
export const spacing = {
  // 内边距
  padding: {
    mobile: 'px-4 py-3',
    tablet: 'md:px-6 md:py-4',
    desktop: 'lg:px-8 lg:py-6',
  },
  // 外边距
  margin: {
    mobile: 'mx-4 my-3',
    tablet: 'md:mx-6 md:my-4',
    desktop: 'lg:mx-8 lg:my-6',
  },
  // 栅格间距
  gap: {
    mobile: 'gap-3',
    tablet: 'md:gap-4',
    desktop: 'lg:gap-6',
  },
} as const;

// 响应式字体大小
export const fontSize = {
  // 标题
  heading: {
    h1: 'text-3xl md:text-4xl lg:text-5xl',
    h2: 'text-2xl md:text-3xl lg:text-4xl',
    h3: 'text-xl md:text-2xl lg:text-3xl',
    h4: 'text-lg md:text-xl lg:text-2xl',
    h5: 'text-base md:text-lg lg:text-xl',
    h6: 'text-sm md:text-base lg:text-lg',
  },
  // 正文
  body: {
    large: 'text-base md:text-lg lg:text-xl',
    normal: 'text-sm md:text-base lg:text-lg',
    small: 'text-xs md:text-sm lg:text-base',
  },
  // 按钮
  button: {
    large: 'text-base md:text-lg',
    normal: 'text-sm md:text-base',
    small: 'text-xs md:text-sm',
  },
} as const;

// 响应式布局
export const layout = {
  // 栅格列数
  grid: {
    mobile: 'grid-cols-1',
    tablet: 'md:grid-cols-2',
    desktop: 'lg:grid-cols-3',
    wide: 'xl:grid-cols-4',
  },
  // Flex 方向
  flex: {
    mobileColumn: 'flex-col',
    tabletRow: 'md:flex-row',
  },
  // 宽度
  width: {
    full: 'w-full',
    tablet: 'md:w-auto',
    desktop: 'lg:w-auto',
  },
} as const;

// 触摸友好的交互元素尺寸 (最小44x44px)
export const touchTarget = {
  // 按钮尺寸
  button: {
    small: 'min-h-[44px] min-w-[44px] px-4 py-2',
    medium: 'min-h-[48px] min-w-[48px] px-6 py-3',
    large: 'min-h-[52px] min-w-[52px] px-8 py-4',
  },
  // 图标按钮
  iconButton: {
    small: 'w-11 h-11', // 44px
    medium: 'w-12 h-12', // 48px
    large: 'w-14 h-14', // 56px
  },
  // 输入框
  input: {
    height: 'min-h-[44px]',
    padding: 'px-4 py-3',
  },
} as const;

// 响应式卡片样式
export const card = {
  padding: 'p-4 md:p-6 lg:p-8',
  borderRadius: 'rounded-lg md:rounded-xl',
  spacing: 'space-y-3 md:space-y-4 lg:space-y-6',
} as const;

// 导航栏响应式
export const navigation = {
  height: 'h-14 md:h-16 lg:h-20',
  padding: 'px-4 md:px-6 lg:px-8',
  logoSize: 'h-8 md:h-10 lg:h-12',
  menuItemSpacing: 'space-x-2 md:space-x-4 lg:space-x-6',
} as const;

// 表格响应式
export const table = {
  // 移动端启用水平滚动
  container: 'overflow-x-auto',
  // 最小宽度确保不会挤在一起
  minWidth: 'min-w-[640px] md:min-w-0',
  // 单元格padding
  cellPadding: 'px-3 py-2 md:px-4 md:py-3 lg:px-6 lg:py-4',
  // 字体大小
  fontSize: 'text-xs md:text-sm lg:text-base',
} as const;

// 响应式图片
export const image = {
  // 圆角
  borderRadius: 'rounded-md md:rounded-lg lg:rounded-xl',
  // 对象适配
  objectFit: 'object-cover',
  // 常见尺寸
  avatar: {
    small: 'w-8 h-8 md:w-10 md:h-10',
    medium: 'w-12 h-12 md:w-14 md:h-14',
    large: 'w-16 h-16 md:w-20 md:h-20',
  },
} as const;

// 模态框响应式
export const modal = {
  // 宽度
  width: {
    small: 'w-full md:max-w-md',
    medium: 'w-full md:max-w-lg lg:max-w-2xl',
    large: 'w-full md:max-w-2xl lg:max-w-4xl',
    full: 'w-full md:max-w-6xl',
  },
  // 边距(移动端占满,桌面端有边距)
  margin: 'mx-0 md:mx-4 lg:mx-auto',
  // Padding
  padding: 'p-4 md:p-6 lg:p-8',
} as const;

// 侧边栏响应式
export const sidebar = {
  // 宽度
  width: 'w-full md:w-64 lg:w-80',
  // 移动端全屏,桌面端固定
  position: 'fixed md:relative',
  // 移动端从侧边滑入
  transform: 'translate-x-0',
} as const;

// 工具函数: 组合响应式类
export function combineResponsive(...classes: string[]): string {
  return classes.filter(Boolean).join(' ');
}

// 工具函数: 根据屏幕尺寸返回值
export function getResponsiveValue<T>(
  mobile: T,
  tablet?: T,
  desktop?: T
): T {
  if (typeof window === 'undefined') return mobile;
  
  const width = window.innerWidth;
  
  if (width >= 1024 && desktop) return desktop;
  if (width >= 768 && tablet) return tablet;
  return mobile;
}

// 工具函数: 检测设备类型
export function getDeviceType(): 'mobile' | 'tablet' | 'desktop' {
  if (typeof window === 'undefined') return 'mobile';
  
  const width = window.innerWidth;
  
  if (width >= 1024) return 'desktop';
  if (width >= 768) return 'tablet';
  return 'mobile';
}

// 工具函数: 检测是否为触摸设备
export function isTouchDevice(): boolean {
  if (typeof window === 'undefined') return false;
  
  return (
    'ontouchstart' in window ||
    navigator.maxTouchPoints > 0 ||
    (navigator as any).msMaxTouchPoints > 0
  );
}

// Hook: 监听窗口尺寸变化
export function useResponsive() {
  if (typeof window === 'undefined') {
    return {
      isMobile: true,
      isTablet: false,
      isDesktop: false,
      deviceType: 'mobile' as const,
    };
  }

  const [deviceType, setDeviceType] = React.useState(getDeviceType());

  React.useEffect(() => {
    const handleResize = () => {
      setDeviceType(getDeviceType());
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return {
    isMobile: deviceType === 'mobile',
    isTablet: deviceType === 'tablet',
    isDesktop: deviceType === 'desktop',
    deviceType,
  };
}

// 导出 React (用于 Hook)
import * as React from 'react';
