/**
 * 页面过渡动画组件
 * 用于路由切换时的动画效果
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { pageTransitionVariants } from '../../config/animations';

interface PageTransitionProps {
  children: ReactNode;
  className?: string;
}

export default function PageTransition({ children, className = '' }: PageTransitionProps) {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageTransitionVariants}
      className={className}
    >
      {children}
    </motion.div>
  );
}
