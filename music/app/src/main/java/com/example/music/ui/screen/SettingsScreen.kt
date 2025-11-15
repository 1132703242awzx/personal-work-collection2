package com.example.music.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Info

import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.music.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onBackClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    var darkMode by remember { mutableStateOf(true) }
    var notificationsEnabled by remember { mutableStateOf(true) }
    var autoPlay by remember { mutableStateOf(false) }
    var highQuality by remember { mutableStateOf(true) }
    
    Column(
        modifier = modifier
            .fillMaxSize()
            .background(BackgroundDark)
    ) {
        // 顶部标题栏
        TopAppBar(
            title = { 
                Text(
                    text = "设置",
                    color = TextPrimary,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
            },
            navigationIcon = {
                IconButton(onClick = onBackClick) {
                    Icon(
                        imageVector = Icons.Default.ArrowBack,
                        contentDescription = "返回",
                        tint = TextPrimary
                    )
                }
            },
            colors = TopAppBarDefaults.topAppBarColors(
                containerColor = BackgroundDark
            )
        )
        
        LazyColumn(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // 外观设置
            item {
                SettingsSection(title = "外观设置") {
                    SettingsItem(
                        icon = Icons.Default.Settings,
                        title = "深色模式",
                        subtitle = "开启深色主题界面",
                        trailing = {
                            Switch(
                                checked = darkMode,
                                onCheckedChange = { darkMode = it },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = PrimaryBlue,
                                    checkedTrackColor = PrimaryBlueLight
                                )
                            )
                        }
                    )
                    
                    SettingsItem(
                        icon = Icons.Default.Settings,
                        title = "主题颜色",
                        subtitle = "选择应用主题色彩",
                        onClick = { /* TODO: 主题选择 */ }
                    )
                    
                    SettingsItem(
                        icon = Icons.Default.Phone,
                        title = "语言设置",
                        subtitle = "简体中文",
                        onClick = { /* TODO: 语言选择 */ }
                    )
                }
            }
            
            // 播放设置
            item {
                SettingsSection(title = "播放设置") {
                    SettingsItem(
                        icon = Icons.Default.Settings,
                        title = "自动播放",
                        subtitle = "启动时自动播放音乐",
                        trailing = {
                            Switch(
                                checked = autoPlay,
                                onCheckedChange = { autoPlay = it },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = PrimaryBlue,
                                    checkedTrackColor = PrimaryBlueLight
                                )
                            )
                        }
                    )
                    
                    SettingsItem(
                        icon = Icons.Default.Settings,
                        title = "音质设置",
                        subtitle = if (highQuality) "高品质" else "标准品质",
                        trailing = {
                            Switch(
                                checked = highQuality,
                                onCheckedChange = { highQuality = it },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = PrimaryBlue,
                                    checkedTrackColor = PrimaryBlueLight
                                )
                            )
                        }
                    )
                    
                    SettingsItem(
                        icon = Icons.Default.Settings,
                        title = "缓存设置",
                        subtitle = "管理音乐缓存和下载",
                        onClick = { /* TODO: 缓存设置 */ }
                    )
                }
            }
            
            // 通知设置
            item {
                SettingsSection(title = "通知设置") {
                    SettingsItem(
                        icon = Icons.Default.Notifications,
                        title = "推送通知",
                        subtitle = "接收音乐推荐和更新通知",
                        trailing = {
                            Switch(
                                checked = notificationsEnabled,
                                onCheckedChange = { notificationsEnabled = it },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = PrimaryBlue,
                                    checkedTrackColor = PrimaryBlueLight
                                )
                            )
                        }
                    )
                }
            }
            
            // 关于部分
            item {
                SettingsSection(title = "关于") {
                    SettingsItem(
                        icon = Icons.Default.Info,
                        title = "版本信息",
                        subtitle = "云音乐 v1.0.0",
                        onClick = { /* TODO: 版本信息 */ }
                    )
                    
                    SettingsItem(
                        icon = Icons.Default.Info,
                        title = "用户协议",
                        subtitle = "查看用户协议和隐私政策",
                        onClick = { /* TODO: 用户协议 */ }
                    )
                }
            }
        }
    }
}

@Composable
fun SettingsSection(
    title: String,
    content: @Composable () -> Unit
) {
    Column {
        Text(
            text = title,
            color = TextPrimary,
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            modifier = Modifier.padding(vertical = 8.dp)
        )
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = CardBackground
            ),
            shape = RoundedCornerShape(12.dp)
        ) {
            content()
        }
    }
}

@Composable
fun SettingsItem(
    icon: ImageVector,
    title: String,
    subtitle: String,
    trailing: @Composable (() -> Unit)? = null,
    onClick: (() -> Unit)? = null,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clickable(enabled = onClick != null) { onClick?.invoke() }
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = title,
            tint = PrimaryBlue,
            modifier = Modifier.size(24.dp)
        )
        
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(horizontal = 16.dp)
        ) {
            Text(
                text = title,
                color = TextPrimary,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium
            )
            
            Text(
                text = subtitle,
                color = TextSecondary,
                fontSize = 14.sp,
                modifier = Modifier.padding(top = 2.dp)
            )
        }
        
        trailing?.invoke()
    }
} 