package fpoly.haideptrai.duan1.utils;

import android.content.Context;
import android.content.SharedPreferences;

import fpoly.haideptrai.duan1.database.entities.NhanVien;

public class SessionManager {
    private static final String PREF_NAME = "session_prefs";
    private static final String KEY_USER_ID = "user_id";
    private static final String KEY_USERNAME = "username";
    private static final String KEY_VAI_TRO = "vai_tro";
    private static final String KEY_LOGIN_FAILED_COUNT_PREFIX = "login_failed_count_";
    private static final String KEY_LOCKED_UNTIL_PREFIX = "locked_until_";
    
    private SharedPreferences sharedPreferences;
    private SharedPreferences.Editor editor;
    
    public SessionManager(Context context) {
        sharedPreferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        editor = sharedPreferences.edit();
    }
    
    public void saveSession(NhanVien nhanVien) {
        editor.putInt(KEY_USER_ID, nhanVien.id);
        editor.putString(KEY_USERNAME, nhanVien.tenDangNhap);
        editor.putString(KEY_VAI_TRO, nhanVien.vaiTro);
        // Reset login failed count cho user này khi đăng nhập thành công
        editor.putInt(KEY_LOGIN_FAILED_COUNT_PREFIX + nhanVien.tenDangNhap, 0);
        editor.putLong(KEY_LOCKED_UNTIL_PREFIX + nhanVien.tenDangNhap, 0);
        editor.apply();
    }
    
    public int getUserId() {
        return sharedPreferences.getInt(KEY_USER_ID, -1);
    }
    
    public String getUsername() {
        return sharedPreferences.getString(KEY_USERNAME, "");
    }
    
    public String getVaiTro() {
        return sharedPreferences.getString(KEY_VAI_TRO, "");
    }
    
    public boolean isAdmin() {
        return "admin".equals(getVaiTro());
    }
    
    public void clearSession() {
        editor.clear();
        editor.apply();
    }
    
    public void incrementLoginFailed(String username) {
        String countKey = KEY_LOGIN_FAILED_COUNT_PREFIX + username;
        int count = sharedPreferences.getInt(countKey, 0) + 1;
        editor.putInt(countKey, count);
        if (count >= 5) {
            // Khóa trong 5 phút
            long lockedUntil = System.currentTimeMillis() + (5 * 60 * 1000);
            editor.putLong(KEY_LOCKED_UNTIL_PREFIX + username, lockedUntil);
        }
        editor.apply();
    }
    
    public void resetLoginFailed(String username) {
        editor.putInt(KEY_LOGIN_FAILED_COUNT_PREFIX + username, 0);
        editor.putLong(KEY_LOCKED_UNTIL_PREFIX + username, 0);
        editor.apply();
    }
    
    public boolean isLocked(String username) {
        if (username == null || username.isEmpty()) {
            return false;
        }
        long lockedUntil = sharedPreferences.getLong(KEY_LOCKED_UNTIL_PREFIX + username, 0);
        if (lockedUntil == 0) {
            return false;
        }
        boolean isStillLocked = System.currentTimeMillis() < lockedUntil;
        // Tự động reset nếu đã hết thời gian khóa
        if (!isStillLocked && lockedUntil > 0) {
            resetLoginFailed(username);
        }
        return isStillLocked;
    }
    
    public long getLockedTimeRemaining(String username) {
        if (username == null || username.isEmpty()) {
            return 0;
        }
        long lockedUntil = sharedPreferences.getLong(KEY_LOCKED_UNTIL_PREFIX + username, 0);
        long remaining = lockedUntil - System.currentTimeMillis();
        return remaining > 0 ? remaining : 0;
    }
}

