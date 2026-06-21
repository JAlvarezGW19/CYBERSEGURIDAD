import os
import re
import argparse
import sys

try:
    import chromadb
except ImportError:
    print("Error: No se encontró ChromaDB. Instálalo ejecutando: pip install chromadb")
    exit(1)

# Inicializar el cliente de ChromaDB (Persistente para guardar en disco)
DB_PATH = "/home/cero/MEGA/VS_CODE_WORKSPACE/CYBERSEGURIDAD/chroma_db"
DOCS_PATH = "/home/cero/MEGA/VS_CODE_WORKSPACE/CYBERSEGURIDAD/docs"
GEMINI_PATH = "/home/cero/MEGA/VS_CODE_WORKSPACE/CYBERSEGURIDAD/.agent"
client = chromadb.PersistentClient(path=DB_PATH)

def get_collection(topic: str):
    """Obtiene o crea una colección basada en el nombre del tema."""
    return client.get_or_create_collection(name=f"{topic}_errors")

def process_markdown_and_populate(topic: str):
    """Lee un archivo .md, extrae errores y soluciones, y los inserta en su colección."""
    docs_file = os.path.join(DOCS_PATH, f"{topic}.md")
    gemini_file = os.path.join(GEMINI_PATH, f"{topic}.md")
    
    if os.path.exists(docs_file):
        file_path = docs_file
    elif os.path.exists(gemini_file):
        file_path = gemini_file
    else:
        print(f"Archivo no encontrado en docs/ ni en .agent/: {topic}.md")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Separar por los encabezados de nivel 2 (##)
    sections = re.split(r'\n## ', content)
    
    # La primera sección es la introducción, la ignoramos
    if len(sections) > 1:
        sections = sections[1:]

    documents = []
    metadatas = []
    ids = []

    for i, section in enumerate(sections):
        # La primera línea contiene el título del error
        lines = section.split('\n', 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        
        # Preparamos los registros
        documents.append(body)
        metadatas.append({"title": title})
        ids.append(f"{topic}_error_{i+1}")

    collection = get_collection(topic)
    # Insertar en ChromaDB (upsert inserta o actualiza si el ID ya existe)
    if documents:
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Se indexaron {len(documents)} registros de errores de '{topic}' en ChromaDB.\n")

def query_error(topic: str, query_text: str, n_results: int = 2, threshold: float = 1.2):
    """Realiza una búsqueda semántica en la base de datos de errores."""
    collection = get_collection(topic)
    if collection.count() == 0:
        print(f"⚠️ La colección '{topic}' está vacía o el archivo .md no existe.")
        return
        
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    print(f"🔍 Resultados para la búsqueda en '{topic}': '{query_text}'\n" + "="*60)
    encontrados = 0
    for i in range(len(results['ids'][0])):
        title = results['metadatas'][0][i]['title']
        document = results['documents'][0][i]
        distance = results['distances'][0][i] if 'distances' in results and results['distances'] else "N/A"
        
        # Ignoramos los resultados que superen la distancia permitida
        if isinstance(distance, float) and distance > threshold:
            continue
            
        encontrados += 1
        dist_str = f"{distance:.4f}" if isinstance(distance, float) else str(distance)
        print(f"📌 Título: {title} (Distancia: {dist_str})")
        print(f"📄 Contenido:\n{document}\n" + "-"*60)
        
    if encontrados == 0:
        print(f"⚠️ No se encontraron resultados relevantes (umbral de distancia > {threshold}).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Base de datos vectorial de errores y conocimientos")
    parser.add_argument("-q", "--query", type=str, help="Búsqueda del error en lenguaje natural")
    parser.add_argument("-u", "--update", action="store_true", help="Actualiza la base de datos leyendo el archivo .md correspondiente")
    parser.add_argument("-c", "--collection", type=str, default="latex", help="Tema a consultar/actualizar (por defecto: latex). Busca docs/<tema>.md")
    parser.add_argument("-t", "--threshold", type=float, default=1.2, help="Umbral de distancia máxima permitida (ej. 1.2)")
    
    args = parser.parse_args()
    collection = get_collection(args.collection)

    # 1. Extraemos de markdown y poblamos la BD Vectorial solo si se pide o si está vacía
    if args.update or collection.count() == 0:
        process_markdown_and_populate(args.collection)
    
    # 2. Hacemos la consulta si se proporcionó una
    if args.query:
        query_error(args.collection, args.query, threshold=args.threshold)
    elif not args.update:
        script_name = os.path.basename(sys.argv[0])
        print(f"💡 Sugerencia: Puedes buscar errores usando: python {script_name} -c {args.collection} -q 'tu error'")
        consulta_ejemplo = "Me da error Missing $ cuando escribo texto con guiones bajos"
        query_error(args.collection, consulta_ejemplo, threshold=args.threshold)