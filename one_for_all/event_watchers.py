import subprocess

from inotify_simple import INotify, flags
from checks.sysctl import directedpingsignored, ipspoofing, ipv6dis, synattacksblocked, sourcepackedrouting

def is_firefox_running() -> bool:
    out = subprocess.run(["pgrep","-c", "firefox"], capture_output=True, text=True)
    txt = int (out.stdout.strip())
    if txt >0:
        return True
    return False

def sys_ctl_changed() -> bool:
    inotify = INotify()
    watch_flags = flags.MODIFY
    try:
        inotify.add_watch('/etc/sysctl.conf', watch_flags)
    except FileNotFoundError:
        print("sysctl.conf not found.")
        return False
    try:
        print(f'Sysctl.conf has been modified, running checks')
        for event in inotify.read():
            for flag in flags.from_mask(event.mask):
                directedpingsignored()
                synattacksblocked()
                ipspoofing()
                ipv6dis()
                sourcepackedrouting()
                return True
    except Exception as e:
        print(f'Unable to track file sysctl.conf due to {e}')
        return False

def on_system_boot():
    return True
                    


    



