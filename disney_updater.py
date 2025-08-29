import requests
import json
import random
from datetime import datetime
import os

class DisneyContentUpdater:
    def __init__(self):
        # URLs de APIs gratuitas
        self.joke_apis = [
            "https://official-joke-api.appspot.com/jokes/random",
            "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single",
            "https://icanhazdadjoke.com/",
        ]
        
        self.quote_apis = [
            "https://api.quotable.io/random?tags=motivational,inspirational&maxLength=150",
            "https://zenquotes.io/api/random",
        ]
        
        # Palabras clave Disney para filtrar contenido relevante
        self.disney_keywords = [
            'magic', 'magical', 'dream', 'dreams', 'wonder', 'adventure', 
            'family', 'friendship', 'love', 'happiness', 'joy', 'believe',
            'princess', 'prince', 'castle', 'fairy', 'star', 'wish'
        ]
        
        # Contenido base Disney que siempre se mantiene
        self.base_disney_content = {
            "chistes": [
                "¿Por qué Mickey Mouse se hizo astronauta? ¡Quería visitar Plutón!",
                "¿Cuál es el restaurante favorito de Peter Pan? ¡Wendy's!",
                "¿Por qué Cenicienta es mala jugando fútbol? ¡Siempre huye del balón!",
                "¿Cómo llamas a un hada que no se ha bañado? ¡Campanilla Apestosa!",
                "¿Por qué rechazaron la tarjeta de crédito de Elsa? ¡Su cuenta estaba congelada!"
            ],
            "frases": {
                "Mickey Mouse": ["¡Oh boy! ¡Hot dog!", "¡Nos vemos pronto!", "¡Gosh!", "¡Ja-ja!"],
                "Stitch": ["Ohana significa familia", "¡Aloha!", "¡Blue punch buggy!"],
                "Elsa": ["¡Let it go!", "El frío nunca me molestó", "El amor descongelará"],
                "Woody": ["¡Hay una serpiente en mi bota!", "¡Apunta al cielo!"],
                "Olaf": ["Algunas personas valen la pena derretirse", "¡Me encantan los abrazos cálidos!"]
            }
        }

    def fetch_jokes(self, count=3):
        """Obtiene chistes de APIs gratuitas"""
        new_jokes = []
        
        for _ in range(count):
            for api_url in self.joke_apis:
                try:
                    if "icanhazdadjoke.com" in api_url:
                        headers = {'Accept': 'application/json'}
                        response = requests.get(api_url, headers=headers, timeout=10)
                    else:
                        response = requests.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Procesar según el formato de cada API
                        if "official-joke-api" in api_url:
                            joke = f"{data['setup']} {data['punchline']}"
                        elif "jokeapi" in api_url:
                            joke = data.get('joke', '')
                        elif "icanhazdadjoke" in api_url:
                            joke = data.get('joke', '')
                        else:
                            continue
                        
                        # Filtrar por palabras clave Disney
                        if self.is_family_friendly(joke) and len(joke) < 200:
                            new_jokes.append(joke)
                            break
                            
                except Exception as e:
                    print(f"Error fetching joke from {api_url}: {e}")
                    continue
        
        return new_jokes

    def fetch_quotes(self, count=2):
        """Obtiene citas inspiracionales"""
        new_quotes = {}
        
        for _ in range(count):
            for api_url in self.quote_apis:
                try:
                    response = requests.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if "quotable" in api_url:
                            quote = data.get('content', '')
                            author = data.get('author', 'Unknown')
                        elif "zenquotes" in api_url and isinstance(data, list):
                            quote = data[0].get('q', '')
                            author = data[0].get('a', 'Unknown')
                        else:
                            continue
                        
                        # Filtrar contenido apropiado
                        if (self.is_family_friendly(quote) and 
                            len(quote) < 150 and 
                            author not in new_quotes):
                            
                            new_quotes[author] = [quote]
                            break
                            
                except Exception as e:
                    print(f"Error fetching quote from {api_url}: {e}")
                    continue
        
        return new_quotes

    def is_family_friendly(self, text):
        """Verifica que el contenido sea apropiado para familias"""
        text_lower = text.lower()
        
        # Lista de palabras/temas a evitar
        banned_words = [
            'death', 'kill', 'murder', 'suicide', 'violence', 'hate',
            'damn', 'hell', 'stupid', 'idiot', 'drunk', 'beer', 'wine',
            'sex', 'sexy', 'adult', 'mature', 'inappropriate'
        ]
        
        # Verificar que no contenga palabras prohibidas
        for word in banned_words:
            if word in text_lower:
                return False
        
        # Verificar longitud razonable
        if len(text) < 10 or len(text) > 300:
            return False
            
        return True

    def load_current_content(self):
        """Carga el contenido actual desde Dropbox"""
        dropbox_url = "https://www.dropbox.com/scl/fi/xluhn4osh3ng428ey3kbt/disney-content.json?rlkey=ddv9cix96srgw4gsnd6qffmq8&st=y8wrha1a&dl=1"
        
        try:
            response = requests.get(dropbox_url, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error loading from Dropbox: {e}")
        
        # Fallback al contenido base
        return self.base_disney_content.copy()

    def update_content(self):
        """Actualiza el contenido con nuevo material"""
        print(f"Iniciando actualización: {datetime.now()}")
        
        # Cargar contenido actual
        current_content = self.load_current_content()
        
        # Obtener nuevo contenido
        new_jokes = self.fetch_jokes(3)
        new_quotes = self.fetch_quotes(2)
        
        # Combinar contenido manteniendo base Disney
        updated_content = {
            "chistes": self.base_disney_content["chistes"].copy(),
            "frases": self.base_disney_content["frases"].copy()
        }
        
        # Añadir chistes existentes (máximo 20 total)
        existing_jokes = current_content.get("chistes", [])
        all_jokes = updated_content["chistes"] + existing_jokes + new_jokes
        
        # Eliminar duplicados y limitar cantidad
        unique_jokes = list(dict.fromkeys(all_jokes))[:20]
        updated_content["chistes"] = unique_jokes
        
        # Añadir frases existentes y nuevas
        existing_quotes = current_content.get("frases", {})
        for author, quotes in existing_quotes.items():
            if author in updated_content["frases"]:
                updated_content["frases"][author].extend(quotes)
            else:
                updated_content["frases"][author] = quotes
        
        # Añadir nuevas citas
        for author, quotes in new_quotes.items():
            if author in updated_content["frases"]:
                updated_content["frases"][author].extend(quotes)
            else:
                updated_content["frases"][author] = quotes
        
        # Limitar frases por autor (máximo 5)
        for author in updated_content["frases"]:
            updated_content["frases"][author] = list(dict.fromkeys(
                updated_content["frases"][author]
            ))[:5]
        
        # Añadir metadatos
        updated_content["ultima_actualizacion"] = datetime.now().isoformat()
        updated_content["version"] = current_content.get("version", 1) + 1
        
        print(f"Contenido actualizado:")
        print(f"- Total chistes: {len(updated_content['chistes'])}")
        print(f"- Total autores frases: {len(updated_content['frases'])}")
        print(f"- Nuevos chistes añadidos: {len(new_jokes)}")
        print(f"- Nuevos autores añadidos: {len(new_quotes)}")
        
        return updated_content

    def save_to_file(self, content, filename="disney-content.json"):
        """Guarda el contenido actualizado a un archivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"Archivo guardado: {filename}")
            return True
        except Exception as e:
            print(f"Error guardando archivo: {e}")
            return False

def main():
    """Función principal"""
    updater = DisneyContentUpdater()
    
    try:
        # Actualizar contenido
        updated_content = updater.update_content()
        
        # Guardar archivo
        if updater.save_to_file(updated_content):
            print("✅ Actualización completada exitosamente")
        else:
            print("❌ Error al guardar el archivo")
            
    except Exception as e:
        print(f"❌ Error en la actualización: {e}")

if __name__ == "__main__":
    main()
