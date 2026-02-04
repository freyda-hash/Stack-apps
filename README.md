## Stack-apps — Déploiement d'une stack avec Docker Compose

Ce dépôt contient la documentation pour déployer une stack complète :

- Client → Nginx (reverse-proxy) → App Python (FastAPI) → PostgreSQL

L'objectif : fournir des recommandations et exemples pour une mise en place sécurisée, une bonne gestion des dépendances, séparation `dev`/`prod`, logs & observabilité, et volumes persistants.

**Architecture**

Client
	↓
Nginx (reverse-proxy, TLS)
	↓
FastAPI (uvicorn)
	↓
PostgreSQL (volume persistant)

**Prérequis**

- `docker` >= 24.x, `docker-compose` (ou Docker CLI compose)
- `uv` (recommandé) ou `pip` pour les dépendances Python
- Accès pour créer volumes et exposer ports

**Principes retenus**

- Sécurité : TLS géré par Nginx, variables d'environnement/screts, utilisateurs non-root dans les conteneurs.
- Dépendances : lockfile (`poetry.lock` ou `requirements.txt`) et image build reproducible.
- Séparation dev/prod : `docker-compose.yml` ou fichiers distincts `docker-compose.dev.yml` / `docker-compose.prod.yml`.
- Logs & observabilité : logs structurés (JSON), métriques exposées (`/metrics`), recommandation Prometheus + Grafana.
- Volumes persistants : PostgreSQL data, certificats TLS, uploads/app-state.

**Quickstart — Développement**

1. Créez un `.env` local (ne pas committer) :

```
POSTGRES_PASSWORD=changeme
POSTGRES_USER=appuser
POSTGRES_DB=appdb
APP_ENV=development
DEBUG=1
```

2. Lancer en dev (montage de code en volume, rebuild si nécessaire) :

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

3. Accéder : `http://localhost` (Nginx reverse-proxy redirige vers l'app)

Remarques dev : monter le code dans le container FastAPI pour rechargement à chaud ; utiliser une image PostgreSQL officielle et un volume local pour les données.

**Quickstart — Production (exemple simplifié)**

1. Préparer un `.env.prod` sécurisé et/ou utiliser `docker secrets` / un gestionnaire de secrets.
2. Construire et lancer :

```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Production : activer TLS (Let's Encrypt / certs), mettre `DEBUG=0`, limiter accès aux ports (proxy public seul), configurer rotation logs et monitoring.

**Gestion des dépendances Python**

- Recommandé : `uv` pour isoler et pinner versions (`pyproject.toml`, `uv.lock`).
- Alternative : `pip` avec `requirements.txt` généré via `pip freeze` ou `pip-tools` (`requirements.in` → `requirements.txt`).
- Construire l'image via `Dockerfile` en multi-stage : installer dépendances à partir du lockfile, exécuter tests, puis copier artefacts dans l'image finale légère.


Sécurité : n'exécutez pas `root` dans l'image finale ; utilisez un utilisateur non-root.

**Séparation dev / prod (compose)**

- `docker-compose.yml` : services communs (nginx, app, db)
- `docker-compose.dev.yml` : montages volumes pour code, variables dev, image local non minifiée
- `docker-compose.prod.yml` : configuration prod, TLS, limites ressources, logging driver et secrets

Exemple d'approche :

```
# Lancer dev
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
# Lancer prod
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

**Nginx (reverse-proxy) — points clés**

- Terminer TLS dans Nginx en prod. Stocker certificats dans un volume monté (ordonné et sauvegardé).
- Configurer `proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr;` et timeouts raisonnables.
- Ne pas exposer directement le port de l'app FastAPI au public ; Nginx est le point d'entrée.

Snippet nginx (server block) :

```
server {
	listen 443 ssl;
	server_name example.com;
	ssl_certificate /etc/nginx/certs/fullchain.pem;
	ssl_certificate_key /etc/nginx/certs/privkey.pem;

	location / {
		proxy_pass http://app:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
}
```

**FastAPI — observabilité & logs**

- Exposer `/metrics` via `prometheus_client` pour métriques.
- Logger en JSON structuré (ex : `python-json-logger`) pour faciliter l'ingestion par la stack de logs.
- Ne pas logguer d'informations sensibles (passwords, tokens).


**PostgreSQL — volumes & sauvegarde**

- Montez les données dans un volume Docker nommé (`pgdata`) :


- Sauvegardes : planifier `pg_dump` réguliers vers un stockage externe ou snapshot du volume.

**Logs & observabilité (recommandations)**

- Logs : utiliser un driver de logs compatible (ex : `json-file` avec rotation) ou envoyer vers Fluentd/ELK.
- Metrics : Prometheus scrape l'exporter fourni par l'app, Grafana pour dashboards.
- Traces : envisager OpenTelemetry pour traces distribuées.


Sécurité prod : utiliser `docker secrets` pour mots de passe ou intégrer un vault (HashiCorp Vault, Azure Key Vault, etc.).

**Bonnes pratiques complémentaires**

- Tests : intégrer linting et tests dans le pipeline CI avant build.
- Immutabilité : produire des images immuables en CI, déployer les images par tags (SHA) en prod.
- Monitoring : alertes sur disponibilité DB, latence des endpoints, erreurs 5xx.

---

