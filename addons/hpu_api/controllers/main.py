from odoo.addons.base_rest.controllers import main


class HpuApiPublicApiController(main.RestController):
    _root_path = "/hpu_api/ping/"
    _collection_name = "hpu.api.ping.services"
    _default_auth = "public"
    


class HpuApiPartnerController(main.RestController):
    _root_path = "/hpu_api/partner/"
    _collection_name = "hpu.api.partner.services"
    _default_auth = "api_key"

