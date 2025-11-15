package com.example.music.ui.player

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.PlayArrow

import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.rememberAsyncImagePainter
import com.example.music.data.PlayerState
import com.example.music.data.RepeatMode
import com.example.music.data.Song
import com.example.music.ui.theme.*
import com.example.music.viewmodel.MusicViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MusicPlayer(
    viewModel: MusicViewModel,
    playerState: PlayerState,
    modifier: Modifier = Modifier
) {
    val currentSong = playerState.currentSong
    
    if (currentSong == null) return
    
    Column(
        modifier = modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(
                        PlayerBackground,
                        BackgroundDark
                    )
                )
            )
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // 歌曲封面
        Box(
            modifier = Modifier
                .size(320.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(SurfaceLight),
            contentAlignment = Alignment.Center
        ) {
            Image(
                painter = rememberAsyncImagePainter(currentSong.coverUrl),
                contentDescription = currentSong.title,
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop
            )
            
            // 播放状态覆盖层
            if (!playerState.isPlaying) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.3f)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = "Paused",
                        tint = Color.White,
                        modifier = Modifier.size(64.dp)
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // 歌曲信息
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = currentSong.title,
                color = TextPrimary,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            
            Text(
                text = currentSong.artist,
                color = TextSecondary,
                fontSize = 18.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(top = 8.dp)
            )
            
            Text(
                text = currentSong.album,
                color = TextTertiary,
                fontSize = 14.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(top = 4.dp)
            )
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // 进度条
        Column {
            Slider(
                value = playerState.currentPosition.toFloat(),
                onValueChange = { viewModel.seekTo(it.toLong()) },
                valueRange = 0f..playerState.duration.toFloat(),
                modifier = Modifier.fillMaxWidth(),
                colors = SliderDefaults.colors(
                    thumbColor = PrimaryBlue,
                    activeTrackColor = PrimaryBlue,
                    inactiveTrackColor = ProgressBarBackground
                )
            )
            
            // 时间显示
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = formatTime(playerState.currentPosition),
                    color = TextSecondary,
                    fontSize = 12.sp
                )
                Text(
                    text = formatTime(playerState.duration),
                    color = TextSecondary,
                    fontSize = 12.sp
                )
            }
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // 播放控制按钮
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 随机播放按钮
            Button(
                onClick = { viewModel.toggleShuffle() },
                modifier = Modifier.size(48.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (playerState.isShuffled) PrimaryBlue else Color.Transparent
                )
            ) {
                Text(
                    text = "🔀",
                    fontSize = 20.sp,
                    color = if (playerState.isShuffled) Color.White else TextSecondary
                )
            }
            
            // 上一首
            Button(
                onClick = { viewModel.previousSong() },
                modifier = Modifier.size(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent
                )
            ) {
                Text(
                    text = "⏮",
                    fontSize = 24.sp,
                    color = TextPrimary
                )
            }
            
            // 播放/暂停
            FloatingActionButton(
                onClick = { viewModel.togglePlayPause() },
                modifier = Modifier.size(72.dp),
                containerColor = PrimaryBlue,
                contentColor = Color.White
            ) {
                if (playerState.isPlaying) {
                    Text(
                        text = "⏸",
                        fontSize = 36.sp,
                        color = Color.White
                    )
                } else {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = "Play",
                        modifier = Modifier.size(36.dp)
                    )
                }
            }
            
            // 下一首
            Button(
                onClick = { viewModel.nextSong() },
                modifier = Modifier.size(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent
                )
            ) {
                Text(
                    text = "⏭",
                    fontSize = 24.sp,
                    color = TextPrimary
                )
            }
            
            // 重复播放
            Button(
                onClick = { viewModel.toggleRepeatMode() },
                modifier = Modifier.size(48.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (playerState.repeatMode != RepeatMode.NONE) PrimaryBlue else Color.Transparent
                )
            ) {
                val text = when (playerState.repeatMode) {
                    RepeatMode.NONE -> "🔁"
                    RepeatMode.ALL -> "🔁"
                    RepeatMode.ONE -> "🔂"
                }
                val color = if (playerState.repeatMode != RepeatMode.NONE) Color.White else TextSecondary
                Text(
                    text = text,
                    fontSize = 20.sp,
                    color = color
                )
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // 喜欢按钮
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center
        ) {
            IconButton(
                onClick = { viewModel.toggleLikeSong(currentSong) },
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    imageVector = if (currentSong.isLiked) Icons.Default.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = if (currentSong.isLiked) "Unlike" else "Like",
                    tint = if (currentSong.isLiked) AccentRed else TextSecondary,
                    modifier = Modifier.size(24.dp)
                )
            }
        }
    }
}

// 迷你播放器组件
@Composable
fun MiniPlayer(
    viewModel: MusicViewModel,
    playerState: PlayerState,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val currentSong = playerState.currentSong ?: return
    
    Card(
        modifier = modifier
            .fillMaxWidth()
            .height(64.dp),
        colors = CardDefaults.cardColors(
            containerColor = PlayerSurface
        ),
        shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 封面
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(SurfaceLight)
            ) {
                Image(
                    painter = rememberAsyncImagePainter(currentSong.coverUrl),
                    contentDescription = currentSong.title,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            }
            
            // 歌曲信息
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 12.dp)
            ) {
                Text(
                    text = currentSong.title,
                    color = TextPrimary,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                
                Text(
                    text = currentSong.artist,
                    color = TextSecondary,
                    fontSize = 12.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
            
            // 播放按钮
            IconButton(
                onClick = { viewModel.togglePlayPause() },
                modifier = Modifier.size(40.dp)
            ) {
                if (playerState.isPlaying) {
                    Text(
                        text = "⏸",
                        fontSize = 20.sp,
                        color = TextPrimary
                    )
                } else {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = "Play",
                        tint = TextPrimary,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }
    }
}

// 格式化时间的工具函数
private fun formatTime(timeMs: Long): String {
    val totalSeconds = timeMs / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d", minutes, seconds)
} 