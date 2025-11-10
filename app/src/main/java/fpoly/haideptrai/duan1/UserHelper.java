package fpoly.haideptrai.duan1;

import android.content.Context;
import android.content.SharedPreferences;

public class UserHelper {
    private static final String PREF_NAME = "user_prefs";
    private static final String KEY_USERNAME = "username";
    private static final String KEY_PASSWORD = "password";
    private static final String KEY_PREFIX = "user_";

    private SharedPreferences sharedPreferences;

    public UserHelper(Context context) {
        sharedPreferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    // Đăng ký tài khoản mới
    public boolean registerUser(String username, String password) {
        // Kiểm tra tài khoản đã tồn tại chưa
        if (isUserExists(username)) {
            return false; // Tài khoản đã tồn tại
        }

        // Lưu tài khoản và mật khẩu
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_PREFIX + username, password);
        editor.apply();
        return true;
    }

    // Kiểm tra tài khoản có tồn tại không
    public boolean isUserExists(String username) {
        return sharedPreferences.contains(KEY_PREFIX + username);
    }

    // Xác thực đăng nhập
    public boolean login(String username, String password) {
        String savedPassword = sharedPreferences.getString(KEY_PREFIX + username, null);
        return savedPassword != null && savedPassword.equals(password);
    }

    // Lưu thông tin đăng nhập hiện tại
    public void saveCurrentUser(String username, String password) {
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_USERNAME, username);
        editor.putString(KEY_PASSWORD, password);
        editor.apply();
    }

    // Lấy thông tin đăng nhập đã lưu
    public String getSavedUsername() {
        return sharedPreferences.getString(KEY_USERNAME, "");
    }

    public String getSavedPassword() {
        return sharedPreferences.getString(KEY_PASSWORD, "");
    }

    // Xóa thông tin đăng nhập đã lưu
    public void clearSavedUser() {
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.remove(KEY_USERNAME);
        editor.remove(KEY_PASSWORD);
        editor.apply();
    }
}









