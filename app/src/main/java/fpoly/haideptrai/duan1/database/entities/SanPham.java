package fpoly.haideptrai.duan1.database.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "san_pham",
        foreignKeys = @ForeignKey(entity = LoaiSanPham.class,
                parentColumns = "id",
                childColumns = "loaiSanPhamId",
                onDelete = ForeignKey.RESTRICT),
        indices = {@Index("loaiSanPhamId")})
public class SanPham {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public String ten;
    public double giaNhap;
    public double giaBan;
    public String moTa;
    public int tonKho;
    public int tonKhoToiThieu;
    public int loaiSanPhamId;
    public String hinhAnh; // Đường dẫn ảnh
    public boolean active; // true = hiển thị, false = ẩn
    
    public SanPham() {}
    
    public SanPham(String ten, double giaNhap, double giaBan, String moTa,
                   int tonKho, int tonKhoToiThieu, int loaiSanPhamId, String hinhAnh, boolean active) {
        this.ten = ten;
        this.giaNhap = giaNhap;
        this.giaBan = giaBan;
        this.moTa = moTa;
        this.tonKho = tonKho;
        this.tonKhoToiThieu = tonKhoToiThieu;
        this.loaiSanPhamId = loaiSanPhamId;
        this.hinhAnh = hinhAnh;
        this.active = active;
    }
}









