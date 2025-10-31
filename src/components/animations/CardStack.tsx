/**
 * 卡片堆叠动画组件
 * 多个卡片依次出现，带有缩放和淡入效果
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { cardStackVariants, cardItemVariants, staggerConfig } from '../../config/animations';

interface CardStackProps {
  children: ReactNode[];
  stagger?: 'fast' | 'normal' | 'slow';
  className?: string;
}

export default function CardStack({ 
  children, 
  stagger = 'normal',
  className = '' 
}: CardStackProps) {
  const containerVariants = {
    ...cardStackVariants,
    visible: {
      ...cardStackVariants.visible,
      transition: {
        ...cardStackVariants.visible.transition,
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
          variants={cardItemVariants}
        >
          {child}
        </motion.div>
      ))}
    </motion.div>
  );
}
