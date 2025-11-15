package com.example.music.ui.navigation

// 导航路由定义
object Routes {
    const val HOME = "home"
    const val SEARCH = "search"
    const val FAVORITE = "favorite"
    const val PROFILE = "profile"
    const val SETTINGS = "settings"
    const val PLAYLIST_DETAIL = "playlist_detail/{playlistId}"
    const val ARTIST_DETAIL = "artist_detail/{artistId}"
    const val HISTORY = "history"
    const val ABOUT = "about"
    
    fun playlistDetail(playlistId: String) = "playlist_detail/$playlistId"
    fun artistDetail(artistId: String) = "artist_detail/$artistId"
} 