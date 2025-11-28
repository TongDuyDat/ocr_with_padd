# Hướng dẫn Cài đặt PaddleOCR API

Tài liệu hướng dẫn cài đặt và triển khai API OCR sử dụng FastAPI và PaddleOCR.

---

## 📋 Yêu cầu Hệ thống

### Phần cứng
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB+)
- **GPU**: NVIDIA GPU với CUDA support (khuyến nghị)
  - VRAM: Tối thiểu 4GB
  - CUDA: 11.2+ hoặc 12.x
- **Ổ cứng**: 10GB trống (cho models và dependencies)

### Phần mềm
- **OS**: Linux (Ubuntu 20.04+), Windows 10/11, hoặc WSL2
- **Python**: 3.8, 3.9, hoặc 3.10
- **CUDA Toolkit**: 11.2+ (nếu dùng GPU)
- **cuDNN**: 8.x (nếu dùng GPU)

---

## 🚀 Cài đặt

### Bước 1: Chuẩn bị Môi trường

#### Tạo virtual environment (khuyến nghị)

```bash
# Sử dụng conda (khuyến nghị)
conda create -n ppocr python=3.9
conda activate ppocr

# Hoặc sử dụng venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### Bước 2: Cài đặt PaddlePaddle

#### Với GPU (CUDA 11.2+)

```bash
python -m pip install paddlepaddle-gpu==3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### Chỉ CPU

```bash
python -m pip install paddlepaddle==3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### Cấu hình LD_LIBRARY_PATH (Linux/WSL - QUAN TRỌNG!)

Nếu dùng GPU, cần set `LD_LIBRARY_PATH` để PaddlePaddle tìm được CUDA libraries:

```bash
# Kiểm tra CUDA installation path
which nvcc
# Output thường là: /usr/local/cuda-11.x/bin/nvcc hoặc /usr/local/cuda/bin/nvcc

# Set LD_LIBRARY_PATH (thay đổi version CUDA cho phù hợp)
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Để permanent, thêm vào ~/.bashrc hoặc ~/.zshrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

**Với Conda environment:**
```bash
# Set cho specific conda env
conda activate ppocr
conda env config vars set LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Hoặc tạo activation script
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

#### Kiểm tra cài đặt

```python
import paddle
print(paddle.__version__)
print("GPU available:", paddle.is_compiled_with_cuda())

# Kiểm tra CUDA device
import paddle
paddle.device.set_device('gpu:0')
print("CUDA device:", paddle.device.get_device())
```

### Bước 3: Cài đặt Dependencies

```bash
cd d:/ThucTap/OCR_Labs/padd_OCR

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

**Nội dung `requirements.txt`:**
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
paddleocr>=2.7.0
Pillow>=10.0.0
aiofiles>=23.2.1
pydantic>=2.0.0
```

### Bước 4: Cài đặt PaddleOCR

```bash
pip install paddleocr>=2.7.0
```

### Bước 5: Cấu hình Custom Model

#### Download hoặc copy custom model

Đảm bảo custom text recognition model đã có tại:
```
/mnt/d/ThucTap/OCR_Labs/models/tdd_ocr/
```

Hoặc update đường dẫn trong `config.py`:

```python
TEXT_OCR_CONFIG = {
    "text_recognition_model_dir": "/path/to/your/custom/model",
    # ...
}
```

---

## ⚙️ Cấu hình

### File `config.py`

Chỉnh sửa các thông số trong `config.py`:

#### 1. GPU/CPU Mode

```python
USE_GPU = True  # Set False nếu chỉ dùng CPU
```

#### 2. Model Paths

```python
TEXT_OCR_CONFIG = {
    "text_recognition_model_dir": "/mnt/d/ThucTap/OCR_Labs/models/tdd_ocr",
    # Adjust path theo hệ thống của bạn
}

TABLE_OCR_CONFIG = {
    "text_recognition_model_dir": "/mnt/d/ThucTap/OCR_Labs/models/tdd_ocr",
    # Adjust path theo hệ thống của bạn
}
```

#### 3. File Upload Settings

```python
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB (adjust nếu cần)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
```

#### 4. CORS Origins (nếu có frontend)

```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://your-frontend-domain.com",
]
```

---

## 🏃 Chạy Server

### Development Mode (với auto-reload)

```bash
# Từ thư mục padd_OCR
python main.py

# Hoặc sử dụng uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Sử dụng gunicorn với uvicorn workers
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### Background Mode (Linux)

```bash
# Sử dụng nohup
nohup python main.py > server.log 2>&1 &

# Hoặc systemd service (xem phần Deploy)
```

---

## 🧪 Kiểm tra Cài đặt

### 1. Health Check

```bash
curl http://localhost:8000/health
```

**Expected output:**
```json
{
  "status": "healthy",
  "service": "paddleocr_api",
  "gpu_enabled": true
}
```

### 2. Test Text OCR

```bash
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@test_image.png"
```

### 3. Test Table OCR

```bash
curl -X POST "http://localhost:8000/table?format=markdown" \
  -F "file=@table_image.png"
```

### 4. API Documentation

Truy cập trong browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Docker Deployment (Optional)

### Dockerfile

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run

```bash
# Build image
docker build -t paddleocr-api .

# Run container (CPU)
docker run -p 8000:8000 paddleocr-api

# Run container (GPU) - requires nvidia-docker
docker run --gpus all -p 8000:8000 paddleocr-api
```

---

## 🔧 Troubleshooting

### Lỗi: ModuleNotFoundError: No module named 'fastapi'

```bash
pip install fastapi uvicorn python-multipart
```

### Lỗi: CUDA not available

**Kiểm tra:**
```python
import paddle
print(paddle.is_compiled_with_cuda())
```

**Giải pháp:**
1. Kiểm tra CUDA installation:
   ```bash
   nvcc --version
   nvidia-smi
   ```

2. **Kiểm tra LD_LIBRARY_PATH** (Linux/WSL):
   ```bash
   echo $LD_LIBRARY_PATH
   # Phải include /usr/local/cuda/lib64
   
   # Nếu chưa có, set lại:
   export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
   ```

3. Cài đặt lại paddlepaddle-gpu với đúng CUDA version

4. Hoặc set `USE_GPU = False` trong config.py nếu không cần GPU

### Lỗi: libcudnn.so.x not found

```bash
# Lỗi: libcudnn.so.8: cannot open shared object file
```

**Giải pháp:**
```bash
# Kiểm tra cuDNN đã cài chưa
ldconfig -p | grep cudnn

# Nếu chưa, cài cuDNN hoặc add vào LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Verify
python -c "import paddle; print(paddle.device.cuda.device_count())"
```

### Lỗi: Model not found

**Kiểm tra đường dẫn:**
```bash
ls -la /mnt/d/ThucTap/OCR_Labs/models/tdd_ocr/
```

**Cập nhật config.py** với đường dẫn đúng.

### Lỗi: Address already in use (port 8000)

```bash
# Tìm process đang dùng port 8000
# Linux/Mac
lsof -i :8000
# Windows
netstat -ano | findstr :8000

# Kill process hoặc đổi port
uvicorn main:app --port 8001
```

### Server chậm khi request đầu tiên

**Bình thường!** Models đang được load lần đầu (3-5 giây). Các request sau sẽ nhanh hơn nhiều do model caching.

### Out of Memory Error

**Giải pháp:**
1. Giảm batch size (nếu có)
2. Giảm MAX_UPLOAD_SIZE
3. Set `USE_GPU = False` nếu VRAM không đủ
4. Tăng RAM/VRAM

---

## 📊 Monitoring & Logs

### Xem logs

```bash
# Development mode
# Logs hiển thị trực tiếp trên terminal

# Production với gunicorn
tail -f /var/log/paddleocr-api/access.log
tail -f /var/log/paddleocr-api/error.log
```

### Performance Monitoring

```python
# Thêm logging vào code
import logging
logging.basicConfig(level=logging.INFO)
```

---

## 🔐 Security (Production)

### 1. API Key Authentication (Optional)

Thêm middleware authentication trong `main.py`.

### 2. Rate Limiting

```bash
pip install slowapi

# Add to main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 3. HTTPS

Sử dụng reverse proxy (nginx) với SSL certificate.

---

## 🎯 Next Steps

1. ✅ Test API với các loại ảnh khác nhau
2. ✅ Monitor performance và memory usage
3. ✅ Set up monitoring (Prometheus/Grafana)
4. ✅ Configure backup cho models
5. ✅ Set up CI/CD pipeline

---

## 📞 Support

- **Issues**: Tạo issue trên repository
- **Documentation**: Xem `API_README.md` cho API usage
- **PaddleOCR Docs**: https://github.com/PaddlePaddle/PaddleOCR

---

## 📝 Changelog

- **v1.0.0** (2025-11-28)
  - Initial release
  - Text OCR endpoint
  - Table OCR endpoint
  - Model caching
  - Async processing
