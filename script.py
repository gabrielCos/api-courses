import pymongo
import json

print("Script iniciado...")

# Connect to MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["courses"]
    collection = db["courses"]
    print("Conectado ao MongoDB.")
except Exception as e:
    print(f"Erro na conexão com MongoDB: {e}")
    exit()

# Read courses from courses.json
try:
    with open("courses.json", "r") as f:
        courses = json.load(f)
        print(f"{len(courses)} cursos lidos do arquivo.")
except Exception as e:
    print(f"Erro ao ler 'courses.json': {e}")
    exit()

# Create index for efficient retrieval
collection.create_index("name")

inseridos = 0

# add rating field to each course
for course in courses:
    course['rating'] = {'total': 0, 'count': 0}

# add rating field to each chapter
for course in courses:
    try:
        course['rating'] = {'total': 0, 'count': 0}
        for chapter in course.get('chapters', []):
            chapter['rating'] = {'total': 0, 'count': 0}
        result = collection.insert_one(course)
        inseridos += 1
        print(f"Curso inserido com _id: {result.inserted_id}")
    except Exception as e:
        print(f"Erro ao inserir curso: {e}")

# Close MongoDB connection
print(f"Total de cursos inseridos: {inseridos}")
client.close()