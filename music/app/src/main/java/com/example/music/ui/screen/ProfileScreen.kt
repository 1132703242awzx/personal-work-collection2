package com.example.music.ui.screen

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.List
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.LocalContext
import android.content.Intent
import android.widget.Toast
import coil.compose.rememberAsyncImagePainter
import com.example.music.ui.theme.*
import com.example.music.viewmodel.MusicViewModel

@Composable
fun ProfileScreen(
    viewModel: MusicViewModel,
    onNavigateToSettings: () -> Unit = {},
    onNavigateToFavorites: () -> Unit = {},
    modifier: Modifier = Modifier
) {
    val songs by viewModel.songs
    val playerState by viewModel.playerState.collectAsState()
    val context = LocalContext.current
    
    // 计算统计数据
    val favoriteSongs = songs.filter { it.isLiked }
    val totalPlayTime = songs.sumOf { it.duration }
    
    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BackgroundDark)
    ) {
        // 用户信息头部
        item {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .background(
                        brush = Brush.verticalGradient(
                            colors = listOf(
                                GradientStart,
                                GradientEnd
                            )
                        )
                    )
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    // 头像
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .clip(CircleShape)
                            .background(SurfaceLight),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.AccountCircle,
                            contentDescription = "Avatar",
                            tint = TextPrimary,
                            modifier = Modifier.size(60.dp)
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // 用户名
                    Text(
                        text = "音乐爱好者",
                        color = TextPrimary,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold
                    )
                    
                    Text(
                        text = "发现生活中的美好音乐",
                        color = TextSecondary,
                        fontSize = 14.sp
                    )
                }
            }
        }
        
        // 统计信息
        item {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = CardBackground
                ),
                shape = RoundedCornerShape(16.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(20.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    StatItem(
                        title = "收藏",
                        count = favoriteSongs.size.toString(),
                        modifier = Modifier.weight(1f)
                    )
                    
                    StatItem(
                        title = "播放时长",
                        count = formatDuration(totalPlayTime),
                        modifier = Modifier.weight(1f)
                    )
                    
                    StatItem(
                        title = "歌曲",
                        count = songs.size.toString(),
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
        
        // 菜单项
        item {
            Column(
                modifier = Modifier.padding(horizontal = 16.dp)
            ) {
                Text(
                    text = "我的音乐",
                    color = TextPrimary,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(vertical = 16.dp)
                )
                
                ProfileMenuItem(
                    icon = Icons.Default.Favorite,
                    title = "我的收藏",
                    subtitle = "${favoriteSongs.size} 首歌曲",
                    onClick = onNavigateToFavorites
                )
                
                ProfileMenuItem(
                    icon = Icons.Default.List,
                    title = "创建的歌单",
                    subtitle = "2 个歌单",
                    onClick = { 
                        Toast.makeText(context, "歌单功能开发中", Toast.LENGTH_SHORT).show()
                    }
                )
                
                ProfileMenuItem(
                    icon = Icons.Default.PlayArrow,
                    title = "播放历史",
                    subtitle = "最近播放的音乐",
                    onClick = { 
                        Toast.makeText(context, "播放历史功能开发中", Toast.LENGTH_SHORT).show()
                    }
                )
            }
        }
        
        // 设置菜单
        item {
            Column(
                modifier = Modifier.padding(horizontal = 16.dp)
            ) {
                Text(
                    text = "更多",
                    color = TextPrimary,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(vertical = 16.dp)
                )
                
                ProfileMenuItem(
                    icon = Icons.Default.Settings,
                    title = "设置",
                    subtitle = "个性化设置",
                    onClick = onNavigateToSettings
                )
                
                ProfileMenuItem(
                    icon = Icons.Default.Share,
                    title = "分享应用",
                    subtitle = "推荐给朋友",
                    onClick = { 
                        try {
                            val shareIntent = Intent().apply {
                                action = Intent.ACTION_SEND
                                type = "text/plain"
                                putExtra(Intent.EXTRA_TEXT, "推荐一个很棒的音乐应用：云音乐！")
                            }
                            context.startActivity(Intent.createChooser(shareIntent, "分享应用"))
                        } catch (e: Exception) {
                            Toast.makeText(context, "分享失败", Toast.LENGTH_SHORT).show()
                        }
                    }
                )
                
                ProfileMenuItem(
                    icon = Icons.Default.Info,
                    title = "关于",
                    subtitle = "版本信息",
                    onClick = { 
                        Toast.makeText(context, "云音乐 v1.0.0\n一个精美的音乐播放器", Toast.LENGTH_LONG).show()
                    }
                )
            }
        }
        
        // 底部间距
        item {
            Spacer(modifier = Modifier.height(100.dp))
        }
    }
}

@Composable
fun StatItem(
    title: String,
    count: String,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = count,
            color = TextPrimary,
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold
        )
        
        Text(
            text = title,
            color = TextSecondary,
            fontSize = 14.sp,
            modifier = Modifier.padding(top = 4.dp)
        )
    }
}

@Composable
fun ProfileMenuItem(
    icon: ImageVector,
    title: String,
    subtitle: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable { onClick() },
        colors = CardDefaults.cardColors(
            containerColor = CardBackground
        ),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 图标
            Icon(
                imageVector = icon,
                contentDescription = title,
                tint = PrimaryBlue,
                modifier = Modifier.size(24.dp)
            )
            
            // 文本信息
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
            
            // 箭头
            Icon(
                imageVector = Icons.Default.KeyboardArrowRight,
                contentDescription = "Navigate",
                tint = TextSecondary,
                modifier = Modifier.size(20.dp)
            )
        }
    }
}

// 格式化时长
private fun formatDuration(durationMs: Long): String {
    val totalMinutes = durationMs / 60000
    val hours = totalMinutes / 60
    val minutes = totalMinutes % 60
    
    return when {
        hours > 0 -> "${hours}h ${minutes}m"
        minutes > 0 -> "${minutes}m"
        else -> "0m"
    }
} 