{
    "name": "Custom Purchase Order(Domestic / Imported)",
    "summary": "Type wise Purchase Order",
    "description": "Type wise Purchase Order.",
    "author": "Primacy Infotech Pvt. Ltd.",
    "version": "18.0.0.3",
    # any module necessary for this one to work correctly
    "depends": ["base", "purchase"],
    # always loaded
    "data": [
        'data/sequence.xml',
        'views/purchase_order.xml',
        'views/purchase_order.xml',
    ],
    "license": "OPL-1",
}

