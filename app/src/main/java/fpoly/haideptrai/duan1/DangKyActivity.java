package fpoly.haideptrai.duan1;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import fpoly.haideptrai.duan1.database.AppDatabase;
import fpoly.haideptrai.duan1.database.entities.NhanVien;
import fpoly.haideptrai.duan1.utils.PasswordHelper;

public class DangKyActivity extends AppCompatActivity {

    private TextInputEditText edtTaiKhoan, edtMatKhau, edtXacNhanMatKhau;
    private TextInputLayout tilTaiKhoan, tilMatKhau, tilXacNhanMatKhau;
    private MaterialButton btnDangKy;
    private AppDatabase database;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dang_ky);

        initViews();
        database = AppDatabase.getInstance(this);

        btnDangKy.setOnClickListener(v -> handleDangKy());

        // Chuyển về màn hình đăng nhập khi click "Đăng nhập"
        findViewById(R.id.txtDangNhap).setOnClickListener(v -> {
            Intent intent = new Intent(DangKyActivity.this, DangNhapActivity.class);
            startActivity(intent);
            finish();
        });
    }

    private void initViews() {
        edtTaiKhoan = findViewById(R.id.edtTaiKhoan);
        edtMatKhau = findViewById(R.id.edtMatKhau);
        edtXacNhanMatKhau = findViewById(R.id.edtXacNhanMatKhau);
        tilTaiKhoan = findViewById(R.id.tilTaiKhoan);
        tilMatKhau = findViewById(R.id.tilMatKhau);
        tilXacNhanMatKhau = findViewById(R.id.tilXacNhanMatKhau);
        btnDangKy = findViewById(R.id.btnDangKy);
    }

    private void handleDangKy() {
        String taiKhoan = edtTaiKhoan.getText().toString().trim();
        String matKhau = edtMatKhau.getText().toString().trim();
        String xacNhanMatKhau = edtXacNhanMatKhau.getText().toString().trim();

        // Reset lỗi
        tilTaiKhoan.setError(null);
        tilMatKhau.setError(null);
        tilXacNhanMatKhau.setError(null);

        // Validate
        if (TextUtils.isEmpty(taiKhoan)) {
            tilTaiKhoan.setError("Vui lòng nhập tài khoản");
            edtTaiKhoan.requestFocus();
            return;
        }

        if (TextUtils.isEmpty(matKhau)) {
            tilMatKhau.setError("Vui lòng nhập mật khẩu");
            edtMatKhau.requestFocus();
            return;
        }

        if (matKhau.length() < 6) {
            tilMatKhau.setError("Mật khẩu phải có ít nhất 6 ký tự");
            edtMatKhau.requestFocus();
            return;
        }

        if (TextUtils.isEmpty(xacNhanMatKhau)) {
            tilXacNhanMatKhau.setError("Vui lòng xác nhận mật khẩu");
            edtXacNhanMatKhau.requestFocus();
            return;
        }

        if (!matKhau.equals(xacNhanMatKhau)) {
            tilXacNhanMatKhau.setError("Mật khẩu xác nhận không khớp");
            edtXacNhanMatKhau.requestFocus();
            return;
        }

        // Kiểm tra tài khoản đã tồn tại
        NhanVien existingNhanVien = database.nhanVienDAO().getByTenDangNhap(taiKhoan);
        if (existingNhanVien != null) {
            tilTaiKhoan.setError("Tài khoản đã tồn tại");
            edtTaiKhoan.requestFocus();
            return;
        }

        // Tạo nhân viên mới
        NhanVien nhanVien = new NhanVien();
        nhanVien.hoTen = taiKhoan; // Tạm thời dùng tên đăng nhập làm họ tên
        nhanVien.gioiTinh = "Nam";
        nhanVien.ngaySinh = "";
        nhanVien.soDienThoai = "";
        nhanVien.tenDangNhap = taiKhoan;
        nhanVien.matKhauHash = PasswordHelper.hashPassword(matKhau);
        nhanVien.vaiTro = "nhan_vien"; // Mặc định là nhân viên
        nhanVien.anhDaiDien = "";

        // Lưu vào database
        try {
            long id = database.nhanVienDAO().insert(nhanVien);
            if (id > 0) {
                Toast.makeText(this, "Đăng ký thành công!", Toast.LENGTH_SHORT).show();
                
                // Chuyển về màn hình đăng nhập và truyền thông tin tài khoản
                Intent intent = new Intent(DangKyActivity.this, DangNhapActivity.class);
                intent.putExtra("username", taiKhoan);
                intent.putExtra("password", matKhau);
                startActivity(intent);
                finish();
            } else {
                Toast.makeText(this, "Đăng ký thất bại. Vui lòng thử lại!", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "Đăng ký thất bại: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }
}

