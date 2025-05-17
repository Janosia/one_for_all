
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

def ipspoofing():
      ''' 
         Reverse Path Filtering (RPF) Settings details 
         
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

def directedpingsignored():
      '''
      Handling of echo packets in reply to any ICMP ping
      
      - Path checked :  /etc/sysctl.conf
      
      '''
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