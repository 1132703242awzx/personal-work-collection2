<template>
	<view class="page">
		<!-- 选择剧本 -->
		<view class="script-section" v-if="!selectedScript">
			<view class="section-title">
				<text class="title-text">📚 选择剧本</text>
			</view>
			<view class="scripts-list">
				<view class="script-item" 
					v-for="script in scripts" 
					:key="script.id"
					@tap="selectScript(script)">
					<image :src="script.cover" class="script-cover"></image>
					<view class="script-info">
						<text class="script-name">{{script.name}}</text>
						<view class="script-meta">
							<text class="meta-text">{{script.playerCount}}人 · {{script.duration}}小时 · ¥{{script.price}}/人</text>
						</view>
						<view class="script-tags">
							<text class="tag" v-for="tag in script.tags" :key="tag">{{tag}}</text>
						</view>
					</view>
					<view class="select-icon">></view>
				</view>
			</view>
		</view>

		<!-- 已选剧本信息 -->
		<view class="selected-script" v-if="selectedScript">
			<view class="script-card">
				<image :src="selectedScript.cover" class="script-cover"></image>
				<view class="script-info">
					<text class="script-name">{{selectedScript.name}}</text>
					<view class="script-meta">
						<text class="meta-text">{{selectedScript.playerCount}}人 · {{selectedScript.duration}}小时 · ¥{{selectedScript.price}}/人</text>
					</view>
				</view>
				<view class="change-script" @tap="changeScript">
					<text>更换</text>
				</view>
			</view>
		</view>

		<!-- 选择日期 -->
		<view class="date-section" v-if="selectedScript">
			<view class="section-title">
				<text class="title-text">📅 选择日期</text>
			</view>
			<scroll-view scroll-x="true" class="date-scroll">
				<view class="date-list">
					<view class="date-item" 
						v-for="date in availableDates" 
						:key="date.dateString"
						:class="{'active': selectedDate === date.dateString}"
						@tap="selectDate(date.dateString)">
						<text class="date-weekday">{{date.weekday}}</text>
						<text class="date-day">{{date.day}}</text>
						<text class="date-month">{{date.month}}</text>
					</view>
				</view>
			</scroll-view>
		</view>

		<!-- 选择场次 -->
		<view class="sessions-section" v-if="selectedDate">
			<view class="section-title">
				<text class="title-text">⏰ 选择场次</text>
			</view>
			<view class="sessions-list">
				<view class="session-item" 
					v-for="session in availableSessions" 
					:key="session.id"
					:class="{'active': selectedSession && selectedSession.id === session.id, 'disabled': session.currentPlayers >= session.maxPlayers}"
					@tap="selectSession(session)">
					<view class="session-time">
						<text class="time-text">{{session.startTime}}</text>
						<text class="time-period">{{session.period}}</text>
					</view>
					<view class="session-info">
						<text class="session-players">{{session.currentPlayers}}/{{session.maxPlayers}}人</text>
						<text class="session-status" :class="{'full': session.currentPlayers >= session.maxPlayers}">
							{{session.currentPlayers >= session.maxPlayers ? '已满' : '可约'}}
						</text>
					</view>
					<view class="session-price">
						<text>¥{{session.price}}</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 联系方式 -->
		<view class="contact-section" v-if="selectedSession">
			<view class="section-title">
				<text class="title-text">📞 联系方式</text>
			</view>
			<view class="form-item">
				<text class="form-label">姓名</text>
				<input class="form-input" v-model="contactInfo.name" placeholder="请输入您的姓名" />
			</view>
			<view class="form-item">
				<text class="form-label">手机号</text>
				<input class="form-input" v-model="contactInfo.phone" placeholder="请输入手机号码" type="number" />
			</view>
			<view class="form-item">
				<text class="form-label">备注</text>
				<textarea class="form-textarea" v-model="contactInfo.note" placeholder="有什么特殊要求可以在这里说明（选填）"></textarea>
			</view>
		</view>

		<!-- 预约须知 -->
		<view class="notice-section" v-if="selectedSession">
			<view class="section-title">
				<text class="title-text">📋 预约须知</text>
			</view>
			<view class="notice-content">
				<view class="notice-item">
					<text class="notice-text">• 请提前15分钟到店，准备身份证件</text>
				</view>
				<view class="notice-item">
					<text class="notice-text">• 游戏过程中请关闭手机或调至静音</text>
				</view>
				<view class="notice-item">
					<text class="notice-text">• 如需取消预约，请提前2小时联系客服</text>
				</view>
				<view class="notice-item">
					<text class="notice-text">• 迟到超过30分钟将视为自动取消</text>
				</view>
			</view>
		</view>

		<!-- 价格明细 -->
		<view class="price-section" v-if="selectedSession">
			<view class="section-title">
				<text class="title-text">💰 价格明细</text>
			</view>
			<view class="price-detail">
				<view class="price-row">
					<text class="price-label">剧本费用</text>
					<text class="price-value">¥{{selectedSession.price}}/人</text>
				</view>
				<view class="price-row">
					<text class="price-label">预约人数</text>
					<view class="player-count">
						<view class="count-btn" @tap="decreaseCount">-</view>
						<text class="count-text">{{playerCount}}</text>
						<view class="count-btn" @tap="increaseCount">+</view>
					</view>
				</view>
				<view class="price-row total">
					<text class="price-label">总计</text>
					<text class="price-value total-price">¥{{totalPrice}}</text>
				</view>
			</view>
		</view>

		<!-- 底部确认按钮 -->
		<view class="bottom-bar" v-if="selectedSession">
			<view class="total-info">
				<text class="total-text">总计：¥{{totalPrice}}</text>
			</view>
			<view class="confirm-btn" @tap="confirmReservation">
				<text>确认预约</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				scriptId: null,
				sessionId: null,
				selectedScript: null,
				selectedDate: '',
				selectedSession: null,
				playerCount: 1,
				contactInfo: {
					name: '',
					phone: '',
					note: ''
				},
				scripts: [
					{
						id: 1,
						name: '年轮',
						cover: '/static/script1.jpg',
						tags: ['悬疑', '推理'],
						playerCount: 6,
						duration: 4,
						price: 88
					},
					{
						id: 2,
						name: '云使',
						cover: '/static/script2.jpg',
						tags: ['古风', '情感'],
						playerCount: 7,
						duration: 5,
						price: 98
					},
					{
						id: 3,
						name: '第七个嫌疑人',
						cover: '/static/script3.jpg',
						tags: ['现代', '悬疑'],
						playerCount: 7,
						duration: 4,
						price: 78
					}
				],
				availableDates: [],
				availableSessions: []
			}
		},
		computed: {
			totalPrice() {
				if (!this.selectedSession) return 0;
				return this.selectedSession.price * this.playerCount;
			}
		},
		onLoad(options) {
			if (options.scriptId) {
				this.scriptId = options.scriptId;
				this.selectScriptById(options.scriptId);
			}
			if (options.sessionId) {
				this.sessionId = options.sessionId;
			}
			this.generateAvailableDates();
		},
		methods: {
			selectScriptById(scriptId) {
				const script = this.scripts.find(s => s.id == scriptId);
				if (script) {
					this.selectedScript = script;
				}
			},
			selectScript(script) {
				this.selectedScript = script;
				this.selectedDate = '';
				this.selectedSession = null;
			},
			changeScript() {
				this.selectedScript = null;
				this.selectedDate = '';
				this.selectedSession = null;
			},
			generateAvailableDates() {
				const dates = [];
				const today = new Date();
				const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
				const months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
				
				for (let i = 0; i < 7; i++) {
					const date = new Date(today);
					date.setDate(today.getDate() + i);
					
					dates.push({
						dateString: date.toISOString().split('T')[0],
						weekday: weekdays[date.getDay()],
						day: date.getDate(),
						month: months[date.getMonth()]
					});
				}
				
				this.availableDates = dates;
			},
			selectDate(dateString) {
				this.selectedDate = dateString;
				this.selectedSession = null;
				this.loadAvailableSessions();
			},
			loadAvailableSessions() {
				// 模拟获取可用场次数据
				this.availableSessions = [
					{
						id: 1,
						startTime: '14:00',
						period: '下午场',
						currentPlayers: 3,
						maxPlayers: this.selectedScript ? this.selectedScript.playerCount : 6,
						price: this.selectedScript ? this.selectedScript.price : 88
					},
					{
						id: 2,
						startTime: '19:00',
						period: '晚场',
						currentPlayers: 5,
						maxPlayers: this.selectedScript ? this.selectedScript.playerCount : 6,
						price: this.selectedScript ? this.selectedScript.price : 88
					},
					{
						id: 3,
						startTime: '20:30',
						period: '夜场',
						currentPlayers: 1,
						maxPlayers: this.selectedScript ? this.selectedScript.playerCount : 6,
						price: this.selectedScript ? this.selectedScript.price : 88
					}
				];
			},
			selectSession(session) {
				if (session.currentPlayers >= session.maxPlayers) {
					uni.showToast({
						title: '该场次已满',
						icon: 'none'
					});
					return;
				}
				this.selectedSession = session;
				this.playerCount = 1;
			},
			decreaseCount() {
				if (this.playerCount > 1) {
					this.playerCount--;
				}
			},
			increaseCount() {
				const maxCount = this.selectedSession.maxPlayers - this.selectedSession.currentPlayers;
				if (this.playerCount < maxCount) {
					this.playerCount++;
				} else {
					uni.showToast({
						title: `最多还能预约${maxCount}人`,
						icon: 'none'
					});
				}
			},
			confirmReservation() {
				// 验证表单
				if (!this.contactInfo.name.trim()) {
					uni.showToast({
						title: '请输入姓名',
						icon: 'none'
					});
					return;
				}
				
				if (!this.contactInfo.phone.trim() || !/^1[3-9]\d{9}$/.test(this.contactInfo.phone)) {
					uni.showToast({
						title: '请输入正确的手机号',
						icon: 'none'
					});
					return;
				}
				
				// 创建预约
				const reservation = {
					scriptId: this.selectedScript.id,
					scriptName: this.selectedScript.name,
					sessionId: this.selectedSession.id,
					date: this.selectedDate,
					startTime: this.selectedSession.startTime,
					playerCount: this.playerCount,
					totalPrice: this.totalPrice,
					contactInfo: this.contactInfo
				};
				
				// 这里可以调用后端接口创建预约
				console.log('创建预约', reservation);
				
				uni.showModal({
					title: '预约成功',
					content: `您已成功预约${this.selectedScript.name}，时间：${this.selectedDate} ${this.selectedSession.startTime}`,
					showCancel: false,
					success: () => {
						// 跳转到订单页面
						uni.redirectTo({
							url: '/pages/orders/orders'
						});
					}
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

	/* 通用区域样式 */
	.script-section, .selected-script, .date-section, .sessions-section, 
	.contact-section, .notice-section, .price-section {
		background: white;
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
	}

	.section-title {
		margin-bottom: 30rpx;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.title-text {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}

	/* 剧本选择 */
	.scripts-list {
		gap: 20rpx;
	}

	.script-item {
		display: flex;
		align-items: center;
		padding: 20rpx;
		background: #f8f9fa;
		border-radius: 15rpx;
		margin-bottom: 20rpx;
		transition: all 0.3s;
	}

	.script-item:last-child {
		margin-bottom: 0;
	}

	.script-cover {
		width: 120rpx;
		height: 80rpx;
		border-radius: 10rpx;
		margin-right: 20rpx;
		object-fit: cover;
	}

	.script-info {
		flex: 1;
	}

	.script-name {
		font-size: 30rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 10rpx;
	}

	.script-meta {
		margin-bottom: 15rpx;
	}

	.meta-text {
		font-size: 24rpx;
		color: #666;
	}

	.script-tags {
		display: flex;
	}

	.tag {
		background: #e3f2fd;
		color: #1976d2;
		font-size: 20rpx;
		padding: 4rpx 10rpx;
		border-radius: 10rpx;
		margin-right: 10rpx;
	}

	.select-icon {
		font-size: 30rpx;
		color: #999;
	}

	/* 已选剧本 */
	.script-card {
		display: flex;
		align-items: center;
	}

	.change-script {
		background: #667eea;
		color: white;
		padding: 10rpx 20rpx;
		border-radius: 15rpx;
		font-size: 24rpx;
	}

	/* 日期选择 */
	.date-scroll {
		white-space: nowrap;
	}

	.date-list {
		display: flex;
		gap: 20rpx;
	}

	.date-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 20rpx;
		background: #f8f9fa;
		border-radius: 15rpx;
		min-width: 100rpx;
		transition: all 0.3s;
	}

	.date-item.active {
		background: #667eea;
		color: white;
	}

	.date-weekday {
		font-size: 22rpx;
		margin-bottom: 8rpx;
	}

	.date-day {
		font-size: 32rpx;
		font-weight: bold;
		margin-bottom: 8rpx;
	}

	.date-month {
		font-size: 20rpx;
		opacity: 0.8;
	}

	/* 场次选择 */
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
		border: 2rpx solid transparent;
	}

	.session-item:last-child {
		margin-bottom: 0;
	}

	.session-item.active {
		background: #e3f2fd;
		border-color: #667eea;
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

	.time-period {
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
		color: #28a745;
	}

	.session-status.full {
		color: #ff6b6b;
	}

	.session-price {
		font-size: 28rpx;
		font-weight: bold;
		color: #667eea;
	}

	/* 表单样式 */
	.form-item {
		margin-bottom: 30rpx;
	}

	.form-label {
		font-size: 28rpx;
		color: #333;
		display: block;
		margin-bottom: 15rpx;
	}

	.form-input {
		width: 100%;
		padding: 25rpx;
		background: #f8f9fa;
		border-radius: 10rpx;
		font-size: 28rpx;
		border: 1rpx solid #e0e0e0;
	}

	.form-textarea {
		width: 100%;
		height: 150rpx;
		padding: 25rpx;
		background: #f8f9fa;
		border-radius: 10rpx;
		font-size: 28rpx;
		border: 1rpx solid #e0e0e0;
		resize: none;
	}

	/* 须知内容 */
	.notice-content {
		gap: 15rpx;
	}

	.notice-item {
		margin-bottom: 15rpx;
	}

	.notice-text {
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
	}

	/* 价格明细 */
	.price-detail {
		gap: 20rpx;
	}

	.price-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.price-row:last-child {
		border-bottom: none;
	}

	.price-row.total {
		border-top: 2rpx solid #e0e0e0;
		padding-top: 25rpx;
		margin-top: 15rpx;
	}

	.price-label {
		font-size: 28rpx;
		color: #333;
	}

	.price-value {
		font-size: 28rpx;
		color: #667eea;
		font-weight: bold;
	}

	.total-price {
		font-size: 32rpx;
		color: #ff6b6b;
	}

	.player-count {
		display: flex;
		align-items: center;
	}

	.count-btn {
		width: 60rpx;
		height: 60rpx;
		background: #667eea;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 30rpx;
		font-size: 28rpx;
		font-weight: bold;
	}

	.count-text {
		margin: 0 30rpx;
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		min-width: 60rpx;
		text-align: center;
	}

	/* 底部确认栏 */
	.bottom-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background: white;
		padding: 20rpx 30rpx;
		border-top: 1rpx solid #f0f0f0;
		box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.05);
		display: flex;
		align-items: center;
	}

	.total-info {
		flex: 1;
	}

	.total-text {
		font-size: 32rpx;
		font-weight: bold;
		color: #ff6b6b;
	}

	.confirm-btn {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		padding: 25rpx 50rpx;
		border-radius: 25rpx;
		font-size: 30rpx;
		font-weight: bold;
	}
</style>
