package com.example.music.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = PrimaryBlue,
    secondary = SecondaryBlue,
    tertiary = AccentBlue,
    background = BackgroundDark,
    surface = SurfaceDark,
    onPrimary = TextPrimary,
    onSecondary = TextPrimary,
    onTertiary = TextPrimary,
    onBackground = TextPrimary,
    onSurface = TextPrimary,
    primaryContainer = PrimaryBlueDark,
    secondaryContainer = SecondaryBlueDark,
    tertiaryContainer = AccentBlue,
    onPrimaryContainer = TextPrimary,
    onSecondaryContainer = TextPrimary,
    onTertiaryContainer = TextPrimary,
    surfaceVariant = SurfaceLight,
    onSurfaceVariant = TextSecondary,
    outline = DividerColor,
    outlineVariant = TextTertiary,
    scrim = BackgroundDark,
    inverseSurface = TextPrimary,
    inverseOnSurface = BackgroundDark,
    inversePrimary = PrimaryBlueLight,
    surfaceDim = BackgroundMedium,
    surfaceBright = BackgroundLight,
    surfaceContainer = CardBackground,
    surfaceContainerHigh = SurfaceLight,
    surfaceContainerHighest = BackgroundLight,
    surfaceContainerLow = SurfaceDark,
    surfaceContainerLowest = BackgroundDark
)

private val LightColorScheme = lightColorScheme(
    primary = PrimaryBlue,
    secondary = SecondaryBlue,
    tertiary = AccentBlue,
    background = TextPrimary,
    surface = TextPrimary,
    onPrimary = TextPrimary,
    onSecondary = TextPrimary,
    onTertiary = TextPrimary,
    onBackground = BackgroundDark,
    onSurface = BackgroundDark,
    primaryContainer = PrimaryBlueLight,
    secondaryContainer = SecondaryBlueLight,
    tertiaryContainer = AccentBlue,
    onPrimaryContainer = TextPrimary,
    onSecondaryContainer = TextPrimary,
    onTertiaryContainer = TextPrimary,
    surfaceVariant = BackgroundLight,
    onSurfaceVariant = TextSecondary,
    outline = DividerColor,
    outlineVariant = TextTertiary,
    scrim = BackgroundDark,
    inverseSurface = BackgroundDark,
    inverseOnSurface = TextPrimary,
    inversePrimary = PrimaryBlueDark,
    surfaceDim = BackgroundMedium,
    surfaceBright = TextPrimary,
    surfaceContainer = CardBackground,
    surfaceContainerHigh = BackgroundLight,
    surfaceContainerHighest = BackgroundMedium,
    surfaceContainerLow = TextPrimary,
    surfaceContainerLowest = TextPrimary
)

@Composable
fun MusicTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Dynamic color is available on Android 12+
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as android.app.Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}