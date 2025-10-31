/**
 * 历史记录服务
 * 处理用户历史记录的增删改查、导出等功能
 */

import apiClient from './axios.instance';
import { API_CONFIG, MOCK_CONFIG } from '../../config/api.config';
import {
  SearchHistory,
  ProjectRequirements,
  AnalysisResult,
  SaveHistoryRequest,
  ApiResponse,
} from '../../types';

class HistoryService {
  /**
   * 获取用户历史记录
   * GET /api/history
   */
  async getHistory(params?: {
    page?: number;
    pageSize?: number;
    sortBy?: 'timestamp' | 'favorite';
    order?: 'asc' | 'desc';
  }): Promise<{ items: SearchHistory[]; total: number }> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockGetHistory(params);
    }

    try {
      const response = await apiClient.get<
        ApiResponse<{ items: SearchHistory[]; total: number }>
      >(API_CONFIG.ENDPOINTS.HISTORY, { params });

      return response.data.data;
    } catch (error) {
      console.error('[HistoryService] getHistory failed:', error);
      throw error;
    }
  }

  /**
   * 获取单条历史记录
   * GET /api/history/:id
   */
  async getHistoryItem(id: string): Promise<SearchHistory> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockGetHistoryItem(id);
    }

    try {
      const response = await apiClient.get<ApiResponse<{ item: SearchHistory }>>(
        API_CONFIG.ENDPOINTS.HISTORY_ITEM(id)
      );

      return response.data.data.item;
    } catch (error) {
      console.error('[HistoryService] getHistoryItem failed:', error);
      throw error;
    }
  }

  /**
   * 保存到历史记录
   * POST /api/history
   */
  async saveToHistory(
    query: string,
    requirements: ProjectRequirements,
    results: AnalysisResult
  ): Promise<SearchHistory> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockSaveToHistory(query, requirements, results);
    }

    try {
      const response = await apiClient.post<ApiResponse<{ item: SearchHistory }>>(
        API_CONFIG.ENDPOINTS.HISTORY,
        { query, requirements, results } as SaveHistoryRequest
      );

      return response.data.data.item;
    } catch (error) {
      console.error('[HistoryService] saveToHistory failed:', error);
      throw error;
    }
  }

  /**
   * 删除历史记录
   * DELETE /api/history/:id
   */
  async deleteHistory(id: string): Promise<void> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      await this.sleep(MOCK_CONFIG.DELAY / 2);
      return;
    }

    try {
      await apiClient.delete(API_CONFIG.ENDPOINTS.HISTORY_ITEM(id));
    } catch (error) {
      console.error('[HistoryService] deleteHistory failed:', error);
      throw error;
    }
  }

  /**
   * 批量删除历史记录
   * POST /api/history/batch-delete
   */
  async batchDeleteHistory(ids: string[]): Promise<void> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      await this.sleep(MOCK_CONFIG.DELAY);
      return;
    }

    try {
      await apiClient.post(`${API_CONFIG.ENDPOINTS.HISTORY}/batch-delete`, { ids });
    } catch (error) {
      console.error('[HistoryService] batchDeleteHistory failed:', error);
      throw error;
    }
  }

  /**
   * 切换收藏状态
   * PATCH /api/history/:id/favorite
   */
  async toggleFavorite(id: string): Promise<SearchHistory> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockToggleFavorite(id);
    }

    try {
      const response = await apiClient.patch<ApiResponse<{ item: SearchHistory }>>(
        API_CONFIG.ENDPOINTS.HISTORY_FAVORITE(id)
      );

      return response.data.data.item;
    } catch (error) {
      console.error('[HistoryService] toggleFavorite failed:', error);
      throw error;
    }
  }

  /**
   * 清空历史记录
   * DELETE /api/history
   */
  async clearHistory(): Promise<void> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      await this.sleep(MOCK_CONFIG.DELAY);
      localStorage.removeItem('ai_advisor_history');
      return;
    }

    try {
      await apiClient.delete(API_CONFIG.ENDPOINTS.HISTORY);
    } catch (error) {
      console.error('[HistoryService] clearHistory failed:', error);
      throw error;
    }
  }

  /**
   * 导出历史记录
   * GET /api/history/export
   */
  async exportHistory(format: 'json' | 'csv' = 'json'): Promise<Blob> {
    // Mock 模式
    if (MOCK_CONFIG.ENABLED) {
      return this.mockExportHistory(format);
    }

    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.HISTORY_EXPORT, {
        params: { format },
        responseType: 'blob',
      });

      return response.data;
    } catch (error) {
      console.error('[HistoryService] exportHistory failed:', error);
      throw error;
    }
  }

  // ==================== Mock 数据方法 ====================

  private async mockGetHistory(params?: {
    page?: number;
    pageSize?: number;
    sortBy?: 'timestamp' | 'favorite';
    order?: 'asc' | 'desc';
  }): Promise<{ items: SearchHistory[]; total: number }> {
    await this.sleep(MOCK_CONFIG.DELAY);

    // 从 localStorage 读取
    const stored = localStorage.getItem('ai_advisor_history');
    let items: SearchHistory[] = stored ? JSON.parse(stored) : [];

    // 排序
    const sortBy = params?.sortBy || 'timestamp';
    const order = params?.order || 'desc';

    items.sort((a, b) => {
      let comparison = 0;

      if (sortBy === 'timestamp') {
        comparison = a.timestamp - b.timestamp;
      } else if (sortBy === 'favorite') {
        comparison = (a.favorite ? 1 : 0) - (b.favorite ? 1 : 0);
      }

      return order === 'asc' ? comparison : -comparison;
    });

    // 分页
    const page = params?.page || 1;
    const pageSize = params?.pageSize || 10;
    const start = (page - 1) * pageSize;
    const end = start + pageSize;

    return {
      items: items.slice(start, end),
      total: items.length,
    };
  }

  private async mockGetHistoryItem(id: string): Promise<SearchHistory> {
    await this.sleep(MOCK_CONFIG.DELAY / 2);

    const stored = localStorage.getItem('ai_advisor_history');
    const items: SearchHistory[] = stored ? JSON.parse(stored) : [];

    const item = items.find((h) => h.id === id);
    if (!item) {
      throw new Error('History item not found');
    }

    return item;
  }

  private async mockSaveToHistory(
    _query: string,
    requirements: ProjectRequirements,
    results: AnalysisResult
  ): Promise<SearchHistory> {
    await this.sleep(MOCK_CONFIG.DELAY / 2);

    const newItem: SearchHistory = {
      id: `history_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      requirements,
      result: results,
      timestamp: Date.now(),
      favorite: false,
    };

    // 保存到 localStorage
    const stored = localStorage.getItem('ai_advisor_history');
    const items: SearchHistory[] = stored ? JSON.parse(stored) : [];
    items.unshift(newItem);

    // 限制最多保存 50 条
    const limitedItems = items.slice(0, 50);
    localStorage.setItem('ai_advisor_history', JSON.stringify(limitedItems));

    return newItem;
  }

  private async mockToggleFavorite(id: string): Promise<SearchHistory> {
    await this.sleep(MOCK_CONFIG.DELAY / 2);

    const stored = localStorage.getItem('ai_advisor_history');
    const items: SearchHistory[] = stored ? JSON.parse(stored) : [];

    const item = items.find((h) => h.id === id);
    if (!item) {
      throw new Error('History item not found');
    }

    item.favorite = !item.favorite;
    localStorage.setItem('ai_advisor_history', JSON.stringify(items));

    return item;
  }

  private async mockExportHistory(format: 'json' | 'csv'): Promise<Blob> {
    await this.sleep(MOCK_CONFIG.DELAY);

    const stored = localStorage.getItem('ai_advisor_history');
    const items: SearchHistory[] = stored ? JSON.parse(stored) : [];

    if (format === 'json') {
      return new Blob([JSON.stringify(items, null, 2)], { type: 'application/json' });
    } else {
      // CSV format
      const csv = this.convertToCSV(items);
      return new Blob([csv], { type: 'text/csv' });
    }
  }

  private convertToCSV(items: SearchHistory[]): string {
    const headers = ['ID', 'Project Type', 'Complexity', 'Budget', 'Timestamp', 'Favorite'];
    const rows = items.map((item) => [
      item.id,
      item.requirements.projectType,
      item.requirements.complexity,
      item.requirements.budget,
      new Date(item.timestamp).toISOString(),
      item.favorite ? 'Yes' : 'No',
    ]);

    return [headers, ...rows].map((row) => row.join(',')).join('\n');
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// 导出单例
export default new HistoryService();
