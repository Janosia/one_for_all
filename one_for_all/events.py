from checks.desktop import cleardesk
from checks.sysctl import directedpingsignored, ipspoofing, ipv6dis, synattacksblocked, sourcepackedrouting
from checks.network import sshlogindis, sshrootlogin
from checks.firefox import read_addons
from checks.media import lightdm, auto_play_devices

event_map = {
    "on_user_login": [cleardesk, sshlogindis, sshrootlogin],
    "on_network_up": [ipspoofing, sourcepackedrouting, directedpingsignored, synattacksblocked],
    "on_system_boot": [ipv6dis, ipspoofing, sourcepackedrouting, synattacksblocked, sshlogindis, sshrootlogin],
    "on_usb_device_inserted": [auto_play_devices],
    "on_firefox_start": [read_addons],
    "on_lightdm_loaded": [lightdm],
    "on_sysctl_change": [ipv6dis, ipspoofing, sourcepackedrouting, synattacksblocked, directedpingsignored]
}
def trigger_event(event_name):
    checks = event_map.get(event_name)
    if not checks:
        print(f" No checks associated with event: {event_name}")
        return
    print(f" Running checks for event: {event_name}")
    for check in checks:
        check()
        print("-" * 40)
