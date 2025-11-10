package fpoly.haideptrai.duan1.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "nhan_vien")
public class NhanVien {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public String hoTen;
    public String gioiTinh; // "Nam" hoặc "Nữ"
    public String ngaySinh; // Format: "dd/MM/yyyy"
    public String soDienThoai;
    public String tenDangNhap;
    public String matKhauHash; // Mật khẩu đã hash
    public String vaiTro; // "admin" hoặc "nhan_vien"
    public String anhDaiDien; // Đường dẫn ảnh
    
    public NhanVien() {}
    
    public NhanVien(String hoTen, String gioiTinh, String ngaySinh, String soDienThoai,
                    String tenDangNhap, String matKhauHash, String vaiTro, String anhDaiDien) {
        this.hoTen = hoTen;
        this.gioiTinh = gioiTinh;
        this.ngaySinh = ngaySinh;
        this.soDienThoai = soDienThoai;
        this.tenDangNhap = tenDangNhap;
        this.matKhauHash = matKhauHash;
        this.vaiTro = vaiTro;
        this.anhDaiDien = anhDaiDien;
    }
}









