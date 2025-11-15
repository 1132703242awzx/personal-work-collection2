<template>
	<view class="page">
		<!-- 用户信息卡片 -->
		<view class="user-card">
			<view class="user-avatar" @tap="chooseAvatar">
				<image :src="userInfo.avatar" class="avatar-img" v-if="userInfo.avatar"></image>
				<text class="avatar-placeholder" v-else>👤</text>
			</view>
			<view class="user-info">
				<text class="user-name" v-if="userInfo.nickName">{{userInfo.nickName}}</text>
				<text class="user-name guest" v-else @tap="login">点击登录</text>
				<text class="user-phone" v-if="userInfo.phone">{{userInfo.phone}}</text>
				<view class="user-stats">
					<view class="stat-item">
						<text class="stat-number">{{userStats.totalGames}}</text>
						<text class="stat-label">已玩剧本</text>
					</view>
					<view class="stat-item">
						<text class="stat-number">{{userStats.totalHours}}</text>
						<text class="stat-label">游戏时长</text>
					</view>
					<view class="stat-item">
						<text class="stat-number">{{userStats.favoriteCount}}</text>
						<text class="stat-label">收藏剧本</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 会员卡片 -->
		<view class="vip-card" v-if="userInfo.isVip">
			<view class="vip-header">
				<text class="vip-title">👑 VIP会员</text>
				<text class="vip-expire">有效期至：{{userInfo.vipExpire}}</text>
			</view>
			<view class="vip-benefits">
				<text class="benefit-item">🎯 优先预约</text>
				<text class="benefit-item">💰 专享折扣</text>
				<text class="benefit-item">🎁 生日福利</text>
			</view>
		</view>

		<!-- 功能菜单 -->
		<view class="menu-section">
			<view class="menu-group">
				<view class="menu-item" @tap="goToOrders">
					<view class="menu-icon">📋</view>
					<text class="menu-title">我的预约</text>
					<view class="menu-badge" v-if="pendingOrderCount > 0">
						<text>{{pendingOrderCount}}</text>
					</view>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToFavorites">
					<view class="menu-icon">❤️</view>
					<text class="menu-title">收藏剧本</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToReviews">
					<view class="menu-icon">⭐</view>
					<text class="menu-title">我的评价</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToCoupons">
					<view class="menu-icon">🎫</view>
					<text class="menu-title">优惠券</text>
					<view class="menu-badge" v-if="availableCoupons > 0">
						<text>{{availableCoupons}}</text>
					</view>
					<text class="menu-arrow">></text>
				</view>
			</view>

			<view class="menu-group">
				<view class="menu-item" @tap="goToPoints">
					<view class="menu-icon">💎</view>
					<text class="menu-title">积分商城</text>
					<text class="menu-subtitle">{{userInfo.points}}积分</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToInvite">
					<view class="menu-icon">🎯</view>
					<text class="menu-title">邀请好友</text>
					<text class="menu-subtitle">赚取积分</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="becomeVip">
					<view class="menu-icon">👑</view>
					<text class="menu-title">开通会员</text>
					<text class="menu-subtitle">享受专属特权</text>
					<text class="menu-arrow">></text>
				</view>
			</view>

			<view class="menu-group">
				<view class="menu-item" @tap="contactService">
					<view class="menu-icon">📞</view>
					<text class="menu-title">联系客服</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToFeedback">
					<view class="menu-icon">💬</view>
					<text class="menu-title">意见反馈</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToAbout">
					<view class="menu-icon">ℹ️</view>
					<text class="menu-title">关于我们</text>
					<text class="menu-arrow">></text>
				</view>
				<view class="menu-item" @tap="goToSettings">
					<view class="menu-icon">⚙️</view>
					<text class="menu-title">设置</text>
					<text class="menu-arrow">></text>
				</view>
			</view>
		</view>

		<!-- 退出登录 -->
		<view class="logout-section" v-if="userInfo.nickName">
			<view class="logout-btn" @tap="logout">
				<text>退出登录</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				userInfo: {
					avatar: '',
					nickName: '剧本杀玩家',
					phone: '138****5678',
					isVip: true,
					vipExpire: '2024-12-31',
					points: 1280
				},
				userStats: {
					totalGames: 15,
					totalHours: 68,
					favoriteCount: 8
				},
				pendingOrderCount: 2,
				availableCoupons: 3
			}
		},
		onLoad() {
			this.loadUserInfo();
		},
		onShow() {
			this.refreshData();
		},
		methods: {
			loadUserInfo() {
				// 这里可以调用后端接口获取用户信息
				console.log('加载用户信息');
			},
			refreshData() {
				// 刷新页面数据
				this.loadUserInfo();
			},
			chooseAvatar() {
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: (res) => {
						this.userInfo.avatar = res.tempFilePaths[0];
						// 这里可以上传头像到服务器
					}
				});
			},
			login() {
				// 这里实现登录逻辑
				uni.login({
					provider: 'weixin',
					success: (res) => {
						console.log('登录成功', res);
						// 调用后端接口进行登录验证
					}
				});
			},
			logout() {
				uni.showModal({
					title: '确认退出',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							// 清除用户信息
							this.userInfo = {
								avatar: '',
								nickName: '',
								phone: '',
								isVip: false,
								vipExpire: '',
								points: 0
							};
							uni.showToast({
								title: '已退出登录',
								icon: 'success'
							});
						}
					}
				});
			},
			goToOrders() {
				uni.switchTab({
					url: '/pages/orders/orders'
				});
			},
			goToFavorites() {
				uni.navigateTo({
					url: '/pages/favorites/favorites'
				});
			},
			goToReviews() {
				uni.navigateTo({
					url: '/pages/reviews/reviews'
				});
			},
			goToCoupons() {
				uni.navigateTo({
					url: '/pages/coupons/coupons'
				});
			},
			goToPoints() {
				uni.navigateTo({
					url: '/pages/points/points'
				});
			},
			goToInvite() {
				uni.navigateTo({
					url: '/pages/invite/invite'
				});
			},
			becomeVip() {
				uni.navigateTo({
					url: '/pages/vip/vip'
				});
			},
			contactService() {
				uni.makePhoneCall({
					phoneNumber: '400-123-4567'
				});
			},
			goToFeedback() {
				uni.navigateTo({
					url: '/pages/feedback/feedback'
				});
			},
			goToAbout() {
				uni.navigateTo({
					url: '/pages/about/about'
				});
			},
			goToSettings() {
				uni.navigateTo({
					url: '/pages/settings/settings'
				});
			}
		}
	}
</script>

<style scoped>
	.page {
		background-color: #f8f9fa;
		min-height: 100vh;
	}

	/* 用户信息卡片 */
	.user-card {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 40rpx;
		color: white;
		display: flex;
		align-items: center;
	}

	.user-avatar {
		width: 120rpx;
		height: 120rpx;
		border-radius: 60rpx;
		margin-right: 30rpx;
		background: rgba(255, 255, 255, 0.2);
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.avatar-img {
		width: 100%;
		height: 100%;
		border-radius: 60rpx;
		object-fit: cover;
	}

	.avatar-placeholder {
		font-size: 60rpx;
		opacity: 0.8;
	}

	.user-info {
		flex: 1;
	}

	.user-name {
		font-size: 36rpx;
		font-weight: bold;
		display: block;
		margin-bottom: 10rpx;
	}

	.user-name.guest {
		opacity: 0.8;
	}

	.user-phone {
		font-size: 26rpx;
		opacity: 0.8;
		display: block;
		margin-bottom: 25rpx;
	}

	.user-stats {
		display: flex;
		gap: 40rpx;
	}

	.stat-item {
		text-align: center;
	}

	.stat-number {
		font-size: 32rpx;
		font-weight: bold;
		display: block;
		margin-bottom: 8rpx;
	}

	.stat-label {
		font-size: 22rpx;
		opacity: 0.8;
	}

	/* VIP卡片 */
	.vip-card {
		background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 30rpx;
		color: #333;
	}

	.vip-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
	}

	.vip-title {
		font-size: 32rpx;
		font-weight: bold;
	}

	.vip-expire {
		font-size: 24rpx;
		opacity: 0.8;
	}

	.vip-benefits {
		display: flex;
		gap: 30rpx;
	}

	.benefit-item {
		font-size: 24rpx;
		background: rgba(255, 255, 255, 0.3);
		padding: 8rpx 16rpx;
		border-radius: 16rpx;
	}

	/* 菜单区域 */
	.menu-section {
		padding: 20rpx;
	}

	.menu-group {
		background: white;
		border-radius: 20rpx;
		margin-bottom: 30rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.menu-item {
		display: flex;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
		transition: all 0.3s;
	}

	.menu-item:last-child {
		border-bottom: none;
	}

	.menu-icon {
		width: 80rpx;
		height: 80rpx;
		background: #f8f9fa;
		border-radius: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 30rpx;
		font-size: 36rpx;
	}

	.menu-title {
		font-size: 30rpx;
		color: #333;
		flex: 1;
	}

	.menu-subtitle {
		font-size: 24rpx;
		color: #999;
		margin-right: 20rpx;
	}

	.menu-badge {
		background: #ff6b6b;
		color: white;
		padding: 4rpx 12rpx;
		border-radius: 16rpx;
		font-size: 20rpx;
		margin-right: 20rpx;
		min-width: 32rpx;
		text-align: center;
	}

	.menu-arrow {
		font-size: 30rpx;
		color: #ccc;
	}

	/* 退出登录 */
	.logout-section {
		padding: 20rpx;
	}

	.logout-btn {
		background: white;
		border-radius: 20rpx;
		padding: 30rpx;
		text-align: center;
		font-size: 30rpx;
		color: #ff6b6b;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}
</style>
