# The binding IP of our interface
# Can be found using 
# ifconfig eth0 | awk '/inet addr/ { print $2}' | sed 's#addr:##g'
bind_addr = "192.168.1.3"

# Where all configurations are saved 
data_dir =  "C:/Users/tu/Desktop/dungth/hpuerp/odoo_template/nomad-config"
datacenter =  "dc1"

# Act as client and communicate with the server one
client =  {
    enabled =  true

    # Server addresses. If we have more than one, we
    # can add them here
    servers = ["node-01.local:4647"]
    host_volume "postgresql" {
        path      = "C:/Users/tu/Desktop/dungth/nomad_volumes/postgresql"
        read_only = false
    }
}

# Where Consul, our service discovery, is listening from.
consul =  {
    address =  "node-01.local:8500"
}

# Addresses to notify Consul how to find us. 
# For this client, we are # accessible from 
# the node-02.local domain
advertise =  {
    http =  "node-02.local"
    rpc  =  "node-02.local"
    serf =  "node-02.local"
}