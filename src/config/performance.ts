/**
 * 性能优化配置
 * 包含代码分割、懒加载、缓存等配置
 */

/**
 * 路由懒加载配置
 */
export const lazyLoadConfig = {
  // 加载超时时间 (毫秒)
  timeout: 10000,
  
  // 重试次数
  retryCount: 3,
  
  // 重试延迟 (毫秒)
  retryDelay: 1000,
  
  // 预加载策略
  preload: {
    // 鼠标悬停预加载
    onHover: true,
    // 可见时预加载
    onVisible: true,
    // 延迟时间 (毫秒)
    delay: 200,
  },
} as const;

/**
 * 虚拟列表配置
 */
export const virtualListConfig = {
  // 默认项高度 (px)
  defaultItemHeight: 80,
  
  // 缓冲区项数 (上下各多渲染几项)
  overscan: 3,
  
  // 滚动节流时间 (毫秒)
  scrollThrottle: 16,
  
  // 启用动态高度
  dynamicHeight: true,
} as const;

/**
 * 图片懒加载配置
 */
export const imageLazyLoadConfig = {
  // 根边距 (提前多少像素开始加载)
  rootMargin: '50px',
  
  // 可见度阈值
  threshold: 0.01,
  
  // 占位符
  placeholder: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"%3E%3Crect fill="%23f0f0f0" width="400" height="300"/%3E%3C/svg%3E',
  
  // 模糊占位符质量 (1-100)
  blurQuality: 20,
  
  // 渐入动画时长 (毫秒)
  fadeInDuration: 300,
} as const;

/**
 * 缓存策略配置
 */
export const cacheConfig = {
  // 内存缓存大小 (MB)
  memoryCacheSize: 50,
  
  // 缓存过期时间 (毫秒)
  ttl: 5 * 60 * 1000, // 5分钟
  
  // 最大缓存项数
  maxItems: 100,
  
  // 启用持久化缓存
  persistent: true,
  
  // LocalStorage 键前缀
  storagePrefix: 'react_app_cache_',
} as const;

/**
 * 防抖节流配置
 */
export const debounceThrottleConfig = {
  // 搜索输入防抖时间 (毫秒)
  searchDebounce: 300,
  
  // 窗口调整大小节流时间 (毫秒)
  resizeThrottle: 150,
  
  // 滚动事件节流时间 (毫秒)
  scrollThrottle: 100,
  
  // API 请求防抖时间 (毫秒)
  apiDebounce: 500,
} as const;

/**
 * 代码分割配置
 */
export const codeSplittingConfig = {
  // 是否启用路由预加载
  routePreload: true,
  
  // 是否启用组件预加载
  componentPreload: true,
  
  // 最小代码块大小 (KB)
  minChunkSize: 20,
  
  // 最大代码块大小 (KB)
  maxChunkSize: 244,
  
  // 并行加载数量
  maxParallelRequests: 6,
} as const;

/**
 * 渲染优化配置
 */
export const renderOptimizationConfig = {
  // 启用严格模式
  strictMode: true,
  
  // 启用并发特性
  concurrent: true,
  
  // 批量更新延迟 (毫秒)
  batchUpdateDelay: 0,
  
  // 启用自动批处理
  autoBatch: true,
  
  // 长任务阈值 (毫秒)
  longTaskThreshold: 50,
} as const;

/**
 * 字体加载配置
 */
export const fontLoadConfig = {
  // 字体加载策略
  display: 'swap' as const,
  
  // 字体子集
  subset: ['latin', 'latin-ext'],
  
  // 预加载字体
  preload: true,
  
  // 字体格式优先级
  formats: ['woff2', 'woff'] as const,
} as const;

/**
 * Bundle 分析配置
 */
export const bundleAnalysisConfig = {
  // 是否生成分析报告
  enabled: process.env.ANALYZE === 'true',
  
  // 报告输出路径
  reportPath: 'dist/bundle-report.html',
  
  // 分析模式
  mode: 'static' as const,
  
  // 是否自动打开报告
  openAnalyzer: false,
} as const;

/**
 * 性能监控配置
 */
export const performanceMonitorConfig = {
  // 是否启用性能监控
  enabled: true,
  
  // 采样率 (0-1)
  sampleRate: 1.0,
  
  // 监控指标
  metrics: {
    // First Contentful Paint
    fcp: true,
    // Largest Contentful Paint
    lcp: true,
    // First Input Delay
    fid: true,
    // Cumulative Layout Shift
    cls: true,
    // Time to Interactive
    tti: true,
  },
  
  // 性能阈值 (毫秒)
  thresholds: {
    fcp: 1800,
    lcp: 2500,
    fid: 100,
    cls: 0.1,
    tti: 3800,
  },
} as const;

/**
 * 预取策略
 */
export const prefetchConfig = {
  // 是否启用链接预取
  linkPrefetch: true,
  
  // 预取优先级
  priority: 'low' as const,
  
  // 预取延迟 (毫秒)
  delay: 100,
  
  // 只在空闲时预取
  idleOnly: true,
} as const;

/**
 * 获取所有性能配置
 */
export function getPerformanceConfig() {
  return {
    lazyLoad: lazyLoadConfig,
    virtualList: virtualListConfig,
    imageLazyLoad: imageLazyLoadConfig,
    cache: cacheConfig,
    debounceThrottle: debounceThrottleConfig,
    codeSplitting: codeSplittingConfig,
    renderOptimization: renderOptimizationConfig,
    fontLoad: fontLoadConfig,
    bundleAnalysis: bundleAnalysisConfig,
    performanceMonitor: performanceMonitorConfig,
    prefetch: prefetchConfig,
  };
}

/**
 * 性能优化工具函数
 */

/**
 * 延迟加载模块 (带重试)
 */
export async function lazyLoadWithRetry<T>(
  importFn: () => Promise<T>,
  retries: number = lazyLoadConfig.retryCount,
  delay: number = lazyLoadConfig.retryDelay
): Promise<T> {
  try {
    return await importFn();
  } catch (error) {
    if (retries <= 0) {
      throw error;
    }
    
    await new Promise(resolve => setTimeout(resolve, delay));
    return lazyLoadWithRetry(importFn, retries - 1, delay);
  }
}

/**
 * 判断是否为慢速网络
 */
export function isSlowNetwork(): boolean {
  if (typeof navigator === 'undefined' || !('connection' in navigator)) {
    return false;
  }
  
  const connection = (navigator as any).connection;
  if (!connection) return false;
  
  const slowTypes = ['slow-2g', '2g', '3g'];
  return (
    slowTypes.includes(connection.effectiveType) ||
    connection.saveData === true
  );
}

/**
 * 判断设备是否为低端设备
 */
export function isLowEndDevice(): boolean {
  if (typeof navigator === 'undefined') return false;
  
  // 检查硬件并发数 (CPU核心数)
  const cores = navigator.hardwareConcurrency || 4;
  if (cores < 4) return true;
  
  // 检查设备内存 (GB)
  const memory = (navigator as any).deviceMemory;
  if (memory && memory < 4) return true;
  
  return false;
}

/**
 * 预加载关键资源
 */
export function preloadCriticalResources(resources: string[]) {
  if (typeof document === 'undefined') return;
  
  resources.forEach(href => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.href = href;
    
    // 根据文件类型设置 as 属性
    if (href.endsWith('.js')) link.as = 'script';
    else if (href.endsWith('.css')) link.as = 'style';
    else if (href.endsWith('.woff2') || href.endsWith('.woff')) link.as = 'font';
    else if (/\.(jpg|jpeg|png|webp|svg)$/.test(href)) link.as = 'image';
    
    document.head.appendChild(link);
  });
}

/**
 * 性能标记
 */
export function performanceMark(name: string) {
  if (typeof performance !== 'undefined' && performance.mark) {
    performance.mark(name);
  }
}

/**
 * 性能测量
 */
export function performanceMeasure(name: string, startMark: string, endMark: string) {
  if (typeof performance !== 'undefined' && performance.measure) {
    try {
      performance.measure(name, startMark, endMark);
      const measure = performance.getEntriesByName(name)[0];
      return measure ? measure.duration : 0;
    } catch (error) {
      console.warn('Performance measure failed:', error);
      return 0;
    }
  }
  return 0;
}

export default getPerformanceConfig;
