---
layout: post
title: "Caveat: Use Ubiquiti ER-X in China"
date: 2020-02-15 15:57:45 +0800
comments: true
categories:
- Network
---

After reading some articles about Ubiquiti EdegeRouter X, I realize this is a device I have no resistance not to buy it. Gigabyte Ethernet, multi-WAN, configurable by CLI (thus a lot of fun), reasonable price, and most importantly, high reliability. I enjoy exploring configurations, and in the meantime, it's a double-edge knife, if not configured well, it could have a very negative effect on your network performance. In this article, I will describe 2 configurations that could severely affect the performance when using it in China.

<!-- more -->

Ubiquiti has a very user-friendly forum for beginners to learn almost all technologies for EdgeRouter X. However, for the second issue (if you think it's an issue), I don't find anything on the internet. Probably it's not that popular in China? Anyway, here is the story.


### Requirement

- Dual WAN, both are connecting through PPPoE. eth0 connects pppoe0 (WAN0), and eth1 connects pppoe1 (WAN1).

- Six machines are in the LAN, with two connecting to WAN1 and four connecting to WAN0. All other devices will go through a load balancer to access the internet.
- No VLAN, because I want all devices to connect directly freely.


### Caveats

The first configuration is an easy one, the DNS name server. For dual WAN, we should use a name server at the system level instead of using the one automatically retrieved from ISP. Commands:

```
set interfaces ethernet eth0 pppoe 0 name-server none
set system name-server 114.114.114.114
```
(Reference: <https://community.ui.com/questions/PPPoE-and-DNS-issues/c6ea0bb1-9a29-45c4-9aa5-eff94ef9f65b>)

The second issue is not so obvious, and I find this issue by reading the message logs in `/var/log/messages`, sometimes, the load balance became inactive and then after a while became active again, and this happened once a while repeatly.

```
$ tail /var/log/messages
```
```
Feb 13 08:55:38 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe0 reachability changes to unreachable.
Feb 13 08:55:38 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe0 state changes to inactive.
Feb 13 08:55:38 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe1 reachability changes to unreachable.
Feb 13 08:55:38 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe1 state changes to inactive.
Feb 13 08:56:23 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe0 reachability changes to reachable.
Feb 13 08:56:23 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe0 state changes to active.
Feb 13 08:56:23 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe1 reachability changes to reachable.
Feb 13 08:56:23 ubnt ubnt-util: WLB: Load-Balance group G interface pppoe1 state changes to active.
```

By checking connections, I see some strange connection to 8.8.8.8, which I never set as a DNS server in anyplace.

```
sudo conntrack -L
```
```
icmp     1 13 src=**** dst=8.8.8.8 type=8 code=0 id=26922 src=8.8.8.8 dst=**** type=0 code=0 id=26922 mark=1694498816 use=1
udp      17 177 src=**** dst=8.8.8.8 sport=26528 dport=53 src=8.8.8.8 dst=**** sport=53 dport=26528 [ASSURED] mark=1686110208 use=1
```

After a thorough read about <https://help.ubnt.com/hc/en-us/articles/205145990-EdgeMAX-Dual-WAN-Load-Balance-Feature>, I get to know that the default behavior for a load balancer is to send a ping to 8.8.8.8 every minute if it fails, then set the reachability to unreachable for that network and redirect all traffic to the other network. With that knowledge, it's an easy fix then.


```
set load-balance group G interface pppoe0 route-test type ping target 114.114.114.114
set load-balance group G interface pppoe1 route-test type ping target 114.114.114.114
```

Also, we can tune the failure count and interval parameters to make this even more robust and reliable.
Then final settings for each interface:

```
route-test {
    count {
        failure 6
        success 6
    }
    initial-delay 1
    interval 10
    type {
        ping {
            target 114.114.114.114
        }
    }
}
```

I hope you enjoyed reading this article, and in case you faced the same issue, and you feel this article helpful, please comment below and let me know.

### Reference
Here is the full configuration:

```
firewall {
    all-ping enable
    broadcast-ping enable
    group {
        network-group PRIVATE_NETS {
            network 192.168.0.0/16
            network 172.16.0.0/12
            network 10.0.0.0/8
        }
    }
    ipv6-receive-redirects disable
    ipv6-src-route disable
    ip-src-route disable
    log-martians disable
    modify balance {
        rule 60 {
            action modify
            modify {
                table 11
            }
            source {
                address 192.168.1.13-192.168.1.16
            }
        }
        rule 70 {
            action modify
            modify {
                table 12
            }
            source {
                address 192.168.1.11-192.168.1.12
            }
        }
        rule 80 {
            action modify
            modify {
                lb-group G
            }
        }
    }
    options {
        mss-clamp {
            mss 1452
        }
    }
    receive-redirects disable
    send-redirects enable
    source-validation disable
    syn-cookies enable
}
interfaces {
    ethernet eth0 {
        description "WAN 0"
        duplex auto
        pppoe 0 {
            default-route none
            description "China Telecommunication"
            mtu 1492
            name-server none
            password ****
            user-id ****
        }
        speed auto
    }
    ethernet eth1 {
        description "WAN 1"
        duplex auto
        pppoe 1 {
            default-route none
            description "China Unicom"
            mtu 1492
            name-server none
            password ****
            user-id ****
        }
        speed auto
    }
    ethernet eth2 {
        duplex auto
        speed auto
    }
    ethernet eth3 {
        duplex auto
        speed auto
    }
    ethernet eth4 {
        duplex auto
        speed auto
    }
    loopback lo {
    }
    switch switch0 {
        address 192.168.1.1/24
        description Local
        firewall {
            in {
                modify balance
            }
        }
        mtu 1492
        switch-port {
            interface eth2 {
            }
            interface eth3 {
            }
            interface eth4 {
            }
            vlan-aware disable
        }
    }
}
load-balance {
    group G {
        exclude-local-dns disable
        flush-on-active enable
        gateway-update-interval 20
        interface pppoe0 {
            route-test {
                count {
                    failure 6
                    success 6
                }
                initial-delay 1
                interval 10
                type {
                    ping {
                        target 114.114.114.114
                    }
                }
            }
            weight 70
        }
        interface pppoe1 {
            route-test {
                count {
                    failure 6
                    success 6
                }
                initial-delay 1
                interval 10
                type {
                    ping {
                        target 114.114.114.114
                    }
                }
            }
            weight 30
        }
        lb-local enable
        lb-local-metric-change disable
        sticky {
            source-addr enable
        }
    }
}
port-forward {
    auto-firewall disable
    hairpin-nat disable
    wan-interface pppoe0
}
protocols {
    static {
        interface-route 0.0.0.0/0 {
            next-hop-interface pppoe0 {
            }
            next-hop-interface pppoe1 {
            }
        }
        table 11 {
            interface-route 0.0.0.0/0 {
                next-hop-interface pppoe0 {
                }
            }
        }
        table 12 {
            interface-route 0.0.0.0/0 {
                next-hop-interface pppoe1 {
                }
            }
        }
    }
}
service {
    dhcp-server {
        disabled false
        hostfile-update disable
        shared-network-name LAN {
            authoritative enable
            subnet 192.168.1.0/24 {
                default-router 192.168.1.1
                dns-server 192.168.1.1
                lease 86400
                start 192.168.1.38 {
                    stop 192.168.1.243
                }
                static-mapping 12 {
                    ip-address 192.168.1.12
                    mac-address ****
                }
                static-mapping 11 {
                    ip-address 192.168.1.11
                    mac-address ****
                }
                static-mapping EdgeSwitch {
                    ip-address 192.168.1.2
                    mac-address ****
                }
                static-mapping 13 {
                    ip-address 192.168.1.13
                    mac-address ****
                }
                static-mapping 14 {
                    ip-address 192.168.1.14
                    mac-address ****
                }
                static-mapping 15 {
                    ip-address 192.168.1.15
                    mac-address ****
                }
                static-mapping 16 {
                    ip-address 192.168.1.16
                    mac-address ****
                }
            }
        }
        static-arp disable
        use-dnsmasq disable
    }
    dns {
        forwarding {
            cache-size 2000
            listen-on switch0
        }
    }
    gui {
        http-port 80
        https-port 443
        older-ciphers disable
    }
    nat {
        rule 1 {
            description 11
            destination {
                port 47900-47910
            }
            inbound-interface pppoe1
            inside-address {
                address 192.168.1.11
                port 47900-47910
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 2 {
            description 12
            destination {
                port 47800-47810
            }
            inbound-interface pppoe1
            inside-address {
                address 192.168.1.12
                port 47800-47810
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 3 {
            description 13
            destination {
                port 47300-47310
            }
            inbound-interface pppoe0
            inside-address {
                address 192.168.1.13
                port 47300-47310
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 4 {
            description 14
            destination {
                port 47400-47410
            }
            inbound-interface pppoe0
            inside-address {
                address 192.168.1.14
                port 47400-47410
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 5 {
            description 15
            destination {
                port 47500-47510
            }
            inbound-interface pppoe0
            inside-address {
                address 192.168.1.15
                port 47500-47510
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 6 {
            description 16
            destination {
                port 47600-47610
            }
            inbound-interface pppoe0
            inside-address {
                address 192.168.1.16
                port 47600-47610
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 7 {
            description 11
            destination {
                port 47900-47910
            }
            inbound-interface pppoe0
            inside-address {
                address 192.168.1.11
                port 47900-47910
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 8 {
            description 12
            destination {
                port 47800-47810
            }
            inbound-interface pppoe0
            inside-address {
                address 192.168.1.12
                port 47800-47810
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 9 {
            description 13
            destination {
                port 47300-47310
            }
            inbound-interface pppoe1
            inside-address {
                address 192.168.1.13
                port 47300-47310
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 10 {
            description 14
            destination {
                port 47400-47410
            }
            inbound-interface pppoe1
            inside-address {
                address 192.168.1.14
                port 47400-47410
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 11 {
            description 15
            destination {
                port 47500-47510
            }
            inbound-interface pppoe1
            inside-address {
                address 192.168.1.15
                port 47500-47510
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 12 {
            description 16
            destination {
                port 47600-47610
            }
            inbound-interface pppoe1
            inside-address {
                address 192.168.1.16
                port 47600-47610
            }
            log disable
            protocol tcp_udp
            type destination
        }
        rule 5000 {
            description "masquerade for WAN 0"
            log disable
            outbound-interface pppoe0
            protocol all
            source {
            }
            type masquerade
        }
        rule 5002 {
            description "masquerade for WAN 1"
            log disable
            outbound-interface pppoe1
            protocol all
            source {
            }
            type masquerade
        }
    }
    ssh {
        port 22
        protocol-version v2
    }
    ubnt-discover {
        disable
    }
    unms {
        disable
    }
}
system {
    conntrack {
        expect-table-size 4096
        hash-size 4096
        modules {
            sip {
                disable
            }
        }
        table-size 32768
        tcp {
            half-open-connections 512
            loose enable
            max-retrans 3
        }
    }
    host-name ubnt
    ipv6 {
        disable
    }
    login {
        user ubnt {
            authentication {
                encrypted-password ****
                plaintext-password ""
            }
            level admin
        }
    }
    name-server 114.114.114.114
    name-server 114.114.115.115
    name-server 119.29.29.29
    name-server 223.5.5.5
    offload {
        hwnat enable
    }
    syslog {
        global {
            facility all {
                level notice
            }
            facility protocols {
                level debug
            }
        }
    }
    time-zone Asia/Singapore
}


/* Warning: Do not remove the following line. */
/* === vyatta-config-version: "config-management@1:conntrack@1:cron@1:dhcp-relay@1:dhcp-server@4:firewall@5:ipsec@5:nat@3:qos@1:quagga@2:suspend@1:system@4:ubnt-pptp@1:ubnt-udapi-server@1:ubnt-unms@1:ubnt-util@1:vrrp@1:vyatta-netflow@1:webgui@1:webproxy@1:zone-policy@1" === */
/* Release version: v2.0.8.5247496.191120.1124 */
```


