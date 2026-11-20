# TP 3 : Service Web REST Calculatrice avec Jakarta EE (JAX-RS)

**Matière :** Architecture SOA et services web  
**Filière :** Licence en Sciences de l'Informatique (LSI3) — FSS  
**Année Universitaire :** 2025–2026  
**Étudiant :** Salmen Zekri  
**Enseignantes Responsables :** Corinne Amel ZAYANI, Hela HAKIM, Rim MOHAMED  

---

## 1. Présentation du Projet

Ce projet implémente un **service web RESTful (JAX-RS)** sous Jakarta EE 10 et géré par Apache Maven.  
Il expose une API de calcul arithmétique fournissant les quatre opérations fondamentales avec des réponses formattées en JSON :
* **Addition** : `GET /api/calculatrice/addition?a={val}&b={val}`
* **Soustraction** : `GET /api/calculatrice/soustraction?a={val}&b={val}`
* **Multiplication** : `GET /api/calculatrice/multiplication?a={val}&b={val}`
* **Division** : `GET /api/calculatrice/division?a={val}&b={val}` (avec contrôle d'erreur HTTP 400 Bad Request en cas de division par zéro)

---

## 2. Structure du Projet

```text
tp3/
├── pom.xml                                   (Descripteur Maven et configuration WAR)
├── CalculatriceREST.war                      (Livrable binaire prêt pour déploiement Tomcat)
├── TP3_REST_Calculatrice_RAPPORT.pdf         (Rapport PDF académique complet)
├── README.md                                 (Documentation technique du projet)
├── assets/                                   (Schémas d'architecture et captures Postman)
│   ├── diagram_rest_architecture.png
│   ├── postman_addition.png
│   ├── postman_soustraction.png
│   ├── postman_multiplication.png
│   └── postman_division.png
└── src/
    └── main/
        ├── java/
        │   ├── service/
        │   │   └── Calculatrice.java         (Logique métier pure)
        │   ├── model/
        │   │   └── Operation.java            (Modèle de données sérialisé en JSON)
        │   ├── rest/
        │   │   ├── CalculRest.java           (Ressource REST annotée JAX-RS)
        │   │   └── RestApplication.java      (Configuration Jersey & ApplicationPath)
        │   └── serveur/
        │       └── ServeurREST.java          (Serveur autonome intégré Grizzly)
        └── webapp/
            └── WEB-INF/
                └── web.xml                   (Configuration Servlet 5.0 pour Tomcat 10+)
```

---

## 3. Schéma de l'Architecture REST

Le traitement d'une requête s'effectue selon la chaîne standardisée :

```text
[ Client HTTP / Postman ]
       │  (Requête HTTP GET paramétrée)
       ▼
[ Serveur Apache Tomcat 10+ ]  (Port 8080 - Contexte /CalculatriceREST)
       │  (Filtrage et routage /api/*)
       ▼
[ Servlet Jersey JAX-RS ]      (ServletContainer / RestApplication)
       │  (Injection @QueryParam a, b)
       ▼
[ Ressource REST : CalculRest ] (@Path("/calculatrice"), @GET, @Produces)
       │  (Appel méthode arithmétique)
       ▼
[ Classe Métier : Calculatrice ]
       │  (Encapsulation résultat)
       ▼
[ Modèle JSON : Operation ]    (Sérialisation Jackson application/json)
       │  (Réponse HTTP 200 OK ou 400 Bad Request)
       ▼
[ Client HTTP / Postman ]
```

---

## 4. Spécification des Endpoints

| Opération | Verbe | URI Relative | Paramètres | Statut HTTP | Format Réponse |
| :--- | :---: | :--- | :--- | :---: | :---: |
| **Addition** | `GET` | `/api/calculatrice/addition` | `a`, `b` (décimaux) | `200 OK` | `application/json` |
| **Soustraction** | `GET` | `/api/calculatrice/soustraction` | `a`, `b` (décimaux) | `200 OK` | `application/json` |
| **Multiplication**| `GET` | `/api/calculatrice/multiplication`| `a`, `b` (décimaux) | `200 OK` | `application/json` |
| **Division** | `GET` | `/api/calculatrice/division` | `a`, `b` (décimaux) | `200 OK` | `application/json` |
| **Division par 0**| `GET` | `/api/calculatrice/division` | `a`, `b = 0` | `400 Bad Request` | `application/json` |

### Exemple de Réponse JSON (`Operation`)
```json
{
    "a": 15.5,
    "b": 4.5,
    "operation": "addition",
    "resultat": 20.0,
    "statut": "SUCCESS"
}
```

---

## 5. Guide de Compilation et Exécution

### 5.1 Prérequis
* JDK 11 ou supérieur (JDK 25 supporté)
* Apache Maven 3.9+
* Apache Tomcat 10+ (pour le déploiement WAR) ou Postman

### 5.2 Génération du fichier `.war`
```bash
mvn clean package
```
Le fichier binaire `CalculatriceREST.war` est automatiquement généré à la racine et sous `target/`.

### 5.3 Déploiement sous Apache Tomcat
1. Copier le fichier `CalculatriceREST.war` dans le répertoire `webapps/` de votre installation Tomcat.
2. Démarrer Tomcat via `bin/startup.bat` (Windows) ou `bin/startup.sh` (Linux/Mac).
3. L'API est instantanément accessible à l'adresse :
   ```text
   http://localhost:8080/CalculatriceREST/api/calculatrice/addition?a=10&b=5
   ```

### 5.4 Exécution Autonome (Serveur Intégré Grizzly)
Pour exécuter et tester directement sans installer Tomcat :
```bash
mvn exec:java
```

---

## 6. Livrables du TP

1. **Dépôt GitHub complet :** [https://github.com/zikosalmen/SOA-tp3.git](https://github.com/zikosalmen/SOA-tp3.git)
2. **Fichier WAR binaire :** `CalculatriceREST.war`
3. **Rapport PDF officiel :** `TP3_REST_Calculatrice_RAPPORT.pdf` (contenant l'environnement technique, le schéma d'architecture, la description de l'API et les captures d'écran Postman)
