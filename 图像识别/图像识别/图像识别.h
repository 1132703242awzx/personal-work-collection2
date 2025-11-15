#pragma once

#include "resource.h"
#include "FaceRecognition.h"
#include <memory>
#include <thread>
#include <atomic>

// 全局变量声明
extern std::unique_ptr<FaceRecognition> g_faceRecognition;
extern std::thread g_cameraThread;
extern std::atomic<bool> g_running;
extern HWND g_hVideoDisplay;
extern HWND g_hStatusText;
extern HWND g_hNameInput;
extern HWND g_hResultText;

// 函数声明
void StartCameraThread();
void StopCameraThread();
void UpdateVideoDisplay(HWND hWnd);
HBITMAP MatToBitmap(const cv::Mat& mat);
