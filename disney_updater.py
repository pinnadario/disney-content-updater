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
                "¿Por qué rechazaron la tarjeta de crédito de Elsa? ¡Su cuenta estaba congelada!",
                "¿Cuál es el ejercicio favorito de Winnie the Pooh? ¡Bear-óbicos!",
                "¿Por qué Alicia nunca gana al póker? ¡Siempre juega contra un Gato de Cheshire!",
                "¿Cuál es la tienda menos favorita del Capitán Garfio? ¡La de segunda mano!",
                "¿Por qué Woody le dio jarabe para la tos a Perdigón? ¡Porque estaba un poco ronco!",
                "¿Cómo llamas a Mickey Mouse cuando está disfrazado? ¡Mickey Moose!",
                "¿Por qué no puedes darle un globo a Elsa? ¡Porque lo dejará ir!",
                "¿Cuál es la canción navideña favorita de Tarzán? ¡Jungle Bells!",
                "¿Por qué Ariel tiró mantequilla de maní al océano? ¡Para ir con las medusas!",
                "¿Cuál es el tipo de música favorito de Goofy? ¡Hip Hop!",
                "¿Por qué no invitan a Dumbo a jugar cartas? ¡Porque siempre está haciendo trampas con las orejas!",
                "¿Qué dice Buzz Lightyear cuando va al baño? ¡Al inodoro y más allá!",
                "¿Por qué Rapunzel nunca tiene mal día de cabello? ¡Porque siempre tiene extensiones!",
                "¿Cuál es el postre favorito de Anna? ¡Sundae de verano!",
                "¿Por qué Simba no puede mentir? ¡Porque siempre se ve en su melena!",
                "¿Qué come Olaf en el desierto? ¡Un helado muy rápido!",
                "¿Por qué Pinocho no puede jugar al escondite? ¡Su nariz siempre lo delata!",
                "¿Cuál es el baile favorito de la Bestia? ¡El vals!",
                "¿Por qué Mufasa nunca usa despertador? ¡Porque es el rey de la sabana!",
                "¿Qué le dice un pez a Nemo? ¡Nada, no puede hablar!",
                "¿Por qué Hércules nunca pierde en el gimnasio? ¡Es un semidiós!",
                "¿Cuál es la película favorita de los Dalmatians? ¡101 Dálmatas!",
                "¿Por qué Aladdin nunca llega tarde? ¡Tiene una alfombra voladora!",
                "¿Qué hace Sulley cuando está triste? ¡Se pone azul!",
                "¿Por qué Anna siempre está feliz? ¡Porque tiene el corazón caliente!",
                "¿Cuál es el deporte favorito de Kristoff? ¡Hockey sobre hielo!"
            ],
            "frases": {
                "Mickey Mouse": ["¡Oh boy! ¡Hot dog!", "¡Nos vemos pronto!", "¡Gosh!", "¡Ja-ja!", "¡Qué día tan maravilloso!", "¡Es magia!"],
                "Minnie Mouse": ["¡Oh, Mickey!", "¡Qué dulce!", "¡Me encantas!", "¡Tú también eres especial!", "¡Qué aventura!", "¡Yupi!"],
                "Donald Duck": ["¡Wak wak wak!", "¡Qué desastre!", "¡Por mis plumas!", "¡No puede ser!", "¡Está bien, está bien!", "¡Sobrinos!"],
                "Goofy": ["¡A-ja!", "¡Gor-shh!", "¡Qué tonto soy!", "¡Vamos, Max!", "¡Uh-oh!", "¡Ah-yuk!"],
                "Stitch": ["Ohana significa familia", "¡Aloha!", "¡Blue punch buggy!", "¡Meega, nala kweesta!", "¡Badness level rising!", "¡Stitch es bueno!"],
                "Elsa": ["Let it go!", "El frío nunca me molestó", "El amor descongelará", "Hacia lo desconocido", "El pasado está en el pasado", "Soy libre"],
                "Anna": ["¿Quieres hacer un muñeco de nieve?", "El amor es una puerta abierta", "¡Elsa!", "Algunos nacieron para el verano", "¡Chocolate!", "¡Por primera vez en años!"],
                "Olaf": ["¡Me encantan los abrazos cálidos!", "Algunas personas valen la pena derretirse", "¡Hola, soy Olaf!", "Me gusta el verano", "¡Ooh, ooh, ooh!", "Los abrazos cálidos"],
                "Woody": ["¡Hay una serpiente en mi bota!", "¡Apunta al cielo!", "¡Eres mi ayudante favorito!", "¡Alguien ha envenenado el pozo!", "¡Este pueblo no es suficiente para ambos!", "¡Yee-haw!"],
                "Buzz Lightyear": ["¡Al infinito y más allá!", "Esto no es volar, es caer con estilo", "¡Comando Estelar!", "¡Soy Buzz Lightyear!", "Misión cumplida", "¡Star Command!"],
                "Dory": ["¡Sigue nadando!", "¡Le llamaré Squishy!", "¡P. Sherman, Calle Wallaby 42, Sidney!", "¡Hablo ballena!", "Tengo pérdida de memoria", "¡Qué bonito!"],
                "Nemo": ["¡Puedo hacerlo!", "¡Papá!", "¡Mi aleta de la suerte!", "¡Nadando, nadando!", "¡Wow!", "¡Qué genial!"],
                "Simba": ["¡Hakuna Matata!", "¿Qué es esa cosa brillante?", "¡No puedo esperar a ser rey!", "¡Rugido!", "El pasado duele", "¡Recuerda quién eres!"],
                "Timon": ["¡Hakuna Matata!", "¡Qué problema!", "¡Sin preocupaciones!", "¡Pumba!", "¡Es nuestro lema!", "¡Grubs!"],
                "Pumba": ["¡Hakuna Matata!", "¡Son las estrellas!", "¡Timon!", "Cuando era joven jabalí", "¡Sin preocupaciones!", "¡Qué vergüenza!"],
                "Belle": ["¡Qué extraño!", "Debe haber algo más", "¡Los libros!", "¡Bestia!", "No juzgues por las apariencias", "¡Aventura!"],
                "Bestia": ["¡Belle!", "¿Podrías ser feliz aquí?", "Soy un monstruo", "¡Por favor!", "Te doy mi palabra", "¡Gruñido!"],
                "Aladdin": ["¡Un diamante en bruto!", "¿Confías en mí?", "¡Jasmine!", "¡Genio!", "¡Abu!", "¡Carpet!"],
                "Jasmine": ["¡No soy un premio!", "¡Quiero ver el mundo!", "¡Aladdin!", "¡Rajah!", "Quiero decidir por mí", "¡Un mundo ideal!"],
                "Genio": ["¡10.000 años te dan tortícolis!", "¡Wish granted!", "¡Ixnay!", "¡Poof!", "¡Tres deseos!", "¡Eres libre!"],
                "Moana": ["El océano me eligió", "¡Maui!", "¡Abuela Tala!", "Sé quién soy", "¡Navegaré!", "El corazón de Te Fiti"],
                "Maui": ["¡De nada!", "Eres bienvenida", "¡Soy Maui!", "¡Qué puedo decir excepto!", "¡Mi anzuelo!", "¡Mini Maui!"],
                "Rapunzel": ["¡Por fin veo la luz!", "¡Madre Gothel!", "¡Flynn!", "¡Pascal!", "¡Maximus!", "Mi cabello brilla"],
                "Flynn Rider": ["¡Smoulder!", "¿Has visto esto?", "¡Blondie!", "¡Rapunzel!", "Mi nombre real es Eugene", "¡Frying pan!"]
            },
            "datos_curiosos": [
                "El Castillo de la Bella Durmiente en Disneyland París mide 167 pies de altura, siendo el más alto de Europa.",
                "El parque cubre 140 acres y recibió más de 15 millones de visitantes en 2019.",
                "Space Mountain: Mission 2 alcanza velocidades de 44 mph y es el único Space Mountain con inversiones.",
                "Piratas del Caribe en Disneyland París tiene escenas únicas donde los barcos van cuesta arriba.",
                "Main Street U.S.A. tiene techos de cristal para proteger a los visitantes del clima parisino.",
                "Phantom Manor tiene una historia completamente diferente a otras atracciones de Haunted Mansion.",
                "Big Thunder Mountain está ubicado en una isla en el medio de los Ríos del Lejano Oeste.",
                "El dragón bajo el castillo es la figura Audio-Animatrónica más grande de cualquier parque Disney."
            ],
            "cuentos_clasicos": [
                {
                    "titulo": "Cenicienta",
                    "resumen": "Una joven bondadosa, con la ayuda de su Hada Madrina, supera la crueldad de su madrastra para asistir al baile real. Cuando huye a medianoche dejando solo un zapato de cristal, el Príncipe busca por todo el reino hasta encontrarla. El amor verdadero triunfa cuando el zapato encaja perfectamente.",
                    "moral": "La bondad y la perseverancia siempre son recompensadas. La verdadera belleza viene del interior, y los sueños pueden hacerse realidad cuando mantenemos la esperanza."
                },
                {
                    "titulo": "Blancanieves y los Siete Enanitos",
                    "resumen": "Una princesa huye de su madrastra celosa y encuentra refugio con siete enanitos en el bosque. La Reina Malvada, disfrazada de anciana, engaña a Blancanieves para que coma una manzana envenenada. Los enanitos la protegen hasta que el beso de amor verdadero de un príncipe rompe el hechizo.",
                    "moral": "El bien siempre triunfa sobre el mal. La verdadera amistad proporciona fuerza en tiempos difíciles, y el amor tiene el poder de superar cualquier maldición."
                },
                {
                    "titulo": "La Bella y la Bestia",
                    "resumen": "Bella se sacrifica para salvar a su padre y queda prisionera de Bestia en un castillo encantado. A través de la paciencia y la comprensión, ve más allá de las apariencias y descubre que Bestia es en realidad un príncipe maldito. Su amor verdadero rompe la maldición.",
                    "moral": "No juzgues por las apariencias. El amor verdadero ve la belleza interior, y la compasión puede transformar incluso los corazones más duros."
                },
                {
                    "titulo": "Pinocho",
                    "resumen": "Geppetto crea una marioneta de madera que cobra vida gracias al Hada Azul. Pinocho debe demostrar que es valiente, sincero y generoso para convertirse en un niño de verdad. Con la ayuda de Pepito Grillo como su conciencia, aprende importantes lecciones sobre la honestidad.",
                    "moral": "La honestidad y la valentía son las cualidades que nos hacen verdaderamente humanos. Siempre debemos escuchar a nuestra conciencia."
                },
                {
                    "titulo": "Bambi",
                    "resumen": "Un joven cervatillo aprende a vivir en el bosque con la ayuda de su madre y sus amigos Tambor el conejo y Flor el zorrillo. Cuando su madre muere, Bambi debe superar su dolor y convertirse en el nuevo príncipe del bosque, protegiendo a su familia y amigos.",
                    "moral": "Crecer significa enfrentar las dificultades con valentía. La verdadera fortaleza viene de proteger y cuidar a quienes amamos."
                }
            ],
            "cuentos_familiares": [
                {
                    "titulo": "Mickey y la Estrella de los Deseos",
                    "historia": "Mickey Mouse descubre que la estrella de los deseos de Disneyland París ha perdido su brillo. Junto con Minnie, Donald, Goofy y Pluto, debe ayudar a los visitantes del parque a cumplir pequeños actos de bondad para restaurar la magia de la estrella. Cada buena acción hace que la estrella brille más intensamente hasta iluminar todo el parque.",
                    "moral": "Los pequeños actos de bondad pueden crear la magia más grande de todas."
                },
                {
                    "titulo": "Stitch y el Jardín de la Ohana",
                    "historia": "Stitch encuentra un jardín abandonado en Disneyland París donde las flores representan diferentes familias. Con la ayuda de Lilo, Angel y Jumba, trabaja para restaurar el jardín ayudando a las familias visitantes a reconectarse y pasar tiempo juntas. Cada familia reunida hace florecer una nueva planta en el jardín.",
                    "moral": "Ohana significa familia, y la familia significa que nadie se queda atrás ni es olvidado."
                },
                {
                    "titulo": "Elsa y el Palacio de Hielo Mágico",
                    "historia": "Durante una visita especial a Disneyland París, Elsa crea un palacio de hielo mágico donde los niños tímidos pueden ganar confianza. Con Anna a su lado, enseña a los visitantes que está bien ser diferente y que nuestras diferencias nos hacen especiales. El palacio se vuelve más hermoso con cada niño que encuentra su confianza.",
                    "moral": "Debemos abrazar lo que nos hace únicos. La verdadera magia está en ser auténticos con nosotros mismos."
                },
                {
                    "titulo": "Woody y la Misión de Rescate",
                    "historia": "Woody descubre que varios juguetes se han perdido en Disneyland París. Junto con Buzz Lightyear, Jessie y los demás juguetes de Toy Story, organiza una misión de rescate para reunir a cada juguete perdido con su dueño. Aprenden que el verdadero valor de un juguete está en la alegría que trae a un niño.",
                    "moral": "Nuestro propósito más importante es hacer felices a otros. El verdadero heroísmo está en ayudar sin esperar nada a cambio."
                },
                {
                    "titulo": "Moana y la Brújula del Corazón",
                    "historia": "Moana llega a Disneyland París siguiendo una brújula mágica que guía a las personas hacia su verdadero propósito. Junto con Maui, ayuda a los visitantes del parque a descubrir sus propios sueños y talentos especiales. La brújula brilla más fuerte cuando alguien encuentra el coraje para seguir su corazón.",
                    "moral": "Debemos tener el coraje de seguir nuestros sueños. El océano de posibilidades está esperando a quienes se atreven a navegar."
                }
            ]
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

    def fetch_disney_facts(self, count=2):
        """Busca datos curiosos relacionados con Disney de APIs gratuitas"""
        new_facts = []
        
        # APIs que podrían contener información relacionada con Disney
        fact_apis = [
            "https://api.api-ninjas.com/v1/facts?limit=10",
            "https://uselessfacts.jsph.pl/random.json?language=en"
        ]
        
        for api_url in fact_apis:
            try:
                if "api-ninjas" in api_url:
                    # Esta API requiere header específico pero intentaremos sin clave
                    continue
                    
                response = requests.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "uselessfacts" in api_url:
                        fact = data.get('text', '')
                    else:
                        continue
                    
                    # Filtrar por relevancia con Disney
                    disney_keywords = ['mouse', 'cartoon', 'animation', 'movie', 'film', 'park', 'theme', 'entertainment']
                    
                    if (self.is_family_friendly(fact) and 
                        any(keyword in fact.lower() for keyword in disney_keywords) and
                        len(fact) < 200):
                        new_facts.append(fact)
                        if len(new_facts) >= count:
                            break
                            
            except Exception as e:
                print(f"Error fetching facts from {api_url}: {e}")
                continue
        
    def generate_new_story_if_needed(self, current_content):
        """Genera una nueva historia solo si hay menos de 30 cuentos totales"""
        total_stories = 0
        
        # Contar cuentos existentes
        if "cuentos_clasicos" in current_content:
            total_stories += len(current_content["cuentos_clasicos"])
        if "cuentos_familiares" in current_content:
            total_stories += len(current_content["cuentos_familiares"])
            
        print(f"Total de cuentos existentes: {total_stories}")
        
        if total_stories >= 30:
            print("Límite de 30 cuentos alcanzado. No se generarán más historias.")
            return None
            
        # Generar nueva historia usando prompts predefinidos
        story_prompts = [
            {
                "titulo": "La Aventura de los Cristales Perdidos",
                "historia": "En Disneyland París, una familia mágica descubre que los cristales que dan poder a las atracciones han desaparecido. Cada miembro debe usar sus habilidades especiales para encontrar los cristales escondidos por todo el parque. Trabajando juntos, descubren que la verdadera magia no está en los cristales, sino en la unión familiar y la ayuda mutua.",
                "moral": "La verdadera magia viene del trabajo en equipo y del amor familiar."
            },
            {
                "titulo": "El Festival de las Estrellas",
                "historia": "Durante el festival anual de Disneyland París, las estrellas del cielo comienzan a desaparecer una por una. Una joven familia debe resolver el misterio antes de que la última estrella se desvanezca para siempre. A través de actos de bondad y generosidad hacia otros visitantes del parque, logran restaurar la luz de las estrellas.",
                "moral": "Los pequeños actos de bondad pueden iluminar el mundo entero."
            },
            {
                "titulo": "El Jardín de los Deseos Olvidados",
                "historia": "Detrás del Castillo de la Bella Durmiente existe un jardín secreto donde crecen los deseos olvidados de las personas. Una familia aventurera lo descubre y decide ayudar a que estos deseos encuentren a sus dueños originales, aprendiendo que cumplir los sueños de otros trae la mayor felicidad.",
                "moral": "Ayudar a otros a cumplir sus sueños multiplica nuestra propia alegría."
            }
        ]
        
        # Seleccionar historia aleatoria
        import random
        new_story = random.choice(story_prompts)
        print(f"Nueva historia generada: {new_story['titulo']}")
        
        return new_story
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
        
        # Obtener nuevo contenido (más cantidad para la rotación)
        new_jokes = self.fetch_jokes(8)  # 8 chistes nuevos cada 2 horas
        new_quotes = self.fetch_quotes(5)  # 5 autores nuevos cada 2 horas
        new_facts = self.fetch_disney_facts(3)  # 3 datos nuevos cada 2 horas
        
        # Combinar contenido manteniendo base Disney
        updated_content = {
            "chistes": self.base_disney_content["chistes"].copy(),
            "frases": self.base_disney_content["frases"].copy(),
            "datos_curiosos": self.base_disney_content["datos_curiosos"].copy(),
            "cuentos_clasicos": self.base_disney_content["cuentos_clasicos"].copy(),
            "cuentos_familiares": self.base_disney_content["cuentos_familiares"].copy()
        }
        
        # Rotar chistes: mantener primeros 22, reemplazar últimos 8
        if new_jokes:
            updated_content["chistes"] = (
                updated_content["chistes"][:22] +  # 22 chistes base fijos
                new_jokes[:8]  # 8 chistes nuevos rotativos
            )
        
        # Añadir frases nuevas manteniendo las Disney base
        existing_quotes = current_content.get("frases", {})
        
        # Mantener siempre las frases Disney base
        final_phrases = updated_content["frases"].copy()
        
        # Añadir frases existentes (no Disney base)
        for author, quotes in existing_quotes.items():
            if author not in final_phrases:  # Solo añadir autores nuevos
                final_phrases[author] = quotes[:3]  # Máximo 3 frases por autor
        
        # Añadir nuevas frases rotativas
        for author, quotes in new_quotes.items():
            final_phrases[author] = quotes[:3]  # Máximo 3 frases por autor
        
        # Limitar total de autores (Disney base + 10 rotativos máximo)
        disney_authors = len(updated_content["frases"])
        if len(final_phrases) > disney_authors + 10:
            # Mantener Disney base + 10 autores rotativos más recientes
            non_disney = {k: v for k, v in final_phrases.items() if k not in updated_content["frases"]}
            recent_authors = dict(list(non_disney.items())[-10:])  # Últimos 10
            final_phrases = {**updated_content["frases"], **recent_authors}
        
        updated_content["frases"] = final_phrases
        
        # Añadir datos curiosos (máximo 15 total)
        existing_facts = current_content.get("datos_curiosos", [])
        all_facts = updated_content["datos_curiosos"] + existing_facts + new_facts
        unique_facts = list(dict.fromkeys(all_facts))[:15]
        updated_content["datos_curiosos"] = unique_facts
        
        # Mantener cuentos existentes si los hay
        if "cuentos_clasicos" in current_content:
            updated_content["cuentos_clasicos"] = current_content["cuentos_clasicos"]
        if "cuentos_familiares" in current_content:
            updated_content["cuentos_familiares"] = current_content["cuentos_familiares"]
        
        # Generar nueva historia si es necesario
        new_story = self.generate_new_story_if_needed(current_content)
        if new_story:
            # Decidir si añadir a clásicos o familiares (aleatorio)
            import random
            if random.choice([True, False]):
                updated_content["cuentos_familiares"].append(new_story)
            else:
                # Convertir formato para cuentos clásicos
                classic_story = {
                    "titulo": new_story["titulo"],
                    "resumen": new_story["historia"][:200] + "...",
                    "moral": new_story["moral"]
                }
                updated_content["cuentos_clasicos"].append(classic_story)
        
        # Añadir metadatos
        updated_content["ultima_actualizacion"] = datetime.now().isoformat()
        updated_content["version"] = current_content.get("version", 1) + 1
        updated_content["total_cuentos"] = len(updated_content["cuentos_clasicos"]) + len(updated_content["cuentos_familiares"])
        
        print(f"Contenido actualizado:")
        print(f"- Total chistes: {len(updated_content['chistes'])}")
        print(f"- Total autores frases: {len(updated_content['frases'])}")
        print(f"- Total datos curiosos: {len(updated_content['datos_curiosos'])}")
        print(f"- Total cuentos: {updated_content['total_cuentos']}")
        print(f"- Nuevos chistes añadidos: {len(new_jokes)}")
        print(f"- Nuevos autores añadidos: {len(new_quotes)}")
        print(f"- Nuevos datos curiosos añadidos: {len(new_facts)}")
        if new_story:
            print(f"- Nueva historia añadida: {new_story['titulo']}")
        
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
