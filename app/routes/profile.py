from flask import render_template, request, redirect, url_for, flash, session
from . import profile_bp
from app.models import User, FortuneResult, Donation

@profile_bp.route('/profile', methods=['GET'])
def profile_index():
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入才能查看您的個人紀錄。', 'warning')
        return redirect(url_for('auth.login'))
        
    # 抓取該用戶所有的籤詩紀錄
    results = FortuneResult.get_by_user_id(user_id)
    # 抓取香油錢捐款明細
    donations = Donation.get_by_user_id(user_id)
    
    return render_template('profile/index.html', results=results, donations=donations)

@profile_bp.route('/donate', methods=['GET'])
def donate_page():
    if not session.get('user_id'):
        flash('請先登入，神明才能紀錄您的發心。', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('profile/donate.html')

@profile_bp.route('/donate/checkout', methods=['POST'])
def donate_checkout():
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    amount = request.form.get('amount')
    if amount and amount.isdigit() and int(amount) > 0:
        # 由於是 MVP 的開發模擬階段，我們假定收到直接設定為 completed 狀態
        donation = Donation.create(user_id=user_id, amount=int(amount), status='completed')
        if donation:
            flash(f'感謝您的發心！您已成功捐獻 NT$ {amount}。', 'success')
        else:
            flash('處理付款時發生錯誤，請稍後再試。', 'danger')
    else:
        flash('無效的金額格式，請返回重新輸入。', 'warning')
        
    return redirect(url_for('profile.profile_index'))
