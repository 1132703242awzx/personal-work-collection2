/**
 * 响应式图片组件
 * 支持懒加载、多分辨率、占位符
 */

import { useState, ImgHTMLAttributes } from 'react';

interface ResponsiveImageProps extends Omit<ImgHTMLAttributes<HTMLImageElement>, 'src'> {
  src: string;
  alt: string;
  srcSet?: string;
  sizes?: string;
  aspectRatio?: '1/1' | '4/3' | '16/9' | '21/9';
  objectFit?: 'cover' | 'contain' | 'fill';
  lazy?: boolean;
  placeholder?: string;
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'full';
  className?: string;
}

export default function ResponsiveImage({
  src,
  alt,
  srcSet,
  sizes,
  aspectRatio,
  objectFit = 'cover',
  lazy = true,
  placeholder,
  rounded = 'md',
  className = '',
  ...props
}: ResponsiveImageProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(false);

  const aspectRatioClasses = {
    '1/1': 'aspect-square',
    '4/3': 'aspect-[4/3]',
    '16/9': 'aspect-video',
    '21/9': 'aspect-[21/9]'
  };

  const roundedClasses = {
    none: '',
    sm: 'rounded md:rounded-lg',
    md: 'rounded-md md:rounded-lg lg:rounded-xl',
    lg: 'rounded-lg md:rounded-xl lg:rounded-2xl',
    full: 'rounded-full'
  };

  const objectFitClasses = {
    cover: 'object-cover',
    contain: 'object-contain',
    fill: 'object-fill'
  };

  if (error) {
    return (
      <div className={`
        ${aspectRatio ? aspectRatioClasses[aspectRatio] : ''}
        ${roundedClasses[rounded]}
        bg-slate-800
        flex items-center justify-center
        ${className}
      `}>
        <svg className="w-12 h-12 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
    );
  }

  return (
    <div className={`
      relative overflow-hidden
      ${aspectRatio ? aspectRatioClasses[aspectRatio] : ''}
      ${roundedClasses[rounded]}
      ${className}
    `}>
      {/* 占位符/骨架屏 */}
      {!isLoaded && (
        <div className="absolute inset-0 bg-slate-800 animate-pulse" />
      )}

      {/* 主图片 */}
      <img
        src={src}
        alt={alt}
        srcSet={srcSet}
        sizes={sizes}
        loading={lazy ? 'lazy' : 'eager'}
        onLoad={() => setIsLoaded(true)}
        onError={() => setError(true)}
        className={`
          w-full h-full
          ${objectFitClasses[objectFit]}
          transition-opacity duration-300
          ${isLoaded ? 'opacity-100' : 'opacity-0'}
        `}
        {...props}
      />
    </div>
  );
}

// 头像组件
export function ResponsiveAvatar({
  src,
  alt,
  size = 'md',
  status,
  fallback,
  className = ''
}: {
  src?: string;
  alt: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  status?: 'online' | 'offline' | 'busy';
  fallback?: string;
  className?: string;
}) {
  const [error, setError] = useState(false);

  const sizeClasses = {
    sm: 'w-8 h-8 md:w-10 md:h-10',
    md: 'w-12 h-12 md:w-14 md:h-14',
    lg: 'w-16 h-16 md:w-20 md:h-20',
    xl: 'w-24 h-24 md:w-32 md:h-32'
  };

  const statusColors = {
    online: 'bg-green-500',
    offline: 'bg-gray-500',
    busy: 'bg-red-500'
  };

  const showFallback = !src || error;

  return (
    <div className={`relative ${sizeClasses[size]} ${className}`}>
      {showFallback ? (
        <div className="
          w-full h-full
          rounded-full
          bg-slate-700
          flex items-center justify-center
          text-white font-semibold
        ">
          {fallback || alt.charAt(0).toUpperCase()}
        </div>
      ) : (
        <img
          src={src}
          alt={alt}
          onError={() => setError(true)}
          className="
            w-full h-full
            rounded-full
            object-cover
            border-2 border-slate-700
          "
        />
      )}

      {/* 状态指示器 */}
      {status && (
        <div className={`
          absolute bottom-0 right-0
          w-3 h-3 md:w-4 md:h-4
          ${statusColors[status]}
          rounded-full
          border-2 border-slate-900
        `} />
      )}
    </div>
  );
}

// 图片网格
export function ResponsiveImageGrid({
  images,
  columns = { mobile: 2, tablet: 3, desktop: 4 },
  gap = 'normal',
  aspectRatio = '1/1',
  className = ''
}: {
  images: Array<{ src: string; alt: string; srcSet?: string }>;
  columns?: { mobile?: number; tablet?: number; desktop?: number };
  gap?: 'small' | 'normal' | 'large';
  aspectRatio?: '1/1' | '4/3' | '16/9';
  className?: string;
}) {
  const gapClasses = {
    small: 'gap-2 md:gap-3',
    normal: 'gap-3 md:gap-4',
    large: 'gap-4 md:gap-6'
  };

  const colClasses = [
    columns.mobile && `grid-cols-${columns.mobile}`,
    columns.tablet && `md:grid-cols-${columns.tablet}`,
    columns.desktop && `lg:grid-cols-${columns.desktop}`
  ].filter(Boolean).join(' ');

  return (
    <div className={`
      grid
      ${colClasses}
      ${gapClasses[gap]}
      ${className}
    `}>
      {images.map((image, index) => (
        <ResponsiveImage
          key={index}
          src={image.src}
          alt={image.alt}
          srcSet={image.srcSet}
          aspectRatio={aspectRatio}
          rounded="md"
        />
      ))}
    </div>
  );
}
