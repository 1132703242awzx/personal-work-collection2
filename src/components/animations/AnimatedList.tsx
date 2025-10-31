/**
 * 列表动画组件
 * 逐项显示列表内容，带交错延迟效果
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { listContainerVariants, listItemVariants, staggerConfig } from '../../config/animations';

interface AnimatedListProps {
  children: ReactNode[];
  stagger?: 'fast' | 'normal' | 'slow';
  className?: string;
}

export default function AnimatedList({ 
  children, 
  stagger = 'normal',
  className = '' 
}: AnimatedListProps) {
  const containerVariants = {
    ...listContainerVariants,
    visible: {
      ...listContainerVariants.visible,
      transition: {
        ...listContainerVariants.visible.transition,
        staggerChildren: staggerConfig[stagger]
      }
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className={className}
    >
      {children.map((child, index) => (
        <motion.div
          key={index}
          variants={listItemVariants}
        >
          {child}
        </motion.div>
      ))}
    </motion.div>
  );
}
