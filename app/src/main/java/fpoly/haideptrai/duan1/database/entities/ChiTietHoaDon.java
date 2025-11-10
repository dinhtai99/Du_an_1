package fpoly.haideptrai.duan1.database.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "chi_tiet_hoa_don",
        foreignKeys = {
            @ForeignKey(entity = HoaDon.class,
                    parentColumns = "id",
                    childColumns = "hoaDonId",
                    onDelete = ForeignKey.CASCADE),
            @ForeignKey(entity = SanPham.class,
                    parentColumns = "id",
                    childColumns = "sanPhamId",
                    onDelete = ForeignKey.RESTRICT)
        },
        indices = {@Index("hoaDonId"), @Index("sanPhamId")})
public class ChiTietHoaDon {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public int hoaDonId;
    public int sanPhamId;
    public int soLuong;
    public double donGia; // Giá tại thời điểm bán
    public double thanhTien; // soLuong * donGia
    
    public ChiTietHoaDon() {}
    
    public ChiTietHoaDon(int hoaDonId, int sanPhamId, int soLuong, double donGia) {
        this.hoaDonId = hoaDonId;
        this.sanPhamId = sanPhamId;
        this.soLuong = soLuong;
        this.donGia = donGia;
        this.thanhTien = soLuong * donGia;
    }
}









