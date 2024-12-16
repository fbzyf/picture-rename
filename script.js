class ImageRenamer {
    constructor() {
        this.selectedFiles = [];
        this.apiKey = 'sk-a86443b11a674f93ad2b1492ca10f23c';
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.fileInput = document.getElementById('fileInput');
        this.selectButton = document.getElementById('selectButton');
        this.processButton = document.getElementById('processButton');
        this.imageList = document.getElementById('imageList');
        this.status = document.getElementById('status');
    }

    setupEventListeners() {
        this.selectButton.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.processButton.addEventListener('click', () => this.processImages());
    }

    async handleFileSelect(event) {
        this.selectedFiles = Array.from(event.target.files);
        this.processButton.disabled = this.selectedFiles.length === 0;
        await this.displaySelectedImages();
    }

    async displaySelectedImages() {
        this.imageList.innerHTML = '';
        for (const file of this.selectedFiles) {
            const div = document.createElement('div');
            div.className = 'image-item';
            
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            
            div.appendChild(img);
            this.imageList.appendChild(div);
        }
    }

    async processImages() {
        this.status.style.display = 'block';
        this.status.textContent = '处理中...';
        
        for (const file of this.selectedFiles) {
            try {
                // 1. 进行OCR识别
                const text = await this.performOCR(file);
                
                // 2. 调用DeepSeek AI生成文件名
                const newName = await this.generateFileName(text);
                
                // 3. 重命名并下载文件
                await this.downloadFile(file, newName);
                
            } catch (error) {
                console.error('处理图片时出错:', error);
            }
        }
        
        this.status.textContent = '处理完成！';
    }

    async performOCR(file) {
        const image = await createImageBitmap(file);
        const result = await Tesseract.recognize(image);
        return result.data.text;
    }

    async generateFileName(text) {
        const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: "deepseek-chat",
                messages: [
                    {
                        role: "system",
                        content: "你是一个文件命名助手。请根据提供的文本内容，生成一个简短的、描述性的文件名（不超过50个字符）。"
                    },
                    {
                        role: "user",
                        content: text
                    }
                ]
            })
        });

        const data = await response.json();
        return data.choices[0].message.content.trim();
    }

    async downloadFile(file, newName) {
        const extension = file.name.split('.').pop();
        const fullNewName = `${newName}.${extension}`;
        
        const url = URL.createObjectURL(file);
        const a = document.createElement('a');
        a.href = url;
        a.download = fullNewName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// 初始化应用
new ImageRenamer(); 