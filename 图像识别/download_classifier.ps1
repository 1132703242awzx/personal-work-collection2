# 下载Haar级联分类器
Write-Host "下载人脸检测分类器文件..." -ForegroundColor Green

$outputDir = "d:\图像识别\图像识别"
$classifierUrl = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt.xml"
$outputFile = "$outputDir\haarcascade_frontalface_alt.xml"

try {
    if (!(Test-Path $outputFile)) {
        Write-Host "正在下载分类器文件..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $classifierUrl -OutFile $outputFile -UseBasicParsing
        Write-Host "分类器文件下载完成！" -ForegroundColor Green
    } else {
        Write-Host "分类器文件已存在" -ForegroundColor Cyan
    }
} catch {
    Write-Host "下载失败，将创建一个简化的人脸检测器" -ForegroundColor Yellow
    Write-Host "错误: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "按任意键继续..."
