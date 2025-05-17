from thefuzz import fuzz

def sshlogindis():
      '''
      Checks if password-based authentication is enabled for client side
      
      - Path used : /etc/ssh/ssh_config
      
      '''
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
         print (" sshd_config - File Not Found. Download OpenSSH server")

