import { FormDraft, ProjectRequirements } from '../types';

const DRAFT_KEY = 'project_requirements_draft';
const AUTO_SAVE_DELAY = 2000; // 2 seconds

export class DraftManager {
  private saveTimeout: NodeJS.Timeout | null = null;

  /**
   * 保存草稿到 localStorage
   */
  saveDraft(step: number, data: Partial<ProjectRequirements>): void {
    const draft: FormDraft = {
      step,
      currentStep: step,
      data,
      timestamp: Date.now(),
    };

    try {
      localStorage.setItem(DRAFT_KEY, JSON.stringify(draft));
      console.log('✅ 草稿已保存', draft);
    } catch (error) {
      console.error('❌ 保存草稿失败:', error);
    }
  }

  /**
   * 自动保存草稿（防抖）
   */
  autoSaveDraft(step: number, data: Partial<ProjectRequirements>): void {
    if (this.saveTimeout) {
      clearTimeout(this.saveTimeout);
    }

    this.saveTimeout = setTimeout(() => {
      this.saveDraft(step, data);
    }, AUTO_SAVE_DELAY);
  }

  /**
   * 加载草稿
   */
  loadDraft(): FormDraft | null {
    try {
      const draft = localStorage.getItem(DRAFT_KEY);
      if (!draft) return null;

      const parsed: FormDraft = JSON.parse(draft);
      
      // 检查草稿是否过期（24小时）
      const isExpired = Date.now() - parsed.timestamp > 24 * 60 * 60 * 1000;
      if (isExpired) {
        this.clearDraft();
        return null;
      }

      return parsed;
    } catch (error) {
      console.error('❌ 加载草稿失败:', error);
      return null;
    }
  }

  /**
   * 清除草稿
   */
  clearDraft(): void {
    try {
      localStorage.removeItem(DRAFT_KEY);
      console.log('🗑️ 草稿已清除');
    } catch (error) {
      console.error('❌ 清除草稿失败:', error);
    }
  }

  /**
   * 检查是否有草稿
   */
  hasDraft(): boolean {
    return this.loadDraft() !== null;
  }

  /**
   * 获取草稿的保存时间
   */
  getDraftTimestamp(): string | null {
    const draft = this.loadDraft();
    if (!draft) return null;

    const date = new Date(draft.timestamp);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
}

export const draftManager = new DraftManager();
