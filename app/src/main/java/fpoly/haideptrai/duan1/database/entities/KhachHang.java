package fpoly.haideptrai.duan1.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "khach_hang")
public class KhachHang {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public String hoTen;
    public String soDienThoai;
    public String diaChi;
    public String email;
    public boolean active; // true = kích hoạt, false = vô hiệu
    
    public KhachHang() {}
    
    public KhachHang(String hoTen, String soDienThoai, String diaChi, String email, boolean active) {
        this.hoTen = hoTen;
        this.soDienThoai = soDienThoai;
        this.diaChi = diaChi;
        this.email = email;
        this.active = active;
    }
}









