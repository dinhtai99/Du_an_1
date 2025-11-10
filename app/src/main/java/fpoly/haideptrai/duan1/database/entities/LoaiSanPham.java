package fpoly.haideptrai.duan1.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "loai_san_pham")
public class LoaiSanPham {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public String tenLoai;
    public boolean active; // true = hiển thị, false = ẩn
    
    public LoaiSanPham() {}
    
    public LoaiSanPham(String tenLoai, boolean active) {
        this.tenLoai = tenLoai;
        this.active = active;
    }
}









