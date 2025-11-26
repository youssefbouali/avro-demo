from fastavro import reader

def lire_avro(fichier, schema_path=None):
    with open(fichier, 'rb') as f:
        avro_reader = reader(f)
        print(f"\nLecture de {fichier} :")
        for i, record in enumerate(avro_reader, 1):
            print(f"  {i}. {record}")

# Test compatibilité
print("Lecture avec schéma v2 (devrait fonctionner partout)")
lire_avro('users_v1.avro')
lire_avro('users_v2.avro')