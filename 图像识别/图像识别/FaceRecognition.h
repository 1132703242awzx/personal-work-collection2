#pragma once

// 禁用OpenCV相关警告
#pragma warning(push)
#pragma warning(disable: 4996)  // deprecated functions
#pragma warning(disable: 26439) // noexcept warnings
#pragma warning(disable: 26495) // uninitialized member warnings  
#pragma warning(disable: 6294)  // for-loop warnings
#pragma warning(disable: 6201)  // buffer overrun warnings

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/objdetect.hpp>

#pragma warning(pop)

#include <vector>
#include <string>
#include <map>
#include <memory>

class FaceRecognition
{
public:
    FaceRecognition();
    ~FaceRecognition();

    // 初始化人脸识别系统
    bool Initialize();

    // 从摄像头捕获人脸
    void StartCamera();
    void StopCamera();

    // 添加新的人脸到数据库
    bool AddFace(const std::string& name, const cv::Mat& image);

    // 识别人脸
    std::string RecognizeFace(const cv::Mat& image);

    // 检测人脸
    std::vector<cv::Rect> DetectFaces(const cv::Mat& image);

    // 获取当前帧
    cv::Mat GetCurrentFrame();

    // 保存和加载训练数据
    bool SaveTrainingData(const std::string& filename);
    bool LoadTrainingData(const std::string& filename);

    // 检查摄像头是否在运行
    bool IsCameraRunning() const { return m_cameraRunning; }

private:
    cv::CascadeClassifier m_faceCascade;
    cv::VideoCapture m_camera;
    cv::Mat m_currentFrame;
    
    std::vector<cv::Mat> m_trainingImages;
    std::vector<int> m_trainingLabels;
    std::map<int, std::string> m_labelToName;
    
    int m_nextLabel;
    bool m_cameraRunning;
    bool m_initialized;

    // 预处理人脸图像
    cv::Mat PreprocessFace(const cv::Mat& face);

    // 简单的人脸匹配
    std::string MatchFace(const cv::Mat& face);
};
