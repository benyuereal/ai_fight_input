from openai import OpenAI
import pandas as pd
import flight_ctrip_crawler


def ai_flights_context(content):
    """
    分析航班数据并返回模型推荐的航班信息。

    参数:
        file_path (str): 航班数据文件的路径。

    返回:
        str: 模型推荐的航班信息。
    """
    # 初始化 OpenAI 客户端
    client = OpenAI(api_key="sk-9aa26ea523044fed9e8fb5a1b3bec918", base_url="https://api.deepseek.com")

    print(content)

    try:
        # 将文件内容作为用户输入传递给模型
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "帮我分析一下下面的信息，分析出发城市、到达城市、出发日期，并且以json的数据形式返回给我,只返回json数据，返回的出发日期必须是2025年，字段分别为:departure_city、arrival_city、begin_date"},
                {"role": "user", "content": content},
            ],
            response_format={
                'type': 'json_object'
            },
            stream=False
        )

        # 返回模型的回复
        return response.choices[0].message.content

    except FileNotFoundError:
        return "文件未找到，请检查路径。"
    except Exception as e:
        return f"发生错误：{e}"

if __name__ == "__main__":
    # 示例文件路径
    file_path = "/Users/Zhuanz/IdeaProjects/flight-app-backend/2025-01-25/2025-01-02/上海-北京.csv"

    # 调用方法并输出结果
    result = ai_flights_context("亲，1.24或者25号，珠海到北京有优惠价吗？")
    print(result)