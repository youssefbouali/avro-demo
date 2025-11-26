from fastavro import writer, parse_schema
import json

# Charge et parse les schémas
with open('user_v1.avsc') as f:
    schema_v1 = parse_schema(json.load(f))
with open('user_v2.avsc') as f:
    schema_v2 = parse_schema(json.load(f))

# Données v1
records_v1 = [
    {"id": 1, "nom": "Alice", "age": 25},
    {"id": 2, "nom": "Bob",   "age": 30}
]

# Données v2 (nouveau champ)
records_v2 = [
    {"id": 3, "nom": "Charlie", "age": 35, "email": "charlie@x.com", "actif": True},
    {"id": 4, "nom": "David",   "age": 28, "email": None, "actif": False}
]

with open('users_v1.avro', 'wb') as out:
    writer(out, schema_v1, records_v1)

with open('users_v2.avro', 'wb') as out:
    writer(out, schema_v2, records_v2)

print("Fichiers générés : users_v1.avro et users_v2.avro")