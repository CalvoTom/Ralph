import pymysql

# Configuration de la base de données
DB_HOST = '192.168.159.132'
DB_USER = 'app'
DB_PASSWORD = '1806'
DB_NAME = 'ralphbdd'

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
    conn = connect()
    cursor = conn.cursor()

    try:
        # Séparer les mots clés de la recherche de l'utilisateur
        keywords = user_input.split()

        # Initialiser un dictionnaire pour stocker le score de chaque page
        page_scores = {}

        # Récupérer les données de chaque page
        cursor.execute("SELECT id, body FROM PAGES")
        pages = cursor.fetchall()

        # Calculer le score de chaque page en fonction de la fréquence des mots clés
        for page_id, body in pages:
            score = 0
            for keyword in keywords:
                score += body.lower().count(keyword.lower())
            page_scores[page_id] = score

        return page_scores

    except Exception as e:
        print("Erreur lors du calcul des scores des pages :", e)
        return {}

    finally:
        cursor.close()
        conn.close()

def rank_pages(page_scores):
    conn = connect()
    cursor = conn.cursor()

    try:
        # Récupérer les données de chaque page
        cursor.execute("SELECT url, title, body FROM PAGES")
        pages = cursor.fetchall()

        ranked_pages = []

        # Pour chaque page, calculer le score et l'ajouter à la liste
        for url, title, body in pages:
            total_words = len(body.split())
            if total_words > 0 and url in page_scores:
                query_count = page_scores[url]
                # Calculer le score basé sur le ratio
                score = total_words / query_count
                ranked_pages.append((url, title, score))
                print(rank_pages, "fef")

        # Trier les pages par score en ordre décroissant
        ranked_pages.sort(key=lambda x: x[2], reverse=True)

        return ranked_pages

    except Exception as e:
        print("Erreur lors du classement des pages :", e)
        return []

    finally:
        cursor.close()
        conn.close()
