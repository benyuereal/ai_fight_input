from openai import OpenAI
import pandas as pd
import flight_ctrip_crawler


def analyze_flights(begin_date, end_date, cities):
    """
    分析航班数据并返回模型推荐的航班信息。

    参数:
        file_path (str): 航班数据文件的路径。

    返回:
        str: 模型推荐的航班信息。
    """
    # 初始化 OpenAI 客户端
    client = OpenAI(api_key="sk-9aa26ea523044fed9e8fb5a1b3bec918", base_url="https://api.deepseek.com")

    result = flight_ctrip_crawler.search(begin_date,end_date, cities)

    simple_result = result[['departureDateTime', 'arrivalDateTime', 'economy_total','航班号', '飞行时长']]
    # 假设 simple_result 是一个 DataFrame
    # 确保 economy_total 列是数字类型
    simple_result.loc[:, 'economy_total'] = pd.to_numeric(simple_result['economy_total'], errors='coerce')
    simple_result.sort_values(by='economy_total', inplace=True)
    # 将 DataFrame 转换为字符串
    # 直接在原 DataFrame 上按照 'age' 列升序排序
    simple_result.sort_values(by='economy_total', inplace=True)
    data_json = simple_result.to_json(orient="records", force_ascii=False)
    print(data_json)

    try:
        # 将文件内容作为用户输入传递给模型
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "我想让您帮我分析一下下面航班，如果我喜欢便宜，选择一个最便宜的航班:"},
                {"role": "user", "content": data_json},
            ],
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
    result = analyze_flights("2025-01-12", "2025-01-12", ["北京", "上海"])
    print(result)