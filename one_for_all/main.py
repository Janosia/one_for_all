from .menu import Menu


def display():
   print ("=" * 50)
   print ("")
   print ("1 : Desktop Details ")
   print ("2 : ICMP Echo packets")
   print ("3 : IP Spoofing/ RPF Settings")
   print ("4 : IPv6 disabled")
   print ("5 : Remote Login enabled")
   print ("6 : Source Packed Routing")
   print ("7 : SSH Remote login via Password Details")
   print ("8 : SSH Root Login via Password")
   print ("9 : TCP SYN Settings ")
   print ("10 : Mozilla Firefox Addons")
   print ("11 : AutoMount/AutoPlay/AutoRun settings")
   print ("0: Exit")
   print ("=" * 50)


def options(op):
  
   if (op == 1):
      Menu.cleardesk()
   elif (op == 2):
      Menu.directedpingsignored()
   elif (op == 3):
      Menu.ipspoofing()
   elif (op == 4 ):
      Menu.ipv6dis()
   elif (op == 5):
      Menu.lightdm()
   elif (op == 6):
      Menu.sourcepackedrouting()
   elif (op == 7):
      Menu.sshlogindis()
   elif (op == 8):
      Menu.sshrootlogin()
   elif (op == 9):
      Menu.synattacksblocked()
   elif (op == 10):
      Menu.read_addons()
   elif (op == 11):
      Menu.auto_play_devices()
   elif (op==0):
      print ("Exiting")
   else:
      print ("Inavlid option")
while True:
    display()
    val = int(input("enter option (1-11)"))
    options(val)
    if(val ==0):
      break