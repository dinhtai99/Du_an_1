package fpoly.haideptrai.duan1.utils;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class PasswordHelper {
    public static String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return password; // Fallback
        }
    }
    
    public static boolean verifyPassword(String password, String hash) {
        return hashPassword(password).equals(hash);
    }
}









