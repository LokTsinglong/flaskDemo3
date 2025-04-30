// static/ocr.js
document.getElementById('processBtn').addEventListener('click', processImage);
// 改用事件监听（推荐）
// 避免使用 onclick 属性，改用 JavaScript 事件绑定：
function processImage() {
    const keyword = document.getElementById('keyword').value.trim();
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('请先选择图片文件');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('keyword', keyword); 

    // 显示加载状态
    const resultText = document.getElementById('resultText');
    resultText.textContent = '识别中...';
    
    // 发送到后端OCR接口
    fetch('/workspace1/ocr', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // 首先检查HTTP状态码
        if (!response.ok) {
            // 尝试解析错误信息
            return response.json().then(errorData => {
                throw new Error(errorData.error || `服务器错误: ${response.status}`);
            }).catch(() => {
                throw new Error(`HTTP错误: ${response.status}`);
            });
        }
        return response.json();
    })
    // .then(response => response.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        
        const keyword = document.getElementById('keyword').value.trim();
        // let result = '';
        let result = `原始识别结果：\n${data.text}\n\n`;
        
        if (keyword) {
            result += `提取结果：「${keyword}」后的数字为：${data.extracted}`;
        }
        
        resultText.textContent = result;
    })
    
    .catch(error => {
        console.error('Error:', error);
        resultText.textContent = '识别失败: ' + error.message;
    });
}

// 图片预览功能
document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    const preview = document.getElementById('imagePreview');
    
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
});