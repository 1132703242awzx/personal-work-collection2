/**
 * 性能监控配置
 * 集成 Web Vitals 和自定义性能指标
 */

// Web Vitals 监控
export interface PerformanceMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  delta: number;
  id: string;
  navigationType?: string;
}

// 性能监控配置
export const performanceConfig = {
  // 是否启用性能监控
  enabled: import.meta.env.VITE_ENABLE_PERFORMANCE_MONITORING === 'true',
  
  // 采样率 (0-1)
  sampleRate: 1.0,
  
  // 报告端点
  endpoint: '/api/performance',
  
  // Web Vitals 阈值
  thresholds: {
    // Largest Contentful Paint (LCP) - 最大内容绘制
    LCP: {
      good: 2500,
      needsImprovement: 4000,
    },
    // First Input Delay (FID) - 首次输入延迟
    FID: {
      good: 100,
      needsImprovement: 300,
    },
    // Cumulative Layout Shift (CLS) - 累积布局偏移
    CLS: {
      good: 0.1,
      needsImprovement: 0.25,
    },
    // First Contentful Paint (FCP) - 首次内容绘制
    FCP: {
      good: 1800,
      needsImprovement: 3000,
    },
    // Time to First Byte (TTFB) - 首字节时间
    TTFB: {
      good: 800,
      needsImprovement: 1800,
    },
    // Interaction to Next Paint (INP) - 交互到下一次绘制
    INP: {
      good: 200,
      needsImprovement: 500,
    },
  },
};

// 性能监控函数
export function reportWebVitals(metric: PerformanceMetric) {
  if (!performanceConfig.enabled) return;
  
  // 采样
  if (Math.random() > performanceConfig.sampleRate) return;
  
  // 确定评级
  const threshold = performanceConfig.thresholds[metric.name as keyof typeof performanceConfig.thresholds];
  if (threshold) {
    if (metric.value <= threshold.good) {
      metric.rating = 'good';
    } else if (metric.value <= threshold.needsImprovement) {
      metric.rating = 'needs-improvement';
    } else {
      metric.rating = 'poor';
    }
  }
  
  // 控制台输出 (开发环境)
  if (import.meta.env.DEV) {
    console.log(`[Performance] ${metric.name}:`, {
      value: metric.value,
      rating: metric.rating,
      delta: metric.delta,
    });
  }
  
  // 发送到分析服务
  sendToAnalytics(metric);
}

// 发送到分析服务
function sendToAnalytics(metric: PerformanceMetric) {
  try {
    // Google Analytics
    if (window.gtag) {
      window.gtag('event', metric.name, {
        event_category: 'Web Vitals',
        value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
        event_label: metric.id,
        non_interaction: true,
      });
    }
    
    // 自定义端点
    if (performanceConfig.endpoint) {
      navigator.sendBeacon(
        performanceConfig.endpoint,
        JSON.stringify({
          ...metric,
          timestamp: Date.now(),
          url: window.location.href,
          userAgent: navigator.userAgent,
        })
      );
    }
    
    // Vercel Analytics
    if (window.va) {
      window.va('event', {
        name: metric.name,
        value: metric.value,
        rating: metric.rating,
      });
    }
  } catch (error) {
    console.error('[Performance] Failed to send metric:', error);
  }
}

// 自定义性能指标
export function measureCustomMetric(name: string, startMark: string, endMark: string) {
  try {
    performance.mark(endMark);
    performance.measure(name, startMark, endMark);
    
    const measure = performance.getEntriesByName(name)[0];
    if (measure) {
      reportWebVitals({
        name,
        value: measure.duration,
        rating: 'good',
        delta: measure.duration,
        id: `custom-${Date.now()}`,
      });
    }
  } catch (error) {
    console.error('[Performance] Failed to measure custom metric:', error);
  }
}

// 页面加载性能
export function measurePageLoad() {
  if (!performanceConfig.enabled) return;
  
  window.addEventListener('load', () => {
    const perfData = performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    const connectTime = perfData.responseEnd - perfData.requestStart;
    const renderTime = perfData.domComplete - perfData.domLoading;
    
    console.log('[Performance] Page Load Metrics:', {
      pageLoadTime: `${pageLoadTime}ms`,
      connectTime: `${connectTime}ms`,
      renderTime: `${renderTime}ms`,
    });
  });
}

// 资源加载性能
export function measureResourceLoading() {
  if (!performanceConfig.enabled) return;
  
  const resources = performance.getEntriesByType('resource');
  const slowResources = resources.filter((resource: any) => resource.duration > 1000);
  
  if (slowResources.length > 0) {
    console.warn('[Performance] Slow resources detected:', slowResources);
  }
}

// Long Task 监控
export function monitorLongTasks() {
  if (!performanceConfig.enabled) return;
  
  if ('PerformanceObserver' in window) {
    try {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          console.warn('[Performance] Long task detected:', {
            duration: entry.duration,
            startTime: entry.startTime,
          });
        }
      });
      
      observer.observe({ entryTypes: ['longtask'] });
    } catch (error) {
      console.error('[Performance] Failed to observe long tasks:', error);
    }
  }
}

// 内存监控
export function monitorMemory() {
  if (!performanceConfig.enabled) return;
  
  if ('memory' in performance) {
    const memory = (performance as any).memory;
    console.log('[Performance] Memory Usage:', {
      usedJSHeapSize: `${(memory.usedJSHeapSize / 1048576).toFixed(2)} MB`,
      totalJSHeapSize: `${(memory.totalJSHeapSize / 1048576).toFixed(2)} MB`,
      jsHeapSizeLimit: `${(memory.jsHeapSizeLimit / 1048576).toFixed(2)} MB`,
    });
  }
}

// 初始化性能监控
export function initPerformanceMonitoring() {
  if (!performanceConfig.enabled) return;
  
  // 监控 Web Vitals
  import('web-vitals').then(({ onCLS, onFID, onFCP, onLCP, onTTFB, onINP }) => {
    onCLS(reportWebVitals);
    onFID(reportWebVitals);
    onFCP(reportWebVitals);
    onLCP(reportWebVitals);
    onTTFB(reportWebVitals);
    onINP(reportWebVitals);
  });
  
  // 其他监控
  measurePageLoad();
  monitorLongTasks();
  
  // 定期监控内存
  setInterval(monitorMemory, 60000); // 每分钟
}

// TypeScript 声明
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    va?: (event: string, data: any) => void;
  }
}
