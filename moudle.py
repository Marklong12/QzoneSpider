import requests
import re
import random
import json
import datetime

def main(num):

    path='D:\code\QZONE\main.txt'
    headers1= {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59"
    }

    headers2 = {

        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/53"
        }

    ls=(headers1,headers2)
    headers=random.choice(ls)
    cookies=dict(pt4_token=   ,p_uin=  ,p_skey=)
    url="https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6"
    params={
        'g_tk': 00000,
        'uin':    ,
        'pos':20,
        #可自行修改
        'num':100}
        #可自行修改
    response=requests.get(url=url,headers=headers,cookies=cookies)
    print(response)
    print(response.text)
    raw_data=response.text
    with open(path,'w') as f:
        f.write(response.text)

    json_start = raw_data.find('{')
    json_end = raw_data.rfind('}') + 1
    json_data = raw_data[json_start:json_end]

    # 自定义JSON解码器处理控制字符
    class ControlCharIgnoringDecoder(json.JSONDecoder):
        def decode(self, s, *args, **kwargs):
            # 替换所有控制字符为空格（包括制表符、换行符等）
            s = re.sub(r'[\x00-\x1f]', ' ', s)
            return super().decode(s, *args, **kwargs)

    # 解析JSON
    try:
        data = json.loads(json_data, cls=ControlCharIgnoringDecoder)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"错误位置: {e.pos}")
        # 打印错误位置附近的文本以便调试
        start = max(0, e.pos - 50)
        end = min(len(json_data), e.pos + 50)
        print("错误附近内容:")
        print(json_data[start:end])
        exit(1)

    # 处理函数：转换时间戳
    def format_timestamp(timestamp):
        if timestamp is None or timestamp == 0:
            return ""
        try:
            dt = datetime.datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError, OSError) as e:
            print(f"时间戳转换错误: {timestamp} - {e}")
            return str(timestamp)

    # 处理单条动态
    def process_msg(msg):
        # 基础信息
        result = {
            "tid": msg.get("tid", ""),
            "content": msg.get("content", ""),
            "created_time": format_timestamp(msg.get("created_time")),
            "source_device": msg.get("source_name", ""),
            "comment_count": msg.get("cmtnum", 0),
            "forward_count": msg.get("fwdnum", 0),
            "images": [],
            "comments": [],
            "forwarded_content": None
        }
        
        # 处理图片
        for pic in msg.get("pic", []):
            # 优先使用url1，如果没有则使用pic_id
            url = pic.get("url1", pic.get("pic_id", ""))
            image_data = {
                "url": url,
                "height": pic.get("height", 0),
                "width": pic.get("width", 0)
            }
            result["images"].append(image_data)
        
        # 处理可能的None值评论列表
        commentlist = msg.get("commentlist")
        if commentlist is None:  # 显式处理None情况
            commentlist = []
        
        # 处理评论
        for comment in commentlist:
            comment_data = {
                "commenter": comment.get("name", ""),
                "content": comment.get("content", ""),
                "comment_time": format_timestamp(comment.get("create_time")),
                "replies": []
            }
            
            # 处理二级回复
            replies = comment.get("list_3", [])
            for reply in replies:
                reply_data = {
                    "replier": reply.get("name", ""),
                    "content": reply.get("content", ""),
                    "reply_time": format_timestamp(reply.get("create_time"))
                }
                comment_data["replies"].append(reply_data)
            
            result["comments"].append(comment_data)
        
        # 处理转发内容
        if "rt_con" in msg:
            rt_con = msg["rt_con"]
            result["forwarded_content"] = {
                "content": rt_con.get("content", ""),
                "original_poster": rt_con.get("rt_uinname", ""),
                "original_tid": rt_con.get("rt_tid", "")
            }
        
        return result

    # 处理用户信息
    user_info = {
        "uin": data["logininfo"]["uin"],
        "name": data["logininfo"]["name"],
        "total_messages": data["usrinfo"]["msgnum"],
        "latest_messages": []
    }

    # 处理动态列表
    for msg in data["msglist"]:
        try:
            processed_msg = process_msg(msg)
            user_info["latest_messages"].append(processed_msg)
        except Exception as e:
            print(f"处理动态时出错 (tid: {msg.get('tid', 'unknown')}): {e}")

    # 转换为易读JSON
    formatted_json = json.dumps(user_info, indent=2, ensure_ascii=False)

    # 输出结果
    print(formatted_json)

    # 保存到文件
    with open("qq_space_data.json", "a", encoding="utf-8") as f:
        f.write(formatted_json)