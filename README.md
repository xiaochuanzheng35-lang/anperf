# AnPerf · 基于视频帧分析的性能计时工具

从录屏/录像中自动定位**锚点帧**（如指定区域文字的出现/消失、指定区域图像变化的开始/结束），
再根据锚点帧序号与视频帧率计算两个事件之间的时间，用于自动化测量性能时间（精度 = 单帧时长）。

## 工作原理

```
视频 ──► 预处理 ──► 逐帧特征检测（定位锚点帧序号）──► 选定起点/终点锚点 ──► 时间 = Δ帧 / fps
```

三个模块各司其职：

| 模块 | 职责 |
| --- | --- |
| `method4preproc/` | 预处理：旋转、增亮、去闪烁等 |
| `method4proc/` | 锚点检测方法库：关键字/区域文字查找、SIFT 面积变化、SSIM 差异、光流运动、亮度突变（Otsu）等 |
| `procline/` | 把检测方法按配置串成流水线，选出起止锚点，按帧率换算时间 |

检测方法通过用例配置（JSON）组合，无需改代码即可适配新的测试场景。

## 使用

```bash
python anperf.py <caseConfigPath> <inputProcRdsPath> <outAnaDataPath> [debugWorkPath]
```

- `caseConfigPath`：用例配置目录
- `inputProcRdsPath`：输入数据路径（工具会从中定位视频文件）
- `outAnaDataPath`：结果输出目录（已存在时写入 `testResult.json` 与 `testInfo.json`）
- `debugWorkPath`：可选，调试用，会加载/落盘关键帧序号列表

输出示例：

```json
{ "perftime": 1234 }          // 毫秒
{ "timeStampLst": [12, 49] }  // 起止锚点帧对应的时刻（秒）
```

## 环境依赖

Python 3，第三方库：

```bash
pip install numpy opencv-python scipy matplotlib scikit-image pandas requests
```

打包为可执行文件使用 `build.py`（基于 PyInstaller）。

## 目录结构

```
anperf.py              入口：解析参数 → 初始化 → 分析 → 输出结果
build.py               PyInstaller 打包脚本
method4preproc/        预处理方法
method4proc/           锚点检测方法库
procline/              流水线编排与时间计算
tools/                 通用工具（文件/JSON 操作、曲线分析等）
```
