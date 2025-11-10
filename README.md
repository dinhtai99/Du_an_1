# Ứng dụng Quản Lý Shop THB

Ứng dụng quản lý cửa hàng điện tử được xây dựng bằng Java + XML trên Android với Room Database.

## 🚀 Tính năng chính

- ✅ Đăng nhập/Đăng ký với phân quyền Admin/Nhân viên
- ✅ Khóa tạm thời sau 5 lần đăng nhập sai
- ✅ Quản lý Nhân viên (chỉ Admin)
- ✅ Quản lý Loại Sản Phẩm
- ✅ Quản lý Sản Phẩm với cảnh báo tồn kho
- ✅ Quản lý Khách hàng
- ✅ Quản lý Hóa đơn với xuất PDF
- ✅ Thống kê & Báo cáo với biểu đồ
- ✅ Đổi mật khẩu
- ✅ Xuất Excel danh sách sản phẩm

## 📦 Công nghệ sử dụng

- **Ngôn ngữ**: Java
- **Database**: Room (SQLite)
- **UI**: XML + Material Design + RecyclerView + CardView
- **Biểu đồ**: MPAndroidChart
- **Xuất PDF**: PdfDocument
- **Xuất Excel**: Apache POI
- **Hình ảnh**: Glide

## 🔑 Tài khoản mặc định

Khi chạy app lần đầu, hệ thống sẽ tự động tạo:

- **Admin**: 
  - Tài khoản: `admin`
  - Mật khẩu: `admin123`
  
- **Nhân viên**: 
  - Tài khoản: `nhanvien`
  - Mật khẩu: `nhanvien123`

## 📁 Cấu trúc Project

```
app/src/main/java/fpoly/haideptrai/duan1/
├── database/
│   ├── entities/          # Các Entity (NhanVien, SanPham, ...)
│   ├── daos/              # Các DAO interface
│   └── AppDatabase.java   # Database class
├── utils/
│   ├── PasswordHelper.java      # Hash mật khẩu
│   ├── SessionManager.java      # Quản lý session
│   └── DatabaseInitializer.java # Khởi tạo dữ liệu mẫu
├── DangNhapActivity.java        # Màn hình đăng nhập
├── DangKyActivity.java          # Màn hình đăng ký
├── ManHinhChinhAdminActivity.java
├── ManHinhChinhNhanVienActivity.java
└── ... (các Activity khác)
```

## 🛠️ Cài đặt và Chạy

1. **Sync Gradle**: File → Sync Project with Gradle Files
2. **Clean & Rebuild**: Build → Clean Project, sau đó Build → Rebuild Project
3. **Chạy app**: Run → Run 'app'

## 📝 Trạng thái triển khai

### ✅ Đã hoàn thành:
- Database layer (Entities, DAOs, Database)
- Authentication & Authorization
- Session Management
- Màn hình đăng nhập/đăng ký
- Màn hình chính Admin với menu điều hướng
- Database Initializer với dữ liệu mẫu

### ⏳ Đang phát triển:
- Các màn hình CRUD cho từng module
- Adapter cho RecyclerView
- Dialog thêm/sửa
- Upload ảnh
- Xuất PDF/Excel
- Biểu đồ thống kê

Xem file `IMPLEMENTATION_GUIDE.md` để biết chi tiết cách tiếp tục phát triển.

## 📚 Tài liệu tham khảo

- [Room Database](https://developer.android.com/training/data-storage/room)
- [MPAndroidChart](https://github.com/PhilJay/MPAndroidChart)
- [Apache POI](https://poi.apache.org/)
- [Glide](https://github.com/bumptech/glide)

## 👨‍💻 Phát triển

Để tiếp tục phát triển, hãy tham khảo:
1. File `IMPLEMENTATION_GUIDE.md` - Hướng dẫn chi tiết
2. Code của `DangNhapActivity` - Ví dụ sử dụng Room và SessionManager
3. Các DAO đã có sẵn - Sử dụng trực tiếp để thao tác database

## 📄 License

Dự án này được phát triển cho mục đích học tập và thương mại.









