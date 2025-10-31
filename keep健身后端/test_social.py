#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Keep健身后端 - 社交系统交互式测试工具

功能:
1. 关注/取消关注用户
2. 发布各类动态(训练/图文/视频)
3. 浏览时间线和探索页
4. 点赞和评论互动
5. 查看和管理通知
6. 私信发送
7. 成就和标签功能

使用方法:
    python test_social.py
"""

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

# API配置
BASE_URL = "http://localhost:5000/api"
TOKEN = None  # 登录后自动获取


class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """打印标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}\n")


def print_success(text: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text: str):
    """打印信息"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def print_warning(text: str):
    """打印警告"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def get_headers() -> Dict[str, str]:
    """获取请求头"""
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def print_json(data: Any, indent: int = 2):
    """格式化打印JSON"""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def login():
    """用户登录"""
    global TOKEN
    print_header("用户登录")
    
    username = input("请输入用户名: ").strip()
    password = input("请输入密码: ").strip()
    
    if not username or not password:
        print_error("用户名和密码不能为空")
        return False
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data["data"]["token"]
            user_info = data["data"]["user"]
            print_success(f"登录成功! 欢迎 {user_info['nickname']} (@{user_info['username']})")
            return True
        else:
            print_error(f"登录失败: {response.json().get('message', '未知错误')}")
            return False
    except Exception as e:
        print_error(f"登录异常: {str(e)}")
        return False


def register():
    """用户注册"""
    print_header("用户注册")
    
    username = input("请输入用户名: ").strip()
    password = input("请输入密码: ").strip()
    nickname = input("请输入昵称: ").strip()
    
    if not all([username, password, nickname]):
        print_error("所有字段都不能为空")
        return False
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "username": username,
                "password": password,
                "nickname": nickname
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print_success("注册成功! 请登录")
            return True
        else:
            print_error(f"注册失败: {response.json().get('message', '未知错误')}")
            return False
    except Exception as e:
        print_error(f"注册异常: {str(e)}")
        return False


def follow_user():
    """关注用户"""
    print_header("关注用户")
    
    user_id = input("请输入要关注的用户ID: ").strip()
    group_tag = input("分组标签(可选): ").strip() or None
    remark = input("备注名称(可选): ").strip() or None
    
    if not user_id.isdigit():
        print_error("用户ID必须是数字")
        return
    
    try:
        data = {"following_id": int(user_id)}
        if group_tag:
            data["group_tag"] = group_tag
        if remark:
            data["remark"] = remark
        
        response = requests.post(
            f"{BASE_URL}/social/follow",
            json=data,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("关注成功!")
            print_json(result["data"])
        else:
            print_error(f"关注失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"关注异常: {str(e)}")


def unfollow_user():
    """取消关注"""
    print_header("取消关注")
    
    user_id = input("请输入要取消关注的用户ID: ").strip()
    
    if not user_id.isdigit():
        print_error("用户ID必须是数字")
        return
    
    try:
        response = requests.post(
            f"{BASE_URL}/social/unfollow/{user_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            print_success("取消关注成功!")
        else:
            print_error(f"取消关注失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"取消关注异常: {str(e)}")


def view_following():
    """查看关注列表"""
    print_header("我的关注")
    
    page = input("页码(默认1): ").strip() or "1"
    per_page = input("每页数量(默认20): ").strip() or "20"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/following?page={page}&per_page={per_page}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"共关注 {data['total']} 人, 当前第 {data['page']}/{data['pages']} 页")
            
            for item in data["items"]:
                user = item["following"]
                mutual = "✓ 互相关注" if item["is_mutual"] else ""
                remark = f" ({item['remark']})" if item.get("remark") else ""
                print(f"\n{Colors.BOLD}@{user['username']}{Colors.END} - {user['nickname']}{remark} {mutual}")
                if item.get("group_tag"):
                    print(f"  分组: {item['group_tag']}")
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def view_followers():
    """查看粉丝列表"""
    print_header("我的粉丝")
    
    page = input("页码(默认1): ").strip() or "1"
    per_page = input("每页数量(默认20): ").strip() or "20"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/followers?page={page}&per_page={per_page}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"共 {data['total']} 位粉丝, 当前第 {data['page']}/{data['pages']} 页")
            
            for item in data["items"]:
                user = item["follower"]
                mutual = "✓ 互相关注" if item["is_mutual"] else ""
                print(f"\n{Colors.BOLD}@{user['username']}{Colors.END} - {user['nickname']} {mutual}")
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def create_feed():
    """发布动态"""
    print_header("发布动态")
    
    print("动态类型:")
    print("1. workout - 训练分享")
    print("2. achievement - 成就分享")
    print("3. photo - 图文动态")
    print("4. text - 纯文字")
    print("5. video - 视频动态")
    
    type_map = {"1": "workout", "2": "achievement", "3": "photo", "4": "text", "5": "video"}
    feed_type = type_map.get(input("请选择类型(1-5): ").strip())
    
    if not feed_type:
        print_error("类型选择无效")
        return
    
    content = input("请输入内容: ").strip()
    if not content:
        print_error("内容不能为空")
        return
    
    data = {
        "feed_type": feed_type,
        "content": content,
        "visibility": "public"
    }
    
    # 根据类型添加额外字段
    if feed_type == "workout":
        workout_id = input("关联训练记录ID(可选): ").strip()
        if workout_id and workout_id.isdigit():
            data["workout_record_id"] = int(workout_id)
    
    if feed_type in ["photo", "video"]:
        images = input("图片URLs(逗号分隔,可选): ").strip()
        if images:
            data["images"] = [url.strip() for url in images.split(",")]
        
        if feed_type == "video":
            video = input("视频URL(可选): ").strip()
            if video:
                data["video_url"] = video
    
    # 通用字段
    hashtags = input("话题标签(逗号分隔,可选,如:#跑步,#减脂): ").strip()
    if hashtags:
        data["hashtags"] = [tag.strip() for tag in hashtags.split(",")]
    
    location = input("位置(可选): ").strip()
    if location:
        data["location"] = location
    
    print("\n可见性:")
    print("1. public - 公开")
    print("2. friends - 好友可见")
    print("3. private - 私密")
    visibility_map = {"1": "public", "2": "friends", "3": "private"}
    visibility = visibility_map.get(input("请选择可见性(1-3,默认1): ").strip() or "1", "public")
    data["visibility"] = visibility
    
    try:
        response = requests.post(
            f"{BASE_URL}/social/feeds",
            json=data,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("发布成功!")
            print_json(result["data"])
        else:
            print_error(f"发布失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"发布异常: {str(e)}")


def view_timeline():
    """查看时间线"""
    print_header("动态时间线")
    
    page = input("页码(默认1): ").strip() or "1"
    per_page = input("每页数量(默认10): ").strip() or "10"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/timeline?page={page}&per_page={per_page}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"共 {data['total']} 条动态, 当前第 {data['page']}/{data['pages']} 页\n")
            
            for feed in data["items"]:
                print_feed(feed)
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def view_explore():
    """浏览探索页"""
    print_header("探索热门")
    
    page = input("页码(默认1): ").strip() or "1"
    per_page = input("每页数量(默认10): ").strip() or "10"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/explore?page={page}&per_page={per_page}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"共 {data['total']} 条热门动态, 当前第 {data['page']} 页\n")
            
            for feed in data["items"]:
                print_feed(feed)
                if "hot_score" in feed:
                    print(f"  {Colors.YELLOW}🔥 热度: {feed['hot_score']:.1f}{Colors.END}")
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def print_feed(feed: Dict):
    """打印动态信息"""
    user = feed.get("user", {})
    print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"{Colors.CYAN}@{user.get('username', 'Unknown')}{Colors.END} - {user.get('nickname', '')}")
    print(f"ID: {feed['id']} | 类型: {feed['feed_type']} | 可见性: {feed.get('visibility', 'public')}")
    print(f"\n{feed['content']}\n")
    
    if feed.get("images"):
        print(f"📷 图片: {len(feed['images'])}张")
    
    if feed.get("video_url"):
        print(f"🎬 视频: {feed['video_url']}")
    
    if feed.get("hashtags"):
        print(f"🏷️  {' '.join(feed['hashtags'])}")
    
    if feed.get("location"):
        print(f"📍 {feed['location']}")
    
    if feed.get("workout_summary"):
        summary = feed["workout_summary"]
        print(f"\n💪 训练摘要:")
        if "duration" in summary:
            print(f"  时长: {summary['duration']}秒")
        if "calories" in summary:
            print(f"  消耗: {summary['calories']}卡")
        if "distance" in summary:
            print(f"  距离: {summary['distance']}公里")
    
    liked = "❤️" if feed.get("is_liked") else "🤍"
    print(f"\n{liked} {feed.get('likes_count', 0)} | 💬 {feed.get('comments_count', 0)} | 🔄 {feed.get('shares_count', 0)} | 👀 {feed.get('views_count', 0)}")
    print(f"🕒 {feed.get('created_at', '')}")


def toggle_like():
    """点赞/取消点赞"""
    print_header("点赞")
    
    print("目标类型:")
    print("1. feed - 动态")
    print("2. comment - 评论")
    print("3. workout_record - 训练记录")
    
    type_map = {"1": "feed", "2": "comment", "3": "workout_record"}
    target_type = type_map.get(input("请选择类型(1-3): ").strip())
    
    if not target_type:
        print_error("类型选择无效")
        return
    
    target_id = input(f"请输入{target_type}的ID: ").strip()
    if not target_id.isdigit():
        print_error("ID必须是数字")
        return
    
    try:
        response = requests.post(
            f"{BASE_URL}/social/like",
            json={"target_type": target_type, "target_id": int(target_id)},
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            action = "点赞" if data["is_liked"] else "取消点赞"
            print_success(f"{action}成功! 当前点赞数: {data['likes_count']}")
        else:
            print_error(f"操作失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"操作异常: {str(e)}")


def add_comment():
    """发表评论"""
    print_header("发表评论")
    
    print("目标类型:")
    print("1. feed - 动态")
    print("2. workout_record - 训练记录")
    
    type_map = {"1": "feed", "2": "workout_record"}
    target_type = type_map.get(input("请选择类型(1-2): ").strip())
    
    if not target_type:
        print_error("类型选择无效")
        return
    
    target_id = input(f"请输入{target_type}的ID: ").strip()
    if not target_id.isdigit():
        print_error("ID必须是数字")
        return
    
    content = input("请输入评论内容: ").strip()
    if not content:
        print_error("评论内容不能为空")
        return
    
    data = {
        "target_type": target_type,
        "target_id": int(target_id),
        "content": content
    }
    
    # 回复评论
    parent_id = input("回复评论ID(可选,一级评论留空): ").strip()
    if parent_id and parent_id.isdigit():
        data["parent_id"] = int(parent_id)
        
        reply_to = input("回复给用户ID(可选): ").strip()
        if reply_to and reply_to.isdigit():
            data["reply_to_user_id"] = int(reply_to)
    
    # @提到
    mentions = input("@提到的用户IDs(逗号分隔,可选): ").strip()
    if mentions:
        data["mentions"] = [int(uid.strip()) for uid in mentions.split(",") if uid.strip().isdigit()]
    
    try:
        response = requests.post(
            f"{BASE_URL}/social/comments",
            json=data,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("评论成功!")
            print_json(result["data"])
        else:
            print_error(f"评论失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"评论异常: {str(e)}")


def view_comments():
    """查看评论"""
    print_header("查看评论")
    
    print("目标类型:")
    print("1. feed - 动态")
    print("2. workout_record - 训练记录")
    
    type_map = {"1": "feed", "2": "workout_record"}
    target_type = type_map.get(input("请选择类型(1-2): ").strip())
    
    if not target_type:
        print_error("类型选择无效")
        return
    
    target_id = input(f"请输入{target_type}的ID: ").strip()
    if not target_id.isdigit():
        print_error("ID必须是数字")
        return
    
    order_by = input("排序方式(1-时间 2-热度,默认1): ").strip()
    order_by = "likes_count" if order_by == "2" else "created_at"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/comments?target_type={target_type}&target_id={target_id}&order_by={order_by}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"共 {data['total']} 条评论\n")
            
            for comment in data["items"]:
                print_comment(comment)
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def print_comment(comment: Dict, indent: int = 0):
    """打印评论信息"""
    prefix = "  " * indent
    user = comment.get("user", {})
    
    print(f"{prefix}{Colors.CYAN}@{user.get('username', 'Unknown')}{Colors.END}: {comment['content']}")
    print(f"{prefix}ID: {comment['id']} | 层级: {comment.get('level', 0)} | 👍 {comment.get('likes_count', 0)} | 💬 {comment.get('replies_count', 0)}")
    print(f"{prefix}🕒 {comment.get('created_at', '')}\n")


def view_notifications():
    """查看通知"""
    print_header("我的通知")
    
    # 先显示未读数
    try:
        count_response = requests.get(
            f"{BASE_URL}/social/notifications/unread-count",
            headers=get_headers()
        )
        if count_response.status_code == 200:
            unread = count_response.json()["data"]["unread_count"]
            print_info(f"未读通知: {unread} 条\n")
    except:
        pass
    
    is_read = input("查看已读通知?(y/n,默认n): ").strip().lower()
    filter_read = "" if is_read == "y" else "&is_read=false"
    
    page = input("页码(默认1): ").strip() or "1"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/notifications?page={page}&per_page=20{filter_read}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            
            if not data["items"]:
                print_info("暂无通知")
                return
            
            notification_ids = []
            for notif in data["items"]:
                print_notification(notif)
                if not notif["is_read"]:
                    notification_ids.append(notif["id"])
            
            # 询问是否标记为已读
            if notification_ids:
                mark = input("\n是否标记这些通知为已读?(y/n): ").strip().lower()
                if mark == "y":
                    mark_response = requests.post(
                        f"{BASE_URL}/social/notifications/read",
                        json={"notification_ids": notification_ids},
                        headers=get_headers()
                    )
                    if mark_response.status_code == 200:
                        print_success("已标记为已读")
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def print_notification(notif: Dict):
    """打印通知信息"""
    type_emoji = {
        "follow": "👥",
        "like": "❤️",
        "comment": "💬",
        "reply": "↩️",
        "mention": "@",
        "share": "🔄",
        "achievement": "🏆",
        "system": "📢",
        "workout_reminder": "⏰",
        "milestone": "🎯"
    }
    
    emoji = type_emoji.get(notif["type"], "🔔")
    read_status = "✓" if notif["is_read"] else "●"
    
    print(f"{Colors.BOLD}{read_status} {emoji} {notif['content']}{Colors.END}")
    
    sender = notif.get("sender")
    if sender:
        print(f"  来自: @{sender.get('username', 'Unknown')}")
    
    print(f"  类型: {notif['type']} | ID: {notif['id']}")
    print(f"  🕒 {notif.get('created_at', '')}\n")


def manage_follow():
    """关注管理菜单"""
    while True:
        print_header("关注管理")
        print("1. 关注用户")
        print("2. 取消关注")
        print("3. 我的关注")
        print("4. 我的粉丝")
        print("5. 检查关注状态")
        print("0. 返回主菜单")
        
        choice = input("\n请选择操作: ").strip()
        
        if choice == "1":
            follow_user()
        elif choice == "2":
            unfollow_user()
        elif choice == "3":
            view_following()
        elif choice == "4":
            view_followers()
        elif choice == "5":
            user_id = input("请输入用户ID: ").strip()
            if user_id.isdigit():
                check_follow_status(user_id)
        elif choice == "0":
            break
        else:
            print_error("无效的选择")


def check_follow_status(user_id: str):
    """检查关注状态"""
    try:
        response = requests.get(
            f"{BASE_URL}/social/follow-status/{user_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"\n与用户 {user_id} 的关注状态:")
            print(f"  我关注对方: {'✓' if data['is_following'] else '✗'}")
            print(f"  对方关注我: {'✓' if data['is_followed'] else '✗'}")
            print(f"  互相关注: {'✓' if data['is_mutual'] else '✗'}")
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def manage_feeds():
    """动态管理菜单"""
    while True:
        print_header("动态管理")
        print("1. 发布动态")
        print("2. 查看时间线")
        print("3. 浏览探索页")
        print("4. 查看动态详情")
        print("5. 查看用户动态")
        print("0. 返回主菜单")
        
        choice = input("\n请选择操作: ").strip()
        
        if choice == "1":
            create_feed()
        elif choice == "2":
            view_timeline()
        elif choice == "3":
            view_explore()
        elif choice == "4":
            feed_id = input("请输入动态ID: ").strip()
            if feed_id.isdigit():
                view_feed_detail(feed_id)
        elif choice == "5":
            user_id = input("请输入用户ID: ").strip()
            if user_id.isdigit():
                view_user_feeds(user_id)
        elif choice == "0":
            break
        else:
            print_error("无效的选择")


def view_feed_detail(feed_id: str):
    """查看动态详情"""
    try:
        response = requests.get(
            f"{BASE_URL}/social/feeds/{feed_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n")
            print_feed(result["data"])
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def view_user_feeds(user_id: str):
    """查看用户动态"""
    page = input("页码(默认1): ").strip() or "1"
    
    try:
        response = requests.get(
            f"{BASE_URL}/social/users/{user_id}/feeds?page={page}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print_info(f"\n用户 {user_id} 的动态 (共 {data['total']} 条)\n")
            
            for feed in data["items"]:
                print_feed(feed)
        else:
            print_error(f"获取失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"获取异常: {str(e)}")


def manage_interactions():
    """互动管理菜单"""
    while True:
        print_header("互动管理")
        print("1. 点赞/取消点赞")
        print("2. 发表评论")
        print("3. 查看评论")
        print("4. 删除评论")
        print("0. 返回主菜单")
        
        choice = input("\n请选择操作: ").strip()
        
        if choice == "1":
            toggle_like()
        elif choice == "2":
            add_comment()
        elif choice == "3":
            view_comments()
        elif choice == "4":
            comment_id = input("请输入要删除的评论ID: ").strip()
            if comment_id.isdigit():
                delete_comment(comment_id)
        elif choice == "0":
            break
        else:
            print_error("无效的选择")


def delete_comment(comment_id: str):
    """删除评论"""
    confirm = input(f"确认删除评论 {comment_id}?(y/n): ").strip().lower()
    if confirm != "y":
        print_info("已取消")
        return
    
    try:
        response = requests.delete(
            f"{BASE_URL}/social/comments/{comment_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            print_success("删除成功!")
        else:
            print_error(f"删除失败: {response.json().get('message', '未知错误')}")
    except Exception as e:
        print_error(f"删除异常: {str(e)}")


def main_menu():
    """主菜单"""
    while True:
        print_header("Keep健身 - 社交系统测试工具")
        print("1. 关注管理")
        print("2. 动态管理")
        print("3. 互动管理")
        print("4. 通知中心")
        print("5. 退出登录")
        print("0. 退出程序")
        
        choice = input("\n请选择操作: ").strip()
        
        if choice == "1":
            manage_follow()
        elif choice == "2":
            manage_feeds()
        elif choice == "3":
            manage_interactions()
        elif choice == "4":
            view_notifications()
        elif choice == "5":
            global TOKEN
            TOKEN = None
            print_success("已退出登录")
            break
        elif choice == "0":
            print_info("再见!")
            exit(0)
        else:
            print_error("无效的选择")


def main():
    """主程序"""
    print_header("欢迎使用 Keep健身 社交系统测试工具")
    
    while True:
        if not TOKEN:
            print("\n请先登录:")
            print("1. 登录")
            print("2. 注册")
            print("0. 退出")
            
            choice = input("\n请选择: ").strip()
            
            if choice == "1":
                if login():
                    main_menu()
            elif choice == "2":
                register()
            elif choice == "0":
                print_info("再见!")
                break
            else:
                print_error("无效的选择")
        else:
            main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}程序已中断{Colors.END}")
    except Exception as e:
        print_error(f"程序异常: {str(e)}")
