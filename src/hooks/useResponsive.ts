import { useState, useEffect } from 'react';

// 媒体查询配置
export const mediaQueries = {
  mobile: '(max-width: 767px)',
  tablet: '(min-width: 768px) and (max-width: 1023px)',
  desktop: '(min-width: 1024px)',
  wide: '(min-width: 1280px)',
  tabletUp: '(min-width: 768px)',
  desktopUp: '(min-width: 1024px)',
} as const;

/**
 * useMediaQuery Hook
 * 监听媒体查询变化
 * 
 * @param query - 媒体查询字符串 (e.g., '(min-width: 768px)')
 * @returns 是否匹配
 * 
 * @example
 * const isMobile = useMediaQuery('(max-width: 767px)');
 * const isDesktop = useMediaQuery(mediaQueries.desktop);
 */
export function useMediaQuery(query: string): boolean {
  // 服务端渲染时默认为 false
  const [matches, setMatches] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    // 服务端渲染时不执行
    if (typeof window === 'undefined') return;

    const mediaQueryList = window.matchMedia(query);
    
    // 初始化状态
    setMatches(mediaQueryList.matches);

    // 监听变化
    const handleChange = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    // 添加监听器 (兼容旧浏览器)
    if (mediaQueryList.addEventListener) {
      mediaQueryList.addEventListener('change', handleChange);
    } else {
      // @ts-ignore - 兼容旧版本 Safari
      mediaQueryList.addListener(handleChange);
    }

    // 清理函数
    return () => {
      if (mediaQueryList.removeEventListener) {
        mediaQueryList.removeEventListener('change', handleChange);
      } else {
        // @ts-ignore - 兼容旧版本 Safari
        mediaQueryList.removeListener(handleChange);
      }
    };
  }, [query]);

  return matches;
}

/**
 * 设备类型
 */
export type DeviceType = 'mobile' | 'tablet' | 'desktop' | 'wide';

/**
 * 响应式信息
 */
export interface ResponsiveInfo {
  /** 是否为移动端 (< 768px) */
  isMobile: boolean;
  /** 是否为平板 (768px - 1023px) */
  isTablet: boolean;
  /** 是否为桌面端 (>= 1024px) */
  isDesktop: boolean;
  /** 是否为超宽屏 (>= 1280px) */
  isWide: boolean;
  /** 是否为平板及以上 (>= 768px) */
  isTabletUp: boolean;
  /** 是否为桌面及以上 (>= 1024px) */
  isDesktopUp: boolean;
  /** 当前设备类型 */
  deviceType: DeviceType;
  /** 当前窗口宽度 */
  windowWidth: number;
  /** 当前窗口高度 */
  windowHeight: number;
  /** 是否为触摸设备 */
  isTouchDevice: boolean;
}

/**
 * useResponsive Hook
 * 获取完整的响应式信息
 * 
 * @returns 响应式信息对象
 * 
 * @example
 * const { isMobile, isDesktop, deviceType } = useResponsive();
 * 
 * if (isMobile) {
 *   // 移动端逻辑
 * }
 */
export function useResponsive(): ResponsiveInfo {
  const isMobile = useMediaQuery(mediaQueries.mobile);
  const isTablet = useMediaQuery(mediaQueries.tablet);
  const isDesktop = useMediaQuery(mediaQueries.desktop);
  const isWide = useMediaQuery(mediaQueries.wide);
  const isTabletUp = useMediaQuery(mediaQueries.tabletUp);
  const isDesktopUp = useMediaQuery(mediaQueries.desktopUp);

  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  const isTouchDevice = typeof window !== 'undefined' && (
    'ontouchstart' in window ||
    navigator.maxTouchPoints > 0 ||
    // @ts-ignore
    navigator.msMaxTouchPoints > 0
  );

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // 更新窗口尺寸
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // 初始化
    handleResize();

    // 监听窗口大小变化
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // 确定设备类型
  const getDeviceType = (): DeviceType => {
    if (isWide) return 'wide';
    if (isDesktop) return 'desktop';
    if (isTablet) return 'tablet';
    return 'mobile';
  };

  return {
    isMobile,
    isTablet,
    isDesktop,
    isWide,
    isTabletUp,
    isDesktopUp,
    deviceType: getDeviceType(),
    windowWidth: windowSize.width,
    windowHeight: windowSize.height,
    isTouchDevice,
  };
}

/**
 * useWindowSize Hook
 * 监听窗口尺寸变化
 * 
 * @returns 窗口宽高
 * 
 * @example
 * const { width, height } = useWindowSize();
 */
export function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // 防抖处理 (避免频繁触发)
    let timeoutId: NodeJS.Timeout;
    const debouncedResize = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(handleResize, 150);
    };

    window.addEventListener('resize', debouncedResize);
    
    // 初始化
    handleResize();

    return () => {
      window.removeEventListener('resize', debouncedResize);
      clearTimeout(timeoutId);
    };
  }, []);

  return windowSize;
}

/**
 * useBreakpoint Hook
 * 获取当前断点名称
 * 
 * @returns 断点名称 ('mobile' | 'tablet' | 'desktop' | 'wide')
 * 
 * @example
 * const breakpoint = useBreakpoint();
 * console.log(breakpoint); // 'mobile' | 'tablet' | 'desktop' | 'wide'
 */
export function useBreakpoint(): DeviceType {
  const { deviceType } = useResponsive();
  return deviceType;
}

/**
 * 工具函数: 检查是否为触摸设备
 */
export function isTouchDevice(): boolean {
  if (typeof window === 'undefined') return false;
  
  return (
    'ontouchstart' in window ||
    navigator.maxTouchPoints > 0 ||
    // @ts-ignore
    navigator.msMaxTouchPoints > 0
  );
}

/**
 * 工具函数: 获取设备类型
 */
export function getDeviceType(): DeviceType {
  if (typeof window === 'undefined') return 'desktop';
  
  const width = window.innerWidth;
  
  if (width >= 1280) return 'wide';
  if (width >= 1024) return 'desktop';
  if (width >= 768) return 'tablet';
  return 'mobile';
}
