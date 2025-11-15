package com.example.music.viewmodel

import android.app.Application
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.os.IBinder
import android.util.Log
import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.music.data.PlayerState
import com.example.music.data.PlaybackState
import com.example.music.data.RepeatMode
import com.example.music.data.Song
import com.example.music.data.SampleData
import com.example.music.service.MusicPlayerService
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MusicViewModel(application: Application) : AndroidViewModel(application) {
    
    private var musicService: MusicPlayerService? = null
    private var isBound = false
    
    private val serviceConnection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            Log.d("MusicViewModel", "音乐服务已连接")
            val binder = service as MusicPlayerService.MusicBinder
            musicService = binder.getService()
            isBound = true
            
            // 监听服务状态变化
            viewModelScope.launch {
                musicService?.isPlaying?.collect { playing ->
                    Log.d("MusicViewModel", "播放状态变化: $playing")
                    val currentState = _playerState.value
                    _playerState.value = currentState.copy(
                        isPlaying = playing,
                        playbackState = if (playing) PlaybackState.PLAYING else PlaybackState.PAUSED
                    )
                }
            }
            
            viewModelScope.launch {
                musicService?.currentSong?.collect { song ->
                    song?.let {
                        Log.d("MusicViewModel", "当前歌曲变化: ${it.title}")
                        val currentState = _playerState.value
                        _playerState.value = currentState.copy(
                            currentSong = it,
                            duration = it.duration
                        )
                    }
                }
            }
        }
        
        override fun onServiceDisconnected(name: ComponentName?) {
            Log.d("MusicViewModel", "音乐服务已断开连接")
            musicService = null
            isBound = false
        }
    }
    
    private val _playerState = MutableStateFlow(PlayerState())
    val playerState: StateFlow<PlayerState> = _playerState.asStateFlow()
    
    private val _songs = mutableStateOf(SampleData.songs)
    val songs: State<List<Song>> = _songs
    
    private val _searchQuery = mutableStateOf("")
    val searchQuery: State<String> = _searchQuery
    
    private val _filteredSongs = mutableStateOf(SampleData.songs)
    val filteredSongs: State<List<Song>> = _filteredSongs
    
    private val _isSearching = mutableStateOf(false)
    val isSearching: State<Boolean> = _isSearching
    
    init {
        Log.d("MusicViewModel", "初始化音乐ViewModel")
        
        // 启动并绑定音乐服务
        val intent = Intent(getApplication(), MusicPlayerService::class.java)
        try {
            getApplication<Application>().startService(intent)
            val bound = getApplication<Application>().bindService(intent, serviceConnection, Context.BIND_AUTO_CREATE)
            Log.d("MusicViewModel", "服务绑定结果: $bound")
        } catch (e: Exception) {
            Log.e("MusicViewModel", "启动音乐服务失败", e)
        }
        
        // 初始化播放列表
        setPlaylist(SampleData.songs)
        Log.d("MusicViewModel", "播放列表已初始化，共${SampleData.songs.size}首歌曲")
        
        // 启动位置更新器
        startPositionUpdater()
    }
    
    // 播放歌曲
    fun playSong(song: Song) {
        Log.d("MusicViewModel", "请求播放歌曲: ${song.title}")
        musicService?.playLocalSong(song)
        
        val currentState = _playerState.value
        val newIndex = currentState.playlist.indexOfFirst { it.id == song.id }
        
        _playerState.value = currentState.copy(
            currentSong = song,
            currentIndex = if (newIndex >= 0) newIndex else 0,
            currentPosition = 0
        )
        Log.d("MusicViewModel", "播放状态已更新，当前歌曲: ${song.title}")
    }
    
    // 播放/暂停
    fun togglePlayPause() {
        Log.d("MusicViewModel", "切换播放状态")
        val currentState = _playerState.value
        if (currentState.isPlaying) {
            Log.d("MusicViewModel", "暂停播放")
            musicService?.pause()
        } else {
            if (currentState.currentSong != null) {
                Log.d("MusicViewModel", "恢复播放")
                musicService?.resume()
            } else {
                // 如果没有当前歌曲，播放第一首
                Log.d("MusicViewModel", "播放第一首歌曲")
                val firstSong = currentState.playlist.firstOrNull()
                firstSong?.let { playSong(it) }
            }
        }
    }
    
    // 上一首
    fun previousSong() {
        val currentState = _playerState.value
        if (currentState.playlist.isNotEmpty()) {
            val currentIndex = currentState.currentIndex
            val newIndex = if (currentIndex > 0) currentIndex - 1 else currentState.playlist.size - 1
            val newSong = currentState.playlist[newIndex]
            playSong(newSong)
        }
    }
    
    // 下一首
    fun nextSong() {
        val currentState = _playerState.value
        if (currentState.playlist.isNotEmpty()) {
            val currentIndex = currentState.currentIndex
            val newIndex = if (currentIndex < currentState.playlist.size - 1) currentIndex + 1 else 0
            val newSong = currentState.playlist[newIndex]
            playSong(newSong)
        }
    }
    
    // 切换重复模式
    fun toggleRepeatMode() {
        val currentState = _playerState.value
        val newRepeatMode = when (currentState.repeatMode) {
            RepeatMode.NONE -> RepeatMode.ALL
            RepeatMode.ALL -> RepeatMode.ONE
            RepeatMode.ONE -> RepeatMode.NONE
        }
        _playerState.value = currentState.copy(repeatMode = newRepeatMode)
    }
    
    // 切换随机播放
    fun toggleShuffle() {
        val currentState = _playerState.value
        _playerState.value = currentState.copy(isShuffled = !currentState.isShuffled)
    }
    
    // 设置播放列表
    fun setPlaylist(playlist: List<Song>, startIndex: Int = 0) {
        val currentState = _playerState.value
        _playerState.value = currentState.copy(
            playlist = playlist,
            currentIndex = startIndex,
            currentSong = if (playlist.isNotEmpty()) playlist[startIndex] else null
        )
    }
    
    // 搜索歌曲
    fun searchSongs(query: String) {
        _searchQuery.value = query
        _isSearching.value = query.isNotEmpty()
        
        if (query.isEmpty()) {
            _filteredSongs.value = _songs.value
        } else {
            _filteredSongs.value = _songs.value.filter { song ->
                song.title.contains(query, ignoreCase = true) ||
                song.artist.contains(query, ignoreCase = true) ||
                song.album.contains(query, ignoreCase = true)
            }
        }
    }
    
    // 清除搜索
    fun clearSearch() {
        _searchQuery.value = ""
        _isSearching.value = false
        _filteredSongs.value = _songs.value
    }
    
    // 收藏/取消收藏歌曲
    fun toggleLikeSong(song: Song) {
        val updatedSongs = _songs.value.map { 
            if (it.id == song.id) {
                it.copy(isLiked = !it.isLiked)
            } else {
                it
            }
        }
        _songs.value = updatedSongs
        
        // 更新搜索结果
        if (_isSearching.value) {
            searchSongs(_searchQuery.value)
        }
        
        // 更新当前播放歌曲状态
        val currentState = _playerState.value
        if (currentState.currentSong?.id == song.id) {
            _playerState.value = currentState.copy(
                currentSong = currentState.currentSong?.copy(isLiked = !song.isLiked)
            )
        }
        
        // 更新播放列表中的歌曲状态
        val updatedPlaylist = currentState.playlist.map {
            if (it.id == song.id) {
                it.copy(isLiked = !it.isLiked)
            } else {
                it
            }
        }
        _playerState.value = currentState.copy(playlist = updatedPlaylist)
    }
    
    // 跳转到指定位置
    fun seekTo(position: Long) {
        musicService?.seekTo(position)
        val currentState = _playerState.value
        _playerState.value = currentState.copy(currentPosition = position)
    }
    
    // 启动播放进度更新
    private fun startPositionUpdater() {
        viewModelScope.launch {
            while (true) {
                delay(1000)
                val currentState = _playerState.value
                if (currentState.isPlaying) {
                    val position = musicService?.getCurrentPosition() ?: currentState.currentPosition
                    val duration = musicService?.getDuration() ?: currentState.duration
                    
                    if (position < duration) {
                        _playerState.value = currentState.copy(
                            currentPosition = position,
                            duration = duration
                        )
                    } else {
                        // 歌曲播放完毕，根据重复模式处理
                        when (currentState.repeatMode) {
                            RepeatMode.ONE -> {
                                val currentSong = currentState.currentSong
                                if (currentSong != null) {
                                    playSong(currentSong)
                                }
                            }
                            RepeatMode.ALL -> {
                                nextSong()
                            }
                            RepeatMode.NONE -> {
                                if (currentState.currentIndex < currentState.playlist.size - 1) {
                                    nextSong()
                                } else {
                                    _playerState.value = currentState.copy(
                                        isPlaying = false,
                                        playbackState = PlaybackState.STOPPED,
                                        currentPosition = 0
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    override fun onCleared() {
        super.onCleared()
        if (isBound) {
            getApplication<Application>().unbindService(serviceConnection)
            isBound = false
        }
    }
} 