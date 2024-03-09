### Yêu cầu hệ thống

-   Python 3.11.4
-   Hệ quản trị CSDL MySQL (phiên bản mới nhất)

### Các thư viện dùng trong dự án:

-   scikit-learn
-   mysql-connector-python
-   pandas
-   env

### Thiết lập trước khi chạy app

**1. Install từng thư viện bằng lệnh**

```bash
pip install <tên thư viện>
```

VD:

```bash
pip install scikit-learn
```

**2. Tạo file biến môi trường**

Tạo file `.env` trong thư mục `sql-dectector/src` với nội dung sau

```env
SHOULD_USE_PREPARED_STATEMENT = 0
SHOULD_DETECT_SQLI = 1
```

**3. Chạy app**

```bash
cd ./sqli-detector
cd ./src
python main.py
```

### Khi chạy app

Có thể sửa file `.env` để thiết lập app, sau đấy dùng app như thường mà không phải chạy lại app. Giá trị luôn là `1` = `True`, còn khác 1 = `False`. Ví dụ như để thiết lập cho app sử dụng prepared statement thay vì raw query, ta thiết lập `SHOULD_USE_PREPARED_STATEMENT = 1`
