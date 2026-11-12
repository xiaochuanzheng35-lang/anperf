# AGENTS.md

给 AI 编码代理（以及人类协作者）的项目约定。修改代码前请先读完本文件。

## 项目是什么

AnPerf：基于视频帧分析的性能计时工具。从视频中按配置定位锚点帧（文字出现/消失、区域图像变化起止等），
再由锚点帧序号与视频帧率计算时间。面向自动化性能测试场景，命令行批处理风格。

## 常用命令

```bash
python anperf.py <caseConfigPath> <inputProcRdsPath> <outAnaDataPath> [debugWorkPath]
                              # 主入口；输出 testResult.json / testInfo.json
python -m py_compile anperf.py procline/*.py method4proc/*.py
                              # 提交前必须过的语法检查
python build.py               # PyInstaller 打包（产出 build/ dist/，已 gitignore）
```

运行依赖 `numpy opencv-python scipy matplotlib scikit-image pandas requests`。

## 架构与数据流

```
anperf.py（参数解析）
  └► procline/perfAnaMain.videoAnalyze(videoFile, caseConfigDict)
       └► procline/compline.setline2Compute      按配置串接检测站，逐站定位锚点帧
            └► procline/compstation.procVideo    逐帧取帧 → 预处理 → 调检测方法
       └► procline/calcBeginEndFrameIndex        选出起止锚点
       └► tools/anPerfToolCalcFrameTime          帧差 / fps → 时间(ms)
```

| 目录 | 职责 |
| --- | --- |
| `method4preproc/` | 预处理方法（旋转、增亮、去闪烁） |
| `method4proc/` | 锚点检测方法库（每个类一种方法） |
| `procline/` | 流水线编排、公共状态、时间计算 |
| `tools/` | 通用工具：JSON/文件、OCR 客户端、调试可视化、曲线分析 |

## 新增检测方法的接口契约（最重要）

检测方法 = `method4proc/` 下的一个**类**，类名即配置里的 `findFrameMethod` 值（如 `findKeywords`），
由 `perfAnaCommon.getClassObj("method4proc", 类名)` 反射加载。必须实现：

```python
class myMethod(object):
    def init(self, methodConfigDict):
        # 从 methodConfigDict 读参数，非法配置 print 错误并 return -1
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        # procFrameList: 按帧序排列的图像帧；frameIdxList 与之对齐
        # 找到锚点帧时 return 对应帧序号(>0)；没找到 return -1
```

- 参数统一走 `methodConfigDict`，阈值用 `perfAnaParam.getThreshold`，返回点（appear/disappear）
  用 `perfAnaParam.getReturnPoint`，不要自造键名
- 预处理由配置 `preprocMethod` / `preprocMethodList` 挂载，检测方法不要自己旋转/增亮
- 调试图像统一走 `tools/anPerfToolDebug.showCvImage`，受 debug_level 控制

## 关键配置约定（不要在代码里绕开）

- 用例配置顶层：`compStationConfigList`（检测站列表）、`compBeginEndTimeConfDict`、`ocr_srv_url`
- 每个检测站：`computeFrameData = [startFrmIdx, skipFrameNum, stepFrmNum, maxCompFrameNum]`，
  其中 `startFrmIdx < 0` 表示"相对上一个已找到的锚点"（负数索引），这是站间依赖的实现方式
- `videoProcWay`：`forward` / `reverse`（反向播放帧序列，用于检测"消失"类事件）
- `areaRectSpecified`：只分析指定区域，检测方法拿到的帧已经裁剪过

## 禁区与注意事项

- **禁止硬编码环境特定信息**：IP、端口、服务器地址、内部系统名一律不进代码。
  外部服务地址（如 OCR）只从用例配置注入（`ocr_srv_url` → `anPerfToolOcr.init()`），
  代码里的默认值只允许 `127.0.0.1`
- OCR 检测（`findKeywords`、`findAreaString`、`findDigitNumber` 等）依赖外部 OCR HTTP 服务，
  离线环境请选纯视觉方法（SIFT/SSIM/光流/亮度类）；新增依赖 OCR 的方法要在 README 说明
- 不引入新的第三方库；确有必要先开 Issue 讨论理由
- 帧读取成本高：能用 `videoCap.grab()` 跳帧就不要 `read()`（参考 `compstation._stepFrames`）
- 错误处理风格：可恢复错误 `print` + 返回 -1/空 dict，让流水线继续走完

## 提交规范

- `类型: 一句话说明`，类型：feat / fix / docs / refactor / chore
- 一个提交一件事；新功能开 `feature/xxx` 分支，完成后 `merge --no-ff` 回 main
- 提交前跑上面的 `py_compile` 语法检查
