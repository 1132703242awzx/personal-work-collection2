# 人脸识别项目编译脚本
Write-Host "开始编译人脸识别项目..." -ForegroundColor Green

# 设置路径
$projectDir = "d:\图像识别"
$vcvarsPath = "${env:ProgramFiles}\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

# 检查VS环境
if (!(Test-Path $vcvarsPath)) {
    $vcvarsPath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
}

if (!(Test-Path $vcvarsPath)) {
    Write-Host "错误：找不到Visual Studio 2022" -ForegroundColor Red
    Write-Host "请确保已正确安装Visual Studio 2022" -ForegroundColor Yellow
    Read-Host "按任意键继续..."
    exit 1
}

# 切换到项目目录
Set-Location $projectDir

# 编译项目
Write-Host "正在编译项目..." -ForegroundColor Yellow

$command = @"
call "$vcvarsPath" && MSBuild 图像识别.sln /p:Configuration=Debug /p:Platform=x64 /m
"@

$result = cmd.exe /c $command

if ($LASTEXITCODE -eq 0) {
    Write-Host "编译成功！" -ForegroundColor Green
    Write-Host "可执行文件位置: $projectDir\x64\Debug\图像识别.exe" -ForegroundColor Cyan
    
    # 检查可执行文件是否存在
    $exePath = "$projectDir\x64\Debug\图像识别.exe"
    if (Test-Path $exePath) {
        Write-Host "是否现在运行程序？(Y/N)" -ForegroundColor Yellow
        $choice = Read-Host
        if ($choice -eq "Y" -or $choice -eq "y") {
            Start-Process $exePath
        }
    }
} else {
    Write-Host "编译失败！" -ForegroundColor Red
    Write-Host "请检查错误信息并确保：" -ForegroundColor Yellow
    Write-Host "1. OpenCV已正确安装并配置环境变量" -ForegroundColor White
    Write-Host "2. OPENCV_DIR环境变量指向OpenCV安装目录" -ForegroundColor White
    Write-Host "3. PATH中包含OpenCV的bin目录" -ForegroundColor White
}

Read-Host "按任意键继续..."
