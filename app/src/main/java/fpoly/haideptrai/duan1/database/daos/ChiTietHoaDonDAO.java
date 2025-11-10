package fpoly.haideptrai.duan1.database.daos;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import java.util.List;

import fpoly.haideptrai.duan1.database.entities.ChiTietHoaDon;

@Dao
public interface ChiTietHoaDonDAO {
    @Insert
    void insert(ChiTietHoaDon chiTietHoaDon);
    
    @Insert
    void insertAll(List<ChiTietHoaDon> chiTietHoaDons);
    
    @Delete
    void delete(ChiTietHoaDon chiTietHoaDon);
    
    @Query("SELECT * FROM chi_tiet_hoa_don WHERE hoaDonId = :hoaDonId")
    List<ChiTietHoaDon> getByHoaDon(int hoaDonId);
    
    @Query("SELECT sanPhamId, SUM(soLuong) as tongSoLuong FROM chi_tiet_hoa_don " +
           "WHERE hoaDonId IN (SELECT id FROM hoa_don WHERE trangThai = 'Hoan tat') " +
           "GROUP BY sanPhamId ORDER BY tongSoLuong DESC LIMIT 5")
    List<TopSanPhamResult> getTop5SanPhamBanChay();
    
    class TopSanPhamResult {
        public int sanPhamId;
        public int tongSoLuong;
    }
}

