// static/ocr.js
document.getElementById('processBtn').addEventListener('click', processImage);
// 改用事件监听（推荐）
// 避免使用 onclick 属性，改用 JavaScript 事件绑定：
function processImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('请先选择图片文件');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // 显示加载状态
    const resultText = document.getElementById('resultText');
    resultText.textContent = '识别中...';
    
    // 发送到后端OCR接口
    fetch('/workspace1/ocr', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        resultText.textContent = data.text || '未识别到文字';
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