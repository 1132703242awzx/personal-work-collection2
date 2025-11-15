package com.example.music.ui.screen

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.music.ui.screen.SongItem
import com.example.music.ui.theme.*
import com.example.music.viewmodel.MusicViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(
    viewModel: MusicViewModel,
    modifier: Modifier = Modifier
) {
    val searchQuery by viewModel.searchQuery
    val filteredSongs by viewModel.filteredSongs
    val isSearching by viewModel.isSearching
    val playerState by viewModel.playerState.collectAsState()
    
    Column(
        modifier = modifier
            .fillMaxSize()
            .background(BackgroundDark)
            .padding(16.dp)
    ) {
        // 搜索栏
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { viewModel.searchSongs(it) },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            placeholder = { 
                Text(
                    text = "搜索歌曲、歌手、专辑",
                    color = TextSecondary
                ) 
            },
            leadingIcon = {
                Icon(
                    imageVector = Icons.Default.Search,
                    contentDescription = "Search",
                    tint = TextSecondary
                )
            },
            trailingIcon = {
                if (searchQuery.isNotEmpty()) {
                    IconButton(
                        onClick = { viewModel.clearSearch() }
                    ) {
                        Icon(
                            imageVector = Icons.Default.Close,
                            contentDescription = "Clear",
                            tint = TextSecondary
                        )
                    }
                }
            },
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = PrimaryBlue,
                unfocusedBorderColor = DividerColor,
                focusedTextColor = TextPrimary,
                unfocusedTextColor = TextPrimary,
                cursorColor = PrimaryBlue
            ),
            shape = RoundedCornerShape(12.dp)
        )
        
        // 搜索结果
        when {
            searchQuery.isEmpty() -> {
                // 空状态 - 显示搜索建议
                SearchEmptyState()
            }
            filteredSongs.isEmpty() -> {
                // 无结果状态
                NoResultsState(searchQuery)
            }
            else -> {
                // 搜索结果列表
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    item {
                        Text(
                            text = "找到 ${filteredSongs.size} 首歌曲",
                            color = TextSecondary,
                            fontSize = 14.sp,
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                    }
                    
                    items(filteredSongs) { song ->
                        SongItem(
                            song = song,
                            isPlaying = playerState.currentSong?.id == song.id && playerState.isPlaying,
                            onPlayClick = { viewModel.playSong(song) },
                            onLikeClick = { viewModel.toggleLikeSong(song) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun SearchEmptyState() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.Search,
            contentDescription = "Search",
            tint = TextTertiary,
            modifier = Modifier.size(64.dp)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "搜索你喜欢的音乐",
            color = TextPrimary,
            fontSize = 20.sp,
            fontWeight = FontWeight.Medium,
            textAlign = TextAlign.Center
        )
        
        Text(
            text = "输入歌曲名、歌手或专辑名",
            color = TextSecondary,
            fontSize = 14.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(top = 8.dp)
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // 热门搜索建议
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "热门搜索",
                color = TextPrimary,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            val hotSearches = listOf("周杰伦", "薛之谦", "张碧晨", "流行音乐", "华语经典")
            
            hotSearches.chunked(2).forEach { row ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    row.forEach { search ->
                        OutlinedButton(
                            onClick = { /* TODO: Handle hot search click */ },
                            modifier = Modifier.padding(4.dp),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = TextSecondary
                            ),
                            border = BorderStroke(
                                width = 1.dp,
                                color = DividerColor
                            )
                        ) {
                            Text(text = search)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun NoResultsState(searchQuery: String) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.Search,
            contentDescription = "No Results",
            tint = TextTertiary,
            modifier = Modifier.size(64.dp)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "没有找到相关结果",
            color = TextPrimary,
            fontSize = 20.sp,
            fontWeight = FontWeight.Medium,
            textAlign = TextAlign.Center
        )
        
        Text(
            text = "尝试使用其他关键词搜索 \"$searchQuery\"",
            color = TextSecondary,
            fontSize = 14.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(top = 8.dp)
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // 搜索建议
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "搜索建议",
                color = TextPrimary,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            val suggestions = listOf(
                "检查拼写是否正确",
                "尝试使用更简单的关键词",
                "尝试使用不同的关键词",
                "减少关键词的数量"
            )
            
            suggestions.forEach { suggestion ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "• ",
                        color = TextSecondary,
                        fontSize = 14.sp
                    )
                    Text(
                        text = suggestion,
                        color = TextSecondary,
                        fontSize = 14.sp
                    )
                }
            }
        }
    }
} 