// 初始化可视化实例
let viz;

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    initVisualization();
    bindEvents();
});

// 事件绑定函数
function bindEvents() {
    document.getElementById('uploadBtn').addEventListener('click', handleUpload);
    document.getElementById('refreshBtn').addEventListener('click', refreshGraph);
}

// 图谱初始化配置
function initVisualization() {
    const config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "123456"
        },
        labels: {
            "buy": { 
                label: "name",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                    color: "#FF6B6B"
                }
            },
            "sell": { 
                label: "amount",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                    color: "#4ECDC4"
                }
            }
        },
        relationships: {
            "money": { 
                caption: "value",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                    color: "#666"
                }
            }
        },
        initialCypher: "MATCH (n)-[r:money]->(m) RETURN n,r,m LIMIT 100"
    };
    
    viz = new NeoVis.default(config);
    viz.render();
}

// 文件上传处理
async function handleUpload() {
    const fileInput = document.getElementById('excelFile');
    const statusDiv = document.getElementById('uploadStatus');

    if (!fileInput.files.length) {
        statusDiv.innerHTML = "⚠️ 请先选择文件";
        return;
    }

    statusDiv.innerHTML = "⏳ 上传中...";
    
    try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('上传失败');
        
        statusDiv.innerHTML = "✅ 上传成功";
        refreshGraph();
        
    } catch (error) {
        statusDiv.innerHTML = `❌ 错误: ${error.message}`;
    }
}

// 图谱刷新函数
function refreshGraph() {
    viz.renderWith({ 
        initialCypher: "MATCH p=()-[r:money]->() RETURN p LIMIT 200",
        visConfig: {
            edges: { 
                arrows: { to: { scaleFactor: 0.5 } }
            }
        }
    });
}