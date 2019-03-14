from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
import datetime
from db import database


Base = declarative_base()
class AdminUsers(Base):
    __tablename__ = 'admin_users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    login_name = Column(String(50),nullable=True)
    password = Column(String(100),nullable=True)
    level = Column(String(10),nullable=True)
    department = Column(String(10),nullable=True)
    created_at = Column(DateTime,nullable=True)
    updated_at = Column(DateTime,onupdate=datetime.datetime.now())
    last_login_at = Column(DateTime)

    #console 输出可读的数据
    def __repr__(self):
        return "<id:{0} login_name:{1} password:{2} level:{3} department:{4} created_at:{5}" \
               " updated_at:{6} last_login_at:{7}>".format(self.id,self.login_name,self.password,self.level,self.department,self.created_at,self.updated_at,self.last_login_at)

class AdminPermission(Base):
    __tablename__ = 'admin_permission'
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,unique=True)
    role = Column(String(20),nullable=True)
    permission = Column(Text,nullable=True)
    def __repr__(self):
        return "<id:{0} user_id:{1} role:{2} permission:{3}>".format(self.id,self.user_id,self.role,self.permission)

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(20), nullable=True)
    amount = Column(Integer,nullable=True)
    interest = Column(Integer,nullable=True)
    interest_rate = Column(Integer,nullable=True)
    service_fee = Column(Integer,nullable=True)
    debts_type = Column(String(20), nullable=True)
    created_at = Column(DateTime,nullable=True)

class FunctionGroups(Base):
    __tablename__ = 'function_groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True)
    children_function_group = Column(String(20), nullable=True)
    children = Column(String(20), nullable=True)
    def __repr__(self):
        return "<id:{0} name:{1} children_function_group:{2} children:{3}>".format(self.id,self.name,self.children_function_group,self.children)

class FunctionPoint(Base):
    __tablename__ = 'function_point'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True)
    path = Column(String(20), nullable=True)
    power_node = Column(String(200), nullable=True)
    show_str = Column(Text, nullable=True)
    def __repr__(self):
        return "<id:{0} name:{1} path:{2} power_node:{3}, show_str:{4} >".format(self.id,self.name,self.path,self.power_node,self.show_str)

class FunctionPointAll(Base):
    __tablename__ = 'function_point_all'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True)
    path = Column(String(20), nullable=True)
    power_node = Column(String(200), nullable=True)
    show_str = Column(Text, nullable=True)
    def __repr__(self):
        return "<id:{0} name:{1} path:{2} power_node:{3}, show_str:{4} >".format(self.id, self.name, self.path,self.power_node, self.show_str)

# 创建表
Base.metadata.create_all(database.engine)