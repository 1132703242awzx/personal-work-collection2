// 图像识别.cpp : 定义应用程序的入口点。
//

#include "framework.h"
#include "图像识别.h"
#include <commctrl.h>
#include <commdlg.h>
#include <sstream>
#include <iostream>
#include <algorithm>  // 添加此头文件以支持 min/max 函数

#pragma comment(lib, "comctl32.lib")

#define MAX_LOADSTRING 100

// 全局变量:
HINSTANCE hInst;                                // 当前实例
WCHAR szTitle[MAX_LOADSTRING];                  // 标题栏文本
WCHAR szWindowClass[MAX_LOADSTRING];            // 主窗口类名

// 人脸识别相关全局变量
std::unique_ptr<FaceRecognition> g_faceRecognition;
std::thread g_cameraThread;
std::atomic<bool> g_running(false);
HWND g_hVideoDisplay = nullptr;
HWND g_hStatusText = nullptr;
HWND g_hNameInput = nullptr;
HWND g_hResultText = nullptr;

// 此代码模块中包含的函数的前向声明:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);
void                CreateControls(HWND hWnd);
void                OnCommand(HWND hWnd, WPARAM wParam);
void                OnAddFace(HWND hWnd);
void                OnRecognizeFace(HWND hWnd);
void                OnSaveData(HWND hWnd);
void                OnLoadData(HWND hWnd);
void                StartCameraThread();
void                StopCameraThread();
void                UpdateVideoDisplay(HWND hWnd);
HBITMAP             MatToBitmap(const cv::Mat& mat);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    // 初始化人脸识别系统
    g_faceRecognition = std::make_unique<FaceRecognition>();
    if (!g_faceRecognition->Initialize())
    {
        MessageBox(nullptr, L"人脸识别系统初始化失败！\n请确保已正确安装OpenCV并配置环境变量。", L"错误", MB_OK | MB_ICONERROR);
        return FALSE;
    }

    // 初始化全局字符串
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_MY, szWindowClass, MAX_LOADSTRING);
    MyRegisterClass(hInstance);

    // 执行应用程序初始化:
    if (!InitInstance (hInstance, nCmdShow))
    {
        return FALSE;
    }

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_MY));

    MSG msg;

    // 主消息循环:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    // 清理资源
    StopCameraThread();
    g_faceRecognition.reset();

    return (int) msg.wParam;
}

//
//  函数: MyRegisterClass()
//
//  目标: 注册窗口类。
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEXW wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style          = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc    = WndProc;
    wcex.cbClsExtra     = 0;
    wcex.cbWndExtra     = 0;
    wcex.hInstance      = hInstance;
    wcex.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_MY));
    wcex.hCursor        = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszMenuName   = MAKEINTRESOURCEW(IDC_MY);
    wcex.lpszClassName  = szWindowClass;
    wcex.hIconSm        = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    return RegisterClassExW(&wcex);
}

//
//   函数: InitInstance(HINSTANCE, int)
//
//   目标: 保存实例句柄并创建主窗口
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // 将实例句柄存储在全局变量中

   HWND hWnd = CreateWindowW(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, 1000, 700, nullptr, nullptr, hInstance, nullptr);

   if (!hWnd)
   {
      return FALSE;
   }

   // 创建控件
   CreateControls(hWnd);

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  函数: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  目标: 处理主窗口的消息。
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_COMMAND:
        OnCommand(hWnd, wParam);
        break;
    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            // 更新视频显示
            if (g_faceRecognition && g_faceRecognition->IsCameraRunning())
            {
                UpdateVideoDisplay(hWnd);
            }
            EndPaint(hWnd, &ps);
        }
        break;
    case WM_TIMER:
        // 定时更新视频显示
        if (g_faceRecognition && g_faceRecognition->IsCameraRunning())
        {
            UpdateVideoDisplay(hWnd);
            InvalidateRect(g_hVideoDisplay, nullptr, FALSE);
        }
        break;
    case WM_DESTROY:
        StopCameraThread();
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

// "关于"框的消息处理程序。
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}

// 创建界面控件
void CreateControls(HWND hWnd)
{
    // 视频显示区域
    g_hVideoDisplay = CreateWindow(L"STATIC", L"",
        WS_VISIBLE | WS_CHILD | SS_BLACKFRAME,
        20, 20, 640, 480, hWnd, (HMENU)IDC_VIDEO_DISPLAY, hInst, nullptr);

    // 按钮
    CreateWindow(L"BUTTON", L"开始摄像头",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        680, 20, 120, 30, hWnd, (HMENU)ID_CAMERA_START, hInst, nullptr);

    CreateWindow(L"BUTTON", L"停止摄像头",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        680, 60, 120, 30, hWnd, (HMENU)ID_CAMERA_STOP, hInst, nullptr);

    CreateWindow(L"BUTTON", L"添加人脸",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        680, 100, 120, 30, hWnd, (HMENU)ID_ADD_FACE, hInst, nullptr);

    CreateWindow(L"BUTTON", L"识别人脸",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        680, 140, 120, 30, hWnd, (HMENU)ID_RECOGNIZE_FACE, hInst, nullptr);

    CreateWindow(L"BUTTON", L"保存数据",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        680, 180, 120, 30, hWnd, (HMENU)ID_SAVE_DATA, hInst, nullptr);

    CreateWindow(L"BUTTON", L"加载数据",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        680, 220, 120, 30, hWnd, (HMENU)ID_LOAD_DATA, hInst, nullptr);

    // 姓名输入框
    CreateWindow(L"STATIC", L"姓名:",
        WS_VISIBLE | WS_CHILD,
        680, 270, 50, 20, hWnd, nullptr, hInst, nullptr);

    g_hNameInput = CreateWindow(L"EDIT", L"",
        WS_VISIBLE | WS_CHILD | WS_BORDER,
        680, 290, 120, 25, hWnd, (HMENU)IDC_NAME_INPUT, hInst, nullptr);

    // 状态文本
    CreateWindow(L"STATIC", L"状态:",
        WS_VISIBLE | WS_CHILD,
        20, 520, 50, 20, hWnd, nullptr, hInst, nullptr);

    g_hStatusText = CreateWindow(L"STATIC", L"就绪",
        WS_VISIBLE | WS_CHILD,
        80, 520, 300, 20, hWnd, (HMENU)IDC_STATUS_TEXT, hInst, nullptr);

    // 识别结果文本
    CreateWindow(L"STATIC", L"识别结果:",
        WS_VISIBLE | WS_CHILD,
        20, 550, 80, 20, hWnd, nullptr, hInst, nullptr);

    g_hResultText = CreateWindow(L"STATIC", L"",
        WS_VISIBLE | WS_CHILD,
        110, 550, 400, 20, hWnd, (HMENU)IDC_RESULT_TEXT, hInst, nullptr);
}

// 处理命令消息
void OnCommand(HWND hWnd, WPARAM wParam)
{
    int wmId = LOWORD(wParam);
    switch (wmId)
    {
    case IDM_ABOUT:
        DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
        break;
    case IDM_EXIT:
        DestroyWindow(hWnd);
        break;
    case ID_CAMERA_START:
        StartCameraThread();
        SetTimer(hWnd, 1, 33, nullptr); // 30 FPS
        SetWindowText(g_hStatusText, L"摄像头已启动");
        break;
    case ID_CAMERA_STOP:
        StopCameraThread();
        KillTimer(hWnd, 1);
        SetWindowText(g_hStatusText, L"摄像头已停止");
        break;
    case ID_ADD_FACE:
        OnAddFace(hWnd);
        break;
    case ID_RECOGNIZE_FACE:
        OnRecognizeFace(hWnd);
        break;
    case ID_SAVE_DATA:
        OnSaveData(hWnd);
        break;
    case ID_LOAD_DATA:
        OnLoadData(hWnd);
        break;
    default:
        DefWindowProc(hWnd, WM_COMMAND, wParam, 0);
        break;
    }
}

// 启动摄像头线程
void StartCameraThread()
{
    if (g_running.load())
        return;

    g_running.store(true);
    g_faceRecognition->StartCamera();
    SetWindowText(g_hStatusText, L"摄像头启动中...");
}

// 停止摄像头线程
void StopCameraThread()
{
    if (!g_running.load())
        return;

    g_running.store(false);
    g_faceRecognition->StopCamera();
    
    if (g_cameraThread.joinable())
        g_cameraThread.join();
}

// 更新视频显示
void UpdateVideoDisplay(HWND hWnd)
{
    if (!g_faceRecognition || !g_faceRecognition->IsCameraRunning())
        return;

    cv::Mat frame = g_faceRecognition->GetCurrentFrame();
    if (frame.empty())
        return;

    // 检测人脸并绘制矩形框
    std::vector<cv::Rect> faces = g_faceRecognition->DetectFaces(frame);
    for (const auto& face : faces)
    {
        cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2);
        
        // 在人脸框上方显示"检测到人脸"文字
        cv::Point textPos(face.x, face.y - 10);
        if (textPos.y < 20) textPos.y = face.y + face.height + 20;
        cv::putText(frame, "Face Detected", textPos, cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
    }

    // 转换为Windows位图并显示（保持长宽比）
    HBITMAP hBitmap = MatToBitmap(frame);
    if (hBitmap)
    {
        HDC hdc = GetDC(g_hVideoDisplay);
        HDC hdcMem = CreateCompatibleDC(hdc);
        HBITMAP hOldBitmap = (HBITMAP)SelectObject(hdcMem, hBitmap);
        
        RECT rect;
        GetClientRect(g_hVideoDisplay, &rect);
        
        // 计算保持长宽比的显示尺寸
        int displayWidth = rect.right;
        int displayHeight = rect.bottom;
        int frameWidth = frame.cols;
        int frameHeight = frame.rows;
        
        // 计算缩放比例
        float scaleX = (float)displayWidth / frameWidth;
        float scaleY = (float)displayHeight / frameHeight;
        float scale = std::min(scaleX, scaleY);
        
        int newWidth = (int)(frameWidth * scale);
        int newHeight = (int)(frameHeight * scale);
        
        // 居中显示
        int offsetX = (displayWidth - newWidth) / 2;
        int offsetY = (displayHeight - newHeight) / 2;
        
        // 清空背景
        HBRUSH hBrush = CreateSolidBrush(RGB(0, 0, 0));
        FillRect(hdc, &rect, hBrush);
        DeleteObject(hBrush);
        
        // 显示图像
        StretchBlt(hdc, offsetX, offsetY, newWidth, newHeight,
                   hdcMem, 0, 0, frameWidth, frameHeight, SRCCOPY);
        
        SelectObject(hdcMem, hOldBitmap);
        DeleteDC(hdcMem);
        ReleaseDC(g_hVideoDisplay, hdc);
        DeleteObject(hBitmap);
    }
}

// 转换Mat到HBITMAP（优化版本）
HBITMAP MatToBitmap(const cv::Mat& mat)
{
    if (mat.empty())
        return nullptr;

    cv::Mat rgbMat;
    
    // 确保图像格式正确
    if (mat.channels() == 3)
    {
        // BGR转RGB
        cv::cvtColor(mat, rgbMat, cv::COLOR_BGR2RGB);
    }
    else if (mat.channels() == 1)
    {
        // 灰度转RGB
        cv::cvtColor(mat, rgbMat, cv::COLOR_GRAY2RGB);
    }
    else if (mat.channels() == 4)
    {
        // BGRA转RGB
        cv::cvtColor(mat, rgbMat, cv::COLOR_BGRA2RGB);
    }
    else
    {
        rgbMat = mat.clone();
    }

    // 确保数据连续性
    if (!rgbMat.isContinuous())
    {
        rgbMat = rgbMat.clone();
    }

    BITMAPINFO bmi;
    ZeroMemory(&bmi, sizeof(bmi));
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = rgbMat.cols;
    bmi.bmiHeader.biHeight = -rgbMat.rows; // 负值表示顶部为原点，避免图像倒置
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 24;
    bmi.bmiHeader.biCompression = BI_RGB;
    bmi.bmiHeader.biSizeImage = 0; // 对于BI_RGB可以为0

    HDC hdc = GetDC(nullptr);
    HBITMAP hBitmap = CreateDIBitmap(hdc, &bmi.bmiHeader, CBM_INIT,
                                     rgbMat.data, &bmi, DIB_RGB_COLORS);
    ReleaseDC(nullptr, hdc);

    return hBitmap;
}

// 添加人脸
void OnAddFace(HWND hWnd)
{
    if (!g_faceRecognition || !g_faceRecognition->IsCameraRunning())
    {
        MessageBox(hWnd, L"请先启动摄像头", L"提示", MB_OK);
        return;
    }

    // 获取姓名
    wchar_t name[256];
    GetWindowText(g_hNameInput, name, 256);
    if (wcslen(name) == 0)
    {
        MessageBox(hWnd, L"请输入姓名", L"提示", MB_OK);
        return;
    }

    // 转换为std::string
    char nameStr[256];
    WideCharToMultiByte(CP_UTF8, 0, name, -1, nameStr, 256, nullptr, nullptr);

    // 获取当前帧并添加人脸
    cv::Mat frame = g_faceRecognition->GetCurrentFrame();
    if (frame.empty())
    {
        MessageBox(hWnd, L"无法获取摄像头图像", L"错误", MB_OK);
        return;
    }

    if (g_faceRecognition->AddFace(nameStr, frame))
    {
        SetWindowText(g_hStatusText, L"人脸添加成功");
        SetWindowText(g_hNameInput, L""); // 清空输入框
    }
    else
    {
        MessageBox(hWnd, L"未检测到人脸，请确保脸部清晰可见", L"提示", MB_OK);
    }
}

// 识别人脸
void OnRecognizeFace(HWND hWnd)
{
    if (!g_faceRecognition || !g_faceRecognition->IsCameraRunning())
    {
        MessageBox(hWnd, L"请先启动摄像头", L"提示", MB_OK);
        return;
    }

    cv::Mat frame = g_faceRecognition->GetCurrentFrame();
    if (frame.empty())
    {
        MessageBox(hWnd, L"无法获取摄像头图像", L"错误", MB_OK);
        return;
    }

    std::string result = g_faceRecognition->RecognizeFace(frame);
    
    // 转换为宽字符并显示
    wchar_t resultW[256];
    MultiByteToWideChar(CP_UTF8, 0, result.c_str(), -1, resultW, 256);
    SetWindowText(g_hResultText, resultW);
}

// 保存训练数据
void OnSaveData(HWND hWnd)
{
    OPENFILENAME ofn;
    wchar_t szFile[260] = { 0 };

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hWnd;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = L"训练数据\0*.xml\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = nullptr;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = nullptr;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT;

    if (GetSaveFileName(&ofn))
    {
        char filename[260];
        WideCharToMultiByte(CP_UTF8, 0, szFile, -1, filename, 260, nullptr, nullptr);
        
        if (g_faceRecognition->SaveTrainingData(filename))
        {
            SetWindowText(g_hStatusText, L"数据保存成功");
        }
        else
        {
            MessageBox(hWnd, L"数据保存失败", L"错误", MB_OK);
        }
    }
}

// 加载训练数据
void OnLoadData(HWND hWnd)
{
    OPENFILENAME ofn;
    wchar_t szFile[260] = { 0 };

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hWnd;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = L"训练数据\0*.xml\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = nullptr;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = nullptr;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

    if (GetOpenFileName(&ofn))
    {
        char filename[260];
        WideCharToMultiByte(CP_UTF8, 0, szFile, -1, filename, 260, nullptr, nullptr);
        
        if (g_faceRecognition->LoadTrainingData(filename))
        {
            SetWindowText(g_hStatusText, L"数据加载成功");
        }
        else
        {
            MessageBox(hWnd, L"数据加载失败", L"错误", MB_OK);
        }
    }
}
