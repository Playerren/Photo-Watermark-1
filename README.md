# 图片水印工具

这是一个命令行工具，可以自动为图片添加基于拍摄日期（EXIF信息）的水印。

## 功能特点

- 从图片的EXIF信息中提取拍摄日期作为水印文本
- 支持自定义水印字体大小、颜色和位置
- 支持处理单个图片文件或整个目录下的所有图片
- 自动将添加水印后的图片保存到原目录的_watermark子目录中

## 安装依赖

```bash
pip install -r requirements.txt
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

### 自定义选项

```bash
python watermark_tool.py /path/to/your/image.jpg --font-size 40 --color red --position bottom_right
```

### 可用选项

- `--font-size`：水印字体大小（默认：30）
- `--color`：水印颜色（可以是预定义颜色名称如'white'、'black'、'red'等，或HEX代码如'#FF0000'，默认：'white'）
- `--position`：水印位置（可选值：'top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'，默认：'bottom_right'）

## 注意事项

1. 程序会自动创建输出目录，命名为原目录名加上'_watermark'后缀
2. 如果图片没有EXIF信息，将使用文件的修改时间作为水印
3. 如果文件修改时间也无法获取，将使用当前日期作为水印
4. 支持的图片格式：PNG、JPG、JPEG、BMP、GIF

## 依赖库

- Pillow：用于图像处理
- piexif：用于读取EXIF信息

## 示例

为图片添加红色、居中的水印，字体大小为40：

```bash
python watermark_tool.py ./photos/image.jpg --font-size 40 --color red --position center
```

处理整个目录，使用黑色水印，位置在左上角：

```bash
python watermark_tool.py ./photos --color black --position top_left
```