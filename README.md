# The "I'm in" script
A self daemonizing, pure python reverse shell with no third party dependancies. It runs in the background on the unsuspecting victim's machine and inserts itself into the userprofile and persists after system restarts and network drops. The "user" can at any time, access the target's shell from their remote VPS via netcat

# Step 1
Enter your your remote host's URL/IP and any exposed port into the VPS_URL and VPS_PORT variables
Find a target and get them to execute shellmesen.py on their system.
This can be done either directly or by importing it inside a non malicious script and calling the main() function.

# Step 2
To access the target's shell, just log into your VPS and execute `ncat -k -l -p $PORT` where PORT is the port you hardcoded in shellmsen.py
![command_screenshot](https://i.imgur.com/hgPwGLg.png)

# Step 3
Say "I'm in" like one of those fancy hollywood hackers, adjust your beret and proceed to use the shell access for `strictly educational purposes`

This tool was created as a fun weekend project and is meant to be used for strictly educational purposes
The authors do not bear any responsibility for what anyone does with the script or any modification of the same.
Just don't be a dick alright?

Credits:  
@Scar26  
@Sin3point14  
A modification of the Daemonization class from here https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
