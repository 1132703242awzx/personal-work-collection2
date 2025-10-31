import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import requirementsReducer from './slices/requirementsSlice';
import recommendationsReducer from './slices/recommendationsSlice';
import uiReducer from './slices/uiSlice';
import historyReducer from './slices/historySlice';

// 持久化中间件配置
const PERSISTED_KEYS = ['ui', 'requirements'];
const STORAGE_KEY = 'redux_state';

// 加载持久化状态
const loadPersistedState = () => {
  try {
    const serialized = localStorage.getItem(STORAGE_KEY);
    if (serialized) {
      return JSON.parse(serialized);
    }
  } catch (error) {
    console.error('加载持久化状态失败:', error);
  }
  return undefined;
};

// 保存状态到 localStorage
const saveStateToStorage = (state: RootState) => {
  try {
    const stateToPersist: any = {};
    
    // 只持久化指定的 keys
    PERSISTED_KEYS.forEach(key => {
      if (key in state) {
        stateToPersist[key] = (state as any)[key];
      }
    });

    localStorage.setItem(STORAGE_KEY, JSON.stringify(stateToPersist));
  } catch (error) {
    console.error('保存状态失败:', error);
  }
};

// 合并 reducers
const rootReducer = combineReducers({
  requirements: requirementsReducer,
  recommendations: recommendationsReducer,
  ui: uiReducer,
  history: historyReducer,
});

// 创建 store
export const store = configureStore({
  reducer: rootReducer,
  preloadedState: loadPersistedState(),
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // 忽略某些 action types 的序列化检查
        ignoredActions: ['recommendations/fetch/fulfilled'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

// 订阅 store 变化，自动持久化
store.subscribe(() => {
  saveStateToStorage(store.getState());
});

// 导出类型
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// 导出 Hooks
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
