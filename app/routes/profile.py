from flask import render_template, request, redirect, url_for, flash, session
from . import profile_bp

@profile_bp.route('/profile', methods=['GET'])
def profile_index():
    """
    個人主頁路由
    GET: 需登入狀態。取出使用者以往儲存的算命歷史紀錄以及捐獻香油錢明細
         然後渲染 templates/profile/index.html 進行展示
    """
    pass

@profile_bp.route('/donate', methods=['GET'])
def donate_page():
    """
    捐獻香油錢表單頁面
    GET: 需登入狀態。渲染 templates/profile/donate.html 提供操作介面
    """
    pass

@profile_bp.route('/donate/checkout', methods=['POST'])
def donate_checkout():
    """
    處理香油錢捐獻付款的路由
    POST: 需登入狀態。接收捐款金額參數，模擬交易程序並將紀錄存入 Donations 表
          交易結果或感謝訊息將以 flash 提示並重導回 /profile
    """
    pass
