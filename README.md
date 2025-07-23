# Gestion des factures

## Mettre en place le projet

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install django
```

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```
L'application est disponible à l'adresse http://localhost:8000/factures/

### Pour l'administrateur

```bash
python manage.py createsuperuser
```

Et se rendre sur http://localhost:8000/admin/ pour se connecter avec les identifiants créés.