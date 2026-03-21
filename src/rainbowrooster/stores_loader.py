import logging

import rainbowrooster.gen.stores.v1.stores_pb2 as stores_pb2


def load_stores() -> list[str]:
    display_name_ext = stores_pb2.DESCRIPTOR.extensions_by_name["display_name"]
    enum_desc = stores_pb2.DESCRIPTOR.enum_types_by_name["StoreId"]
    stores = [
        value_desc.GetOptions().Extensions[display_name_ext]
        for value_desc in enum_desc.values
        if value_desc.number != 0
    ]
    logging.debug(f"Loaded {len(stores)} stores from heatedhornet schema")
    return stores
