# 图片水印工具

<div align="center">
  <strong>📷 自动为图片添加基于拍摄日期的水印工具</strong>
</div>

这是一个功能强大的命令行工具，可以自动从图片的EXIF信息中提取拍摄日期，并将其作为水印添加到图片上。工具支持自定义水印的字体大小、颜色和位置，让您轻松批量处理大量照片。

## 功能特点

- 从图片的EXIF信息中提取拍摄日期作为水印文本
- 支持自定义水印字体大小、颜色和位置
- 支持处理单个图片文件或整个目录下的所有图片
- 自动将添加水印后的图片保存到原目录的_watermark子目录中

## 安装指南

### 前提条件

- 确保您的系统已安装Python 3.6或更高版本
- 可以通过以下命令检查Python版本：

```bash
python --version
# 或者
python3 --version
```

### 安装步骤

1. 克隆或下载本项目到您的本地计算机

2. 进入项目目录

```bash
cd Photo-Watermark-1
```

3. 安装依赖库

```bash
pip install -r requirements.txt
# 或者
pip3 install -r requirements.txt
```

### 验证安装

安装完成后，可以通过查看帮助信息来验证安装是否成功：

```bash
python watermark_tool.py --help
```

## 工作原理

该工具的工作流程如下：

1. **读取输入**：接收用户提供的图片文件路径或目录路径
2. **提取日期**：尝试从图片的EXIF信息中提取拍摄日期（DateTimeOriginal）
3. **备选方案**：如果无法获取EXIF信息，使用文件的修改时间作为备选
4. **创建水印**：根据用户指定的字体大小、颜色和位置创建文本水印
5. **处理图片**：将水印添加到原始图片上
6. **保存结果**：将处理后的图片保存到自动创建的输出目录中

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  输入图片    │ -> │ 提取EXIF信息 │ -> │ 创建文本水印 │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                                               ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  输出目录    │ <- │  保存图片    │ <- │ 添加水印到图片│
└──────────────┘    └──────────────┘    └──────────────┘
```

## 使用方法

### 基本用法

处理单个图片文件：

```bash
python watermark_tool.py /path/to/your/image.jpg
```

处理整个目录下的所有图片：

```bash
python watermark_tool.py /path/to/your/image/folder
```

### 命令行参数详解

```bash
python watermark_tool.py [选项] <图片路径或目录路径>
```

### 可用选项

| 选项 | 描述 | 默认值 | 示例值 |
|------|------|--------|--------|
| `--font-size` | 水印字体大小 | 30 | 40 |
| `--color` | 水印颜色（预定义颜色或HEX代码） | white | black, #FF0000 |
| `--position` | 水印位置 | bottom_right | top_left, center |

### 支持的颜色值

**预定义颜色**：
- black, white, red, green, blue, yellow, cyan, magenta

**HEX颜色代码**：
- #RRGGBB 格式，如 #FF0000 (红色)
- #RRGGBBAA 格式，支持透明度，如 #FF000080 (半透明红色)

## 注意事项

1. 程序会自动创建输出目录，命名为原目录名加上'_watermark'后缀
2. 如果图片没有EXIF信息，将使用文件的修改时间作为水印
3. 如果文件修改时间也无法获取，将使用当前日期作为水印
4. 支持的图片格式：PNG、JPG、JPEG、BMP、GIF

## 依赖库

- Pillow：用于图像处理
- piexif：用于读取EXIF信息

## 实用示例

### 示例1：基本水印

为图片添加默认设置的水印（白色、右下角、字体大小30）：

```bash
python watermark_tool.py ./vacation_photos/IMG_1234.jpg
```

### 示例2：自定义水印样式

为图片添加红色、居中的水印，字体大小为40：

```bash
python watermark_tool.py ./vacation_photos/IMG_1234.jpg --font-size 40 --color red --position center
```

### 示例3：批量处理照片集

处理整个目录，使用黑色水印，位置在左上角：

```bash
python watermark_tool.py ./vacation_photos --color black --position top_left
```

### 示例4：使用透明水印

为图片添加半透明蓝色水印，以避免遮挡图片内容：

```bash
python watermark_tool.py ./vacation_photos/IMG_1234.jpg --color #0000FF80 --position bottom_left
```

## 常见问题 (FAQ)

### Q: 程序无法读取我的图片的EXIF信息怎么办？
A: 如果图片没有EXIF信息，程序会自动使用文件的修改时间作为备选方案。如果修改时间也无法获取，将使用当前日期作为水印。

### Q: 支持哪些图片格式？
A: 支持常见的图片格式，包括PNG、JPG、JPEG、BMP和GIF。

### Q: 程序处理图片时出现错误怎么办？
A: 检查输入路径是否正确，确保您有足够的读写权限，并确保所有依赖库已正确安装。

### Q: 为什么我的水印颜色与预期不符？
A: 请检查您提供的颜色值是否正确。预定义颜色不区分大小写，但HEX代码需要以#开头并包含正确的十六进制值。

### Q: 我可以在Windows、Mac和Linux上使用这个工具吗？
A: 是的，只要您的系统上安装了Python和所需的依赖库，该工具可以在所有主流操作系统上运行。

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 功能扩展建议

以下是一些可能的功能扩展方向：

1. 添加自定义文本水印功能，而不仅限于日期
2. 支持添加图片水印
3. 提供更多水印样式选项，如旋转、背景、边框等
4. 添加图形用户界面(GUI)
5. 支持批处理进度显示

## 贡献指南

欢迎提交问题和改进建议！如果您想贡献代码，请遵循以下步骤：

1. Fork本仓库
2. 创建您的功能分支
3. 提交您的更改
4. 推送到您的分支
5. 提交Pull Request