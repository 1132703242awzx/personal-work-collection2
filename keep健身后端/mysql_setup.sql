-- Keep健身后端 - MySQL配置脚本
-- 此脚本用于配置MySQL用户和权限

-- 方案1: 修改root密码为'password' (仅用于开发环境)
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;

-- 方案2: 创建新的数据库用户 (推荐用于生产环境)
CREATE USER IF NOT EXISTS 'keep_fitness'@'localhost' IDENTIFIED BY 'keep_fitness_2024';
GRANT ALL PRIVILEGES ON keep_fitness.* TO 'keep_fitness'@'localhost';
FLUSH PRIVILEGES;

-- 显示当前用户
SELECT User, Host FROM mysql.user WHERE User IN ('root', 'keep_fitness');
