/**
 * 响应式表格组件
 * 移动端水平滚动,桌面端正常显示
 */

import { ReactNode } from 'react';

interface Column {
  key: string;
  title: string;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value: any, row: any, index: number) => ReactNode;
}

interface ResponsiveTableProps {
  columns: Column[];
  data: any[];
  loading?: boolean;
  emptyText?: string;
  className?: string;
}

export default function ResponsiveTable({
  columns,
  data,
  loading = false,
  emptyText = '暂无数据',
  className = ''
}: ResponsiveTableProps) {
  const getAlignment = (align?: string) => {
    switch (align) {
      case 'center': return 'text-center';
      case 'right': return 'text-right';
      default: return 'text-left';
    }
  };

  if (loading) {
    return (
      <div className="w-full overflow-x-auto">
        <div className="min-w-[640px] md:min-w-0">
          <div className="bg-slate-800 rounded-lg p-8 text-center">
            <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-gray-400">加载中...</p>
          </div>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full overflow-x-auto">
        <div className="min-w-[640px] md:min-w-0">
          <div className="bg-slate-800 rounded-lg p-8 text-center">
            <p className="text-gray-400">{emptyText}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`w-full overflow-x-auto ${className}`}>
      {/* 最小宽度确保移动端可以滚动 */}
      <div className="min-w-[640px] md:min-w-0">
        <table className="w-full">
          <thead className="bg-slate-800 border-b border-slate-700">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  style={{ width: column.width }}
                  className={`
                    px-3 py-3 md:px-4 md:py-3 lg:px-6 lg:py-4
                    text-xs md:text-sm lg:text-base
                    font-semibold
                    text-gray-300
                    ${getAlignment(column.align)}
                  `}
                >
                  {column.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-slate-900 divide-y divide-slate-700">
            {data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="hover:bg-slate-800 transition-colors"
              >
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className={`
                      px-3 py-2 md:px-4 md:py-3 lg:px-6 lg:py-4
                      text-xs md:text-sm lg:text-base
                      text-gray-300
                      ${getAlignment(column.align)}
                    `}
                  >
                    {column.render
                      ? column.render(row[column.key], row, rowIndex)
                      : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// 移动端卡片式表格(替代方案)
export function ResponsiveCardTable({
  columns,
  data,
  keyExtractor,
  className = ''
}: {
  columns: Column[];
  data: any[];
  keyExtractor: (item: any, index: number) => string;
  className?: string;
}) {
  return (
    <div className={`space-y-4 ${className}`}>
      {data.map((row, index) => (
        <div
          key={keyExtractor(row, index)}
          className="
            bg-slate-800 
            rounded-lg 
            p-4 md:p-6
            border border-slate-700
            hover:border-blue-500
            transition-colors
          "
        >
          {columns.map((column) => (
            <div key={column.key} className="flex justify-between items-start py-2 border-b border-slate-700 last:border-b-0">
              <span className="text-sm text-gray-400 font-medium">
                {column.title}
              </span>
              <span className="text-sm text-white text-right ml-4">
                {column.render
                  ? column.render(row[column.key], row, index)
                  : row[column.key]}
              </span>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
