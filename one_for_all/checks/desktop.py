import os 

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