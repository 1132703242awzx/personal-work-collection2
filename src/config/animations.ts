/**
 * 动画配置常量
 * 统一管理所有动画参数，确保一致性
 */

// Framer Motion 动画变体
export const fadeInVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.5, ease: [0.4, 0, 0.2, 1] as const }
  },
  exit: { 
    opacity: 0,
    transition: { duration: 0.3 }
  }
};

export const fadeInUpVariants = {
  hidden: { 
    opacity: 0, 
    y: 20 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.6, ease: [0.4, 0, 0.2, 1] as const }
  },
  exit: { 
    opacity: 0, 
    y: -20,
    transition: { duration: 0.3 }
  }
};

export const fadeInDownVariants = {
  hidden: { 
    opacity: 0, 
    y: -20 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.6, ease: [0.4, 0, 0.2, 1] as const }
  },
  exit: { 
    opacity: 0, 
    y: 20,
    transition: { duration: 0.3 }
  }
};

export const slideInRightVariants = {
  hidden: { 
    x: 100, 
    opacity: 0 
  },
  visible: { 
    x: 0, 
    opacity: 1,
    transition: { duration: 0.5, ease: [0.4, 0, 0.2, 1] as const }
  },
  exit: { 
    x: -100, 
    opacity: 0,
    transition: { duration: 0.3 }
  }
};

export const slideInLeftVariants = {
  hidden: { 
    x: -100, 
    opacity: 0 
  },
  visible: { 
    x: 0, 
    opacity: 1,
    transition: { duration: 0.5, ease: [0.4, 0, 0.2, 1] as const }
  },
  exit: { 
    x: 100, 
    opacity: 0,
    transition: { duration: 0.3 }
  }
};

export const scaleInVariants = {
  hidden: { 
    scale: 0.9, 
    opacity: 0 
  },
  visible: { 
    scale: 1, 
    opacity: 1,
    transition: { duration: 0.4, ease: [0.4, 0, 0.2, 1] as const }
  },
  exit: { 
    scale: 0.9, 
    opacity: 0,
    transition: { duration: 0.3 }
  }
};

export const bounceInVariants = {
  hidden: { 
    scale: 0.3, 
    opacity: 0 
  },
  visible: { 
    scale: 1, 
    opacity: 1,
    transition: { 
      duration: 0.6,
      ease: [0.68, -0.55, 0.265, 1.55] as const
    }
  }
};

// 列表动画（逐项显示）
export const listContainerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

export const listItemVariants = {
  hidden: { 
    opacity: 0, 
    x: -20 
  },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.5, ease: [0.4, 0, 0.2, 1] as const }
  }
};

// 卡片堆叠动画
export const cardStackVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.1
    }
  }
};

export const cardItemVariants = {
  hidden: { 
    opacity: 0, 
    y: 30,
    scale: 0.95
  },
  visible: { 
    opacity: 1, 
    y: 0,
    scale: 1,
    transition: { 
      duration: 0.5, 
      ease: [0.4, 0, 0.2, 1] as const
    }
  }
};

// 页面过渡动画
export const pageTransitionVariants = {
  initial: { 
    opacity: 0,
    x: -20
  },
  animate: { 
    opacity: 1,
    x: 0,
    transition: { 
      duration: 0.4,
      ease: [0.4, 0, 0.2, 1] as const
    }
  },
  exit: { 
    opacity: 0,
    x: 20,
    transition: { 
      duration: 0.3
    }
  }
};

// 模态框动画
export const modalBackdropVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { duration: 0.2 }
  },
  exit: { 
    opacity: 0,
    transition: { duration: 0.2 }
  }
};

export const modalContentVariants = {
  hidden: { 
    scale: 0.8, 
    opacity: 0,
    y: 20
  },
  visible: { 
    scale: 1, 
    opacity: 1,
    y: 0,
    transition: { 
      duration: 0.3,
      ease: [0.68, -0.55, 0.265, 1.55] as const
    }
  },
  exit: { 
    scale: 0.8, 
    opacity: 0,
    y: 20,
    transition: { duration: 0.2 }
  }
};

// 加载动画
export const spinnerVariants = {
  animate: {
    rotate: 360,
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: 'linear' as const
    }
  }
};

export const pulseVariants = {
  animate: {
    scale: [1, 1.05, 1],
    opacity: [1, 0.8, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: [0.4, 0, 0.6, 1] as const
    }
  }
};

// 按钮悬停动画
export const buttonHoverVariants = {
  rest: { scale: 1 },
  hover: { 
    scale: 1.05,
    transition: { 
      duration: 0.2,
      ease: [0.4, 0, 0.2, 1] as const
    }
  },
  tap: { 
    scale: 0.95,
    transition: { duration: 0.1 }
  }
};

// 悬浮卡片动画
export const floatingCardVariants = {
  rest: { y: 0 },
  hover: { 
    y: -10,
    transition: { 
      duration: 0.3,
      ease: [0.4, 0, 0.2, 1] as const
    }
  }
};

// 通知动画
export const notificationVariants = {
  hidden: { 
    x: 400,
    opacity: 0,
    scale: 0.8
  },
  visible: { 
    x: 0,
    opacity: 1,
    scale: 1,
    transition: { 
      duration: 0.4,
      ease: [0.68, -0.55, 0.265, 1.55] as const
    }
  },
  exit: { 
    x: 400,
    opacity: 0,
    scale: 0.8,
    transition: { duration: 0.3 }
  }
};

// 进度条动画
export const progressBarVariants = {
  initial: { scaleX: 0, originX: 0 },
  animate: (progress: number) => ({
    scaleX: progress / 100,
    transition: {
      duration: 0.5,
      ease: 'easeOut'
    }
  })
};

// 骨架屏动画
export const skeletonVariants = {
  animate: {
    opacity: [0.5, 1, 0.5],
    transition: {
      duration: 1.5,
      repeat: Infinity,
      ease: [0.4, 0, 0.6, 1] as const
    }
  }
};

// 交错动画配置
export const staggerConfig = {
  fast: 0.05,
  normal: 0.1,
  slow: 0.2
};

// 动画持续时间
export const duration = {
  fast: 0.2,
  normal: 0.4,
  slow: 0.6
};

// 缓动函数
export const easing = {
  easeOut: [0.4, 0, 0.2, 1],
  easeIn: [0.4, 0, 1, 1],
  easeInOut: [0.4, 0, 0.6, 1],
  bounce: [0.68, -0.55, 0.265, 1.55],
  spring: { type: 'spring', stiffness: 300, damping: 30 }
};
