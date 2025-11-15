import React from 'react';
import { useResponsive } from '@/hooks/useResponsive';

export interface ShowProps {
  /** 组件在移动端是否显示 */
  mobile?: boolean;
  /** 组件在平板是否显示 */
  tablet?: boolean;
  /** 组件在桌面端是否显示 */
  desktop?: boolean;
  /** 组件在超宽屏是否显示 */
  wide?: boolean;
  /** 子组件 */
  children: React.ReactNode;
}

/**
 * Show 组件
 * 根据断点条件显示组件
 * 
 * @example
 * // 仅在移动端显示
 * <Show mobile>
 *   <MobileMenu />
 * </Show>
 * 
 * // 在桌面端和超宽屏显示
 * <Show desktop wide>
 *   <DesktopSidebar />
 * </Show>
 */
export function Show({ mobile, tablet, desktop, wide, children }: ShowProps) {
  const { isMobile, isTablet, isDesktop, isWide } = useResponsive();

  // 如果没有指定任何断点,默认在所有设备显示
  if (!mobile && !tablet && !desktop && !wide) {
    return <>{children}</>;
  }

  // 检查当前设备是否应该显示
  const shouldShow = (
    (mobile && isMobile) ||
    (tablet && isTablet) ||
    (desktop && isDesktop && !isWide) ||
    (wide && isWide)
  );

  return shouldShow ? <>{children}</> : null;
}

export interface HideProps {
  /** 组件在移动端是否隐藏 */
  mobile?: boolean;
  /** 组件在平板是否隐藏 */
  tablet?: boolean;
  /** 组件在桌面端是否隐藏 */
  desktop?: boolean;
  /** 组件在超宽屏是否隐藏 */
  wide?: boolean;
  /** 子组件 */
  children: React.ReactNode;
}

/**
 * Hide 组件
 * 根据断点条件隐藏组件
 * 
 * @example
 * // 在移动端隐藏
 * <Hide mobile>
 *   <DesktopOnlyFeature />
 * </Hide>
 * 
 * // 在移动端和平板隐藏
 * <Hide mobile tablet>
 *   <DesktopSidebar />
 * </Hide>
 */
export function Hide({ mobile, tablet, desktop, wide, children }: HideProps) {
  const { isMobile, isTablet, isDesktop, isWide } = useResponsive();

  // 如果没有指定任何断点,默认不隐藏
  if (!mobile && !tablet && !desktop && !wide) {
    return <>{children}</>;
  }

  // 检查当前设备是否应该隐藏
  const shouldHide = (
    (mobile && isMobile) ||
    (tablet && isTablet) ||
    (desktop && isDesktop && !isWide) ||
    (wide && isWide)
  );

  return shouldHide ? null : <>{children}</>;
}

export interface ShowAboveProps {
  /** 断点: 在此断点及以上显示 */
  breakpoint: 'mobile' | 'tablet' | 'desktop';
  /** 子组件 */
  children: React.ReactNode;
}

/**
 * ShowAbove 组件
 * 在指定断点及以上显示
 * 
 * @example
 * // 在平板及以上显示
 * <ShowAbove breakpoint="tablet">
 *   <TabletAndDesktopContent />
 * </ShowAbove>
 */
export function ShowAbove({ breakpoint, children }: ShowAboveProps) {
  const { isTabletUp, isDesktopUp } = useResponsive();

  const shouldShow = 
    (breakpoint === 'mobile') ||
    (breakpoint === 'tablet' && isTabletUp) ||
    (breakpoint === 'desktop' && isDesktopUp);

  return shouldShow ? <>{children}</> : null;
}

export interface ShowBelowProps {
  /** 断点: 在此断点以下显示 */
  breakpoint: 'tablet' | 'desktop' | 'wide';
  /** 子组件 */
  children: React.ReactNode;
}

/**
 * ShowBelow 组件
 * 在指定断点以下显示
 * 
 * @example
 * // 在桌面端以下(平板+移动端)显示
 * <ShowBelow breakpoint="desktop">
 *   <MobileAndTabletContent />
 * </ShowBelow>
 */
export function ShowBelow({ breakpoint, children }: ShowBelowProps) {
  const { isMobile, isTablet, isDesktop } = useResponsive();

  const shouldShow = 
    (breakpoint === 'tablet' && isMobile) ||
    (breakpoint === 'desktop' && (isMobile || isTablet)) ||
    (breakpoint === 'wide' && (isMobile || isTablet || isDesktop));

  return shouldShow ? <>{children}</> : null;
}

export interface ResponsiveSwitchProps {
  /** 移动端渲染内容 */
  mobile?: React.ReactNode;
  /** 平板渲染内容 */
  tablet?: React.ReactNode;
  /** 桌面端渲染内容 */
  desktop?: React.ReactNode;
  /** 超宽屏渲染内容 */
  wide?: React.ReactNode;
  /** 默认渲染内容 */
  fallback?: React.ReactNode;
}

/**
 * ResponsiveSwitch 组件
 * 根据当前设备类型渲染不同内容
 * 
 * @example
 * <ResponsiveSwitch
 *   mobile={<MobileView />}
 *   tablet={<TabletView />}
 *   desktop={<DesktopView />}
 *   fallback={<DefaultView />}
 * />
 */
export function ResponsiveSwitch({
  mobile,
  tablet,
  desktop,
  wide,
  fallback,
}: ResponsiveSwitchProps) {
  const { deviceType } = useResponsive();

  switch (deviceType) {
    case 'mobile':
      return <>{mobile ?? fallback}</>;
    case 'tablet':
      return <>{tablet ?? fallback}</>;
    case 'desktop':
      return <>{desktop ?? wide ?? fallback}</>;
    case 'wide':
      return <>{wide ?? desktop ?? fallback}</>;
    default:
      return <>{fallback}</>;
  }
}

/**
 * 快捷组件: 仅移动端显示
 */
export function ShowMobile({ children }: { children: React.ReactNode }) {
  return <Show mobile>{children}</Show>;
}

/**
 * 快捷组件: 仅平板显示
 */
export function ShowTablet({ children }: { children: React.ReactNode }) {
  return <Show tablet>{children}</Show>;
}

/**
 * 快捷组件: 仅桌面端显示
 */
export function ShowDesktop({ children }: { children: React.ReactNode }) {
  return <Show desktop>{children}</Show>;
}

/**
 * 快捷组件: 桌面端及以上显示
 */
export function ShowDesktopUp({ children }: { children: React.ReactNode }) {
  return <Show desktop wide>{children}</Show>;
}

/**
 * 快捷组件: 移动端隐藏
 */
export function HideMobile({ children }: { children: React.ReactNode }) {
  return <Hide mobile>{children}</Hide>;
}

/**
 * 快捷组件: 桌面端隐藏
 */
export function HideDesktop({ children }: { children: React.ReactNode }) {
  return <Hide desktop wide>{children}</Hide>;
}
