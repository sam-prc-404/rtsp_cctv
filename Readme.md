# >>> <<< >>> <<<

## TODO

1. Directly connect the camera to etehrnet of our pc (enps0) (interface name may vary.)

1. Configure Your Ethernet Interface (enp2s0)
    Set your IP address manually:
    ```sh
    sudo ip addr add 192.168.1.1/24 dev enp2s0
    sudo ip link set enp2s0 up
    ```

    To make it persistent, add it to `/etc/network/interfaces` (Debian-based) or use `netplan/systemd-networkd` depending on your setup.


3. Next Steps (Optional):
    If you actually want to route traffic (since you're making yourself the gateway), you'll need to enable IP forwarding and set up NAT:
    ```sh
    sudo sysctl -w net.ipv4.ip_forward=1
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  # If  forwarding to the internet
    ```

4. Run the `simple_dhcp.py` script to assign the default ip `192.168.1.66` to the camera.

5. Figure out rtsp url .

5. View the stream through `vlc`,`ffplay` or as you wish.
    Currently for the camera the url is `"rtsp://admin:123456@192.168.1.66:554/mpeg4"  `
    ```sh
    ffplay "rtsp://admin:123456@192.168.1.66:554/mpeg4"  
    ```
