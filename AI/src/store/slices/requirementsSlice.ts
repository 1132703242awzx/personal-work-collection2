import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ProjectRequirements, RequirementsState } from '../../types';

const initialState: RequirementsState = {
  data: {
    projectType: '',
    targetPlatform: [],
    complexity: 3,
    budget: 'medium',
    features: [],
    description: '',
  },
  currentStep: 1,
  isValid: false,
};

const requirementsSlice = createSlice({
  name: 'requirements',
  initialState,
  reducers: {
    // 更新需求数据
    updateRequirements: (state, action: PayloadAction<Partial<ProjectRequirements>>) => {
      state.data = { ...state.data, ...action.payload };
    },

    // 重置需求
    resetRequirements: (state) => {
      state.data = initialState.data;
      state.currentStep = 1;
      state.isValid = false;
    },

    // 设置当前步骤
    setCurrentStep: (state, action: PayloadAction<number>) => {
      state.currentStep = action.payload;
    },

    // 下一步
    nextStep: (state) => {
      if (state.currentStep < 4) {
        state.currentStep += 1;
      }
    },

    // 上一步
    previousStep: (state) => {
      if (state.currentStep > 1) {
        state.currentStep -= 1;
      }
    },

    // 设置验证状态
    setValidationState: (state, action: PayloadAction<boolean>) => {
      state.isValid = action.payload;
    },

    // 从草稿加载
    loadFromDraft: (state, action: PayloadAction<{ data: Partial<ProjectRequirements>; step: number }>) => {
      state.data = action.payload.data;
      state.currentStep = action.payload.step;
    },
  },
});

export const {
  updateRequirements,
  resetRequirements,
  setCurrentStep,
  nextStep,
  previousStep,
  setValidationState,
  loadFromDraft,
} = requirementsSlice.actions;

export default requirementsSlice.reducer;
