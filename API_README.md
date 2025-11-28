# PaddleOCR FastAPI Application

API web application để thực hiện OCR (Optical Character Recognition) cho text và bảng sử dụng PaddleOCR và FastAPI.

## Tính năng

- ✅ **Text OCR** (`/ocr`): Nhận diện text từ ảnh với bounding boxes và confidence scores
- ✅ **Table OCR** (`/table`): Nhận diện bảng từ ảnh, xuất ra markdown hoặc text thông thường
- ⚡ **Async Processing**: Tất cả endpoints đều async để xử lý concurrent requests
- 🚀 **Model Caching**: Models được cache trong memory để tối ưu performance
- 🔒 **Validation**: Kiểm tra file type, size, và image validity
- 🌐 **CORS Support**: Cho phép cross-origin requests từ frontend

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý**: Nếu không có GPU, sửa `paddlepaddle-gpu` thành `paddlepaddle` trong `requirements.txt`

### 2. Cấu hình (Optional)

Sửa file `config.py` để thay đổi:
- `USE_GPU`: Set `False` nếu chỉ dùng CPU
- `MODEL_LANG`: Ngôn ngữ model (mặc định: "vi")
- `MAX_UPLOAD_SIZE`: Giới hạn kích thước file upload
- `CORS_ORIGINS`: Domains được phép gọi API

## Chạy ứng dụng

### Khởi động server

```bash
# Cách 1: Sử dụng uvicorn trực tiếp
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Cách 2: Chạy file main.py
python main.py
```

Server sẽ chạy tại: `http://localhost:8000`

### API Documentation

Sau khi khởi động, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Text OCR

**POST** `/ocr`

Upload ảnh để nhận diện text.

**Request:**
```bash
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@image.png"
```

**Response:**
```json
{
  "success": true,
  "message": "OCR completed successfully",
  "results": [
    {
      "text": "Detected text here",
      "confidence": 0.98,
      "bounding_box": {
        "points": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
      }
    }
  ],
  "total_detections": 1
}
```

### 2. Table OCR

**POST** `/table?format=markdown`

Upload ảnh có bảng để nhận diện.

**Parameters:**
- `format`: `markdown` hoặc `text` (mặc định: `markdown`)

**Request:**
```bash
# Export markdown
curl -X POST "http://localhost:8000/table?format=markdown" \
  -F "file=@table_image.png"

# Export plain text
curl -X POST "http://localhost:8000/table?format=text" \
  -F "file=@table_image.png"
```

**Response:**
```json
{
  "success": true,
  "message": "Table OCR completed successfully",
  "format": "markdown",
  "content": "| Col1 | Col2 |\n|------|------|\n| A | B |",
  "raw_result": {...}
}
```

### 3. Health Check

**GET** `/health`

Kiểm tra trạng thái server.

```bash
curl http://localhost:8000/health
```

## Các file trong project

```
padd_OCR/
├── main.py              # FastAPI application chính
├── config.py            # Cấu hình (GPU, upload size, CORS, etc.)
├── models.py            # Pydantic models cho request/response
├── ocr_service.py       # Business logic và model caching
├── utils.py             # Utility functions (validation, file handling)
├── routes/
│   ├── __init__.py
│   ├── ocr.py          # Text OCR endpoint
│   └── table.py        # Table OCR endpoint
├── requirements.txt     # Python dependencies
└── output/             # Thư mục output (tự động tạo)
```

## Sử dụng với Python

```python
import requests

# Text OCR
with open("image.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/ocr",
        files={"file": f}
    )
    result = response.json()
    print(result)

# Table OCR (markdown)
with open("table.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/table?format=markdown",
        files={"file": f}
    )
    result = response.json()
    print(result["content"])
```

## Lưu ý

1. **Lần chạy đầu tiên**: Models sẽ được download tự động (có thể mất vài phút)
2. **Model Caching**: Models được load vào memory và giữ lại, request đầu tiên sẽ chậm hơn
3. **File Types**: Hỗ trợ jpg, jpeg, png, bmp, tiff, webp
4. **Max File Size**: Mặc định 10MB (có thể thay đổi trong `config.py`)
5. **GPU**: Nếu có GPU, đảm bảo đã cài đặt `paddlepaddle-gpu` và CUDA drivers

## Troubleshooting

### Lỗi import PaddleOCR
```bash
pip install paddleocr --upgrade
```

### Lỗi GPU
Nếu gặp lỗi với GPU, set `USE_GPU = False` trong `config.py`

### Port đã được sử dụng
Thay đổi port trong lệnh chạy:
```bash
uvicorn main:app --reload --port 8001
```

## Production Deployment

```bash
# Sử dụng gunicorn với uvicorn workers
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## License

MIT
