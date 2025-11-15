<template>
	<view class="scripts-page">
		<!-- 顶部搜索栏 -->
		<view class="search-bar">
			<view class="search-input-wrap">
				<input 
					class="search-input" 
					v-model="searchKeyword"
					placeholder="搜索剧本名称或类型"
					@input="onSearchInput"
					@confirm="onSearchConfirm"
				/>
				<text class="search-icon">🔍</text>
			</view>
			<view class="search-btn" @tap="onSearchConfirm">
				<text>搜索</text>
			</view>
		</view>

		<!-- 分类筛选选项卡 -->
		<view class="category-tabs">
			<scroll-view scroll-x="true" class="category-scroll">
				<view 
					class="category-item"
					:class="{'active': activeCategory === category.key}" 
					v-for="category in categoryList" 
					:key="category.key"
					@tap="handleCategoryChange(category.key)"
				>
					<text>{{category.name}}</text>
				</view>
			</scroll-view>
		</view>

		<!-- 排序和筛选栏 -->
		<view class="sort-toolbar">
			<view class="sort-options">
				<view class="sort-item" 
					:class="{'active': sortType === 'default'}"
					@tap="handleSortChange('default')">
					<text>综合</text>
				</view>
				<view class="sort-item" 
					:class="{'active': sortType === 'price'}"
					@tap="handleSortChange('price')">
					<text>价格 {{sortType === 'price' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}}</text>
				</view>
				<view class="sort-item" 
					:class="{'active': sortType === 'rating'}"
					@tap="handleSortChange('rating')">
					<text>评分 {{sortType === 'rating' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}}</text>
				</view>
				<view class="sort-item" 
					:class="{'active': sortType === 'playerCount'}"
					@tap="handleSortChange('playerCount')">
					<text>人数 {{sortType === 'playerCount' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}}</text>
				</view>
			</view>
			<view class="result-count">
				<text>共{{displayScriptList.length}}个剧本</text>
			</view>
		</view>

		<!-- 剧本卡片网格布局 -->
		<view class="scripts-container">
			<!-- 下拉刷新提示 -->
			<view class="refresh-tip" v-if="isRefreshing">
				<text>正在刷新...</text>
			</view>
			
			<!-- 剧本网格列表 -->
			<view class="scripts-grid">
				<view 
					class="script-card" 
					v-for="script in displayScriptList" 
					:key="script.id"
					@tap="handleScriptTap(script)"
				>
					<!-- 剧本封面 -->
					<view class="script-cover">
						<image 
							:src="script.coverImage" 
							class="cover-image"
							mode="aspectFill"
							:lazy-load="true"
						/>
						<view class="cover-overlay"></view>
						<!-- 热门标签 -->
						<view class="hot-badge" v-if="script.isHot">
							<text>HOT</text>
						</view>
						<!-- 难度标签 -->
						<view class="difficulty-badge" :class="script.difficulty === '简单' ? 'easy' : script.difficulty === '中等' ? 'medium' : 'hard'">
							<text>{{script.difficulty}}</text>
						</view>
					</view>
					
					<!-- 剧本信息 -->
					<view class="script-info">
						<text class="script-title">{{script.title}}</text>
						
						<!-- 标签列表 -->
						<view class="script-tags">
							<text 
								class="tag-item" 
								v-for="tag in script.tags.slice(0, 3)" 
								:key="tag"
							>{{tag}}</text>
						</view>
						
						<text class="script-description">{{script.description}}</text>
						
						<!-- 基本信息 -->
						<view class="script-meta">
							<view class="meta-item">
								<text>👥</text>
								<text>{{script.playerCount}}人</text>
							</view>
							<view class="meta-item">
								<text>⏱</text>
								<text>{{script.duration}}h</text>
							</view>
						</view>
						
						<!-- 价格和状态 -->
						<view class="script-bottom">
							<view class="script-price">
								<text>¥{{script.price}}</text>
								<text class="price-unit">/人</text>
							</view>
							<view class="script-rating">
								<text class="rating-stars">⭐</text>
								<text class="rating-score">{{script.rating}}</text>
							</view>
						</view>
						
						<view class="available-sessions" v-if="script.availableSessions > 0">
							<text>今日{{script.availableSessions}}场可约</text>
						</view>
					</view>
				</view>
			</view>
			
			<!-- 加载状态 -->
			<view class="loading-container" v-if="isLoading">
				<text class="loading-text">正在加载...</text>
			</view>
			
			<!-- 上拉加载更多 -->
			<view class="load-more-container" v-if="hasMoreData && !isLoading">
				<view v-if="isLoadingMore">
					<text class="load-more-text">正在加载更多...</text>
				</view>
				<view v-else @tap="loadMoreScripts">
					<text class="load-more-text">点击加载更多</text>
				</view>
			</view>
			
			<!-- 没有更多数据提示 -->
			<view class="load-more-container" v-if="!hasMoreData && displayScriptList.length > 0">
				<text class="load-more-text">已加载全部剧本</text>
			</view>
			
			<!-- 空状态 -->
			<view class="empty-container" v-if="displayScriptList.length === 0 && !isLoading">
				<text class="empty-icon">📚</text>
				<text class="empty-title">暂无符合条件的剧本</text>
				<text class="empty-description">尝试调整筛选条件或重新搜索</text>
				<button class="reset-button" @tap="resetFilters">
					<text>重置筛选条件</text>
				</button>
			</view>
		</view>
	</view>
</template>

<script>
/**
 * 剧本列表页面
 * 功能：搜索、筛选、排序、分页加载剧本列表
 * @author: 剧本杀小程序开发团队
 * @date: 2025-08-23
 */
export default {
	name: 'ScriptsList',
	
	data() {
		return {
			// 搜索相关
			searchKeyword: '',
			searchTimer: null,
			
			// 筛选相关
			activeCategory: 'all',
			sortType: 'default', // default, price, rating, playerCount
			sortOrder: 'desc', // asc, desc
			
			// 列表数据
			scriptList: [],
			displayScriptList: [],
			currentPage: 1,
			pageSize: 10,
			totalCount: 0,
			
			// 状态管理
			isLoading: false,
			isRefreshing: false,
			isLoadingMore: false,
			hasMoreData: true,
			
			// 分类配置
			categoryList: [
				{ key: 'all', name: '全部' },
				{ key: 'mystery', name: '悬疑推理' },
				{ key: 'horror', name: '恐怖惊悚' },
				{ key: 'emotion', name: '情感还原' },
				{ key: 'ancient', name: '古风武侠' },
				{ key: 'modern', name: '现代都市' },
				{ key: 'fantasy', name: '奇幻冒险' },
				{ key: 'comedy', name: '欢乐喜剧' }
			],
			
			// 模拟数据
			mockScriptData: [
				{
					id: 1,
					title: '年轮',
					description: '一个关于时间与记忆的悬疑故事，每个人都有不为人知的秘密...',
					coverImage: 'https://picsum.photos/300/400?random=1',
					category: 'mystery',
					tags: ['悬疑', '推理', '烧脑'],
					playerCount: 6,
					duration: 4,
					price: 88,
					difficulty: '中等',
					rating: 4.5,
					availableSessions: 3,
					isHot: true,
					createTime: '2025-08-20'
				},
				{
					id: 2,
					title: '云使',
					description: '古风情感本，讲述了一段跨越千年的爱恨情仇...',
					coverImage: 'https://picsum.photos/300/400?random=2',
					category: 'ancient',
					tags: ['古风', '情感', '虐心'],
					playerCount: 7,
					duration: 5,
					price: 98,
					difficulty: '简单',
					rating: 4.8,
					availableSessions: 2,
					isHot: false,
					createTime: '2025-08-19'
				},
				{
					id: 3,
					title: '第七个嫌疑人',
					description: '经典推理本，七个嫌疑人，一个真相，你能找到凶手吗？',
					coverImage: 'https://picsum.photos/300/400?random=3',
					category: 'mystery',
					tags: ['现代', '悬疑', '经典'],
					playerCount: 7,
					duration: 4,
					price: 78,
					difficulty: '困难',
					rating: 4.6,
					availableSessions: 4,
					isHot: true,
					createTime: '2025-08-18'
				},
				{
					id: 4,
					title: '镜中人',
					description: '恐怖惊悚本，胆小者慎入，极度烧脑的心理悬疑...',
					coverImage: 'https://picsum.photos/300/400?random=4',
					category: 'horror',
					tags: ['惊悚', '心理', '烧脑'],
					playerCount: 6,
					duration: 3,
					price: 68,
					difficulty: '中等',
					rating: 4.3,
					availableSessions: 1,
					isHot: false,
					createTime: '2025-08-17'
				},
				{
					id: 5,
					title: '桃花债',
					description: '情感还原本，三生三世的纠葛，谁欠了谁的桃花债？',
					coverImage: 'https://picsum.photos/300/400?random=5',
					category: 'emotion',
					tags: ['情感', '还原', '唯美'],
					playerCount: 5,
					duration: 4,
					price: 85,
					difficulty: '简单',
					rating: 4.7,
					availableSessions: 3,
					isHot: false,
					createTime: '2025-08-16'
				},
				{
					id: 6,
					title: '末日生存',
					description: '末日题材，在绝境中求生，考验人性与智慧...',
					coverImage: 'https://picsum.photos/300/400?random=6',
					category: 'fantasy',
					tags: ['科幻', '生存', '策略'],
					playerCount: 8,
					duration: 6,
					price: 108,
					difficulty: '困难',
					rating: 4.4,
					availableSessions: 0,
					isHot: false,
					createTime: '2025-08-15'
				}
			]
		}
	},
	
	computed: {
		/**
		 * 根据筛选条件过滤剧本列表
		 */
		filteredScriptList() {
			let result = [...this.scriptList];
			
			// 分类筛选
			if (this.activeCategory !== 'all') {
				result = result.filter(script => script.category === this.activeCategory);
			}
			
			// 搜索筛选
			if (this.searchKeyword.trim()) {
				const keyword = this.searchKeyword.toLowerCase();
				result = result.filter(script => 
					script.title.toLowerCase().includes(keyword) ||
					script.description.toLowerCase().includes(keyword) ||
					script.tags.some(tag => tag.toLowerCase().includes(keyword))
				);
			}
			
			// 排序
			result = this.sortScriptList(result);
			
			return result;
		}
	},
	
	// 页面生命周期
	onLoad(options) {
		console.log('剧本列表页面加载', options);
		this.initPageData();
	},
	
	onShow() {
		console.log('剧本列表页面显示');
		// 每次显示时刷新数据
		this.refreshScriptList();
	},
	
	onReachBottom() {
		console.log('触发上拉加载');
		this.loadMoreScripts();
	},
	
	onPullDownRefresh() {
		console.log('触发下拉刷新');
		this.refreshScriptList();
	},
	
	methods: {
		/**
		 * 初始化页面数据
		 */
		initPageData() {
			this.loadScriptList();
		},
		
		/**
		 * 加载剧本列表数据
		 * @param {Boolean} isLoadMore - 是否为加载更多
		 */
		async loadScriptList(isLoadMore = false) {
			if (this.isLoading || (isLoadMore && !this.hasMoreData)) {
				return;
			}
			
			try {
				if (isLoadMore) {
					this.isLoadingMore = true;
				} else {
					this.isLoading = true;
					this.currentPage = 1;
				}
				
				// 模拟API请求
				const response = await this.mockApiRequest();
				
				if (response.success) {
					const newScripts = response.data.list;
					
					if (isLoadMore) {
						// 加载更多时追加数据
						this.scriptList = [...this.scriptList, ...newScripts];
					} else {
						// 首次加载或刷新时替换数据
						this.scriptList = newScripts;
					}
					
					this.totalCount = response.data.total;
					this.hasMoreData = this.scriptList.length < this.totalCount;
					
					// 更新显示列表
					this.updateDisplayList();
				}
				
			} catch (error) {
				console.error('加载剧本列表失败:', error);
				uni.showToast({
					title: '加载失败，请重试',
					icon: 'none'
				});
			} finally {
				this.isLoading = false;
				this.isLoadingMore = false;
				this.isRefreshing = false;
				
				// 停止下拉刷新
				uni.stopPullDownRefresh();
			}
		},
		
		/**
		 * 模拟API请求
		 */
		mockApiRequest() {
			return new Promise((resolve) => {
				setTimeout(() => {
					// 模拟分页数据
					const startIndex = (this.currentPage - 1) * this.pageSize;
					const endIndex = startIndex + this.pageSize;
					const list = this.mockScriptData.slice(startIndex, endIndex);
					
					resolve({
						success: true,
						data: {
							list: list,
							total: this.mockScriptData.length,
							currentPage: this.currentPage,
							pageSize: this.pageSize
						}
					});
				}, 800);
			});
		},
		
		/**
		 * 更新显示列表
		 */
		updateDisplayList() {
			this.displayScriptList = this.filteredScriptList;
		},
		
		/**
		 * 刷新剧本列表
		 */
		refreshScriptList() {
			this.isRefreshing = true;
			this.loadScriptList(false);
		},
		
		/**
		 * 加载更多剧本
		 */
		loadMoreScripts() {
			if (this.hasMoreData && !this.isLoadingMore) {
				this.currentPage++;
				this.loadScriptList(true);
			}
		},
		
		/**
		 * 搜索输入处理
		 */
		onSearchInput(event) {
			// 防抖处理
			clearTimeout(this.searchTimer);
			this.searchTimer = setTimeout(() => {
				this.updateDisplayList();
			}, 300);
		},
		
		/**
		 * 搜索确认
		 */
		onSearchConfirm() {
			console.log('搜索关键词:', this.searchKeyword);
			this.updateDisplayList();
		},
		
		/**
		 * 分类变更处理
		 */
		handleCategoryChange(categoryKey) {
			console.log('切换分类:', categoryKey);
			this.activeCategory = categoryKey;
			this.updateDisplayList();
		},
		
		/**
		 * 排序变更处理
		 */
		handleSortChange(sortType) {
			console.log('切换排序:', sortType);
			
			if (this.sortType === sortType) {
				// 同一排序字段，切换排序方向
				this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
			} else {
				// 不同排序字段，设置默认排序方向
				this.sortType = sortType;
				this.sortOrder = 'desc';
			}
			
			this.updateDisplayList();
		},
		
		/**
		 * 剧本列表排序
		 */
		sortScriptList(list) {
			if (this.sortType === 'default') {
				return list;
			}
			
			return list.sort((a, b) => {
				let valueA, valueB;
				
				switch (this.sortType) {
					case 'price':
						valueA = a.price;
						valueB = b.price;
						break;
					case 'rating':
						valueA = a.rating;
						valueB = b.rating;
						break;
					case 'playerCount':
						valueA = a.playerCount;
						valueB = b.playerCount;
						break;
					default:
						return 0;
				}
				
				if (this.sortOrder === 'asc') {
					return valueA - valueB;
				} else {
					return valueB - valueA;
				}
			});
		},
		
		/**
		 * 剧本卡片点击处理
		 */
		handleScriptTap(script) {
			console.log('点击剧本:', script.title);
			uni.navigateTo({
				url: `/pages/script-detail/script-detail?id=${script.id}`
			});
		},
		
		/**
		 * 重置筛选条件
		 */
		resetFilters() {
			this.searchKeyword = '';
			this.activeCategory = 'all';
			this.sortType = 'default';
			this.sortOrder = 'desc';
			this.updateDisplayList();
		}
	}
}
</script>

<style scoped>
/**
 * 剧本列表页面样式
 * 使用rpx响应式单位，支持多设备适配
 */

/* 页面整体布局 */
.scripts-page {
	min-height: 100vh;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding-bottom: 120rpx;
}

/* 搜索栏样式 */
.search-bar {
	position: sticky;
	top: 0;
	z-index: 100;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20rpx);
	padding: 20rpx 30rpx;
	border-bottom: 2rpx solid #f0f0f0;
}

.search-input {
	width: 100%;
	height: 80rpx;
	background: #f8f9fa;
	border-radius: 40rpx;
	padding: 0 40rpx;
	font-size: 28rpx;
	color: #333;
	border: 2rpx solid transparent;
	transition: all 0.3s ease;
}

.search-input:focus {
	background: #fff;
	border-color: #667eea;
	box-shadow: 0 0 20rpx rgba(102, 126, 234, 0.2);
}

/* 分类标签栏 */
.category-tabs {
	background: #fff;
	padding: 20rpx 0;
	border-bottom: 2rpx solid #f0f0f0;
}

.category-scroll {
	white-space: nowrap;
	padding: 0 30rpx;
}

.category-item {
	display: inline-block;
	padding: 12rpx 24rpx;
	margin-right: 16rpx;
	background: #f8f9fa;
	color: #666;
	border-radius: 40rpx;
	font-size: 26rpx;
	transition: all 0.3s ease;
	border: 2rpx solid transparent;
}

.category-item.active {
	background: linear-gradient(135deg, #667eea, #764ba2);
	color: #fff;
	transform: scale(1.05);
	box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.3);
}

/* 排序工具栏 */
.sort-toolbar {
	background: #fff;
	padding: 20rpx 30rpx;
	display: flex;
	align-items: center;
	justify-content: space-between;
	border-bottom: 2rpx solid #f0f0f0;
}

.sort-options {
	display: flex;
	align-items: center;
}

.sort-item {
	padding: 12rpx 20rpx;
	margin-right: 16rpx;
	background: #f8f9fa;
	color: #666;
	border-radius: 20rpx;
	font-size: 24rpx;
	transition: all 0.3s ease;
	position: relative;
}

.sort-item.active {
	background: #667eea;
	color: #fff;
}

.sort-item::after {
	content: '';
	position: absolute;
	right: 6rpx;
	top: 50%;
	transform: translateY(-50%);
	width: 0;
	height: 0;
	border-left: 6rpx solid transparent;
	border-right: 6rpx solid transparent;
	border-top: 8rpx solid currentColor;
}

.sort-item.active.desc::after {
	border-top: none;
	border-bottom: 8rpx solid currentColor;
}

.result-count {
	font-size: 24rpx;
	color: #999;
}

/* 剧本列表网格布局 */
.scripts-grid {
	padding: 20rpx 30rpx;
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 20rpx;
}

.script-card {
	background: #fff;
	border-radius: 24rpx;
	overflow: hidden;
	box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
	transition: all 0.3s ease;
	position: relative;
}

.script-card:hover {
	transform: translateY(-8rpx);
	box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.15);
}

.script-card:active {
	transform: translateY(-4rpx);
}

/* 剧本封面 */
.script-cover {
	position: relative;
	height: 240rpx;
	overflow: hidden;
}

.cover-image {
	width: 100%;
	height: 100%;
	object-fit: cover;
	transition: transform 0.3s ease;
}

.script-card:hover .cover-image {
	transform: scale(1.05);
}

.cover-overlay {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: linear-gradient(
		180deg,
		rgba(0, 0, 0, 0) 0%,
		rgba(0, 0, 0, 0.3) 70%,
		rgba(0, 0, 0, 0.6) 100%
	);
}

.hot-badge {
	position: absolute;
	top: 16rpx;
	left: 16rpx;
	background: linear-gradient(135deg, #ff6b6b, #ff8e53);
	color: #fff;
	padding: 8rpx 16rpx;
	border-radius: 20rpx;
	font-size: 20rpx;
	font-weight: bold;
	box-shadow: 0 4rpx 12rpx rgba(255, 107, 107, 0.4);
}

.difficulty-badge {
	position: absolute;
	top: 16rpx;
	right: 16rpx;
	padding: 8rpx 16rpx;
	border-radius: 20rpx;
	font-size: 20rpx;
	font-weight: bold;
	color: #fff;
}

.difficulty-badge.easy {
	background: linear-gradient(135deg, #51cf66, #40c057);
}

.difficulty-badge.medium {
	background: linear-gradient(135deg, #ffd43b, #fab005);
}

.difficulty-badge.hard {
	background: linear-gradient(135deg, #ff6b6b, #fa5252);
}

/* 剧本信息 */
.script-info {
	padding: 24rpx;
}

.script-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 12rpx;
	line-height: 1.2;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 1;
	line-clamp: 1;
	overflow: hidden;
}

.script-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 8rpx;
	margin-bottom: 16rpx;
}

.tag-item {
	padding: 6rpx 12rpx;
	background: #f8f9fa;
	color: #666;
	border-radius: 12rpx;
	font-size: 20rpx;
}

.script-description {
	font-size: 24rpx;
	color: #666;
	line-height: 1.4;
	margin-bottom: 16rpx;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 2;
	line-clamp: 2;
	overflow: hidden;
}

.script-meta {
	display: flex;
	align-items: center;
	justify-content: space-between;
	font-size: 22rpx;
	color: #999;
	margin-bottom: 16rpx;
}

.meta-item {
	display: flex;
	align-items: center;
	gap: 4rpx;
}

.script-bottom {
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.script-price {
	font-size: 28rpx;
	font-weight: bold;
	color: #ff6b6b;
}

.price-unit {
	font-size: 20rpx;
	color: #999;
}

.script-rating {
	display: flex;
	align-items: center;
	gap: 8rpx;
}

.rating-stars {
	color: #ffd43b;
	font-size: 24rpx;
}

.rating-score {
	font-size: 22rpx;
	color: #666;
}

.available-sessions {
	font-size: 20rpx;
	color: #667eea;
	padding: 4rpx 8rpx;
	background: rgba(102, 126, 234, 0.1);
	border-radius: 8rpx;
}

/* 加载状态 */
.loading-container {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 60rpx 0;
}

.loading-text {
	font-size: 28rpx;
	color: #666;
	margin-left: 20rpx;
}

.load-more-container {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 40rpx 0;
	background: rgba(255, 255, 255, 0.8);
	margin: 20rpx 30rpx;
	border-radius: 20rpx;
}

.load-more-text {
	font-size: 26rpx;
	color: #999;
}

/* 空状态 */
.empty-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 120rpx 60rpx;
	text-align: center;
}

.empty-icon {
	font-size: 120rpx;
	color: #ddd;
	margin-bottom: 24rpx;
}

.empty-title {
	font-size: 32rpx;
	color: #999;
	margin-bottom: 16rpx;
}

.empty-description {
	font-size: 24rpx;
	color: #ccc;
	line-height: 1.5;
}

.reset-button {
	margin-top: 40rpx;
	padding: 20rpx 40rpx;
	background: linear-gradient(135deg, #667eea, #764ba2);
	color: #fff;
	border-radius: 40rpx;
	font-size: 28rpx;
	border: none;
}

/* 骨架屏效果 */
.skeleton-card {
	background: #fff;
	border-radius: 24rpx;
	overflow: hidden;
	box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
}

.skeleton-cover {
	height: 240rpx;
	background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
	background-size: 200% 100%;
	animation: skeleton-loading 1.5s infinite;
}

.skeleton-info {
	padding: 24rpx;
}

.skeleton-line {
	height: 28rpx;
	background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
	background-size: 200% 100%;
	animation: skeleton-loading 1.5s infinite;
	border-radius: 4rpx;
	margin-bottom: 16rpx;
}

.skeleton-line.short {
	width: 60%;
}

.skeleton-line.medium {
	width: 80%;
}

@keyframes skeleton-loading {
	0% {
		background-position: 200% 0;
	}
	100% {
		background-position: -200% 0;
	}
}

/* 响应式适配 */
@media (max-width: 375px) {
	.scripts-grid {
		grid-template-columns: 1fr;
		gap: 16rpx;
		padding: 16rpx 20rpx;
	}
	
	.script-card {
		border-radius: 20rpx;
	}
	
	.script-cover {
		height: 200rpx;
	}
	
	.script-info {
		padding: 20rpx;
	}
}

@media (min-width: 768px) {
	.scripts-grid {
		grid-template-columns: repeat(3, 1fr);
		max-width: 1200rpx;
		margin: 0 auto;
	}
}
</style>
