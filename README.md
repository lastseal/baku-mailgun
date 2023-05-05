# Baku Mailgun
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Instalación

```bash
pip install git+https://github.com/lastseal/baku-mailgun
```

## Uso Básico

```python
from baku import mailgun

res = mailgun.send({
  "subject": "Título del correo",
  "from": "origin@origin.com",
  "to": "correo_1@correo.com,correo_2@correo.com,correo_3@correo.com",
  "text": "Contenido en texto plano"
})
```
