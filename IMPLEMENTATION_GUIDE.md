# Hướng dẫn triển khai ứng dụng "Quản Lý Shop THB"

## ✅ Đã hoàn thành:

### 1. Cấu hình Dependencies
- ✅ Room Database (2.6.1)
- ✅ Glide (4.16.0) 
- ✅ MPAndroidChart (3.1.0)
- ✅ Apache POI (5.2.5)
- ✅ CardView, Material Design

### 2. Database Layer
- ✅ **Entities**: NhanVien, LoaiSanPham, SanPham, KhachHang, HoaDon, ChiTietHoaDon
- ✅ **DAOs**: Tất cả các DAO với đầy đủ query methods
- ✅ **AppDatabase**: Database class với Room
- ✅ **DatabaseInitializer**: Khởi tạo dữ liệu mẫu (admin/admin123, nhanvien/nhanvien123)

### 3. Utilities
- ✅ **PasswordHelper**: Hash và verify mật khẩu (SHA-256)
- ✅ **SessionManager**: Quản lý session, khóa tạm thời sau 5 lần sai
- ✅ **MyApplication**: Application class để khởi tạo database

### 4. Authentication & Authorization
- ✅ **DangNhapActivity**: Đăng nhập với Room, phân quyền admin/nhân viên
- ✅ **DangKyActivity**: Đăng ký tài khoản mới
- ✅ Khóa tạm thời sau 5 lần đăng nhập sai
- ✅ Lưu mật khẩu với SharedPreferences

### 5. Màn hình chính
- ✅ **ManHinhChinhAdminActivity**: Menu điều hướng cho admin
- ✅ Menu với đổi mật khẩu và đăng xuất

## 📋 Cần tiếp tục triển khai:

### 1. Quản lý Nhân viên (DanhSachNhanVienActivity)
**Cần tạo:**
- Adapter cho RecyclerView
- Dialog thêm/sửa nhân viên
- Xử lý upload ảnh đại diện
- Validate dữ liệu
- Tìm kiếm theo tên/số điện thoại

**Layout đã có sẵn:**
- `activity_danh_sach_nhan_vien.xml`
- `item_nhan_vien.xml`

### 2. Quản lý Loại Sản Phẩm (DanhSachLoaiSanPhamActivity)
**Cần tạo:**
- Adapter cho RecyclerView
- Dialog thêm/sửa loại
- Toggle ẩn/hiện loại
- Kiểm tra không cho xóa loại đang có sản phẩm
- Tìm kiếm theo tên

### 3. Quản lý Sản phẩm (DanhSachSanPhamActivity)
**Cần tạo:**
- Adapter với Glide để load ảnh
- Dialog thêm/sửa sản phẩm
- Upload/chọn ảnh sản phẩm
- Cảnh báo tồn kho thấp
- Lọc theo loại sản phẩm
- **Xuất Excel**: Sử dụng Apache POI
- Tìm kiếm theo tên

### 4. Quản lý Khách hàng (DanhSachKhachHangActivity)
**Cần tạo:**
- Adapter cho RecyclerView
- Dialog thêm/sửa khách hàng
- Hiển thị tổng chi tiêu và số đơn hàng
- Toggle kích hoạt/vô hiệu
- Tìm kiếm theo tên/số điện thoại

### 5. Quản lý Hóa đơn (DanhSachHoaDonActivity)
**Cần tạo:**
- Activity tạo hóa đơn mới
- Chọn khách hàng và nhân viên
- Thêm nhiều sản phẩm với số lượng
- Tính tổng tiền và giảm giá %
- Trừ tồn kho khi lưu hóa đơn
- Cập nhật trạng thái hóa đơn
- **Xuất PDF**: Sử dụng PdfDocument
- Tìm kiếm theo mã/ngày/khách hàng

### 6. Thống kê & Báo cáo (ThongKeActivity)
**Cần tạo:**
- Top 5 sản phẩm bán chạy
- Biểu đồ doanh thu (MPAndroidChart)
- Tổng doanh thu, tổng hóa đơn, lợi nhuận
- Danh sách sản phẩm tồn kho thấp

### 7. Đổi mật khẩu
**Cần tạo:**
- Activity đổi mật khẩu
- Validate mật khẩu cũ
- Cập nhật mật khẩu mới trong database

### 8. Màn hình Nhân viên (ManHinhChinhNhanVienActivity)
**Cần tạo:**
- Menu chỉ có: Bán hàng, Hóa đơn, Đổi mật khẩu, Đăng xuất
- Không có quyền quản lý nhân viên, loại sản phẩm, khách hàng

## 🎨 Màu sắc chủ đạo:
- Màu xanh: `#1976D2` (holo_blue_dark)

## 📝 Ghi chú quan trọng:

1. **Database**: Đã được khởi tạo tự động với dữ liệu mẫu khi app chạy lần đầu
2. **Session**: Sử dụng SessionManager để quản lý session và kiểm tra quyền
3. **Password**: Mật khẩu được hash bằng SHA-256 trước khi lưu
4. **Thread Safety**: Room database đã được cấu hình `allowMainThreadQueries()` để đơn giản hóa, nhưng nên chuyển sang background thread trong production

## 🚀 Cách tiếp tục:

1. Bắt đầu với **DanhSachNhanVienActivity** - tạo Adapter và Dialog
2. Áp dụng pattern tương tự cho các màn hình khác
3. Sử dụng các DAO đã có sẵn để thao tác với database
4. Tham khảo code của DangNhapActivity để hiểu cách sử dụng Room và SessionManager

## 📚 Tài liệu tham khảo:
- Room: https://developer.android.com/training/data-storage/room
- MPAndroidChart: https://github.com/PhilJay/MPAndroidChart
- Apache POI: https://poi.apache.org/
- Glide: https://github.com/bumptech/glide









