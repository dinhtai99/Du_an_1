package fpoly.haideptrai.duan1.database.daos;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

import fpoly.haideptrai.duan1.database.entities.NhanVien;

@Dao
public interface NhanVienDAO {
    @Insert
    long insert(NhanVien nhanVien);
    
    @Update
    void update(NhanVien nhanVien);
    
    @Delete
    void delete(NhanVien nhanVien);
    
    @Query("SELECT * FROM nhan_vien ORDER BY id DESC")
    List<NhanVien> getAll();
    
    @Query("SELECT * FROM nhan_vien WHERE id = :id")
    NhanVien getById(int id);
    
    @Query("SELECT * FROM nhan_vien WHERE tenDangNhap = :tenDangNhap LIMIT 1")
    NhanVien getByTenDangNhap(String tenDangNhap);
    
    @Query("SELECT * FROM nhan_vien WHERE hoTen LIKE '%' || :keyword || '%' OR soDienThoai LIKE '%' || :keyword || '%' ORDER BY id DESC")
    List<NhanVien> search(String keyword);
}









