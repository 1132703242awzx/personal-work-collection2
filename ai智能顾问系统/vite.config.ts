import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { visualizer } from 'rollup-plugin-visualizer';
import viteCompression from 'vite-plugin-compression';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
    plugins: [
      react({
        // 启用 React Fast Refresh
        fastRefresh: true,
        // Babel 配置
        babel: {
          plugins: [
            // 生产环境移除 console
            mode === 'production' && [
              'babel-plugin-transform-remove-console',
              { exclude: ['error', 'warn'] },
            ],
          ].filter(Boolean),
        },
      }),
      // Gzip 压缩
      viteCompression({
        verbose: true,
        disable: false,
        threshold: 10240, // 10KB 以上才压缩
        algorithm: 'gzip',
        ext: '.gz',
      }),
      // Brotli 压缩
      viteCompression({
        verbose: true,
        disable: false,
        threshold: 10240,
        algorithm: 'brotliCompress',
        ext: '.br',
      }),
      // 打包分析(仅在分析模式下)
      process.env.ANALYZE && visualizer({
        open: true,
        gzipSize: true,
        brotliSize: true,
        filename: 'dist/stats.html',
      }),
    ].filter(Boolean),
    
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    
    // 开发服务器配置
    server: {
      port: parseInt(env.VITE_PORT || '3000'),
      open: true,
      cors: true,
      // 代理配置(开发环境 API 代理)
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8080',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
    
    // 预览服务器配置
    preview: {
      port: 4173,
      open: true,
    },
    
    // 构建配置
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      // 生产环境生成 sourcemap
      sourcemap: mode === 'production' ? 'hidden' : true,
      // 构建目标
      target: 'es2015',
      // chunk 大小警告限制 (KB)
      chunkSizeWarningLimit: 1000,
      // Rollup 配置
      rollupOptions: {
        output: {
          // 代码分割策略
          manualChunks: {
            // React 核心库
            'react-vendor': ['react', 'react-dom', 'react-router-dom'],
            // Redux 状态管理
            'redux-vendor': ['@reduxjs/toolkit', 'react-redux'],
            // 动画库
            'animation-vendor': ['framer-motion'],
            // 工具库
            'utils-vendor': ['axios', 'date-fns'],
          },
          // 静态资源命名
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name?.split('.') || [];
            const ext = info[info.length - 1];
            
            // 根据文件类型分类
            if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(ext)) {
              return 'assets/images/[name]-[hash][extname]';
            }
            if (/woff2?|eot|ttf|otf/i.test(ext)) {
              return 'assets/fonts/[name]-[hash][extname]';
            }
            return 'assets/[ext]/[name]-[hash][extname]';
          },
        },
      },
      // 压缩配置
      minify: 'terser',
      terserOptions: {
        compress: {
          // 生产环境移除 console 和 debugger
          drop_console: mode === 'production',
          drop_debugger: true,
          // 移除无用代码
          pure_funcs: mode === 'production' ? ['console.log'] : [],
        },
        format: {
          // 移除注释
          comments: false,
        },
      },
      // CSS 代码分割
      cssCodeSplit: true,
      // 清除输出目录
      emptyOutDir: true,
    },
    
    // 依赖优化
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
        '@reduxjs/toolkit',
        'react-redux',
        'framer-motion',
        'axios',
      ],
    },
    
    // 环境变量前缀
    envPrefix: 'VITE_',
    
    // 定义全局常量
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    },
  };
});
