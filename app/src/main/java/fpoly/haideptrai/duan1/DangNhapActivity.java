package fpoly.haideptrai.duan1;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import fpoly.haideptrai.duan1.database.AppDatabase;
import fpoly.haideptrai.duan1.database.entities.NhanVien;
import fpoly.haideptrai.duan1.utils.PasswordHelper;
import fpoly.haideptrai.duan1.utils.SessionManager;

public class DangNhapActivity extends AppCompatActivity {

    private TextInputEditText edtTaiKhoan, edtMatKhau;
    private TextInputLayout tilTaiKhoan, tilMatKhau;
    private MaterialButton btnDangNhap;
    private CheckBox chkLuuMatKhau;
    private Spinner spnVaiTro;
    private AppDatabase database;
    private SessionManager sessionManager;
    private SharedPreferences prefs;
    private String[] vaiTroArray = {"admin", "nhan_vien"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dang_nhap);

        initViews();
        database = AppDatabase.getInstance(this);
        sessionManager = new SessionManager(this);
        prefs = getSharedPreferences("login_prefs", MODE_PRIVATE);

        // Nhận thông tin từ màn hình đăng ký
        Intent intent = getIntent();
        if (intent != null) {
            String username = intent.getStringExtra("username");
            String password = intent.getStringExtra("password");
            if (username != null && password != null) {
                edtTaiKhoan.setText(username);
                edtMatKhau.setText(password);
            }
        }

        // Load thông tin đã lưu nếu có
        loadSavedCredentials();
        
        // Setup Spinner vai trò
        setupVaiTroSpinner();

        btnDangNhap.setOnClickListener(v -> handleDangNhap());

        // Chuyển sang màn hình đăng ký
        findViewById(R.id.txtDangKy).setOnClickListener(v -> {
            Intent dangKyIntent = new Intent(DangNhapActivity.this, DangKyActivity.class);
            startActivity(dangKyIntent);
        });
        
        // Không cần kiểm tra khóa ở đây vì chưa có username
    }
    
    private void checkLockStatus(String username) {
        if (username == null || username.isEmpty()) {
            return;
        }
        if (sessionManager.isLocked(username)) {
            long remaining = sessionManager.getLockedTimeRemaining(username);
            int minutes = (int) (remaining / 60000);
            int seconds = (int) ((remaining % 60000) / 1000);
            btnDangNhap.setEnabled(false);
            Toast.makeText(this, "Tài khoản \"" + username + "\" bị khóa. Vui lòng thử lại sau " + minutes + " phút " + seconds + " giây", Toast.LENGTH_LONG).show();
            
            // Enable lại sau khi hết thời gian khóa
            new android.os.Handler().postDelayed(() -> {
                sessionManager.resetLoginFailed(username);
                btnDangNhap.setEnabled(true);
            }, remaining);
        } else {
            btnDangNhap.setEnabled(true);
        }
    }

    private void initViews() {
        edtTaiKhoan = findViewById(R.id.edtTaiKhoan);
        edtMatKhau = findViewById(R.id.edtMatKhau);
        tilTaiKhoan = findViewById(R.id.tilTaiKhoan);
        tilMatKhau = findViewById(R.id.tilMatKhau);
        btnDangNhap = findViewById(R.id.btnDangNhap);
        chkLuuMatKhau = findViewById(R.id.chkLuuMatKhau);
        spnVaiTro = findViewById(R.id.spnVaiTro);
    }
    
    private void setupVaiTroSpinner() {
        String[] vaiTroDisplay = {"Quản trị viên", "Nhân viên"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, vaiTroDisplay);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spnVaiTro.setAdapter(adapter);
        // Mặc định chọn Nhân viên (index 1)
        spnVaiTro.setSelection(1);
    }

    private void loadSavedCredentials() {
        String savedUsername = prefs.getString("saved_username", "");
        String savedPassword = prefs.getString("saved_password", "");
        int savedVaiTro = prefs.getInt("saved_vai_tro", 1); // Mặc định là nhân viên
        if (!TextUtils.isEmpty(savedUsername) && !TextUtils.isEmpty(savedPassword)) {
            edtTaiKhoan.setText(savedUsername);
            edtMatKhau.setText(savedPassword);
            spnVaiTro.setSelection(savedVaiTro);
            chkLuuMatKhau.setChecked(true);
        }
    }

    private void handleDangNhap() {
        String taiKhoan = edtTaiKhoan.getText().toString().trim();
        String matKhau = edtMatKhau.getText().toString().trim();

        // Reset lỗi
        tilTaiKhoan.setError(null);
        tilMatKhau.setError(null);

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

        // Kiểm tra khóa tạm thời cho tài khoản cụ thể này
        if (sessionManager.isLocked(taiKhoan)) {
            long remaining = sessionManager.getLockedTimeRemaining(taiKhoan);
            int minutes = (int) (remaining / 60000);
            int seconds = (int) ((remaining % 60000) / 1000);
            Toast.makeText(this, "Tài khoản \"" + taiKhoan + "\" bị khóa. Vui lòng thử lại sau " + minutes + " phút " + seconds + " giây", Toast.LENGTH_LONG).show();
            checkLockStatus(taiKhoan);
            return;
        }

        // Tìm nhân viên theo tên đăng nhập
        NhanVien nhanVien = database.nhanVienDAO().getByTenDangNhap(taiKhoan);
        
        if (nhanVien == null) {
            sessionManager.incrementLoginFailed(taiKhoan);
            tilTaiKhoan.setError("Tài khoản không tồn tại");
            Toast.makeText(this, "Đăng nhập thất bại!", Toast.LENGTH_SHORT).show();
            checkLockStatus(taiKhoan);
            return;
        }

        // Xác thực mật khẩu
        if (PasswordHelper.verifyPassword(matKhau, nhanVien.matKhauHash)) {
            // Đăng nhập thành công
            sessionManager.resetLoginFailed(taiKhoan);
            
            // Lấy vai trò được chọn từ Spinner
            String vaiTroChon = vaiTroArray[spnVaiTro.getSelectedItemPosition()];
            
            // Tạm thời thay đổi vai trò của nhân viên để điều hướng đúng
            String vaiTroCu = nhanVien.vaiTro;
            nhanVien.vaiTro = vaiTroChon;
            sessionManager.saveSession(nhanVien);
            // Khôi phục lại vai trò gốc trong database (không lưu vào database)
            nhanVien.vaiTro = vaiTroCu;
            
            // Lưu thông tin nếu checkbox được chọn
            if (chkLuuMatKhau.isChecked()) {
                prefs.edit().putString("saved_username", taiKhoan)
                        .putString("saved_password", matKhau)
                        .putInt("saved_vai_tro", spnVaiTro.getSelectedItemPosition())
                        .apply();
            } else {
                prefs.edit().remove("saved_username").remove("saved_password").remove("saved_vai_tro").apply();
            }

            Toast.makeText(this, "Đăng nhập thành công!", Toast.LENGTH_SHORT).show();
            redirectToMainScreen(vaiTroChon);
        } else {
            sessionManager.incrementLoginFailed(taiKhoan);
            tilMatKhau.setError("Mật khẩu không đúng");
            Toast.makeText(this, "Đăng nhập thất bại!", Toast.LENGTH_SHORT).show();
            checkLockStatus(taiKhoan);
        }
    }
    
    private void redirectToMainScreen(String vaiTro) {
        Intent intent;
        if ("admin".equals(vaiTro)) {
            intent = new Intent(DangNhapActivity.this, ManHinhChinhAdminActivity.class);
        } else {
            intent = new Intent(DangNhapActivity.this, ManHinhChinhNhanVienActivity.class);
        }
        startActivity(intent);
        finish();
    }
    
    private void redirectToMainScreen() {
        redirectToMainScreen(sessionManager.getVaiTro());
    }
}


