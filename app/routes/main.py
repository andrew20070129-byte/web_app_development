from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import main_bp

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁路由
    GET: 渲染 templates/index.html，顯示網站簡介與主要操作入口
    """
    pass

@main_bp.route('/fortune/draw', methods=['GET', 'POST'])
def draw_fortune():
    """
    抽籤/擲筊互動路由
    GET: 渲染 templates/fortune/draw.html 提供擲筊 UI
    POST: 當使用者擲出聖筊，後端隨機選取抽中的籤詩，並可能回傳 JSON 或重導向至詳細頁面
    """
    pass

@main_bp.route('/fortune/<int:fortune_id>', methods=['GET'])
def fortune_detail(fortune_id):
    """
    特定籤詩詳情與解析路由
    GET: 依照傳入的 fortune_id 查詢 DB，渲染 templates/fortune/detail.html 顯示詳細解籤內容
         若找不到紀錄則返回 404
    """
    pass

@main_bp.route('/fortune/<int:fortune_id>/save', methods=['POST'])
def save_fortune(fortune_id):
    """
    儲存算命紀錄路由
    POST: 必須在登入狀態下呼叫，將此支籤儲存進使用者的 FortuneResult 歷史紀錄中
          完成後重導向至個人主頁 /profile
    """
    pass
