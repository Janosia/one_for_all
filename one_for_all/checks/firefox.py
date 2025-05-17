import os 
import json

def read_addons():
    '''
    Find mozilla firefox addons for each profile and display their ability to run on incognito mode
    
    Path Checked for Profiles: ~/snap/firefox/common/.mozilla/firefox
    
    '''
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