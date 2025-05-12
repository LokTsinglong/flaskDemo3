from flask import Blueprint, render_template, session, redirect, url_for,jsonify,request

import pandas as pd
from py2neo import Graph, Node, Relationship

# 注册蓝图
workspace3_api = Blueprint('workspace3_api', __name__, template_folder='../../templates')

@workspace3_api.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("workspace3.html")


# Neo4j配置（硬编码简化版）
graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))



@workspace3_api.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_excel(file)
    
    # 清空现有数据
    # graph.delete_all()
    # 使用`graph.delete_all()`来清空数据，但这个方法在py2neo中可能已被弃用

    # 使用事务批量操作
    tx = graph.begin()

    # 清空现有数据
    graph.run("MATCH (n) DETACH DELETE n")
    
    # 创建节点
    buyers = df['甲方名称'].unique()
    sellers = df['乙方名称'].unique()
    
    for name in buyers:
        graph.create(Node("StartIS", name=name))
        
    for name in sellers:
        graph.create(Node("EndIS", name=name))
    
    # 创建关系
    for _, row in df.iterrows():
        buyer = graph.nodes.match("StartIS", name=row['甲方名称']).first()
        seller = graph.nodes.match("EndIS", name=row['乙方名称']).first()
        rel = Relationship(buyer, "Flow", seller, amount=row['金额'])
        graph.create(rel)

    # 提交事务
    tx.commit()
    
    return "数据上传成功！"

