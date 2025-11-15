<template>
	<view class="page">
		<!-- 自定义导航栏 -->
		<view class="custom-navbar">
			<view class="navbar-content">
				<text class="navbar-title">剧本杀小程序</text>
				<view class="navbar-icons">
					<text class="navbar-icon" @tap="showSearch">🔍</text>
					<text class="navbar-icon" @tap="showNotifications">🔔</text>
				</view>
			</view>
		</view>

		<!-- 头部轮播图 -->
		<view class="header-section">
			<swiper class="banner" indicator-dots="true" autoplay="true" interval="3000" duration="500">
				<swiper-item v-for="(banner, index) in bannerList" :key="index">
					<view class="banner-item" :style="'background: ' + banner.background">
						<view class="banner-overlay">
							<text class="banner-title">{{banner.title}}</text>
							<text class="banner-subtitle">{{banner.subtitle}}</text>
						</view>
					</view>
				</swiper-item>
			</swiper>
		</view>

		<!-- 功能入口 -->
		<view class="function-section">
			<view class="function-grid">
				<view class="function-item" @tap="goToScripts">
					<view class="function-icon">
						<text class="iconfont">📚</text>
					</view>
					<text class="function-text">选择剧本</text>
				</view>
				<view class="function-item" @tap="goToReservation">
					<view class="function-icon">
						<text class="iconfont">📅</text>
					</view>
					<text class="function-text">预约场次</text>
				</view>
				<view class="function-item" @tap="goToMyOrders">
					<view class="function-icon">
						<text class="iconfont">📋</text>
					</view>
					<text class="function-text">我的预约</text>
				</view>
				<view class="function-item" @tap="goToProfile">
					<view class="function-icon">
						<text class="iconfont">👤</text>
					</view>
					<text class="function-text">个人中心</text>
				</view>
			</view>
		</view>

		<!-- 热门剧本推荐 -->
		<view class="recommend-section">
			<view class="section-header">
				<text class="section-title">🔥 热门推荐</text>
				<text class="section-more" @tap="goToScripts">查看更多 ></text>
			</view>
			<scroll-view scroll-x="true" class="recommend-scroll">
				<view class="recommend-list">
					<view class="recommend-item" v-for="(script, index) in hotScripts" :key="index" @tap="viewScriptDetail(script)">
						<image :src="script.cover" class="script-cover"></image>
						<view class="script-info">
							<text class="script-name">{{script.name}}</text>
							<view class="script-tags">
								<text class="script-tag" v-for="tag in script.tags" :key="tag">{{tag}}</text>
							</view>
							<view class="script-meta">
								<text class="script-players">{{script.playerCount}}人本</text>
								<text class="script-duration">{{script.duration}}小时</text>
							</view>
							<text class="script-price">¥{{script.price}}/人</text>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>

		<!-- 今日场次 -->
		<view class="today-section">
			<view class="section-header">
				<text class="section-title">📍 今日场次</text>
				<text class="section-more" @tap="goToReservation">查看更多 ></text>
			</view>
			<view class="today-list">
				<view class="today-item" v-for="(session, index) in todaySessions" :key="index" @tap="reserveSession(session)">
					<view class="session-time">
						<text class="time-hour">{{session.startTime}}</text>
						<text class="time-period">{{session.period}}</text>
					</view>
					<view class="session-info">
						<text class="session-script">{{session.scriptName}}</text>
						<text class="session-players">{{session.currentPlayers}}/{{session.maxPlayers}}人</text>
						<view class="session-tags">
							<text class="session-tag difficulty">{{session.difficulty}}</text>
							<text class="session-tag type">{{session.type}}</text>
						</view>
					</view>
					<view class="session-action">
						<text class="session-price">¥{{session.price}}</text>
						<view class="reserve-btn" :class="{'disabled': session.currentPlayers >= session.maxPlayers}">
							<text>{{session.currentPlayers >= session.maxPlayers ? '已满' : '预约'}}</text>
						</view>
					</view>
				</view>
			</view>
		</view>

		<!-- 店铺信息 -->
		<view class="store-section">
			<view class="section-header">
				<text class="section-title">🏪 店铺信息</text>
			</view>
			<view class="store-info">
				<view class="store-item">
					<text class="store-label">营业时间</text>
					<text class="store-value">10:00 - 22:00</text>
				</view>
				<view class="store-item">
					<text class="store-label">联系电话</text>
					<text class="store-value" @tap="makeCall">400-123-4567</text>
				</view>
				<view class="store-item">
					<text class="store-label">店铺地址</text>
					<text class="store-value" @tap="openLocation">北京市朝阳区xxx街道xxx号</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				bannerList: [
					{
						title: '沉浸式剧本杀体验',
						subtitle: '精彩剧情等你来探索',
						background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
					},
					{
						title: '多人推理对战',
						subtitle: '考验智慧与逻辑的时刻',
						background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
					},
					{
						title: '专业DM主持',
						subtitle: '带你进入剧情世界',
						background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
					}
				],
				hotScripts: [
					{
						id: 1,
						name: '年轮',
						cover: 'https://picsum.photos/200/300?random=1',
						tags: ['悬疑', '推理'],
						playerCount: 6,
						duration: 4,
						price: 88,
						difficulty: '中等'
					},
					{
						id: 2,
						name: '云使',
						cover: 'https://picsum.photos/200/300?random=2',
						tags: ['古风', '情感'],
						playerCount: 7,
						duration: 5,
						price: 98,
						difficulty: '简单'
					},
					{
						id: 3,
						name: '第七个嫌疑人',
						cover: 'https://picsum.photos/200/300?random=3',
						tags: ['现代', '悬疑'],
						playerCount: 7,
						duration: 4,
						price: 78,
						difficulty: '困难'
					},
					{
						id: 4,
						name: '镜中人',
						cover: 'https://picsum.photos/200/300?random=4',
						tags: ['惊悚', '推理'],
						playerCount: 6,
						duration: 3,
						price: 68,
						difficulty: '中等'
					}
				],
				todaySessions: [
					{
						id: 1,
						startTime: '14:00',
						period: '下午场',
						scriptName: '年轮',
						currentPlayers: 4,
						maxPlayers: 6,
						price: 88,
						difficulty: '中等',
						type: '悬疑'
					},
					{
						id: 2,
						startTime: '19:00',
						period: '晚场',
						scriptName: '云使',
						currentPlayers: 6,
						maxPlayers: 7,
						price: 98,
						difficulty: '简单',
						type: '古风'
					},
					{
						id: 3,
						startTime: '20:30',
						period: '夜场',
						scriptName: '第七个嫌疑人',
						currentPlayers: 3,
						maxPlayers: 7,
						price: 78,
						difficulty: '困难',
						type: '悬疑'
					}
				]
			}
		},
		onLoad() {
			this.loadData();
		},
		methods: {
			loadData() {
				// 这里可以调用后端接口获取数据
				console.log('加载数据');
			},
			goToScripts() {
				uni.navigateTo({
					url: '/pages/scripts/scripts'
				});
			},
			goToReservation() {
				uni.navigateTo({
					url: '/pages/reservation/reservation'
				});
			},
			goToMyOrders() {
				uni.navigateTo({
					url: '/pages/orders/orders'
				});
			},
			goToProfile() {
				uni.navigateTo({
					url: '/pages/profile/profile'
				});
			},
			viewScriptDetail(script) {
				uni.navigateTo({
					url: `/pages/script-detail/script-detail?id=${script.id}`
				});
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
					url: `/pages/reservation/reservation?sessionId=${session.id}`
				});
			},
			makeCall() {
				uni.makePhoneCall({
					phoneNumber: '400-123-4567'
				});
			},
			openLocation() {
				uni.openLocation({
					latitude: 39.908823,
					longitude: 116.397470,
					name: '剧本杀店铺',
					address: '北京市朝阳区xxx街道xxx号'
				});
			},
			showSearch() {
				uni.showToast({
					title: '搜索功能开发中',
					icon: 'none'
				});
			},
			showNotifications() {
				uni.showToast({
					title: '暂无新消息',
					icon: 'none'
				});
			}
		}
	}
</script>

<style scoped>
	.page {
		background-color: #f8f9fa;
		min-height: 100vh;
		padding-top: 100rpx; /* 给自定义导航栏留空间 */
	}

	/* 自定义导航栏 */
	.custom-navbar {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 1000;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		padding-top: var(--status-bar-height, 0);
	}

	.navbar-content {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20rpx 30rpx;
		height: 80rpx;
	}

	.navbar-title {
		color: white;
		font-size: 36rpx;
		font-weight: bold;
	}

	.navbar-icons {
		display: flex;
		gap: 30rpx;
	}

	.navbar-icon {
		color: white;
		font-size: 36rpx;
		width: 60rpx;
		height: 60rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	/* 头部轮播图 */
	.header-section {
		position: relative;
	}

	.banner {
		height: 400rpx;
	}

	.banner-item {
		width: 100%;
		height: 100%;
		position: relative;
	}

	.banner-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.banner-overlay {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
		padding: 60rpx 40rpx 40rpx;
		color: white;
	}

	.banner-title {
		font-size: 48rpx;
		font-weight: bold;
		display: block;
		margin-bottom: 10rpx;
	}

	.banner-subtitle {
		font-size: 28rpx;
		opacity: 0.9;
	}

	/* 功能入口 */
	.function-section {
		background: white;
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 40rpx 20rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.function-grid {
		display: flex;
		justify-content: space-around;
	}

	.function-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		flex: 1;
	}

	.function-icon {
		width: 100rpx;
		height: 100rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 20rpx;
		font-size: 40rpx;
	}

	.function-text {
		font-size: 26rpx;
		color: #333;
	}

	/* 区域标题 */
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0 30rpx;
		margin-bottom: 20rpx;
	}

	.section-title {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
	}

	.section-more {
		font-size: 26rpx;
		color: #999;
	}

	/* 热门推荐 */
	.recommend-section {
		margin: 40rpx 0;
	}

	.recommend-scroll {
		white-space: nowrap;
	}

	.recommend-list {
		display: flex;
		padding: 0 20rpx;
	}

	.recommend-item {
		display: inline-block;
		width: 280rpx;
		background: white;
		border-radius: 20rpx;
		margin-right: 20rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.script-cover {
		width: 100%;
		height: 200rpx;
		object-fit: cover;
	}

	.script-info {
		padding: 20rpx;
	}

	.script-name {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 15rpx;
	}

	.script-tags {
		margin-bottom: 15rpx;
	}

	.script-tag {
		display: inline-block;
		background: #f0f0f0;
		color: #666;
		font-size: 22rpx;
		padding: 4rpx 12rpx;
		border-radius: 12rpx;
		margin-right: 10rpx;
	}

	.script-meta {
		display: flex;
		justify-content: space-between;
		font-size: 24rpx;
		color: #999;
		margin-bottom: 15rpx;
	}

	.script-price {
		font-size: 28rpx;
		color: #ff6b6b;
		font-weight: bold;
	}

	/* 今日场次 */
	.today-section {
		margin: 40rpx 20rpx;
	}

	.today-list {
		background: white;
		border-radius: 20rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.today-item {
		display: flex;
		padding: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
		align-items: center;
	}

	.today-item:last-child {
		border-bottom: none;
	}

	.session-time {
		margin-right: 30rpx;
		text-align: center;
		min-width: 120rpx;
	}

	.time-hour {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		display: block;
	}

	.time-period {
		font-size: 22rpx;
		color: #999;
	}

	.session-info {
		flex: 1;
	}

	.session-script {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 10rpx;
	}

	.session-players {
		font-size: 26rpx;
		color: #666;
		display: block;
		margin-bottom: 15rpx;
	}

	.session-tags {
		display: flex;
	}

	.session-tag {
		font-size: 22rpx;
		padding: 4rpx 12rpx;
		border-radius: 12rpx;
		margin-right: 10rpx;
	}

	.session-tag.difficulty {
		background: #e3f2fd;
		color: #1976d2;
	}

	.session-tag.type {
		background: #f3e5f5;
		color: #7b1fa2;
	}

	.session-action {
		text-align: center;
		min-width: 120rpx;
	}

	.session-price {
		font-size: 28rpx;
		color: #ff6b6b;
		font-weight: bold;
		display: block;
		margin-bottom: 15rpx;
	}

	.reserve-btn {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		padding: 12rpx 24rpx;
		border-radius: 20rpx;
		font-size: 26rpx;
	}

	.reserve-btn.disabled {
		background: #ccc;
	}

	/* 店铺信息 */
	.store-section {
		margin: 40rpx 20rpx;
		background: white;
		border-radius: 20rpx;
		padding: 40rpx 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.store-info {
		margin-top: 20rpx;
	}

	.store-item {
		display: flex;
		justify-content: space-between;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.store-item:last-child {
		border-bottom: none;
	}

	.store-label {
		font-size: 28rpx;
		color: #666;
	}

	.store-value {
		font-size: 28rpx;
		color: #333;
	}
</style>
