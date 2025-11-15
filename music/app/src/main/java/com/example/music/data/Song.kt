package com.example.music.data

import androidx.compose.runtime.Immutable

@Immutable
data class Song(
    val id: String,
    val title: String,
    val artist: String,
    val album: String,
    val duration: Long, // in milliseconds
    val coverUrl: String,
    val audioUrl: String,
    val isLiked: Boolean = false,
    val playCount: Int = 0
)

@Immutable
data class Playlist(
    val id: String,
    val name: String,
    val description: String,
    val coverUrl: String,
    val songs: List<Song>,
    val createdAt: Long,
    val isPublic: Boolean = true
)

@Immutable
data class Artist(
    val id: String,
    val name: String,
    val coverUrl: String,
    val bio: String,
    val followerCount: Int,
    val isFollowed: Boolean = false
)

@Immutable
data class Album(
    val id: String,
    val title: String,
    val artist: String,
    val coverUrl: String,
    val releaseDate: Long,
    val songs: List<Song>
)

// 音乐播放状态
enum class PlaybackState {
    PLAYING, PAUSED, STOPPED, BUFFERING
}

// 播放模式
enum class RepeatMode {
    NONE, ONE, ALL
}

// 播放器状态
@Immutable
data class PlayerState(
    val currentSong: Song? = null,
    val isPlaying: Boolean = false,
    val playbackState: PlaybackState = PlaybackState.STOPPED,
    val currentPosition: Long = 0,
    val duration: Long = 0,
    val repeatMode: RepeatMode = RepeatMode.NONE,
    val isShuffled: Boolean = false,
    val playlist: List<Song> = emptyList(),
    val currentIndex: Int = 0
)

// 示例数据
object SampleData {
    val songs = listOf(
        Song(
            id = "1",
            title = "夜曲",
            artist = "周杰伦",
            album = "十一月的肖邦",
            duration = 240000,
            coverUrl = "https://p1.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
            audioUrl = "https://music.163.com/song/media/outer/url?id=185668.mp3",
            isLiked = true,
            playCount = 1234567
        ),
        Song(
            id = "2",
            title = "青花瓷",
            artist = "周杰伦",
            album = "我很忙",
            duration = 230000,
            coverUrl = "https://p1.music.126.net/Fd69Yt_MoMBVByw3-pLZkA==/109951163081564547.jpg",
            audioUrl = "https://music.163.com/song/media/outer/url?id=185856.mp3",
            isLiked = false,
            playCount = 987654
        ),
        Song(
            id = "3",
            title = "稻香",
            artist = "周杰伦",
            album = "魔杰座",
            duration = 220000,
            coverUrl = "https://p1.music.126.net/qWnv8lq8QO-HE4rJBq1QUg==/109951163081564547.jpg",
            audioUrl = "https://music.163.com/song/media/outer/url?id=185668.mp3",
            isLiked = true,
            playCount = 2345678
        ),
        Song(
            id = "4",
            title = "演员",
            artist = "薛之谦",
            album = "绅士",
            duration = 250000,
            coverUrl = "https://p1.music.126.net/g-4Qyht7ljO_qUJvxKPVyg==/109951163081564547.jpg",
            audioUrl = "https://music.163.com/song/media/outer/url?id=418603077.mp3",
            isLiked = false,
            playCount = 1876543
        ),
        Song(
            id = "5",
            title = "年轮",
            artist = "张碧晨",
            album = "年轮",
            duration = 280000,
            coverUrl = "https://p1.music.126.net/8KlJOaGzTVUhEWYJhQKzlQ==/109951163081564547.jpg",
            audioUrl = "https://music.163.com/song/media/outer/url?id=29724020.mp3",
            isLiked = true,
            playCount = 3456789
        )
    )
    
    val playlists = listOf(
        Playlist(
            id = "1",
            name = "我的收藏",
            description = "收藏的好听音乐",
            coverUrl = "https://p1.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
            songs = songs.filter { it.isLiked },
            createdAt = System.currentTimeMillis(),
            isPublic = false
        ),
        Playlist(
            id = "2",
            name = "华语金曲",
            description = "精选华语经典歌曲",
            coverUrl = "https://p1.music.126.net/Fd69Yt_MoMBVByw3-pLZkA==/109951163081564547.jpg",
            songs = songs,
            createdAt = System.currentTimeMillis(),
            isPublic = true
        )
    )
    
    val artists = listOf(
        Artist(
            id = "1",
            name = "周杰伦",
            coverUrl = "https://p1.music.126.net/6y-UleORITEDbvrOLV0Q8A==/5639395138885805.jpg",
            bio = "华语流行音乐天王",
            followerCount = 12345678,
            isFollowed = true
        ),
        Artist(
            id = "2",
            name = "薛之谦",
            coverUrl = "https://p1.music.126.net/g-4Qyht7ljO_qUJvxKPVyg==/109951163081564547.jpg",
            bio = "创作才子",
            followerCount = 8765432,
            isFollowed = false
        )
    )
} 