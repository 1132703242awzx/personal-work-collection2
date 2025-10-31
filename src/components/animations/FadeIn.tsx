/**
 * 淡入动画组件
 * 通用的淡入效果，可自定义延迟和持续时间
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { fadeInVariants, fadeInUpVariants, fadeInDownVariants } from '../../config/animations';

interface FadeInProps {
  children: ReactNode;
  direction?: 'none' | 'up' | 'down';
  delay?: number;
  duration?: number;
  className?: string;
}

export default function FadeIn({ 
  children, 
  direction = 'none',
  delay = 0,
  duration = 0.5,
  className = '' 
}: FadeInProps) {
  const getVariants = () => {
    switch (direction) {
      case 'up':
        return fadeInUpVariants;
      case 'down':
        return fadeInDownVariants;
      default:
        return fadeInVariants;
    }
  };

  const variants = getVariants();
  const customVariants = {
    ...variants,
    visible: {
      ...variants.visible,
      transition: {
        ...variants.visible.transition,
        delay,
        duration
      }
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      exit="exit"
      variants={customVariants}
      className={className}
    >
      {children}
    </motion.div>
  );
}
