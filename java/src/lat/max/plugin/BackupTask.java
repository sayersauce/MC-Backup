package lat.max.plugin;

import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;

public class BackupTask extends BukkitRunnable {
	
	private final JavaPlugin plugin;

    public BackupTask(JavaPlugin plugin) {
        this.plugin = plugin;
    }

	@Override
	public void run() {
		plugin.getServer().broadcastMessage("test");
	}

}
