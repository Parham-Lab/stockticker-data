from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection


settings = initialize_vpn("France")  # starts nordvpn and stuff
rotate_VPN(settings)  # actually connect to server
settings = initialize_vpn("Brazil")  # starts nordvpn and stuff
rotate_VPN(settings)  # actually connect to server  


