import threading
import json
from flask import Flask, jsonify, request, abort
from ai_flight_charge import analyze_flights
from ai_flight_input import  ai_flights_context
app = Flask(__name__)

# 模拟数据存储
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]

# 获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# 获取单个用户
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user)

# 创建用户
@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'age' in request.json:
        abort(400, description="Invalid request: 'name' and 'age' are required")

    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": request.json["name"],
        "age": request.json["age"],
    }
    users.append(new_user)
    return jsonify(new_user), 201

# 更新用户
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        abort(404, description="User not found")

    if not request.json:
        abort(400, description="Invalid request: JSON body is required")

    user["name"] = request.json.get("name", user["name"])
    user["age"] = request.json.get("age", user["age"])
    return jsonify(user)

# 删除用户
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        abort(404, description="User not found")

    users = [user for user in users if user["id"] != user_id]
    return '', 204


@app.route('/search_flights', methods=['GET'])
def search_flights():
    departure_city = request.args.get('departure_city')
    arrival_city = request.args.get('arrival_city')
    begin_date = request.args.get('begin_date')
    end_date = request.args.get('end_date')

    if not departure_city or not arrival_city or not begin_date:
        return jsonify({"error": "Missing parameters: departure_city, arrival_city, flight_date"}), 400

    # 使用多线程运行爬虫，避免阻塞API
    citys = [departure_city, arrival_city]
    result = analyze_flights(begin_date, end_date, citys)

    # 返回爬取结果
    return result


@app.route('/search_flights/context', methods=['GET'])
def search_flights_context():
    context = request.args.get('context')
    json_string = ai_flights_context(context)
    # 将字符串转换为 JSON 对象（字典）
    json_object = json.loads(json_string)

    # 打印结果
    print(json_object)
    departure_city = json_object['departure_city']
    arrival_city = json_object['arrival_city']
    begin_date = json_object['begin_date']
    end_date = json_object['begin_date']

    if not departure_city or not arrival_city or not begin_date:
        return jsonify({"error": "Missing parameters: departure_city, arrival_city, flight_date"}), 400

    # 使用多线程运行爬虫，避免阻塞API
    citys = [departure_city, arrival_city]
    result = analyze_flights(begin_date, end_date, citys)

    # 返回爬取结果
    return result


# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)