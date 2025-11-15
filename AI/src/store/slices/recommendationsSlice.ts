import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { RecommendationsState, ProjectRequirements, AnalysisResult } from '../../types';
import { AIAdvisorService } from '../../services/AIAdvisorService';

const initialState: RecommendationsState = {
  techStack: [],
  prompts: null,
  suggestions: [],
  loading: false,
  error: null,
};

// 异步 Thunk: 获取 AI 推荐
export const fetchRecommendations = createAsyncThunk(
  'recommendations/fetch',
  async (requirements: ProjectRequirements, { rejectWithValue }) => {
    try {
      // 模拟 API 调用延迟
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // 调用 AI 服务
      const result = AIAdvisorService.analyzeProject({
        projectName: requirements.projectType,
        description: requirements.description,
        category: requirements.projectType,
        targetPlatform: requirements.targetPlatform,
        features: requirements.features,
      });

      return result;
    } catch (error: any) {
      return rejectWithValue(error.message || '获取推荐失败');
    }
  }
);

// 异步 Thunk: 重新生成提示词
export const regeneratePrompts = createAsyncThunk(
  'recommendations/regeneratePrompts',
  async (requirements: ProjectRequirements, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 重新生成提示词
      const result = AIAdvisorService.analyzeProject({
        projectName: requirements.projectType,
        description: requirements.description,
        category: requirements.projectType,
        targetPlatform: requirements.targetPlatform,
        features: requirements.features,
      });

      return result.aiPrompt;
    } catch (error: any) {
      return rejectWithValue(error.message || '重新生成失败');
    }
  }
);

const recommendationsSlice = createSlice({
  name: 'recommendations',
  initialState,
  reducers: {
    // 清空推荐
    clearRecommendations: (state) => {
      state.techStack = [];
      state.prompts = null;
      state.suggestions = [];
      state.error = null;
    },

    // 更新技术栈
    updateTechStack: (state, action: PayloadAction<typeof state.techStack>) => {
      state.techStack = action.payload;
    },

    // 清除错误
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // fetchRecommendations
    builder
      .addCase(fetchRecommendations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRecommendations.fulfilled, (state, action: PayloadAction<AnalysisResult>) => {
        state.loading = false;
        state.techStack = action.payload.techStack;
        state.prompts = action.payload.aiPrompt;
        state.suggestions = action.payload.developmentAdvice;
        state.error = null;
      })
      .addCase(fetchRecommendations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // regeneratePrompts
    builder
      .addCase(regeneratePrompts.pending, (state) => {
        state.loading = true;
      })
      .addCase(regeneratePrompts.fulfilled, (state, action) => {
        state.loading = false;
        state.prompts = action.payload;
      })
      .addCase(regeneratePrompts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearRecommendations,
  updateTechStack,
  clearError,
} = recommendationsSlice.actions;

export default recommendationsSlice.reducer;
