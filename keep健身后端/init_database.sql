-- ============================================
-- Keep健身后端 - 完整数据库初始化脚本
-- 创建时间: 2025-10-19
-- 数据库: MySQL 8.0+
-- 字符集: utf8mb4 (支持emoji)
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS keep_fitness 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE keep_fitness;

-- ============================================
-- 1. 用户系统相关表
-- ============================================

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    status ENUM('active', 'inactive', 'banned') NOT NULL DEFAULT 'active' COMMENT '账号状态',
    email_verified BOOLEAN NOT NULL DEFAULT FALSE COMMENT '邮箱是否验证',
    phone_verified BOOLEAN NOT NULL DEFAULT FALSE COMMENT '手机是否验证',
    last_login_at DATETIME COMMENT '最后登录时间',
    last_login_ip VARCHAR(45) COMMENT '最后登录IP',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_last_login_at (last_login_at),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户资料表
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL UNIQUE COMMENT '用户ID',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    gender ENUM('male', 'female', 'other') COMMENT '性别',
    birthday DATE COMMENT '生日',
    height DECIMAL(5,2) COMMENT '身高(cm)',
    weight DECIMAL(5,2) COMMENT '体重(kg)',
    target_weight DECIMAL(5,2) COMMENT '目标体重(kg)',
    bio TEXT COMMENT '个人简介',
    location VARCHAR(100) COMMENT '所在地',
    fitness_level ENUM('beginner', 'intermediate', 'advanced') COMMENT '健身水平',
    fitness_goal VARCHAR(100) COMMENT '健身目标',
    followers_count INT DEFAULT 0 COMMENT '粉丝数',
    following_count INT DEFAULT 0 COMMENT '关注数',
    total_workouts INT DEFAULT 0 COMMENT '总锻炼次数',
    total_duration INT DEFAULT 0 COMMENT '总锻炼时长(分钟)',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_nickname (nickname),
    INDEX idx_fitness_level (fitness_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户资料表';

-- 用户设置表
CREATE TABLE IF NOT EXISTS user_settings (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL UNIQUE COMMENT '用户ID',
    language VARCHAR(10) DEFAULT 'zh-CN' COMMENT '语言',
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai' COMMENT '时区',
    theme VARCHAR(20) DEFAULT 'light' COMMENT '主题',
    privacy_level ENUM('public', 'friends', 'private') DEFAULT 'public' COMMENT '隐私级别',
    show_real_name BOOLEAN DEFAULT FALSE COMMENT '显示真实姓名',
    allow_follow BOOLEAN DEFAULT TRUE COMMENT '允许关注',
    allow_message BOOLEAN DEFAULT TRUE COMMENT '允许私信',
    email_notifications BOOLEAN DEFAULT TRUE COMMENT '邮件通知',
    push_notifications BOOLEAN DEFAULT TRUE COMMENT '推送通知',
    workout_reminders BOOLEAN DEFAULT TRUE COMMENT '锻炼提醒',
    social_notifications BOOLEAN DEFAULT TRUE COMMENT '社交通知',
    extra_settings JSON COMMENT '额外设置',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设置表';

-- ============================================
-- 2. 认证系统相关表
-- ============================================

-- 用户角色表
CREATE TABLE IF NOT EXISTS user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role VARCHAR(50) NOT NULL COMMENT '角色',
    granted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授予时间',
    granted_by INT COMMENT '授予者ID',
    expires_at DATETIME COMMENT '过期时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),

    
    INDEX idx_role (role),
    UNIQUE KEY uk_user_role (user_id, role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色表';

-- 第三方账号表
CREATE TABLE IF NOT EXISTS third_party_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    provider VARCHAR(50) NOT NULL COMMENT '提供商',
    provider_user_id VARCHAR(255) NOT NULL COMMENT '第三方用户ID',
    access_token TEXT COMMENT '访问令牌',
    refresh_token TEXT COMMENT '刷新令牌',
    expires_at DATETIME COMMENT '过期时间',
    profile_data JSON COMMENT '第三方资料',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_provider (provider),
    UNIQUE KEY uk_provider_user (provider, provider_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='第三方账号表';

-- 刷新令牌表
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    token VARCHAR(255) NOT NULL UNIQUE COMMENT '令牌',
    device_id VARCHAR(255) COMMENT '设备ID',
    device_info JSON COMMENT '设备信息',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT 'User Agent',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
    expires_at DATETIME NOT NULL COMMENT '过期时间',
    last_used_at DATETIME COMMENT '最后使用时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token),
    INDEX idx_device_id (device_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='刷新令牌表';

-- 密码重置令牌表
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    token VARCHAR(255) NOT NULL UNIQUE COMMENT '令牌',
    is_used BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否已使用',
    expires_at DATETIME NOT NULL COMMENT '过期时间',
    used_at DATETIME COMMENT '使用时间',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token),
    INDEX idx_expires_at (expires_at),
    INDEX idx_is_used (is_used)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='密码重置令牌表';

-- 登录历史表
CREATE TABLE IF NOT EXISTS login_history (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    login_method VARCHAR(50) NOT NULL COMMENT '登录方式',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT 'User Agent',
    device_id VARCHAR(255) COMMENT '设备ID',
    device_info JSON COMMENT '设备信息',
    location VARCHAR(255) COMMENT '登录地点',
    is_successful BOOLEAN NOT NULL COMMENT '是否成功',
    failure_reason VARCHAR(255) COMMENT '失败原因',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_login_method (login_method),
    INDEX idx_created_at (created_at),
    INDEX idx_is_successful (is_successful)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='登录历史表';

-- 安全日志表
CREATE TABLE IF NOT EXISTS security_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT COMMENT '用户ID',
    action VARCHAR(100) NOT NULL COMMENT '操作',
    resource_type VARCHAR(50) COMMENT '资源类型',
    resource_id INT COMMENT '资源ID',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT 'User Agent',
    risk_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'low' COMMENT '风险级别',
    details JSON COMMENT '详细信息',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='安全日志表';

-- ============================================
-- 3. 训练计划相关表
-- ============================================

-- 训练计划表
CREATE TABLE IF NOT EXISTS training_plans (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '计划ID',
    user_id INT NOT NULL COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '计划名称',
    description TEXT COMMENT '计划描述',
    cover_image VARCHAR(255) COMMENT '封面图片',
    difficulty ENUM('beginner', 'intermediate', 'advanced') NOT NULL COMMENT '难度等级',
    duration_weeks INT NOT NULL COMMENT '计划周期(周)',
    days_per_week INT NOT NULL COMMENT '每周训练天数',
    goal VARCHAR(50) COMMENT '训练目标',
    target_muscle_group ENUM('chest', 'back', 'shoulders', 'arms', 'legs', 'core', 'cardio', 'full_body') COMMENT '主要目标肌群',
    is_active BOOLEAN DEFAULT FALSE COMMENT '是否激活',
    is_template BOOLEAN DEFAULT FALSE COMMENT '是否为模板',
    is_public BOOLEAN DEFAULT FALSE COMMENT '是否公开',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    completion_rate INT DEFAULT 0 COMMENT '完成率',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_template (is_template),
    INDEX idx_is_public (is_public),
    INDEX idx_difficulty (difficulty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练计划表';

-- 计划每日安排表
CREATE TABLE IF NOT EXISTS plan_days (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    training_plan_id INT NOT NULL COMMENT '训练计划ID',
    day_number INT NOT NULL COMMENT '第几天',
    day_name VARCHAR(50) COMMENT '当天名称',
    description TEXT COMMENT '训练描述',
    warm_up TEXT COMMENT '热身内容',
    cool_down TEXT COMMENT '放松内容',
    estimated_duration INT COMMENT '预计时长(分钟)',
    target_calories INT COMMENT '目标消耗卡路里',
    rest_time INT COMMENT '组间休息时间(秒)',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (training_plan_id) REFERENCES training_plans(id) ON DELETE CASCADE,
    INDEX idx_training_plan_id (training_plan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='计划每日安排表';

-- 运动动作表
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    plan_day_id INT NOT NULL COMMENT '计划日ID',
    name VARCHAR(100) NOT NULL COMMENT '动作名称',
    description TEXT COMMENT '动作描述',
    video_url VARCHAR(255) COMMENT '演示视频URL',
    image_url VARCHAR(255) COMMENT '演示图片URL',
    exercise_type VARCHAR(50) NOT NULL COMMENT '动作类型',
    muscle_group ENUM('chest', 'back', 'shoulders', 'arms', 'legs', 'core', 'cardio', 'full_body') NOT NULL COMMENT '目标肌群',
    equipment VARCHAR(50) COMMENT '所需器械',
    order_number INT NOT NULL COMMENT '顺序',
    sets INT COMMENT '组数',
    reps INT COMMENT '每组次数',
    duration INT COMMENT '持续时间(秒)',
    weight INT COMMENT '建议重量(kg)',
    rest_time INT COMMENT '休息时间(秒)',
    difficulty ENUM('beginner', 'intermediate', 'advanced') COMMENT '难度等级',
    calories_per_set INT COMMENT '每组消耗卡路里',
    key_points JSON COMMENT '动作要点',
    common_mistakes JSON COMMENT '常见错误',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (plan_day_id) REFERENCES plan_days(id) ON DELETE CASCADE,
    INDEX idx_plan_day_id (plan_day_id),
    INDEX idx_name (name),
    INDEX idx_muscle_group (muscle_group),
    INDEX idx_exercise_type (exercise_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='运动动作表';

-- ============================================
-- 4. 运动记录相关表
-- ============================================

-- 运动记录表
CREATE TABLE IF NOT EXISTS workout_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    training_plan_id INT COMMENT '训练计划ID',
    plan_day_id INT COMMENT '计划日ID',
    workout_date DATE NOT NULL COMMENT '运动日期',
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME COMMENT '结束时间',
    duration INT COMMENT '持续时间(分钟)',
    total_calories INT DEFAULT 0 COMMENT '总消耗卡路里',
    avg_heart_rate INT COMMENT '平均心率',
    max_heart_rate INT COMMENT '最大心率',
    feeling ENUM('excellent', 'good', 'normal', 'tired', 'exhausted') COMMENT '感觉',
    notes TEXT COMMENT '备注',
    location VARCHAR(100) COMMENT '运动地点',
    weather VARCHAR(50) COMMENT '天气',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (training_plan_id) REFERENCES training_plans(id) ON DELETE SET NULL,
    FOREIGN KEY (plan_day_id) REFERENCES plan_days(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_training_plan_id (training_plan_id),
    INDEX idx_workout_date (workout_date),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='运动记录表';

-- 动作记录表
CREATE TABLE IF NOT EXISTS exercise_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    workout_record_id INT NOT NULL COMMENT '运动记录ID',
    exercise_id INT COMMENT '动作ID',
    exercise_name VARCHAR(100) NOT NULL COMMENT '动作名称',
    exercise_type VARCHAR(50) COMMENT '动作类型',
    muscle_group VARCHAR(50) COMMENT '目标肌群',
    order_number INT NOT NULL COMMENT '顺序',
    total_sets INT DEFAULT 0 COMMENT '总组数',
    completed_sets INT DEFAULT 0 COMMENT '完成组数',
    total_reps INT DEFAULT 0 COMMENT '总次数',
    total_weight INT DEFAULT 0 COMMENT '总重量(kg)',
    total_duration INT DEFAULT 0 COMMENT '总时长(秒)',
    calories INT DEFAULT 0 COMMENT '消耗卡路里',
    avg_heart_rate INT COMMENT '平均心率',
    max_heart_rate INT COMMENT '最大心率',
    notes TEXT COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (workout_record_id) REFERENCES workout_records(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE SET NULL,
    INDEX idx_workout_record_id (workout_record_id),
    INDEX idx_exercise_id (exercise_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动作记录表';

-- 组记录表
CREATE TABLE IF NOT EXISTS set_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    exercise_record_id INT NOT NULL COMMENT '动作记录ID',
    set_number INT NOT NULL COMMENT '组号',
    reps INT COMMENT '次数',
    weight DECIMAL(6,2) COMMENT '重量(kg)',
    duration INT COMMENT '持续时间(秒)',
    rest_time INT COMMENT '休息时间(秒)',
    distance DECIMAL(8,2) COMMENT '距离(米)',
    calories INT COMMENT '消耗卡路里',
    heart_rate INT COMMENT '心率',
    feeling ENUM('excellent', 'good', 'normal', 'tired', 'exhausted') COMMENT '感觉',
    notes TEXT COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (exercise_record_id) REFERENCES exercise_records(id) ON DELETE CASCADE,
    INDEX idx_exercise_record_id (exercise_record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='组记录表';

-- ============================================
-- 5. 课程系统相关表
-- ============================================

-- 课程表
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '课程ID',
    title VARCHAR(200) NOT NULL COMMENT '课程标题',
    description TEXT COMMENT '课程描述',
    cover_image VARCHAR(255) COMMENT '封面图片',
    instructor_id INT NOT NULL COMMENT '讲师ID',
    category VARCHAR(50) COMMENT '课程分类',
    difficulty ENUM('beginner', 'intermediate', 'advanced') NOT NULL COMMENT '难度等级',
    duration INT COMMENT '总时长(分钟)',
    price DECIMAL(10,2) DEFAULT 0.00 COMMENT '价格',
    is_free BOOLEAN DEFAULT FALSE COMMENT '是否免费',
    is_published BOOLEAN DEFAULT FALSE COMMENT '是否发布',
    published_at DATETIME COMMENT '发布时间',
    enrollment_count INT DEFAULT 0 COMMENT '报名人数',
    completion_count INT DEFAULT 0 COMMENT '完成人数',
    rating DECIMAL(3,2) DEFAULT 0.00 COMMENT '评分',
    review_count INT DEFAULT 0 COMMENT '评论数',
    view_count INT DEFAULT 0 COMMENT '浏览量',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_instructor_id (instructor_id),
    INDEX idx_category (category),
    INDEX idx_difficulty (difficulty),
    INDEX idx_is_published (is_published)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- 章节表
CREATE TABLE IF NOT EXISTS chapters (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '章节ID',
    course_id INT NOT NULL COMMENT '课程ID',
    title VARCHAR(200) NOT NULL COMMENT '章节标题',
    description TEXT COMMENT '章节描述',
    order_number INT NOT NULL COMMENT '顺序',
    duration INT COMMENT '时长(分钟)',
    is_free BOOLEAN DEFAULT FALSE COMMENT '是否免费',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_course_id (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='章节表';

-- 视频表
CREATE TABLE IF NOT EXISTS videos (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '视频ID',
    chapter_id INT NOT NULL COMMENT '章节ID',
    title VARCHAR(200) NOT NULL COMMENT '视频标题',
    description TEXT COMMENT '视频描述',
    video_url VARCHAR(255) NOT NULL COMMENT '视频URL',
    thumbnail VARCHAR(255) COMMENT '缩略图',
    duration INT NOT NULL COMMENT '时长(秒)',
    order_number INT NOT NULL COMMENT '顺序',
    is_free BOOLEAN DEFAULT FALSE COMMENT '是否免费',
    view_count INT DEFAULT 0 COMMENT '播放量',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
    INDEX idx_chapter_id (chapter_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='视频表';

-- 课程分类表
CREATE TABLE IF NOT EXISTS course_categories (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
    description TEXT COMMENT '分类描述',
    icon VARCHAR(255) COMMENT '图标',
    parent_id INT COMMENT '父分类ID',
    order_number INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_parent_id (parent_id),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程分类表';

-- 课程标签表
CREATE TABLE IF NOT EXISTS course_tags (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '标签ID',
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '标签名称',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_usage_count (usage_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程标签表';

-- 课程标签关系表
CREATE TABLE IF NOT EXISTS course_tag_relations (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    course_id INT NOT NULL COMMENT '课程ID',
    tag_id INT NOT NULL COMMENT '标签ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES course_tags(id) ON DELETE CASCADE,
    UNIQUE KEY uk_course_tag (course_id, tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程标签关系表';

-- 学习进度表
CREATE TABLE IF NOT EXISTS learning_progress (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    course_id INT NOT NULL COMMENT '课程ID',
    chapter_id INT COMMENT '章节ID',
    video_id INT COMMENT '视频ID',
    progress INT DEFAULT 0 COMMENT '进度百分比',
    last_position INT DEFAULT 0 COMMENT '最后观看位置(秒)',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_course_id (course_id),
    UNIQUE KEY uk_user_video (user_id, video_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习进度表';

-- 课程报名表
CREATE TABLE IF NOT EXISTS course_enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    course_id INT NOT NULL COMMENT '课程ID',
    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
    expires_at DATETIME COMMENT '过期时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否有效',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_course_id (course_id),
    UNIQUE KEY uk_user_course (user_id, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程报名表';

-- ============================================
-- 6. 社交系统相关表
-- ============================================

-- 关注关系表
CREATE TABLE IF NOT EXISTS follows (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    follower_id INT NOT NULL COMMENT '关注者ID',
    following_id INT NOT NULL COMMENT '被关注者ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_follower_id (follower_id),
    INDEX idx_following_id (following_id),
    UNIQUE KEY uk_follower_following (follower_id, following_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='关注关系表';

-- 点赞表
CREATE TABLE IF NOT EXISTS likes (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    target_type VARCHAR(50) NOT NULL COMMENT '目标类型',
    target_id INT NOT NULL COMMENT '目标ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_target (target_type, target_id),
    UNIQUE KEY uk_user_target (user_id, target_type, target_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='点赞表';

-- 评论表
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评论ID',
    user_id INT NOT NULL COMMENT '用户ID',
    target_type VARCHAR(50) NOT NULL COMMENT '目标类型',
    target_id INT NOT NULL COMMENT '目标ID',
    parent_id INT COMMENT '父评论ID',
    content TEXT NOT NULL COMMENT '评论内容',
    like_count INT DEFAULT 0 COMMENT '点赞数',
    reply_count INT DEFAULT 0 COMMENT '回复数',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_target (target_type, target_id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- 动态表
CREATE TABLE IF NOT EXISTS feeds (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '动态ID',
    user_id INT NOT NULL COMMENT '用户ID',
    content TEXT NOT NULL COMMENT '动态内容',
    images JSON COMMENT '图片列表',
    video_url VARCHAR(255) COMMENT '视频URL',
    location VARCHAR(100) COMMENT '位置',
    workout_record_id INT COMMENT '关联运动记录ID',
    visibility ENUM('public', 'friends', 'private') DEFAULT 'public' COMMENT '可见性',
    like_count INT DEFAULT 0 COMMENT '点赞数',
    comment_count INT DEFAULT 0 COMMENT '评论数',
    share_count INT DEFAULT 0 COMMENT '分享数',
    view_count INT DEFAULT 0 COMMENT '浏览量',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (workout_record_id) REFERENCES workout_records(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_workout_record_id (workout_record_id),
    INDEX idx_created_at (created_at),
    INDEX idx_visibility (visibility)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动态表';

-- 话题标签表
CREATE TABLE IF NOT EXISTS hashtags (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '标签ID',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '标签名称',
    description TEXT COMMENT '标签描述',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    follow_count INT DEFAULT 0 COMMENT '关注数',
    is_trending BOOLEAN DEFAULT FALSE COMMENT '是否热门',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_usage_count (usage_count),
    INDEX idx_is_trending (is_trending)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='话题标签表';

-- 成就表
CREATE TABLE IF NOT EXISTS achievements (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '成就ID',
    name VARCHAR(100) NOT NULL COMMENT '成就名称',
    description TEXT COMMENT '成就描述',
    icon VARCHAR(255) COMMENT '成就图标',
    category VARCHAR(50) COMMENT '成就分类',
    requirement JSON COMMENT '达成要求',
    reward_points INT DEFAULT 0 COMMENT '奖励积分',
    difficulty ENUM('easy', 'normal', 'hard', 'legend') DEFAULT 'normal' COMMENT '难度',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成就表';

-- 用户成就表
CREATE TABLE IF NOT EXISTS user_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    achievement_id INT NOT NULL COMMENT '成就ID',
    progress INT DEFAULT 0 COMMENT '进度百分比',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '是否完成',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_achievement_id (achievement_id),
    UNIQUE KEY uk_user_achievement (user_id, achievement_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户成就表';

-- ============================================
-- 7. 通知系统相关表
-- ============================================

-- 通知表
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '通知ID',
    user_id INT NOT NULL COMMENT '用户ID',
    type VARCHAR(50) NOT NULL COMMENT '通知类型',
    title VARCHAR(200) NOT NULL COMMENT '通知标题',
    content TEXT COMMENT '通知内容',
    data JSON COMMENT '附加数据',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    read_at DATETIME COMMENT '阅读时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知表';

-- 私信表
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID',
    sender_id INT NOT NULL COMMENT '发送者ID',
    receiver_id INT NOT NULL COMMENT '接收者ID',
    content TEXT NOT NULL COMMENT '消息内容',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    read_at DATETIME COMMENT '阅读时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sender_id (sender_id),
    INDEX idx_receiver_id (receiver_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='私信表';

-- ============================================
-- 8. 身体数据相关表
-- ============================================

-- 体重记录表
CREATE TABLE IF NOT EXISTS weight_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    weight DECIMAL(5,2) NOT NULL COMMENT '体重(kg)',
    bmi DECIMAL(4,2) COMMENT 'BMI指数',
    body_fat_rate DECIMAL(4,2) COMMENT '体脂率(%)',
    muscle_mass DECIMAL(5,2) COMMENT '肌肉量(kg)',
    record_date DATE NOT NULL COMMENT '记录日期',
    notes TEXT COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_record_date (record_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='体重记录表';

-- 身体围度表
CREATE TABLE IF NOT EXISTS body_measurements (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    chest DECIMAL(5,2) COMMENT '胸围(cm)',
    waist DECIMAL(5,2) COMMENT '腰围(cm)',
    hips DECIMAL(5,2) COMMENT '臀围(cm)',
    left_arm DECIMAL(5,2) COMMENT '左臂围(cm)',
    right_arm DECIMAL(5,2) COMMENT '右臂围(cm)',
    left_thigh DECIMAL(5,2) COMMENT '左腿围(cm)',
    right_thigh DECIMAL(5,2) COMMENT '右腿围(cm)',
    left_calf DECIMAL(5,2) COMMENT '左小腿围(cm)',
    right_calf DECIMAL(5,2) COMMENT '右小腿围(cm)',
    record_date DATE NOT NULL COMMENT '记录日期',
    notes TEXT COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_record_date (record_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='身体围度表';

-- 综合身体数据表
CREATE TABLE IF NOT EXISTS body_data (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    data_type VARCHAR(50) NOT NULL COMMENT '数据类型',
    value DECIMAL(10,2) NOT NULL COMMENT '数值',
    unit VARCHAR(20) COMMENT '单位',
    record_date DATE NOT NULL COMMENT '记录日期',
    notes TEXT COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_data_type (data_type),
    INDEX idx_record_date (record_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='综合身体数据表';

-- ============================================
-- 数据库初始化完成
-- ============================================

-- 显示所有表
SHOW TABLES;

-- 显示数据库信息
SELECT 
    'Database initialization completed!' AS Status,
    COUNT(*) AS TotalTables 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'keep_fitness';
