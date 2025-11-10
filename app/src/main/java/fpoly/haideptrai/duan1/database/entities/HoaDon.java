package fpoly.haideptrai.duan1.database.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "hoa_don",
        foreignKeys = {
            @ForeignKey(entity = KhachHang.class,
                    parentColumns = "id",
                    childColumns = "khachHangId",
                    onDelete = ForeignKey.SET_NULL),
            @ForeignKey(entity = NhanVien.class,
                    parentColumns = "id",
                    childColumns = "nhanVienId",
                    onDelete = ForeignKey.SET_NULL)
        },
        indices = {@Index("khachHangId"), @Index("nhanVienId")})
public class HoaDon {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public String maHoaDon; // Mã hóa đơn duy nhất
    public int khachHangId;
    public int nhanVienId;
    public String ngayTao; // Format: "dd/MM/yyyy HH:mm"
    public double tongTien;
    public double giamGia; // Phần trăm giảm giá
    public String trangThai; // "Dang xu ly", "Hoan tat", "Da huy"
    
    public HoaDon() {}
    
    public HoaDon(String maHoaDon, int khachHangId, int nhanVienId, String ngayTao,
                  double tongTien, double giamGia, String trangThai) {
        this.maHoaDon = maHoaDon;
        this.khachHangId = khachHangId;
        this.nhanVienId = nhanVienId;
        this.ngayTao = ngayTao;
        this.tongTien = tongTien;
        this.giamGia = giamGia;
        this.trangThai = trangThai;
    }
}









