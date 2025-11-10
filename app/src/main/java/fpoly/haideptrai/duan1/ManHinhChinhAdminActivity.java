package fpoly.haideptrai.duan1;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.card.MaterialCardView;

import fpoly.haideptrai.duan1.utils.SessionManager;

public class ManHinhChinhAdminActivity extends AppCompatActivity {

    private SessionManager sessionManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_man_hinh_chinh_admin);

        sessionManager = new SessionManager(this);

        // Kiểm tra quyền admin
        if (!sessionManager.isAdmin()) {
            Toast.makeText(this, "Bạn không có quyền truy cập!", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        setupClickListeners();
        
        // Thiết lập nút đăng xuất
        findViewById(R.id.btnDangXuat).setOnClickListener(v -> showLogoutDialog());
    }

    private void setupClickListeners() {
        findViewById(R.id.cardNhanVien).setOnClickListener(v -> {
            Intent intent = new Intent(this, DanhSachNhanVienActivity.class);
            startActivity(intent);
        });

        findViewById(R.id.cardLoaiSanPham).setOnClickListener(v -> {
            Intent intent = new Intent(this, DanhSachLoaiSanPhamActivity.class);
            startActivity(intent);
        });

        findViewById(R.id.cardSanPham).setOnClickListener(v -> {
            Intent intent = new Intent(this, DanhSachSanPhamActivity.class);
            startActivity(intent);
        });

        findViewById(R.id.cardKhachHang).setOnClickListener(v -> {
            Intent intent = new Intent(this, DanhSachKhachHangActivity.class);
            startActivity(intent);
        });

        findViewById(R.id.cardHoaDon).setOnClickListener(v -> {
            Intent intent = new Intent(this, DanhSachHoaDonActivity.class);
            startActivity(intent);
        });

        findViewById(R.id.cardThongKe).setOnClickListener(v -> {
            Intent intent = new Intent(this, ThongKeActivity.class);
            startActivity(intent);
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_admin, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.menuDoiMatKhau) {
            // TODO: Mở màn hình đổi mật khẩu
            Toast.makeText(this, "Chức năng đổi mật khẩu", Toast.LENGTH_SHORT).show();
            return true;
        } else if (id == R.id.menuDangXuat) {
            showLogoutDialog();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void showLogoutDialog() {
        new AlertDialog.Builder(this)
                .setTitle("Đăng xuất")
                .setMessage("Bạn có chắc chắn muốn đăng xuất?")
                .setPositiveButton("Đăng xuất", (dialog, which) -> {
                    sessionManager.clearSession();
                    Intent intent = new Intent(ManHinhChinhAdminActivity.this, DangNhapActivity.class);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                    startActivity(intent);
                    finish();
                })
                .setNegativeButton("Hủy", null)
                .show();
    }
}


