package fpoly.haideptrai.duan1.database.daos;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

import fpoly.haideptrai.duan1.database.entities.KhachHang;

@Dao
public interface KhachHangDAO {
    @Insert
    long insert(KhachHang khachHang);
    
    @Update
    void update(KhachHang khachHang);
    
    @Delete
    void delete(KhachHang khachHang);
    
    @Query("SELECT * FROM khach_hang WHERE active = 1 ORDER BY id DESC")
    List<KhachHang> getAllActive();
    
    @Query("SELECT * FROM khach_hang ORDER BY id DESC")
    List<KhachHang> getAll();
    
    @Query("SELECT * FROM khach_hang WHERE id = :id")
    KhachHang getById(int id);
    
    @Query("SELECT * FROM khach_hang WHERE hoTen LIKE '%' || :keyword || '%' OR soDienThoai LIKE '%' || :keyword || '%' ORDER BY id DESC")
    List<KhachHang> search(String keyword);
    
    @Query("SELECT COUNT(*) FROM hoa_don WHERE khachHangId = :khachHangId")
    int countHoaDonByKhachHang(int khachHangId);
    
    @Query("SELECT COALESCE(SUM(tongTien), 0) FROM hoa_don WHERE khachHangId = :khachHangId AND trangThai = 'Hoan tat'")
    double getTongChiTieu(int khachHangId);
}









