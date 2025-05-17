import subprocess
import os 
def auto_play_devices():

      '''
      Using GSetting command line tool. To check manually use Dconf GUI. 
      For more details read : https://askubuntu.com/questions/22313/what-is-dconf-what-is-its-function-and-how-do-i-use-it
      
      - Auto mounting
      
         Feature in Ubuntu that allows the operating system to automatically detect and mount external storage devices, 
         such as USB drives, CDs, and DVDs, as soon as they are connected to the computer
      
      - AutoRun 
         
         Runs a program automatically when a USB drive or a CD/DVD is inserted into reader, 
         Application set on AutoRun could be a malicious program that started automatically without user interaction.

      - AutoPlay 
         Defines a set of actions to perform when a device or a drive is connected to the computer. 
         Newer versions have limited device options:- Cameras, PDAs, Printers & Scanners or Input Devices (Mice, Keyboards, etc).

      '''
      command = ["gsettings", "list-schemas"] 
      try:
         out = subprocess.run(command, capture_output=True, text=True)
         txt = out.stdout.split("\n") 
         for i in txt:
            if ("org.gnome.desktop" in i): 
               if ("media-handling" in i): 
                  command1 = ["gsettings", "list-keys", i] 
                  out1 = subprocess.run(command1, capture_output=True, text=True)
                  res = out1.stdout.split("\n")
                  for j in res:
                     if ("automount" in j): 
                        command2 =["gsettings", "get", i, j]
                        out2 = subprocess.run(command2, capture_output =True, text=True)
                        print ( j, "enabled - ", out2.stdout)
                     elif ("autorun-never" in j): 
                        command3=["gsettings", "get", i, j]
                        out3= subprocess.run(command3, capture_output=True, text=True)
                        print (j,"enabled - ", out3.stdout) 
                  print ("automount will automatically mount the media")
                  print ("automount -open mounts and opens a file manager to show contents of the device")
                  print ("autorun is related to automatic execution of the device")
      except:
        print (out.stderr)

def lightdm():
       ''' 
         Remote Login in (LightDM) Lightweight Display Manager 

         LightDM is a display manager which was pre-installed in Ubuntu (till 17.04)

         In LightDM, "REMOTE LOGIN" option on login screen refers to use of Remote Desktop Protocol (RDP) or X11
         forwarding. These options allow users to access a desktop session on the system from a
         remote location.
       
       '''
       path = "/etc/lightdm/lightdm.conf.d/lightdm.conf"
       try :
         with open (path, "r") as fobj:
           contents = fobj.read()
           searchfor = "greeter-show-remote-login = false" 
           print ("Remote desktop - disabled") if(searchfor in contents) else print ("Remote desktop - enabled")
       except FileNotFoundError:
        print ("File /etc/lightdm/lightdm.conf.d/lightdm.conf does not exist. You can install LightDM using 'apt-get install lightdm' ")

