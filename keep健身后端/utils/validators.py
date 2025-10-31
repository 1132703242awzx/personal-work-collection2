"""
数据验证工具
"""
from typing import Optional, List
import re
from datetime import datetime


class Validator:
    """数据验证类"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号格式（中国）"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """验证用户名格式"""
        # 4-20位，字母数字下划线
        pattern = r'^[a-zA-Z0-9_]{4,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        # 至少8位，包含大小写字母和数字
        if len(password) < 8:
            return False
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        return has_upper and has_lower and has_digit
    
    @staticmethod
    def validate_age(birthday: datetime) -> bool:
        """验证年龄是否合法（5-120岁）"""
        today = datetime.now()
        age = today.year - birthday.year
        if age < 5 or age > 120:
            return False
        return True
    
    @staticmethod
    def validate_weight(weight: float) -> bool:
        """验证体重范围（20-300kg）"""
        return 20 <= weight <= 300
    
    @staticmethod
    def validate_height(height: int) -> bool:
        """验证身高范围（50-250cm）"""
        return 50 <= height <= 250
    
    @staticmethod
    def validate_heart_rate(heart_rate: int) -> bool:
        """验证心率范围（30-220bpm）"""
        return 30 <= heart_rate <= 220
    
    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """清理字符串"""
        if not text:
            return ""
        # 去除首尾空格
        text = text.strip()
        # 限制长度
        if max_length and len(text) > max_length:
            text = text[:max_length]
        return text
    
    @staticmethod
    def validate_enum(value: str, allowed_values: List[str]) -> bool:
        """验证枚举值"""
        return value in allowed_values
