import jsonschema

message_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'date': {'type': 'string', 'format': 'date-time'},
        'message': {'type': ['string', 'null']},
        'media': {'type': 'boolean'},
    },
    'required': ['id', 'date']
}