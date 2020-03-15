package lat.max.plugin.commands;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.plugin.Plugin;

import lat.max.plugin.Main;

public class Backup implements CommandExecutor {

	Plugin plugin;
	
	public Backup(Plugin plugin) {
		this.plugin = plugin;
	}
	
	public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
		if(sender.isOp()) {
			Main.backup(args);
		} else {
			sender.sendMessage("Insufficient permissions.");
		}
		return true;
	}
	
}
