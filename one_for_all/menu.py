import os
import warnings
import json
import subprocess
warnings.filterwarnings("ignore")
from thefuzz import fuzz

class Menu:
   ''' 11 different functions containing checks for both server and client side configurations'''
   def cleardesk():
      '''Checks if desktop has any files/directories'''
      path = "/home" 
      out = os.listdir(path) 
      for i in out:
         subpath = "/home/" + i+"/Desktop" 
         try:
            subout = os.listdir(subpath) 
            print (f'{i}: desktop is EMPTY') if(len(subout) == 0) else print (f'{i} desktop is NOT empty')
         except NotADirectoryError as e:
            print (subpath , "not found")
   
   def directedpingsignored():
      '''
      Handling of echo packets in reply to any ICMP ping
      
      - Path checked :  /etc/sysctl.conf'''
      path = "/etc/sysctl.conf"
      try:
         with open(path, "r") as fobj:
            s = "net.ipv4.imcp_echo_ignore_all=1"
            line = fobj.readline()
            flag =0
            while line :
               if ("#" not in line ):
                  if(s in line):
                     flag =1
                     break
               line = fobj.readline()
            print (f'{s}, NOT found. Echo packets will NOT be ignored') if (flag == 0) else print ("Linux kernel will ignore all incoming ICMP(Internet Control Message Protocol) Echo Request messages.")
      except FileNotFoundError:
         print ("File /etc/sysctl.conf not found") 

   def ipspoofing():
      ''' Reverse Path Filtering (RPF) Settings details 
         
         RPF verifies that source IP address of a packet is reachable via the same interface through which it was received. 
         It does not allow attackers to forge IP Addresses. By verifying the reverse path, it ensures that packets are coming from legitimate sources and reduces the risk of accepting spoofed packets.
         
         
         In Linux, RPF can be configured using the following sysctl settings:

         - net.ipv4.conf.all.rp_filter
         - net.ipv4.conf.default.rp_filter

         Setting these parameters to '1' enables strict mode, where packets are
         accepted only if they are received on the best reverse path as determined
         by the routing table.

      '''
      path = "/etc/sysctl.conf"
      try:
         with open(path, "r") as fobj:
            out = fobj.readline()
            s1= "net.ipv4.conf.all.rp_filter=1"
            s2 = "net.ipv4.conf.default.rp_filter=1"
            flag = 0
            print (" Is Reverse path filtering is enabled with strict mode for all interfaces and the default interface ? ", end="")
            while out :
               if ("#" not in out):
                  if(s1 in out or s2 in out):
                     flag = flag+1
               out = fobj.readline()
            print(" Yes ")  if(flag == 2) else print (f' No. Recommended to uncomment lines : {s1} \n {s2}')
      except FileNotFoundError:
         print ("File /etc/sysctl.conf not found ")

   def ipv6dis():
         '''
         Checks if IPv6 is disabled
         
         It is recommended to disable IPv4 instead since v6 is simpler than v4
         '''
         path = "/etc/sysctl.conf"
         
         try:
          with open (path,"r")as fobj:
            out = fobj.readline() 
            match = "net.ipv6.conf.all.disable_ipv6=1"
            match2 = "net.ipv6.conf.default.disable_ipv6=1"
            match3 = "net.ipv6.conf.lo.disable_ipv6=1"
            print (f'{match} - disables IPv6 on all network interfaces.')
            print (f'{match2} - disables IPv6 on the default network interface.' )
            print (f'{match3} - disables IPv6 on the loopback interface , which is a virtual network interface that allows communication within the local host.')
            flag = 0
            while out:
               if ("#" not in out ):
                  if(match in out or match2 in out or match3 in out):
                    flag = flag+1
               out = fobj.readline()
            print ("All found") if(flag == 3) else print ("Only", flag, "found")
         
         except FileNotFoundError:
            print ("File Not Found") 

   def lightdm():
       ''' 
         Remote Login in LightDM Daemon 
       
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
        print ("File /etc/lightdm/lightdm.conf.d/lightdm.conf does not exist. Install LightDM daemon")

   def sourcepackedrouting():
        '''
         Source Packed Routing 

         Source routing allows a packet to carry a predefined list of destination addresses (e.g., [A, B, C, D]).
         At each hop, the router reads the next address in the list and forwards the packet accordingly.
         This means the packet's path is determined by the sender, rather than dynamically by each router.
        
         This gives users power to bypass network security measures allowing them to send packets to an address normally shielded by a firewall. 
         This can be used as a network recce tool.

         This has been deprecated for security concerns.

         Following lines in /etc/sysctl.conf file :

         - net.ipv4.conf.all.accept_source_route = 0 | Source Routing disabled on ALL interfaces 
        
         - net.ipv4.conf.default.accept_source_route = 0 | Source Routing disabled on DEFAULT interfaces ONLY
        
        '''
        path = "/etc/sysctl.conf"
        try:
         with open (path, "r") as fobj:
          line = fobj.readline()
          all_interface = "net.ipv4.conf.all.accept_source_route = 0" #specifies that the system should not accept source-routed packets on all network interfaces
          default_interface = "net.ipv4.conf.default.accept_source_route = 0" #parameter specifies that the system should not accept source-routed packets on the default network interface
          check1 = 0
          check2 = 0
          while line:
            if("#" not in line):
               if(all_interface in line):
                  check1=1 
               if(default_interface in line):
                  check2=1
            line = fobj.readline()
         if (check1 and check2):
            print ("System does not accept source routed packets")
         elif (check2):
            print ("System does not accept source routed packets on DEFAULT INTERFACE")
         else:
            print(f'Source Routing enabled.From {path} Uncomment lines \n {all_interface} \n {default_interface} ')
        except FileNotFoundError:
         print ("File /etc/sysctl.conf Not found")

   def sshlogindis():
      '''
      Checks if password-based authentication is enabled for client side
      
      - Path used : /etc/ssh/ssh_config'''
      path = "/etc/ssh/ssh_config"
      print(' PASSWORD AUTHENTICATION ? ', end="")
      try:
         with open (path, "r") as fobj:
            line =fobj.readline()
            look_for = "PasswordAuthentication yes" 
            flag =0
            while line:
               if(fuzz.partial_ratio(line, look_for)>=80):
                  flag =1
                  break
               line = fobj.readline()
            
            print ("NOT present")if(flag ==0) else print('PRESENT')
      except FileNotFoundError :
         print ("/etc/ssh/ssh_config - File Not Found ")

   def sshrootlogin() :
      '''
      Checks if Root user is prohibited from password-based authentication for REMOTE LOGINS.
      This uses server configuration file (OpenSSH server). 
      
      - Ensure that OpenSSH server is present.
      
      - Path used : /etc/ssh/sshd_config
      '''
      path = "/etc/ssh/sshd_config"
      try:
         flag=0
         with open(path , "r") as fobj:
            print('PUBLIC KEY AUTHENTICATION ?', end = "")
            out = fobj.readline()
            s = "PermitRootLogin prohibit -password"
            while out:
               if(fuzz.partial_ratio(s, out)>=80):
                  # print (s, " Is set. Prohibits the root user from logging in with a password. login through public key authentication")
                  flag =1
               out = fobj.readline()   
         print ("NO") if(flag == 0) else 'YES'
      except FileNotFoundError:
         print (" sshd_config - File Not Found. Download openssh server")
   
   def synattacksblocked():
      '''
      Settings for TCP SYN cookies/packets/retransmission/SYN-ACK retransmission
      
      - Path used : /etc/sysctl.conf
      
      ''' 
      path = "/etc/sysctl.conf"
      try:
         with open (path, "r") as fobj:
            out = fobj.readline()
            s1 = "net.ipv4.tcp_syncookies=1"
            s2 = "net.ipv4.tcp_max_sys_backlog=2048"
            s3 = "net.ipv4.tcp_synack_retries=2"
            s4 = "net.ipv4.tcp_syn_retries =5"
            flag = 0
            while out :
               if("#" not in out):
                  if(s1 in out or s2 in out or s3 in out or s4 in out):
                     flag +=1
               out = fobj.readline()
            print (s1, "- TCP SYN cookies use enabled. Kernel uses SYN cookies to handle incoming TCP connection requests and mitigate the impact of SYN flood attacks.")
            print (s2, "- the maximum number of outstanding TCP SYN requests that can be queued")
            print (s3, "- sets the maximum number of SYN-ACK retransmissions that the TCP stack will attempt for a new connection. ")
            print (s4, "- the maximum number of SYN retransmissions that the TCP stack will attempt for a new connection")
            print ("All enabled") if(flag == 4) else print ("Only", flag, " enabled ")
      except FileNotFoundError:
         print ("File /etc/sysctl.conf Not Found ")

   def auto_play_devices():

      '''
      Using GSetting command line tool. To check manually use Dconf GUI. 
      For more details read : 
      - https://askubuntu.com/questions/22313/what-is-dconf-what-is-its-function-and-how-do-i-use-it
      
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


   def read_addons():
      '''
      Find mozilla firefox addons for each profile and display their ability to run on incognito mode
      
      Path Checked for Profiles: ~/snap/firefox/common/.mozilla/firefox'''
      try:
         profiles_stored_path = os.path.expanduser("~/snap/firefox/common/.mozilla/firefox")
         
         if (not os.path.isdir(profiles_stored_path)):
            print(f'Path {profiles_stored_path} is wrong.')
            return 
         direc= os.listdir(profiles_stored_path)
         
         for i in direc:
            
            print (f'Profile : {i.strip('.default')}') if(".default" in i) else print()
            
            pr_direc = os.path.join(profiles_stored_path, i)
            addons_file = os.path.join(pr_direc, "extensions.json")
            
            if (os.path.isfile(addons_file)):
               with open (addons_file, "r") as fobj:
                  addons= json.load(fobj)
                  for i in addons['addons']:
                     print (f'Name : {i["defaultLocale"]["name"]}')
                     print (f'Path : {i["path"]}')
                     
                     print("Installed from ", end="")
                     print (" local/ manual  install")if (i["sourceURI"] == 'null') else print (f'Installed From: {i["sourceURI"]}')
                     
                     print("Description ", end="")
                     print (f'Description : {i["defaultLocale"]["description"]}') if ("description" in i["defaultLocale"]) else print ("No description available")
                     
                     
                     print("Can this work in Incognito Mode ? ", end="")
                     if ("incognito" in i):
                        if (i["incognito"]=="spanning"):
                           print ("YES and is able to ACCESS and MODIFY data in both modes")
                        elif (i["incognito"] == "split"):
                           print ("YES but in different instances will not be able to access or modify data")
                        else :
                           print ("NO")
                     else:
                        print ("NO INFORMATION")
                     
                     print ("-" * 50) 
               
            else:
               print("NO EXTENSION FILE FOR THIS PROFILE")
            print("#" * 50)
      except Exception as e:
         print (f'Error has occured, {e}')



   
 


