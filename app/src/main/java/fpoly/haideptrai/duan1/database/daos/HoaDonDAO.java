package fpoly.haideptrai.duan1.database.daos;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

import fpoly.haideptrai.duan1.database.entities.HoaDon;

@Dao
public interface HoaDonDAO {
    @Insert
    long insert(HoaDon hoaDon);
    
    @Update
    void update(HoaDon hoaDon);
    
    @Delete
    void delete(HoaDon hoaDon);
    
    @Query("SELECT * FROM hoa_don ORDER BY id DESC")
    List<HoaDon> getAll();
    
    @Query("SELECT * FROM hoa_don WHERE id = :id")
    HoaDon getById(int id);
    
    @Query("SELECT * FROM hoa_don WHERE maHoaDon LIKE '%' || :keyword || '%' OR ngayTao LIKE '%' || :keyword || '%' ORDER BY id DESC")
    List<HoaDon> search(String keyword);
    
    @Query("SELECT * FROM hoa_don WHERE khachHangId = :khachHangId ORDER BY id DESC")
    List<HoaDon> getByKhachHang(int khachHangId);
    
    @Query("SELECT * FROM hoa_don WHERE ngayTao LIKE :ngay || '%' ORDER BY id DESC")
    List<HoaDon> getByNgay(String ngay);
    
    @Query("SELECT COALESCE(SUM(tongTien), 0) FROM hoa_don WHERE trangThai = 'Hoan tat'")
    double getTongDoanhThu();
    
    @Query("SELECT COALESCE(SUM(tongTien), 0) FROM hoa_don WHERE ngayTao LIKE :ngay || '%' AND trangThai = 'Hoan tat'")
    double getDoanhThuTheoNgay(String ngay);
    
    @Query("SELECT COUNT(*) FROM hoa_don WHERE trangThai = 'Hoan tat'")
    int getTongHoaDon();
}









