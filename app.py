from flask import Flask, request, render_template, redirect
from supabase import create_client
import qrcode
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

app = Flask(__name__)

# 初始化 Supabase 客户端
supabase = create_client(
    os.getenv("https://ylmwengsakeflaqlqaef.supabase.co"),
    os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlsbXdlbmdzYWtlZmxhcWxxYWVmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIyMzkzNzAsImV4cCI6MjA2NzgxNTM3MH0.eAIPIu0ro0Vwr2gx0kKZLmpUPUir88rePm5Gz518Z14")
)

# 生成二维码
def generate_qr(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 首页（生成二维码）
@app.route('/')
def home():
    feedback_url = f"{request.url_root}submit"  # 动态获取提交链接
    qr_img = generate_qr(feedback_url)
    return render_template('index.html', qr_img=qr_img)

# 提交意见
@app.route('/submit', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        content = request.form['content']
        supabase.table("feedback").insert({"content": content}).execute()
        return "感谢您的反馈！"
    return render_template('submit.html')

# 护士后台（查看数据）
@app.route('/admin')
def admin():
    data = supabase.table("feedback").select("*").order("created_at", desc=True).execute()
    return render_template('admin.html', feedbacks=data.data)

if __name__ == '__main__':
    app.run(debug=True)