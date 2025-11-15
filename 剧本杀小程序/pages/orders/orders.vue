<template>
	<view class="page">
		<!-- 状态筛选 -->
		<view class="filter-tabs">
			<view class="tab-item" 
				:class="{'active': activeTab === 'all'}"
				@tap="switchTab('all')">
				<text>全部</text>
			</view>
			<view class="tab-item" 
				:class="{'active': activeTab === 'upcoming'}"
				@tap="switchTab('upcoming')">
				<text>待参加</text>
			</view>
			<view class="tab-item" 
				:class="{'active': activeTab === 'completed'}"
				@tap="switchTab('completed')">
				<text>已完成</text>
			</view>
			<view class="tab-item" 
				:class="{'active': activeTab === 'cancelled'}"
				@tap="switchTab('cancelled')">
				<text>已取消</text>
			</view>
		</view>

		<!-- 订单列表 -->
		<view class="orders-list" v-if="filteredOrders.length > 0">
			<view class="order-card" v-for="order in filteredOrders" :key="order.id">
				<!-- 订单状态 -->
				<view class="order-header">
					<text class="order-number">订单号：{{order.orderNumber}}</text>
					<view class="order-status" :class="order.status">
						<text>{{getStatusText(order.status)}}</text>
					</view>
				</view>

				<!-- 剧本信息 -->
				<view class="order-content">
					<image :src="order.scriptCover" class="script-cover"></image>
					<view class="order-info">
						<text class="script-name">{{order.scriptName}}</text>
						<view class="order-details">
							<view class="detail-row">
								<text class="detail-label">游戏时间：</text>
								<text class="detail-value">{{order.playDate}} {{order.startTime}}</text>
							</view>
							<view class="detail-row">
								<text class="detail-label">游戏时长：</text>
								<text class="detail-value">{{order.duration}}小时</text>
							</view>
							<view class="detail-row">
								<text class="detail-label">预约人数：</text>
								<text class="detail-value">{{order.playerCount}}人</text>
							</view>
							<view class="detail-row">
								<text class="detail-label">联系方式：</text>
								<text class="detail-value">{{order.contactName}} {{order.contactPhone}}</text>
							</view>
						</view>
					</view>
				</view>

				<!-- 价格信息 -->
				<view class="order-price">
					<text class="price-label">总计：</text>
					<text class="price-value">¥{{order.totalPrice}}</text>
				</view>

				<!-- 操作按钮 -->
				<view class="order-actions">
					<view class="action-btn secondary" 
						v-if="order.status === 'upcoming'" 
						@tap="cancelOrder(order)">
						<text>取消预约</text>
					</view>
					<view class="action-btn secondary" 
						@tap="contactStore">
						<text>联系客服</text>
					</view>
					<view class="action-btn primary" 
						v-if="order.status === 'upcoming'" 
						@tap="modifyOrder(order)">
						<text>修改预约</text>
					</view>
					<view class="action-btn primary" 
						v-if="order.status === 'completed'" 
						@tap="reviewOrder(order)">
						<text>评价</text>
					</view>
					<view class="action-btn primary" 
						@tap="rebookOrder(order)">
						<text>再次预约</text>
					</view>
				</view>

				<!-- 倒计时 -->
				<view class="countdown" v-if="order.status === 'upcoming' && order.countdown > 0">
					<text class="countdown-text">距离游戏开始还有：{{formatCountdown(order.countdown)}}</text>
				</view>
			</view>
		</view>

		<!-- 空状态 -->
		<view class="empty-state" v-else>
			<image src="/static/empty-orders.png" class="empty-image"></image>
			<text class="empty-text">暂无预约记录</text>
			<view class="empty-action" @tap="goToReservation">
				<text>立即预约</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				activeTab: 'all',
				orders: [
					{
						id: 1,
						orderNumber: 'JBK20231210001',
						scriptName: '年轮',
						scriptCover: '/static/script1.jpg',
						playDate: '2023-12-15',
						startTime: '19:00',
						duration: 4,
						playerCount: 2,
						totalPrice: 176,
						contactName: '张三',
						contactPhone: '138****5678',
						status: 'upcoming',
						createTime: '2023-12-10 14:30:00',
						countdown: 432000 // 秒数
					},
					{
						id: 2,
						orderNumber: 'JBK20231208002',
						scriptName: '云使',
						scriptCover: '/static/script2.jpg',
						playDate: '2023-12-08',
						startTime: '14:00',
						duration: 5,
						playerCount: 1,
						totalPrice: 98,
						contactName: '李四',
						contactPhone: '139****1234',
						status: 'completed',
						createTime: '2023-12-05 16:20:00',
						countdown: 0
					},
					{
						id: 3,
						orderNumber: 'JBK20231205003',
						scriptName: '第七个嫌疑人',
						scriptCover: '/static/script3.jpg',
						playDate: '2023-12-05',
						startTime: '20:30',
						duration: 4,
						playerCount: 3,
						totalPrice: 234,
						contactName: '王五',
						contactPhone: '137****9876',
						status: 'cancelled',
						createTime: '2023-12-03 10:15:00',
						countdown: 0
					}
				]
			}
		},
		computed: {
			filteredOrders() {
				if (this.activeTab === 'all') {
					return this.orders;
				}
				return this.orders.filter(order => order.status === this.activeTab);
			}
		},
		onLoad() {
			this.loadOrders();
			this.startCountdown();
		},
		onUnload() {
			if (this.countdownTimer) {
				clearInterval(this.countdownTimer);
			}
		},
		methods: {
			switchTab(tab) {
				this.activeTab = tab;
			},
			loadOrders() {
				// 这里可以调用后端接口获取订单数据
				console.log('加载订单数据');
			},
			getStatusText(status) {
				const statusMap = {
					'upcoming': '待参加',
					'completed': '已完成',
					'cancelled': '已取消'
				};
				return statusMap[status] || '未知状态';
			},
			formatCountdown(seconds) {
				const days = Math.floor(seconds / 86400);
				const hours = Math.floor((seconds % 86400) / 3600);
				const minutes = Math.floor((seconds % 3600) / 60);
				
				if (days > 0) {
					return `${days}天${hours}小时${minutes}分钟`;
				} else if (hours > 0) {
					return `${hours}小时${minutes}分钟`;
				} else {
					return `${minutes}分钟`;
				}
			},
			startCountdown() {
				this.countdownTimer = setInterval(() => {
					this.orders.forEach(order => {
						if (order.countdown > 0) {
							order.countdown--;
						}
					});
				}, 1000);
			},
			cancelOrder(order) {
				uni.showModal({
					title: '确认取消',
					content: '确定要取消这个预约吗？',
					success: (res) => {
						if (res.confirm) {
							// 这里可以调用后端接口取消订单
							order.status = 'cancelled';
							uni.showToast({
								title: '取消成功',
								icon: 'success'
							});
						}
					}
				});
			},
			modifyOrder(order) {
				uni.navigateTo({
					url: `/pages/reservation/reservation?orderId=${order.id}`
				});
			},
			reviewOrder(order) {
				uni.navigateTo({
					url: `/pages/review/review?orderId=${order.id}`
				});
			},
			rebookOrder(order) {
				uni.navigateTo({
					url: `/pages/reservation/reservation?scriptId=${order.scriptId}`
				});
			},
			contactStore() {
				uni.makePhoneCall({
					phoneNumber: '400-123-4567'
				});
			},
			goToReservation() {
				uni.switchTab({
					url: '/pages/scripts/scripts'
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

	/* 状态筛选 */
	.filter-tabs {
		display: flex;
		background: white;
		padding: 0 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
		position: sticky;
		top: 0;
		z-index: 100;
	}

	.tab-item {
		flex: 1;
		text-align: center;
		padding: 30rpx 0;
		font-size: 28rpx;
		color: #666;
		position: relative;
		transition: all 0.3s;
	}

	.tab-item.active {
		color: #667eea;
		font-weight: bold;
	}

	.tab-item.active::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 60rpx;
		height: 4rpx;
		background: #667eea;
		border-radius: 2rpx;
	}

	/* 订单列表 */
	.orders-list {
		padding: 20rpx;
	}

	.order-card {
		background: white;
		border-radius: 20rpx;
		margin-bottom: 30rpx;
		padding: 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 25rpx;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.order-number {
		font-size: 26rpx;
		color: #999;
	}

	.order-status {
		padding: 8rpx 16rpx;
		border-radius: 16rpx;
		font-size: 22rpx;
	}

	.order-status.upcoming {
		background: #e3f2fd;
		color: #1976d2;
	}

	.order-status.completed {
		background: #e8f5e8;
		color: #2e7d32;
	}

	.order-status.cancelled {
		background: #ffebee;
		color: #c62828;
	}

	/* 订单内容 */
	.order-content {
		display: flex;
		margin-bottom: 25rpx;
	}

	.script-cover {
		width: 120rpx;
		height: 160rpx;
		border-radius: 10rpx;
		margin-right: 25rpx;
		object-fit: cover;
	}

	.order-info {
		flex: 1;
	}

	.script-name {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 20rpx;
	}

	.order-details {
		gap: 10rpx;
	}

	.detail-row {
		display: flex;
		margin-bottom: 10rpx;
	}

	.detail-label {
		font-size: 26rpx;
		color: #666;
		min-width: 140rpx;
	}

	.detail-value {
		font-size: 26rpx;
		color: #333;
		flex: 1;
	}

	/* 价格信息 */
	.order-price {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		margin-bottom: 25rpx;
		padding: 20rpx 0;
		border-top: 1rpx solid #f0f0f0;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.price-label {
		font-size: 28rpx;
		color: #333;
		margin-right: 15rpx;
	}

	.price-value {
		font-size: 36rpx;
		font-weight: bold;
		color: #ff6b6b;
	}

	/* 操作按钮 */
	.order-actions {
		display: flex;
		gap: 20rpx;
		flex-wrap: wrap;
	}

	.action-btn {
		padding: 15rpx 30rpx;
		border-radius: 20rpx;
		font-size: 26rpx;
		text-align: center;
		min-width: 140rpx;
		transition: all 0.3s;
	}

	.action-btn.secondary {
		background: #f8f9fa;
		color: #666;
		border: 1rpx solid #dee2e6;
	}

	.action-btn.primary {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
	}

	/* 倒计时 */
	.countdown {
		margin-top: 20rpx;
		padding: 15rpx;
		background: #fff3cd;
		border-radius: 10rpx;
		text-align: center;
	}

	.countdown-text {
		font-size: 24rpx;
		color: #856404;
	}

	/* 空状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 100rpx 50rpx;
		text-align: center;
	}

	.empty-image {
		width: 300rpx;
		height: 300rpx;
		margin-bottom: 40rpx;
		opacity: 0.6;
	}

	.empty-text {
		font-size: 32rpx;
		color: #999;
		margin-bottom: 50rpx;
	}

	.empty-action {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		padding: 25rpx 50rpx;
		border-radius: 25rpx;
		font-size: 30rpx;
	}
</style>
