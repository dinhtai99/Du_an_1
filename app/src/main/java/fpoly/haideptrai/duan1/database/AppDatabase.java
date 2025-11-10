package fpoly.haideptrai.duan1.database;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import fpoly.haideptrai.duan1.database.daos.ChiTietHoaDonDAO;
import fpoly.haideptrai.duan1.database.daos.HoaDonDAO;
import fpoly.haideptrai.duan1.database.daos.KhachHangDAO;
import fpoly.haideptrai.duan1.database.daos.LoaiSanPhamDAO;
import fpoly.haideptrai.duan1.database.daos.NhanVienDAO;
import fpoly.haideptrai.duan1.database.daos.SanPhamDAO;
import fpoly.haideptrai.duan1.database.entities.ChiTietHoaDon;
import fpoly.haideptrai.duan1.database.entities.HoaDon;
import fpoly.haideptrai.duan1.database.entities.KhachHang;
import fpoly.haideptrai.duan1.database.entities.LoaiSanPham;
import fpoly.haideptrai.duan1.database.entities.NhanVien;
import fpoly.haideptrai.duan1.database.entities.SanPham;

@Database(entities = {
        NhanVien.class,
        LoaiSanPham.class,
        SanPham.class,
        KhachHang.class,
        HoaDon.class,
        ChiTietHoaDon.class
}, version = 1, exportSchema = false)
public abstract class AppDatabase extends RoomDatabase {
    private static AppDatabase instance;
    
    public abstract NhanVienDAO nhanVienDAO();
    public abstract LoaiSanPhamDAO loaiSanPhamDAO();
    public abstract SanPhamDAO sanPhamDAO();
    public abstract KhachHangDAO khachHangDAO();
    public abstract HoaDonDAO hoaDonDAO();
    public abstract ChiTietHoaDonDAO chiTietHoaDonDAO();
    
    public static synchronized AppDatabase getInstance(Context context) {
        if (instance == null) {
            instance = Room.databaseBuilder(context.getApplicationContext(),
                    AppDatabase.class, "shop_thb_database")
                    .allowMainThreadQueries()
                    .build();
        }
        return instance;
    }
}









