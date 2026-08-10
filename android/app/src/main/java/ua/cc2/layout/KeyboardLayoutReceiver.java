package ua.cc2.layout;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * Never actually invoked.  InputManagerService only queries for receivers of
 * ACTION_QUERY_KEYBOARD_LAYOUTS and reads the KEYBOARD_LAYOUTS meta-data off
 * the manifest entry -- but the component has to exist for the query to
 * resolve it.
 */
public class KeyboardLayoutReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
    }
}
