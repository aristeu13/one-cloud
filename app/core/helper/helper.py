from bson import ObjectId


def convert_object_id(data):
    """Convert ObjectId to string in a MongoDB document."""
    if isinstance(data, list):
        return [convert_object_id(item) for item in data]
    if isinstance(data, dict):
        return {k: convert_object_id(v) for k, v in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data
