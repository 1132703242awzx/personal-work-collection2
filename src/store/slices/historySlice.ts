import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { HistoryState, SearchHistory, AnalysisResult, ProjectRequirements } from '../../types';

const HISTORY_STORAGE_KEY = 'ai_advisor_history';
const MAX_HISTORY_ITEMS = 50;

// 从 localStorage 加载历史记录
const loadHistoryFromStorage = (): SearchHistory[] => {
  try {
    const stored = localStorage.getItem(HISTORY_STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      // 按时间戳降序排序
      return parsed.sort((a: SearchHistory, b: SearchHistory) => b.timestamp - a.timestamp);
    }
  } catch (error) {
    console.error('加载历史记录失败:', error);
  }
  return [];
};

// 保存历史记录到 localStorage
const saveHistoryToStorage = (history: SearchHistory[]) => {
  try {
    // 只保存最新的 MAX_HISTORY_ITEMS 条记录
    const itemsToSave = history.slice(0, MAX_HISTORY_ITEMS);
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(itemsToSave));
  } catch (error) {
    console.error('保存历史记录失败:', error);
  }
};

const initialState: HistoryState = {
  items: loadHistoryFromStorage(),
  loading: false,
  error: null,
};

// 异步 Thunk: 添加历史记录
export const addHistoryItem = createAsyncThunk(
  'history/add',
  async ({ requirements, result }: { requirements: ProjectRequirements; result: AnalysisResult }) => {
    const historyItem: SearchHistory = {
      id: Date.now().toString(),
      requirements,
      result,
      timestamp: Date.now(),
      favorite: false,
    };

    // 模拟异步保存
    await new Promise(resolve => setTimeout(resolve, 100));

    return historyItem;
  }
);

// 异步 Thunk: 删除历史记录
export const deleteHistoryItem = createAsyncThunk(
  'history/delete',
  async (id: string) => {
    await new Promise(resolve => setTimeout(resolve, 100));
    return id;
  }
);

// 异步 Thunk: 清空历史记录
export const clearHistory = createAsyncThunk(
  'history/clear',
  async () => {
    await new Promise(resolve => setTimeout(resolve, 100));
    return true;
  }
);

const historySlice = createSlice({
  name: 'history',
  initialState,
  reducers: {
    // 切换收藏状态
    toggleFavorite: (state, action: PayloadAction<string>) => {
      const item = state.items.find(i => i.id === action.payload);
      if (item) {
        item.favorite = !item.favorite;
        saveHistoryToStorage(state.items);
      }
    },

    // 批量删除
    batchDelete: (state, action: PayloadAction<string[]>) => {
      state.items = state.items.filter(item => !action.payload.includes(item.id));
      saveHistoryToStorage(state.items);
    },

    // 导入历史记录
    importHistory: (state, action: PayloadAction<SearchHistory[]>) => {
      state.items = [...action.payload, ...state.items]
        .sort((a, b) => b.timestamp - a.timestamp)
        .slice(0, MAX_HISTORY_ITEMS);
      saveHistoryToStorage(state.items);
    },
  },
  extraReducers: (builder) => {
    // addHistoryItem
    builder
      .addCase(addHistoryItem.pending, (state) => {
        state.loading = true;
      })
      .addCase(addHistoryItem.fulfilled, (state, action) => {
        state.loading = false;
        state.items.unshift(action.payload);
        // 限制历史记录数量
        if (state.items.length > MAX_HISTORY_ITEMS) {
          state.items = state.items.slice(0, MAX_HISTORY_ITEMS);
        }
        saveHistoryToStorage(state.items);
      })
      .addCase(addHistoryItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || '添加历史记录失败';
      });

    // deleteHistoryItem
    builder
      .addCase(deleteHistoryItem.pending, (state) => {
        state.loading = true;
      })
      .addCase(deleteHistoryItem.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter(item => item.id !== action.payload);
        saveHistoryToStorage(state.items);
      })
      .addCase(deleteHistoryItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || '删除失败';
      });

    // clearHistory
    builder
      .addCase(clearHistory.pending, (state) => {
        state.loading = true;
      })
      .addCase(clearHistory.fulfilled, (state) => {
        state.loading = false;
        state.items = [];
        localStorage.removeItem(HISTORY_STORAGE_KEY);
      })
      .addCase(clearHistory.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || '清空失败';
      });
  },
});

export const {
  toggleFavorite,
  batchDelete,
  importHistory,
} = historySlice.actions;

export default historySlice.reducer;
