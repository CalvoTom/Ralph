import pymysql

# Configuration de la base de données
DB_HOST = '192.168.159.132'
DB_USER = 'app'
DB_PASSWORD = '1806'
DB_NAME = 'raplhbdd'

# Seuil pour le score
THRESHOLD = 10

# Fonction pour se connecter à la base de données
def connect():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Fonction pour ajouter une page
def add_page(url, name, title, body):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO PAGES (url, name, title, body) VALUES (%s, %s, %s, %s)",
                       (url, name, title, body))
        conn.commit()
        print("Page ajoutée avec succès")
    except Exception as e:
        conn.rollback()
        print("Erreur lors de l'ajout de la page :", e)
    finally:
        cursor.close()
        conn.close()

def get_word_frequencies(user_input):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    try:
        # Séparer les mots clés de la recherche de l'utilisateur
        keywords = user_input.split()

        # Initialiser un dictionnaire pour stocker la fréquence de chaque mot clé
        word_freqs = {keyword: 0 for keyword in keywords}

        # Récupérer le contenu de chaque page
        cursor.execute("SELECT id, body FROM PAGES")
        pages = cursor.fetchall()

        # Calculer la fréquence de chaque mot clé dans le corps de chaque page
        for page_id, body in pages:
            for keyword in keywords:
                word_freqs[keyword] += body.lower().count(keyword.lower())

        return word_freqs

    except Exception as e:
        print("Erreur lors du calcul de la fréquence des mots clés :", e)
        return {}

    finally:
        cursor.close()
        conn.close()

def rank_pages(word_freqs):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    try:
        # Récupérer les données de chaque page
        cursor.execute("SELECT id, url, title, body FROM PAGES")
        pages = cursor.fetchall()

        # Calculer le score de chaque page en fonction de la fréquence des mots clés
        scored_pages = []
        for page_id, url, title, body in pages:
            score = sum(word_freqs.values())
            scored_pages.append({'id': page_id, 'url': url, 'title': title, 'score': score})

        # Trier les pages par score en ordre décroissant
        scored_pages.sort(key=lambda x: x['score'], reverse=True)

        # Filtrer les pages avec un score inférieur au seuil
        scored_pages = [page for page in scored_pages if page['score'] >= THRESHOLD]

        return scored_pages

    except Exception as e:
        print("Erreur lors du classement des pages :", e)
        return []

    finally:
        cursor.close()
        conn.close()
