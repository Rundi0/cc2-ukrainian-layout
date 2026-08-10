package ua.cc2.layout;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Exists so the package can be launched at least once.  A never-launched app
 * stays in the stopped state, and the system skips stopped packages when it
 * looks for keyboard layouts.
 */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        TextView t = new TextView(this);
        int p = (int) (24 * getResources().getDisplayMetrics().density);
        t.setPadding(p, p, p, p);
        t.setText(getString(R.string.instructions));
        setContentView(t);
    }
}
