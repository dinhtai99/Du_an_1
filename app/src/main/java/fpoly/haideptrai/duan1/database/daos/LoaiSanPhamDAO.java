package fpoly.haideptrai.duan1.database.daos;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

import fpoly.haideptrai.duan1.database.entities.LoaiSanPham;

@Dao
public interface LoaiSanPhamDAO {
    @Insert
    long insert(LoaiSanPham loaiSanPham);
    
    @Update
    void update(LoaiSanPham loaiSanPham);
    
    @Delete
    void delete(LoaiSanPham loaiSanPham);
    
    @Query("SELECT * FROM loai_san_pham WHERE active = 1 ORDER BY id DESC")
    List<LoaiSanPham> getAllActive();
    
    @Query("SELECT * FROM loai_san_pham ORDER BY id DESC")
    List<LoaiSanPham> getAll();
    
    @Query("SELECT * FROM loai_san_pham WHERE id = :id")
    LoaiSanPham getById(int id);
    
    @Query("SELECT * FROM loai_san_pham WHERE tenLoai LIKE '%' || :keyword || '%' ORDER BY id DESC")
    List<LoaiSanPham> search(String keyword);
    
    @Query("SELECT COUNT(*) FROM san_pham WHERE loaiSanPhamId = :loaiId")
    int countSanPhamByLoai(int loaiId);
}









