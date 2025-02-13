
##### 首先替换掉自己的apikey和大模型api接口

本案例中使用的是deepseek的接口
```pycon
    # 初始化 OpenAI 客户端
    client = OpenAI(api_key="sk-9aa26ea523044fed9e8fb5a1b3bec918", base_url="https://api.deepseek.com")

```
##### 启动后端项目
app.py main方法

##### 进行检索
1. 智能模式检索
   http://localhost:5000/search_flights/context?context=%E5%96%80%E4%BB%80%E5%88%B0%E8%A5%BF%E5%AE%89%E7%9A%84%E6%9C%BA%E7%A5%A8%203.12%203.13%E4%BB%80%E4%B9%88%E4%BB%B7%E6%A0%BC
2. 精准模式检索
   http://localhost:5000/search_flights?departure_city=%E4%B8%8A%E6%B5%B7&arrival_city=%E5%8C%97%E4%BA%AC&begin_date=2025-03-25&end_date=2025-03-25

##### 得到结果