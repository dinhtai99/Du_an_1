package fpoly.haideptrai.duan1;

import android.app.Application;

import fpoly.haideptrai.duan1.utils.DatabaseInitializer;

public class MyApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        DatabaseInitializer.initialize(this);
    }
}









