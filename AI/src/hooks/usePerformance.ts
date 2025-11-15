/**
 * 性能监控 Hooks
 * 用于监控组件渲染性能和 Web Vitals 指标
 */

import { useEffect, useRef, useState } from 'react';
import { performanceMark, performanceMeasure, performanceMonitorConfig } from '@/config/performance';

/**
 * useRenderCount Hook
 * 统计组件渲染次数
 * 
 * @returns 渲染次数
 * 
 * @example
 * const renderCount = useRenderCount();
 * console.log(`组件渲染了 ${renderCount} 次`);
 */
export function useRenderCount(): number {
  const renderCount = useRef(0);
  
  useEffect(() => {
    renderCount.current += 1;
  });

  return renderCount.current;
}

/**
 * useWhyDidYouUpdate Hook
 * 调试 props 变化导致的重渲染
 * 
 * @param name - 组件名称
 * @param props - 组件 props
 * 
 * @example
 * useWhyDidYouUpdate('MyComponent', props);
 */
export function useWhyDidYouUpdate(name: string, props: Record<string, any>) {
  const previousProps = useRef<Record<string, any> | undefined>(undefined);

  useEffect(() => {
    if (previousProps.current) {
      const allKeys = Object.keys({ ...previousProps.current, ...props });
      const changedProps: Record<string, { from: any; to: any }> = {};

      allKeys.forEach(key => {
        if (previousProps.current![key] !== props[key]) {
          changedProps[key] = {
            from: previousProps.current![key],
            to: props[key],
          };
        }
      });

      if (Object.keys(changedProps).length > 0) {
        console.log('[why-did-you-update]', name, changedProps);
      }
    }

    previousProps.current = props;
  });
}

/**
 * usePerformance Hook
 * 测量组件挂载和更新性能
 * 
 * @param componentName - 组件名称
 * 
 * @example
 * usePerformance('MyComponent');
 */
export function usePerformance(componentName: string) {
  const mountTimeRef = useRef<number>(0);
  const renderCountRef = useRef(0);

  useEffect(() => {
    renderCountRef.current += 1;

    if (renderCountRef.current === 1) {
      // 首次挂载
      const startMark = `${componentName}-mount-start`;
      const endMark = `${componentName}-mount-end`;
      
      performanceMark(endMark);
      const duration = performanceMeasure(
        `${componentName}-mount`,
        startMark,
        endMark
      );

      mountTimeRef.current = duration;
      
      if (performanceMonitorConfig.enabled) {
        console.log(`[Performance] ${componentName} 挂载耗时: ${duration.toFixed(2)}ms`);
      }
    }
  });

  // 组件挂载前的标记
  performanceMark(`${componentName}-mount-start`);

  return {
    mountTime: mountTimeRef.current,
    renderCount: renderCountRef.current,
  };
}

/**
 * useWebVitals Hook
 * 监控 Web Vitals 核心指标
 * 
 * @returns Web Vitals 指标
 * 
 * @example
 * const vitals = useWebVitals();
 * console.log('LCP:', vitals.lcp);
 */
export function useWebVitals() {
  const [vitals, setVitals] = useState<{
    lcp?: number;
    fid?: number;
    cls?: number;
    fcp?: number;
    ttfb?: number;
  }>({});

  useEffect(() => {
    if (typeof window === 'undefined' || !performanceMonitorConfig.enabled) {
      return;
    }

    // Largest Contentful Paint (LCP)
    const observeLCP = () => {
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        const lcp = lastEntry.startTime;
        
        setVitals(prev => ({ ...prev, lcp }));
        
        if (lcp > performanceMonitorConfig.thresholds.lcp) {
          console.warn(`[Web Vitals] LCP 超过阈值: ${lcp.toFixed(2)}ms`);
        }
      });

      observer.observe({ type: 'largest-contentful-paint', buffered: true });
      return observer;
    };

    // First Contentful Paint (FCP)
    const observeFCP = () => {
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          if (entry.name === 'first-contentful-paint') {
            const fcp = entry.startTime;
            setVitals(prev => ({ ...prev, fcp }));
            
            if (fcp > performanceMonitorConfig.thresholds.fcp) {
              console.warn(`[Web Vitals] FCP 超过阈值: ${fcp.toFixed(2)}ms`);
            }
          }
        });
      });

      observer.observe({ type: 'paint', buffered: true });
      return observer;
    };

    // First Input Delay (FID)
    const observeFID = () => {
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          const fid = entry.processingStart - entry.startTime;
          setVitals(prev => ({ ...prev, fid }));
          
          if (fid > performanceMonitorConfig.thresholds.fid) {
            console.warn(`[Web Vitals] FID 超过阈值: ${fid.toFixed(2)}ms`);
          }
        });
      });

      observer.observe({ type: 'first-input', buffered: true });
      return observer;
    };

    // Cumulative Layout Shift (CLS)
    const observeCLS = () => {
      let clsValue = 0;
      
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
            setVitals(prev => ({ ...prev, cls: clsValue }));
            
            if (clsValue > performanceMonitorConfig.thresholds.cls) {
              console.warn(`[Web Vitals] CLS 超过阈值: ${clsValue.toFixed(4)}`);
            }
          }
        });
      });

      observer.observe({ type: 'layout-shift', buffered: true });
      return observer;
    };

    // Time to First Byte (TTFB)
    const observeTTFB = () => {
      const navigationEntry = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      if (navigationEntry) {
        const ttfb = navigationEntry.responseStart - navigationEntry.requestStart;
        setVitals(prev => ({ ...prev, ttfb }));
      }
    };

    // 初始化所有观察器
    const observers: PerformanceObserver[] = [];
    
    try {
      observers.push(observeLCP());
      observers.push(observeFCP());
      observers.push(observeFID());
      observers.push(observeCLS());
      observeTTFB();
    } catch (error) {
      console.error('[Web Vitals] 初始化失败:', error);
    }

    // 清理
    return () => {
      observers.forEach(observer => observer.disconnect());
    };
  }, []);

  return vitals;
}

/**
 * useMemoryMonitor Hook
 * 监控内存使用情况
 * 
 * @returns 内存信息
 */
export function useMemoryMonitor() {
  const [memoryInfo, setMemoryInfo] = useState<{
    usedJSHeapSize?: number;
    totalJSHeapSize?: number;
    jsHeapSizeLimit?: number;
    usedPercentage?: number;
  }>({});

  useEffect(() => {
    const checkMemory = () => {
      // @ts-ignore - performance.memory 在某些浏览器中可用
      const memory = (performance as any).memory;
      
      if (memory) {
        const usedPercentage = (memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100;
        
        setMemoryInfo({
          usedJSHeapSize: memory.usedJSHeapSize,
          totalJSHeapSize: memory.totalJSHeapSize,
          jsHeapSizeLimit: memory.jsHeapSizeLimit,
          usedPercentage,
        });

        // 警告内存使用过高
        if (usedPercentage > 90) {
          console.warn(`[Memory] 内存使用率过高: ${usedPercentage.toFixed(2)}%`);
        }
      }
    };

    checkMemory();
    const interval = setInterval(checkMemory, 5000); // 每5秒检查一次

    return () => clearInterval(interval);
  }, []);

  return memoryInfo;
}

/**
 * useLongTask Hook
 * 监控长任务 (阻塞主线程的任务)
 * 
 * @returns 长任务信息
 */
export function useLongTask() {
  const [longTasks, setLongTasks] = useState<Array<{
    duration: number;
    startTime: number;
  }>>([]);

  useEffect(() => {
    if (typeof PerformanceObserver === 'undefined') {
      return;
    }

    const observer = new PerformanceObserver(list => {
      const entries = list.getEntries();
      const tasks = entries.map((entry: any) => ({
        duration: entry.duration,
        startTime: entry.startTime,
      }));

      setLongTasks(prev => [...prev, ...tasks]);

      tasks.forEach(task => {
        if (task.duration > performanceMonitorConfig.thresholds.tti) {
          console.warn(
            `[Long Task] 检测到长任务: ${task.duration.toFixed(2)}ms at ${task.startTime.toFixed(2)}ms`
          );
        }
      });
    });

    try {
      observer.observe({ type: 'longtask', buffered: true });
    } catch (error) {
      // longtask API 可能不被支持
      console.debug('[Long Task] 浏览器不支持 longtask API');
    }

    return () => observer.disconnect();
  }, []);

  return longTasks;
}
