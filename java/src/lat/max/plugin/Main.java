package lat.max.plugin;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.bukkit.Bukkit;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitScheduler;

import lat.max.plugin.commands.Backup;

public class Main extends JavaPlugin {
	
    FileConfiguration config = getConfig();
    static String command = "";
    static String pythonPath = "";
    static boolean debug;

    @Override
    public void onEnable() {
    	generateConfig();
    	command = config.getString("python");
    	pythonPath = config.getString("path");
    	debug = config.getBoolean("debug");
    	
    	this.getCommand("backup").setExecutor(new Backup(this));
    	
    	BukkitScheduler scheduler = getServer().getScheduler();
        scheduler.scheduleSyncRepeatingTask(this, new Runnable() {
            @Override
            public void run() {
            	backup(null);
            }
        }, 0L, config.getLong("frequency"));
    }

    public void generateConfig() {
		config.addDefault("frequency", 72000);
    	config.addDefault("path", "mc_backup.py");
    	config.addDefault("python", "python");
    	config.addDefault("debug", false);
        config.options().copyDefaults(true);
        saveConfig();
    }
    
    public static void backup(String[] emails) {
    	Bukkit.broadcastMessage("Backing up.");
    	Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "save-all flush");
    	String args = "";
    	
    	if(emails != null) {
	    	for(int i = 0; i < emails.length; i++) {
	    		args += " " + emails[i];
	    	}
    	}
    	
    	String s = null;
    	if(debug) {
    		System.out.println("Command: " + command + " " + pythonPath + args);
    	}

    	try {
    		Process p = Runtime.getRuntime().exec(command + " " + pythonPath + args);

    		if(debug) {
    			BufferedReader stdInput = new BufferedReader(new 
                        InputStreamReader(p.getInputStream()));

                BufferedReader stdError = new BufferedReader(new 
                        InputStreamReader(p.getErrorStream()));

                System.out.println("Here is the standard output of the command:\n");
	       		while ((s = stdInput.readLine()) != null) {
	       			System.out.println(s);
               }

	       		System.out.println("Here is the standard error of the command (if any):");
               	while ((s = stdError.readLine()) != null) {
                	System.out.println(s);
                }
    		}
    		
		} catch (IOException e) {
			e.printStackTrace();
		}
    }

}
