package com.example.music

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.music.ui.navigation.BottomNavItem
import com.example.music.ui.navigation.MusicBottomNavigation
import com.example.music.ui.navigation.Routes
import com.example.music.ui.player.MiniPlayer
import com.example.music.ui.player.MusicPlayer
import com.example.music.ui.screen.FavoriteScreen
import com.example.music.ui.screen.HomeScreen
import com.example.music.ui.screen.ProfileScreen
import com.example.music.ui.screen.SearchScreen
import com.example.music.ui.screen.SettingsScreen
import com.example.music.ui.theme.BackgroundDark
import com.example.music.ui.theme.MusicTheme
import com.example.music.viewmodel.MusicViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MusicTheme {
                MusicApp()
            }
        }
    }
}

@Composable
fun MusicApp() {
    val navController = rememberNavController()
    val viewModel: MusicViewModel = viewModel()
    val playerState by viewModel.playerState.collectAsState()
    
    // 控制播放器展开状态
    var isPlayerExpanded by remember { mutableStateOf(false) }
    
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(BackgroundDark)
    ) {
        // 主界面内容
        Column(
            modifier = Modifier.fillMaxSize()
        ) {
            // 导航内容
            Box(
                modifier = Modifier.weight(1f)
            ) {
                NavigationHost(
                    navController = navController,
                    viewModel = viewModel,
                    modifier = Modifier.fillMaxSize()
                )
            }
            
            // 迷你播放器
            if (playerState.currentSong != null && !isPlayerExpanded) {
                MiniPlayer(
                    viewModel = viewModel,
                    playerState = playerState,
                    onClick = { isPlayerExpanded = true }
                )
            }
            
            // 底部导航栏 - 只在主要页面显示
            val currentRoute = navController.currentBackStackEntry?.destination?.route
            val showBottomNav = currentRoute in listOf(
                Routes.HOME, Routes.SEARCH, Routes.FAVORITE, Routes.PROFILE
            )
            
            if (showBottomNav) {
                MusicBottomNavigation(
                    navController = navController,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }
        
        // 全屏播放器
        if (isPlayerExpanded && playerState.currentSong != null) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.95f))
                    .clickable { isPlayerExpanded = false }
            ) {
                MusicPlayer(
                    viewModel = viewModel,
                    playerState = playerState,
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    }
}

@Composable
fun NavigationHost(
    navController: NavHostController,
    viewModel: MusicViewModel,
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Routes.HOME,
        modifier = modifier
    ) {
        composable(Routes.HOME) {
            HomeScreen(
                viewModel = viewModel,
                modifier = Modifier.fillMaxSize()
            )
        }
        
        composable(Routes.SEARCH) {
            SearchScreen(
                viewModel = viewModel,
                modifier = Modifier.fillMaxSize()
            )
        }
        
        composable(Routes.FAVORITE) {
            FavoriteScreen(
                viewModel = viewModel,
                modifier = Modifier.fillMaxSize()
            )
        }
        
        composable(Routes.PROFILE) {
            ProfileScreen(
                viewModel = viewModel,
                onNavigateToSettings = { 
                    navController.navigate(Routes.SETTINGS)
                },
                onNavigateToFavorites = { 
                    navController.navigate(Routes.FAVORITE)
                },
                modifier = Modifier.fillMaxSize()
            )
        }
        
        composable(Routes.SETTINGS) {
            SettingsScreen(
                onBackClick = { 
                    navController.popBackStack()
                },
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}