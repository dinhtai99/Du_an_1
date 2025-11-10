package fpoly.haideptrai.duan1.database.daos;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

import fpoly.haideptrai.duan1.database.entities.SanPham;

@Dao
public interface SanPhamDAO {
    @Insert
    long insert(SanPham sanPham);
    
    @Update
    void update(SanPham sanPham);
    
    @Delete
    void delete(SanPham sanPham);
    
    @Query("SELECT * FROM san_pham WHERE active = 1 ORDER BY id DESC")
    List<SanPham> getAllActive();
    
    @Query("SELECT * FROM san_pham ORDER BY id DESC")
    List<SanPham> getAll();
    
    @Query("SELECT * FROM san_pham WHERE id = :id")
    SanPham getById(int id);
    
    @Query("SELECT * FROM san_pham WHERE ten LIKE '%' || :keyword || '%' AND active = 1 ORDER BY id DESC")
    List<SanPham> search(String keyword);
    
    @Query("SELECT * FROM san_pham WHERE loaiSanPhamId = :loaiId AND active = 1 ORDER BY id DESC")
    List<SanPham> getByLoai(int loaiId);
    
    @Query("SELECT * FROM san_pham WHERE tonKho < tonKhoToiThieu AND active = 1 ORDER BY tonKho ASC")
    List<SanPham> getTonKhoThap();
    
    @Query("UPDATE san_pham SET tonKho = tonKho - :soLuong WHERE id = :id")
    void giamTonKho(int id, int soLuong);
    
    @Query("UPDATE san_pham SET tonKho = tonKho + :soLuong WHERE id = :id")
    void tangTonKho(int id, int soLuong);
}









