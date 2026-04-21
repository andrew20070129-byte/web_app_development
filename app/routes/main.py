import random
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import main_bp
from app.models import Fortune, FortuneResult

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁路由
    GET: 渲染 templates/index.html，顯示網站簡介與主要操作入口
    """
    return render_template('index.html')

@main_bp.route('/fortune/draw', methods=['GET', 'POST'])
def draw_fortune():
    """
    抽籤/擲筊互動路由
    GET: 渲染 templates/fortune/draw.html 提供擲筊 UI
    POST: 當使用者擲出聖筊，後端隨機選取抽中的籤詩，並重導向至詳細頁面 (或回傳 JSON)
    """
    if request.method == 'POST':
        # 取得系統中所有的籤詩
        fortunes = Fortune.get_all()
        if not fortunes:
            flash("目前系統內沒有籤詩資料，請聯絡廟公/管理員新增！", "danger")
            return redirect(url_for('main.index'))
            
        # 隨機選出一首籤詩
        selected_fortune = random.choice(fortunes)
        
        # 若前端透過 AJAX 傳送要求，則回傳 JSON 以供前端處理跳轉動畫
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({
                "status": "success", 
                "fortune_id": selected_fortune.id,
                "redirect_url": url_for('main.fortune_detail', fortune_id=selected_fortune.id)
            })
            
        # 傳統表單提交的重導向
        return redirect(url_for('main.fortune_detail', fortune_id=selected_fortune.id))

    return render_template('fortune/draw.html')

@main_bp.route('/fortune/<int:fortune_id>', methods=['GET'])
def fortune_detail(fortune_id):
    """
    特定籤詩詳情與解析路由
    GET: 依照傳入的 fortune_id 查詢 DB，渲染 templates/fortune/detail.html 顯示詳細解籤內容
    """
    fortune = Fortune.get_by_id(fortune_id)
    if not fortune:
        flash("找不到指定的籤詩，請重新嘗試！", "warning")
        return redirect(url_for('main.draw_fortune'))
        
    return render_template('fortune/detail.html', fortune=fortune)

@main_bp.route('/fortune/<int:fortune_id>/save', methods=['POST'])
def save_fortune(fortune_id):
    """
    儲存算命紀錄路由
    POST: 必須在登入狀態下呼叫，將此支籤儲存進使用者的 FortuneResult 歷史紀錄中
    """
    # 檢查是否登入
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入才能將結果儲存至您的紀錄中！", "warning")
        return redirect(url_for('auth.login'))
        
    fortune = Fortune.get_by_id(fortune_id)
    if not fortune:
        flash("儲存失敗，該籤詩不存在。", "danger")
        return redirect(url_for('main.draw_fortune'))
        
    result = FortuneResult.create(user_id=user_id, fortune_id=fortune_id)
    if result:
        flash("籤詩已成功收入您的個人算命紀錄中！", "success")
    else:
        flash("處理儲存時發生系統錯誤，請稍後再試。", "danger")
        
    return redirect(url_for('profile.profile_index'))
