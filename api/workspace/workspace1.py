from flask import Blueprint, render_template, session, redirect, url_for,jsonify,request
from PIL import Image
import pytesseract
import re
import io

# 配置Tesseract的路径
pytesseract.pytesseract.tesseract_cmd = r'D:\TesseractOCR\tesseract.exe'
# 子蓝图：实际路径 /workspace/1
workspace1_api = Blueprint('workspace1_api', __name__, template_folder='../../templates')
# from . import workspace1_api 注意这里的应用名字是blueprint的名字

def ocr_from_image(file_stream):
    try:
        # 直接从文件流打开图片
        img = Image.open(io.BytesIO(file_stream))
        
        # 转换图片模式为RGB（解决某些PNG图片的Alpha通道问题）
        if img.mode in ('RGBA', 'LA'):
            img = img.convert('RGB')
            
        # 使用Tesseract进行OCR识别
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        return text.strip(), None
    
    except Exception as e:
        return None, str(e)
    
def extract_number_after_keyword(text, keyword):
    """
    提取关键词后的第一个连续数字
    """
    try:
        # 转义关键词中的特殊字符
        pattern = re.escape(keyword) + r'\s*(\d+)'
        match = re.search(pattern, text)
        
        if match:
            return match.group(1)
        return f"未找到「{keyword}」后的数字"
    except Exception as e:
        return f"提取错误: {str(e)}"
    
@workspace1_api.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("workspace1.html")



@workspace1_api.route('/ocr', methods=['POST'])
def ocr():
    
    # 检查用户登录状态
    if 'user' not in session:
        return jsonify({'error': '未登录'}), 401
    
    # 检查文件上传
    if 'image' not in request.files:
        return jsonify({'error': '未选择文件'}), 400
        
    file = request.files['image']
     # 新增获取关键词参数
    keyword = request.form.get('keyword', '').strip()
    
    # 验证文件名
    if file.filename == '':
        return jsonify({'error': '空文件名'}), 400
    
    # 验证文件类型
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': '仅支持PNG/JPG/JPEG格式'}), 400
    try:
        # 在内存中处理文件
        file_stream = file.read()
        text, error = ocr_from_image(file_stream)
         # 新增数字提取逻辑
        extracted_number = extract_number_after_keyword(text, keyword) if keyword else text
        
        if error:
            return jsonify({'error': error}), 500
            
        # return jsonify({'text': text})
        return jsonify({ 'text': text, 'extracted': extracted_number})
        
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500