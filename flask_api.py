from flask import Flask,Request,Response, jsonify,request, abort, make_response,url_for
from models import AdminPermission,AdminUsers,FunctionGroups,FunctionPoint,FunctionPointAll
from db import database
from sqlalchemy import and_
import json
from migrate import MyEncoder
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

#登录
@app.route('/login',methods=['POST'])
def login():
    session = database.sess()
    login_name = request.form["login_name"]
    password = request.form["password"]
    user_info = session.query(AdminUsers.login_name,AdminPermission.permission)\
        .filter(AdminUsers.login_name==login_name,AdminUsers.password==password,AdminUsers.id==AdminPermission.user_id)\
        .all()
    if len(user_info) == 0:
        abort(404)
    userObj = user_info[0]
    power = query_menu(login_name)
    return jsonify({"name":userObj.login_name,"token":"1111111","power": power,"code":"200"})

#获取功能列表
@app.route('/point_all', methods=['GET'])
def point_all():
    session = database.sess()
    results = session.query(FunctionPointAll).all()
    function_arr = []
    for result in results:
        function_obj = dict()
        function_obj['id'] = result.id
        function_obj['label'] = result.name
        function_obj['path'] = result.path
        function_arr.append(function_obj)
    return jsonify({"point_all":json.dumps(function_arr), "code":"200"})

#添加新功能
@app.route('/add_fun', methods=['POST'])
def add_fun():
    session = database.sess()
    group_id = request.form["group_id"]
    fun_id = request.form["fun_id"]
    fun_groups = session.query(FunctionGroups).filter(FunctionGroups.id==group_id).first()
    children = fun_groups.children
    if fun_id not in children:
        fun_groups.children = children+","+fun_id
        session.commit()
    return jsonify({"result":'is ok', "code":"200"})

#获取菜单
@app.route('/menu',methods=['POST'])
def menu():
    # session = database.sess()
    login_name = request.form["login_name"]
    # p = []
    power = query_menu(login_name)
    # p.append(menu)
    return jsonify({"power": power,"code":"200"})

def query_menu(login_name):
    session = database.sess()
    permission = session.query(AdminPermission.permission)\
        .filter(AdminUsers.login_name==login_name,AdminUsers.id==AdminPermission.user_id)\
        .first()
    fun_groups = session.query(FunctionGroups).filter(FunctionGroups.id.in_((permission[0]))).all()
    print(fun_groups)
    p = []
    for fun_group in fun_groups:
        menu = dict()
        menu["id"] = fun_group.id
        menu["label"] = fun_group.name
        #暂无用到
        menu['path'] = "/"
        print(fun_group.children)
        if fun_group.children:
            children_menu_list = []
            fun_points = session.query(FunctionPoint).filter(FunctionPoint.id.in_((fun_group.children))).all()
            print(fun_points)
            for fun_point in fun_points:
                children_menu = dict()
                children_menu["id"] = fun_point.id
                children_menu["label"] = fun_point.name
                children_menu["path"] = fun_point.path
                children_menu_list.append(children_menu)
            menu["children"] = children_menu_list
            p.append(menu)
    print(p)
    return p

#删除功能
@app.route('/delete/point',methods=['POST'])
def delete_point():
    session = database.sess()
    group_id = request.form["group_id"]
    fun_id = request.form["fun_id"]
    fun_groups = session.query(FunctionGroups).filter(FunctionGroups.id==group_id).first()
    children = fun_groups.children
    children = children.split(",")
    if fun_id in children:
        children.remove(fun_id)
        fun_groups.children = ','.join(children)
        session.commit()
        return jsonify({"result": 'is ok', "code": "200"})
    else:
        return jsonify({"result": 'is error', "code": "404"})




#后端登出 注销token
@app.route('/logout',methods=['POST'])
def logout():
    return jsonify({"code":"200"})

@app.route('/user/<int:user_id>',methods=['GET'])
def get_user_info(user_id):
    name = request.args.get('name')
    return name

@app.route('/getUserInfo/<user_id>',methods=['GET'])
def user_info(user_id):
    session = database.sess()
    user_mes = session.query(AdminUsers).filter(AdminUsers.id == user_id).all()
    if len(user_mes) == 0:
        abort(404)
    return user_id
@app.route('/userRegister/',methods=['POST'])
def user_register():
    if not request.json or not 'login_name' in request.json:
        abort(404)

    return jsonify({'result':'is ok'}),201



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    result = list(map(make_public_task, tasks))
    print(type(result))
    print(result)
    return jsonify({'tasks': list(map(make_public_task, tasks))})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}),404)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
