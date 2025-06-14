# QzoneSpider
# QQ空间动态抓取工具

这个工具可以定时抓取QQ空间动态，并将抓取到的数据保存为结构化的JSON格式。

## 功能概述

- 定时抓取QQ空间动态数据
- 自动处理原始JSON数据中的特殊字符
- 将动态内容结构化保存
- 支持图片、评论、转发内容的抓取
- 自动转换时间戳为可读格式

## 文件结构

```
qq-space-crawler/
├── run.py              # 主运行脚本
├── moudle.py           # 核心功能模块
└── qq_space_data.json  # 输出文件（运行后生成）
```

## 代码说明

### run.py

```python
import moudle
import time

num=0
while 1:
    num+=1
    moudle.main(num)
    time.sleep(1)
```

这个脚本会：
1. 导入核心功能模块
2. 创建一个无限循环
3. 每次循环调用抓取功能并传入计数
4. 每次抓取间隔1秒

### moudle.py

这个模块包含核心功能：

1. **请求配置**：
   - 使用随机User-Agent模拟浏览器
   - 设置固定cookies用于身份验证
   - 定义API请求参数

2. **数据处理**：
   - 提取有效JSON数据
   - 自定义JSON解码器处理控制字符
   - 时间戳转换工具

3. **数据结构化**：
   - 动态内容提取（文本、图片、转发内容）
   - 评论及回复处理
   - 用户信息收集

4. **输出**：
   - 原始数据保存为main.txt
   - 结构化数据追加到qq_space_data.json

## 使用说明

1. **安装依赖**：
   ```bash
   pip install requests
   ```

2. **配置参数**：
   - 修改`moudle.py`中的cookies值：
     ```python
     cookies=dict(pt4_token='YOUR_TOKEN',p_uin='YOUR_UIN',p_skey='YOUR_SKEY')
     ```
   - 修改目标用户ID：
     ```python
     'uin':TARGET_UIN
     ```

3. **运行程序**：
   ```bash
   python run.py
   ```

4. **查看结果**：
   结构化数据将保存在`qq_space_data.json`文件中

## 输出数据结构

```json
{
  "uin": "1395650301",
  "name": "用户名",
  "total_messages": 120,
  "latest_messages": [
    {
      "tid": "动态ID",
      "content": "动态内容",
      "created_time": "2023-01-01 12:00:00",
      "source_device": "发布设备",
      "comment_count": 5,
      "forward_count": 3,
      "images": [
        {
          "url": "图片链接",
          "height": 800,
          "width": 600
        }
      ],
      "comments": [
        {
          "commenter": "评论者",
          "content": "评论内容",
          "comment_time": "2023-01-01 12:05:00",
          "replies": [
            {
              "replier": "回复者",
              "content": "回复内容",
              "reply_time": "2023-01-01 12:10:00"
            }
          ]
        }
      ],
      "forwarded_content": {
        "content": "转发内容",
        "original_poster": "原发布者",
        "original_tid": "原动态ID"
      }
    }
  ]
}
```

## 注意事项

1. 需要有效的QQ空间cookies才能正常运行
2. 抓取频率不宜过高，避免被QQ服务器封禁
3. 输出文件`qq_space_data.json`使用追加模式写入
4. 原始响应数据会覆盖写入`main.txt`

## 自定义选项

1. **修改抓取间隔**：
   在`run.py`中调整`time.sleep()`的值

2. **修改抓取数量**：
   在`moudle.py`中修改params中的num参数

3. **修改输出路径**：
   在`moudle.py`中修改path变量

4. **添加更多请求头**：
   在headers元组中添加更多User-Agent选项

## 贡献指南

欢迎提交改进建议！请确保：
1. 代码符合PEP8规范
2. 提交详细的修改说明
3. 更新相关文档
4. 测试代码功能正常
