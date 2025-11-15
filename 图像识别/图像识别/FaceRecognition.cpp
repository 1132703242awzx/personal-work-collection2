// 禁用OpenCV相关警告
#pragma warning(push)
#pragma warning(disable: 4996)  // deprecated functions
#pragma warning(disable: 26439) // noexcept warnings
#pragma warning(disable: 26495) // uninitialized member warnings  
#pragma warning(disable: 6294)  // for-loop warnings
#pragma warning(disable: 6201)  // buffer overrun warnings

#include "FaceRecognition.h"

#pragma warning(pop)

#include <iostream>
#include <fstream>
#include <algorithm>

FaceRecognition::FaceRecognition()
    : m_nextLabel(0)
    , m_cameraRunning(false)
    , m_initialized(false)
{
}

FaceRecognition::~FaceRecognition()
{
    StopCamera();
}

bool FaceRecognition::Initialize()
{
    // 加载Haar级联分类器用于人脸检测
    std::string cascadePath = "haarcascade_frontalface_alt.xml";
    
    if (!m_faceCascade.load(cascadePath))
    {
        // 尝试常见的级联分类器路径
        std::vector<std::string> possiblePaths = {
            "haarcascade_frontalface_alt.xml",
            "haarcascade_frontalface_default.xml",
            "C:/opencv/build/etc/haarcascades/haarcascade_frontalface_alt.xml",
            "data/haarcascades/haarcascade_frontalface_alt.xml"
        };
        
        bool loaded = false;
        for (const auto& path : possiblePaths)
        {
            if (m_faceCascade.load(path))
            {
                loaded = true;
                break;
            }
        }
        
        if (!loaded)
        {
            std::cerr << "错误：无法加载人脸检测级联分类器" << std::endl;
            return false;
        }
    }

    m_initialized = true;
    return true;
}

void FaceRecognition::StartCamera()
{
    if (m_cameraRunning)
        return;

    m_camera.open(0);
    if (!m_camera.isOpened())
    {
        std::cerr << "错误：无法打开摄像头" << std::endl;
        return;
    }

    // 设置摄像头分辨率和参数
    m_camera.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    m_camera.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
    m_camera.set(cv::CAP_PROP_FPS, 30);
    
    // 设置缓冲区大小为1，减少延迟
    m_camera.set(cv::CAP_PROP_BUFFERSIZE, 1);
    
    // 启用自动曝光和白平衡
    m_camera.set(cv::CAP_PROP_AUTO_EXPOSURE, 0.25);
    m_camera.set(cv::CAP_PROP_AUTOFOCUS, 1);

    m_cameraRunning = true;
}

void FaceRecognition::StopCamera()
{
    if (m_cameraRunning)
    {
        m_camera.release();
        m_cameraRunning = false;
    }
}

bool FaceRecognition::AddFace(const std::string& name, const cv::Mat& image)
{
    if (!m_initialized)
        return false;

    // 检测人脸
    std::vector<cv::Rect> faces = DetectFaces(image);
    if (faces.empty())
        return false;

    // 取第一个检测到的人脸
    cv::Mat face = image(faces[0]);
    cv::Mat processedFace = PreprocessFace(face);

    // 添加到训练数据
    m_trainingImages.push_back(processedFace);
    m_trainingLabels.push_back(m_nextLabel);
    m_labelToName[m_nextLabel] = name;
    m_nextLabel++;

    return true;
}

std::string FaceRecognition::RecognizeFace(const cv::Mat& image)
{
    if (!m_initialized || m_trainingImages.empty())
        return "未知";

    // 检测人脸
    std::vector<cv::Rect> faces = DetectFaces(image);
    if (faces.empty())
        return "未检测到人脸";

    // 预处理第一个检测到的人脸
    cv::Mat face = image(faces[0]);
    cv::Mat processedFace = PreprocessFace(face);

    // 使用简单的模板匹配进行识别
    return MatchFace(processedFace);
}

std::vector<cv::Rect> FaceRecognition::DetectFaces(const cv::Mat& image)
{
    std::vector<cv::Rect> faces;
    
    if (!m_initialized)
        return faces;

    cv::Mat grayImage;
    if (image.channels() == 3)
        cv::cvtColor(image, grayImage, cv::COLOR_BGR2GRAY);
    else
        grayImage = image.clone();

    // 直方图均衡化
    cv::equalizeHist(grayImage, grayImage);

    // 检测人脸
    m_faceCascade.detectMultiScale(
        grayImage,
        faces,
        1.1,        // scaleFactor
        3,          // minNeighbors
        0,          // flags
        cv::Size(30, 30)  // minSize
    );

    return faces;
}

cv::Mat FaceRecognition::GetCurrentFrame()
{
    if (!m_cameraRunning)
        return cv::Mat();

    m_camera >> m_currentFrame;
    return m_currentFrame.clone();
}

bool FaceRecognition::SaveTrainingData(const std::string& filename)
{
    if (m_trainingImages.empty())
        return false;

    try
    {
        cv::FileStorage fs(filename, cv::FileStorage::WRITE);
        if (!fs.isOpened())
            return false;
            
        // 保存训练图像
        fs << "training_images" << "[";
        for (const auto& img : m_trainingImages)
        {
            fs << img;
        }
        fs << "]";
        
        // 保存标签
        fs << "training_labels" << m_trainingLabels;
        
        fs.release();
        
        // 保存标签映射
        std::ofstream mapFile(filename + ".map");
        if (mapFile.is_open())
        {
            for (const auto& pair : m_labelToName)
            {
                mapFile << pair.first << " " << pair.second << std::endl;
            }
            mapFile.close();
        }
        
        return true;
    }
    catch (const cv::Exception& e)
    {
        std::cerr << "保存训练数据失败: " << e.what() << std::endl;
        return false;
    }
}

bool FaceRecognition::LoadTrainingData(const std::string& filename)
{
    try
    {
        cv::FileStorage fs(filename, cv::FileStorage::READ);
        if (!fs.isOpened())
            return false;
            
        // 加载训练图像
        cv::FileNode imagesNode = fs["training_images"];
        m_trainingImages.clear();
        for (cv::FileNodeIterator it = imagesNode.begin(); it != imagesNode.end(); ++it)
        {
            cv::Mat img;
            *it >> img;
            m_trainingImages.push_back(img);
        }
        
        // 加载标签
        fs["training_labels"] >> m_trainingLabels;
        fs.release();
        
        // 加载标签映射
        std::ifstream mapFile(filename + ".map");
        if (mapFile.is_open())
        {
            m_labelToName.clear();
            int label;
            std::string name;
            while (mapFile >> label >> name)
            {
                m_labelToName[label] = name;
                if (label >= m_nextLabel)
                    m_nextLabel = label + 1;
            }
            mapFile.close();
        }
        
        return true;
    }
    catch (const cv::Exception& e)
    {
        std::cerr << "加载训练数据失败: " << e.what() << std::endl;
        return false;
    }
}

cv::Mat FaceRecognition::PreprocessFace(const cv::Mat& face)
{
    cv::Mat grayFace, resizedFace;
    
    // 转换为灰度图
    if (face.channels() == 3)
        cv::cvtColor(face, grayFace, cv::COLOR_BGR2GRAY);
    else
        grayFace = face.clone();

    // 调整大小到标准尺寸
    cv::resize(grayFace, resizedFace, cv::Size(100, 100));

    // 直方图均衡化
    cv::equalizeHist(resizedFace, resizedFace);

    return resizedFace;
}

std::string FaceRecognition::MatchFace(const cv::Mat& face)
{
    if (m_trainingImages.empty())
        return "未知";

    double bestMatch = -1;
    std::string bestName = "未知";
    
    // 使用模板匹配和直方图比较
    for (size_t i = 0; i < m_trainingImages.size(); ++i)
    {
        // 计算直方图相关性
        cv::Mat hist1, hist2;
        int histSize = 256;
        float range[] = {0, 256};
        const float* histRange = {range};
        
        cv::calcHist(&face, 1, 0, cv::Mat(), hist1, 1, &histSize, &histRange);
        cv::calcHist(&m_trainingImages[i], 1, 0, cv::Mat(), hist2, 1, &histSize, &histRange);
        
        double correlation = cv::compareHist(hist1, hist2, cv::HISTCMP_CORREL);
        
        if (correlation > bestMatch)
        {
            bestMatch = correlation;
            int label = m_trainingLabels[i];
            if (m_labelToName.find(label) != m_labelToName.end())
            {
                bestName = m_labelToName[label];
            }
        }
    }
    
    // 设置阈值
    if (bestMatch > 0.7)
    {
        return bestName + " (匹配度: " + std::to_string((int)(bestMatch * 100)) + "%)";
    }
    
    return "未知";
}
