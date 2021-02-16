1. Start consul:

docker run     -d     -p 8500:8500     -p 8600:8600/udp  
   --name=badger     consul agent -server -ui -node=server- 
1 -bootstrap-expect=1 -client=0.0.0.0

2. Start nomad server:

nomad agent -config=C:\Users\tu\Desktop\dungth\hpuerp\odoo_template\server.nomad

3. Start nomad client:

nomad agent -config=C:\Users\tu\Desktop\dungth\hpuerp\odoo_template\client.nomad