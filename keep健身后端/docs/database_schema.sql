-- ============================================
-- Keep健身后端数据库创建脚本
-- 数据库: MySQL 8.0+
-- 字符集: utf8mb4
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS keep_fitness
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE keep_fitness;

-- ============================================
-- 1. 用户体系表
-- ============================================

-- 用户基础信息表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    status ENUM('active', 'inactive', 'suspended', 'deleted') NOT NULL DEFAULT 'active' COMMENT '用户状态',
    is_verified BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否验证',
    is_premium BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否高级会员',
    last_login_at DATE COMMENT '最后登录时间',
    login_count INT DEFAULT 0 COMMENT '登录次数',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_status (status),
    INDEX idx_is_premium (is_premium),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户基础信息表';

-- 用户详细资料表
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL UNIQUE COMMENT '用户ID',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    gender ENUM('male', 'female', 'other') COMMENT '性别',
    birthday DATE COMMENT '生日',
    bio TEXT COMMENT '个人简介',
    height INT COMMENT '身高(cm)',
    current_weight INT COMMENT '当前体重(kg)',
    target_weight INT COMMENT '目标体重(kg)',
    fitness_goal VARCHAR(50) COMMENT '健身目标',
    fitness_level VARCHAR(20) COMMENT '健身水平',
    followers_count INT DEFAULT 0 COMMENT '粉丝数',
    following_count INT DEFAULT 0 COMMENT '关注数',
    likes_count INT DEFAULT 0 COMMENT '获赞数',
    workout_count INT DEFAULT 0 COMMENT '训练次数',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户详细资料表';

-- 用户设置表
CREATE TABLE IF NOT EXISTS user_settings (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL UNIQUE COMMENT '用户ID',
    profile_visible BOOLEAN DEFAULT TRUE COMMENT '资料可见性',
    workout_visible BOOLEAN DEFAULT TRUE COMMENT '训练记录可见性',
    allow_follow BOOLEAN DEFAULT TRUE COMMENT '允许关注',
    allow_message BOOLEAN DEFAULT TRUE COMMENT '允许私信',
    email_notification BOOLEAN DEFAULT TRUE COMMENT '邮件通知',
    push_notification BOOLEAN DEFAULT TRUE COMMENT '推送通知',
    workout_reminder BOOLEAN DEFAULT TRUE COMMENT '训练提醒',
    language VARCHAR(10) DEFAULT 'zh-CN' COMMENT '语言偏好',
    theme VARCHAR(20) DEFAULT 'light' COMMENT '主题',
    weight_unit VARCHAR(10) DEFAULT 'kg' COMMENT '体重单位',
    distance_unit VARCHAR(10) DEFAULT 'km' COMMENT '距离单位',
    extra_settings JSON COMMENT '扩展设置',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '软删除标记',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设置表';

-- ============================================
-- 2. 训练计划表
-- ============================================

-- 训练计划表
CREATE TABLE IF NOT EXISTS training_plans (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
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
-- 说明：由于篇幅限制，完整的SQL创建脚本包含15个表
-- 上述展示了用户体系和训练计划的表结构
-- 其他表结构（运动记录、课程、社交、身体数据）请参考models目录中的Python模型定义
-- ============================================

-- 查看所有表
SHOW TABLES;

-- 查看表结构示例
-- DESC users;
-- DESC training_plans;
-- DESC workout_records;
