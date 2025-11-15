<template>
	<view class="page">
		<!-- 剧本封面 -->
		<view class="cover-section">
			<image :src="script.cover" class="cover-image"></image>
			<view class="cover-overlay">
				<view class="script-info">
					<text class="script-name">{{script.name}}</text>
					<view class="script-tags">
						<text class="tag" v-for="tag in script.tags" :key="tag">{{tag}}</text>
					</view>
					<view class="script-rating">
						<text class="rating-text">{{script.rating}}</text>
						<text class="rating-stars">⭐⭐⭐⭐⭐</text>
						<text class="rating-count">({{script.reviewCount}}条评价)</text>
					</view>
				</view>
				<view class="price-info">
					<text class="price-label">价格</text>
					<view class="price-value">
						<text class="price-symbol">¥</text>
						<text class="price-number">{{script.price}}</text>
						<text class="price-unit">/人</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 基本信息 -->
		<view class="info-section">
			<view class="info-grid">
				<view class="info-item">
					<text class="info-icon">👥</text>
					<text class="info-label">游戏人数</text>
					<text class="info-value">{{script.playerCount}}人</text>
				</view>
				<view class="info-item">
					<text class="info-icon">⏱</text>
					<text class="info-label">游戏时长</text>
					<text class="info-value">{{script.duration}}小时</text>
				</view>
				<view class="info-item">
					<text class="info-icon">⭐</text>
					<text class="info-label">难度等级</text>
					<text class="info-value">{{script.difficulty}}</text>
				</view>
				<view class="info-item">
					<text class="info-icon">🎭</text>
					<text class="info-label">剧本类型</text>
					<text class="info-value">{{script.type}}</text>
				</view>
			</view>
		</view>

		<!-- 剧本介绍 -->
		<view class="desc-section">
			<view class="section-title">
				<text class="title-text">📖 剧本介绍</text>
			</view>
			<view class="desc-content">
				<text class="desc-text">{{script.description}}</text>
			</view>
		</view>

		<!-- 角色介绍 -->
		<view class="roles-section" v-if="script.roles && script.roles.length > 0">
			<view class="section-title">
				<text class="title-text">🎭 角色介绍</text>
			</view>
			<view class="roles-list">
				<view class="role-item" v-for="role in script.roles" :key="role.id">
					<image :src="role.avatar" class="role-avatar"></image>
					<view class="role-info">
						<text class="role-name">{{role.name}}</text>
						<text class="role-desc">{{role.description}}</text>
						<view class="role-tags">
							<text class="role-tag" v-for="tag in role.tags" :key="tag">{{tag}}</text>
						</view>
					</view>
				</view>
			</view>
		</view>

		<!-- 今日场次 -->
		<view class="sessions-section">
			<view class="section-title">
				<text class="title-text">📅 今日场次</text>
				<text class="more-sessions" @tap="goToReservation">查看更多</text>
			</view>
			<view class="sessions-list">
				<view class="session-item" 
					v-for="session in todaySessions" 
					:key="session.id"
					:class="{'disabled': session.currentPlayers >= session.maxPlayers}"
					@tap="reserveSession(session)">
					<view class="session-time">
						<text class="time-text">{{session.startTime}}</text>
						<text class="time-label">{{session.period}}</text>
					</view>
					<view class="session-info">
						<text class="session-players">{{session.currentPlayers}}/{{session.maxPlayers}}人</text>
						<text class="session-status" v-if="session.currentPlayers >= session.maxPlayers">已满员</text>
						<text class="session-status available" v-else>可预约</text>
					</view>
					<view class="session-price">
						<text>¥{{session.price}}</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 用户评价 -->
		<view class="reviews-section">
			<view class="section-title">
				<text class="title-text">💬 用户评价</text>
				<text class="review-count">({{script.reviewCount}}条)</text>
			</view>
			<view class="reviews-list">
				<view class="review-item" v-for="review in reviews" :key="review.id">
					<view class="review-header">
						<image :src="review.userAvatar" class="user-avatar"></image>
						<view class="user-info">
							<text class="user-name">{{review.userName}}</text>
							<view class="review-rating">
								<text class="stars">{{getStars(review.rating)}}</text>
								<text class="review-date">{{review.date}}</text>
							</view>
						</view>
					</view>
					<text class="review-content">{{review.content}}</text>
				</view>
			</view>
		</view>

		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="action-buttons">
				<view class="btn-secondary" @tap="addToFavorite">
					<text class="btn-icon">❤️</text>
					<text>收藏</text>
				</view>
				<view class="btn-secondary" @tap="shareScript">
					<text class="btn-icon">📤</text>
					<text>分享</text>
				</view>
				<view class="btn-primary" @tap="goToReservation">
					<text>立即预约</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				scriptId: null,
				script: {
					id: 1,
					name: '年轮',
					cover: '/static/script1.jpg',
					description: '一个关于时间与记忆的悬疑故事。在这个充满谜团的世界里，每个人都有不为人知的秘密，时间的齿轮缓缓转动，过去与现在交织在一起。你需要通过线索推理，揭开隐藏在时间深处的真相。这不仅是一场智慧的较量，更是一次对人性的深度探索。',
					tags: ['悬疑', '推理', '烧脑'],
					playerCount: 6,
					duration: 4,
					price: 88,
					difficulty: '中等',
					type: '悬疑推理',
					rating: 4.5,
					reviewCount: 128,
					roles: [
						{
							id: 1,
							name: '林昭',
							avatar: '/static/role1.jpg',
							description: '神秘的古董店老板，似乎知道很多关于过去的秘密',
							tags: ['神秘', '智慧']
						},
						{
							id: 2,
							name: '苏婉',
							avatar: '/static/role2.jpg',
							description: '年轻的记者，正在调查一起陈年旧案',
							tags: ['敏锐', '勇敢']
						},
						{
							id: 3,
							name: '陈教授',
							avatar: '/static/role3.jpg',
							description: '退休的历史教授，对这个案子有着特殊的关注',
							tags: ['博学', '严谨']
						}
					]
				},
				todaySessions: [
					{
						id: 1,
						startTime: '14:00',
						period: '下午场',
						currentPlayers: 4,
						maxPlayers: 6,
						price: 88
					},
					{
						id: 2,
						startTime: '19:00',
						period: '晚场',
						currentPlayers: 6,
						maxPlayers: 6,
						price: 88
					},
					{
						id: 3,
						startTime: '20:30',
						period: '夜场',
						currentPlayers: 2,
						maxPlayers: 6,
						price: 88
					}
				],
				reviews: [
					{
						id: 1,
						userName: '推理达人',
						userAvatar: '/static/avatar1.jpg',
						rating: 5,
						date: '2023-12-10',
						content: '非常精彩的剧本！逻辑严密，线索设计巧妙，每个角色都有自己的故事线，强烈推荐！'
					},
					{
						id: 2,
						userName: '剧本杀新手',
						userAvatar: '/static/avatar2.jpg',
						rating: 4,
						date: '2023-12-08',
						content: '作为新手第一次玩这个剧本，DM引导得很好，虽然有些烧脑但很有成就感。'
					}
				]
			}
		},
		onLoad(options) {
			if (options.id) {
				this.scriptId = options.id;
				this.loadScriptDetail();
			}
		},
		methods: {
			loadScriptDetail() {
				// 这里可以调用后端接口获取剧本详情
				console.log('加载剧本详情', this.scriptId);
			},
			getStars(rating) {
				return '⭐'.repeat(rating);
			},
			reserveSession(session) {
				if (session.currentPlayers >= session.maxPlayers) {
					uni.showToast({
						title: '该场次已满',
						icon: 'none'
					});
					return;
				}
				uni.navigateTo({
					url: `/pages/reservation/reservation?scriptId=${this.script.id}&sessionId=${session.id}`
				});
			},
			goToReservation() {
				uni.navigateTo({
					url: `/pages/reservation/reservation?scriptId=${this.script.id}`
				});
			},
			addToFavorite() {
				uni.showToast({
					title: '已添加到收藏',
					icon: 'success'
				});
			},
			shareScript() {
				uni.share({
					provider: 'weixin',
					type: 0,
					title: this.script.name,
					summary: this.script.description,
					imageUrl: this.script.cover
				});
			}
		}
	}
</script>

<style scoped>
	.page {
		background-color: #f8f9fa;
		padding-bottom: 120rpx;
	}

	/* 封面区域 */
	.cover-section {
		position: relative;
		height: 500rpx;
	}

	.cover-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.cover-overlay {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
		padding: 80rpx 30rpx 30rpx;
		color: white;
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
	}

	.script-info {
		flex: 1;
	}

	.script-name {
		font-size: 48rpx;
		font-weight: bold;
		display: block;
		margin-bottom: 20rpx;
	}

	.script-tags {
		margin-bottom: 15rpx;
	}

	.tag {
		display: inline-block;
		background: rgba(255, 255, 255, 0.2);
		padding: 8rpx 16rpx;
		border-radius: 16rpx;
		font-size: 22rpx;
		margin-right: 15rpx;
	}

	.script-rating {
		display: flex;
		align-items: center;
	}

	.rating-text {
		font-size: 32rpx;
		font-weight: bold;
		margin-right: 15rpx;
	}

	.rating-stars {
		font-size: 20rpx;
		margin-right: 15rpx;
	}

	.rating-count {
		font-size: 24rpx;
		opacity: 0.8;
	}

	.price-info {
		text-align: center;
		min-width: 120rpx;
	}

	.price-label {
		font-size: 24rpx;
		opacity: 0.8;
		display: block;
		margin-bottom: 10rpx;
	}

	.price-value {
		display: flex;
		align-items: baseline;
		justify-content: center;
	}

	.price-symbol {
		font-size: 24rpx;
	}

	.price-number {
		font-size: 42rpx;
		font-weight: bold;
	}

	.price-unit {
		font-size: 24rpx;
	}

	/* 基本信息 */
	.info-section {
		background: white;
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.info-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 30rpx;
	}

	.info-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
	}

	.info-icon {
		font-size: 40rpx;
		margin-bottom: 15rpx;
	}

	.info-label {
		font-size: 24rpx;
		color: #999;
		margin-bottom: 10rpx;
	}

	.info-value {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
	}

	/* 通用区域样式 */
	.desc-section, .roles-section, .sessions-section, .reviews-section {
		background: white;
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.section-title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30rpx;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.title-text {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}

	.more-sessions, .review-count {
		font-size: 26rpx;
		color: #667eea;
	}

	/* 剧本介绍 */
	.desc-content {
		line-height: 1.8;
	}

	.desc-text {
		font-size: 28rpx;
		color: #666;
	}

	/* 角色介绍 */
	.roles-list {
		gap: 30rpx;
	}

	.role-item {
		display: flex;
		margin-bottom: 30rpx;
		padding-bottom: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.role-item:last-child {
		border-bottom: none;
		margin-bottom: 0;
		padding-bottom: 0;
	}

	.role-avatar {
		width: 120rpx;
		height: 120rpx;
		border-radius: 60rpx;
		margin-right: 30rpx;
		object-fit: cover;
	}

	.role-info {
		flex: 1;
	}

	.role-name {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 15rpx;
	}

	.role-desc {
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
		display: block;
		margin-bottom: 20rpx;
	}

	.role-tags {
		display: flex;
	}

	.role-tag {
		background: #f0f0f0;
		color: #666;
		font-size: 22rpx;
		padding: 6rpx 12rpx;
		border-radius: 12rpx;
		margin-right: 15rpx;
	}

	/* 今日场次 */
	.sessions-list {
		gap: 20rpx;
	}

	.session-item {
		display: flex;
		align-items: center;
		padding: 25rpx;
		background: #f8f9fa;
		border-radius: 15rpx;
		margin-bottom: 20rpx;
		transition: all 0.3s;
	}

	.session-item:last-child {
		margin-bottom: 0;
	}

	.session-item.disabled {
		opacity: 0.6;
	}

	.session-time {
		text-align: center;
		margin-right: 30rpx;
		min-width: 100rpx;
	}

	.time-text {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		display: block;
	}

	.time-label {
		font-size: 22rpx;
		color: #999;
	}

	.session-info {
		flex: 1;
	}

	.session-players {
		font-size: 28rpx;
		color: #333;
		display: block;
		margin-bottom: 8rpx;
	}

	.session-status {
		font-size: 24rpx;
		color: #ff6b6b;
	}

	.session-status.available {
		color: #28a745;
	}

	.session-price {
		font-size: 28rpx;
		font-weight: bold;
		color: #667eea;
	}

	/* 用户评价 */
	.reviews-list {
		gap: 30rpx;
	}

	.review-item {
		margin-bottom: 30rpx;
		padding-bottom: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.review-item:last-child {
		border-bottom: none;
		margin-bottom: 0;
		padding-bottom: 0;
	}

	.review-header {
		display: flex;
		margin-bottom: 20rpx;
	}

	.user-avatar {
		width: 80rpx;
		height: 80rpx;
		border-radius: 40rpx;
		margin-right: 20rpx;
		object-fit: cover;
	}

	.user-info {
		flex: 1;
	}

	.user-name {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 10rpx;
	}

	.review-rating {
		display: flex;
		align-items: center;
	}

	.stars {
		font-size: 20rpx;
		margin-right: 15rpx;
	}

	.review-date {
		font-size: 24rpx;
		color: #999;
	}

	.review-content {
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
	}

	/* 底部操作栏 */
	.bottom-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background: white;
		padding: 20rpx 30rpx;
		border-top: 1rpx solid #f0f0f0;
		box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.action-buttons {
		display: flex;
		gap: 20rpx;
	}

	.btn-secondary, .btn-primary {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 25rpx;
		border-radius: 25rpx;
		font-size: 28rpx;
		transition: all 0.3s;
	}

	.btn-secondary {
		background: #f8f9fa;
		color: #666;
		border: 1rpx solid #dee2e6;
		min-width: 120rpx;
	}

	.btn-primary {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		flex: 1;
	}

	.btn-icon {
		margin-right: 8rpx;
		font-size: 24rpx;
	}
</style>
