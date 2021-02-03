from opa_client.opa import OpaClient

client = OpaClient(host='opa') # default host='localhost', port=8181, version='v1'

client.check_connection() # response is  Yes I'm here :)

# Ensure the connection is closed correctly by deleting the client
del client
