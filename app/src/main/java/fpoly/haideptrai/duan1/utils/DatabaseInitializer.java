package fpoly.haideptrai.duan1.utils;

import android.content.Context;

import fpoly.haideptrai.duan1.database.AppDatabase;
import fpoly.haideptrai.duan1.database.entities.LoaiSanPham;
import fpoly.haideptrai.duan1.database.entities.NhanVien;

public class DatabaseInitializer {
    public static void initialize(Context context) {
        AppDatabase database = AppDatabase.getInstance(context);
        
        // Kiểm tra xem đã có dữ liệu chưa
        if (database.nhanVienDAO().getAll().isEmpty()) {
            // Tạo admin mặc định
            NhanVien admin = new NhanVien();
            admin.hoTen = "Admin";
            admin.gioiTinh = "Nam";
            admin.ngaySinh = "01/01/1990";
            admin.soDienThoai = "0123456789";
            admin.tenDangNhap = "admin";
            admin.matKhauHash = PasswordHelper.hashPassword("admin123");
            admin.vaiTro = "admin";
            admin.anhDaiDien = "";
            database.nhanVienDAO().insert(admin);
            
            // Tạo nhân viên mẫu
            NhanVien nhanVien = new NhanVien();
            nhanVien.hoTen = "Nguyễn Văn A";
            nhanVien.gioiTinh = "Nam";
            nhanVien.ngaySinh = "15/05/1995";
            nhanVien.soDienThoai = "0987654321";
            nhanVien.tenDangNhap = "nhanvien";
            nhanVien.matKhauHash = PasswordHelper.hashPassword("nhanvien123");
            nhanVien.vaiTro = "nhan_vien";
            nhanVien.anhDaiDien = "";
            database.nhanVienDAO().insert(nhanVien);
        }
        
        // Tạo loại sản phẩm mẫu
        if (database.loaiSanPhamDAO().getAll().isEmpty()) {
            database.loaiSanPhamDAO().insert(new LoaiSanPham("Điện thoại", true));
            database.loaiSanPhamDAO().insert(new LoaiSanPham("Laptop", true));
            database.loaiSanPhamDAO().insert(new LoaiSanPham("Phụ kiện", true));
        }
    }
}









