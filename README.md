# 📚 FastAPI Courses API

Uma API desenvolvida com [FastAPI](https://fastapi.tiangolo.com/) para listar cursos, permitindo ordenação por data, avaliação e filtragem por domínio. Utiliza MongoDB como banco de dados.

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Uvicorn](https://www.uvicorn.org/) como servidor ASGI
- [Pymongo](https://pymongo.readthedocs.io/)

## 📂 Estrutura do Projeto

```bash
.
├── api/
│   ├── __init__.py
│   └── routes.py
├── app/
│   └── __init__.py (opcional se usado)
├── main.py
├── db.py
├── script.py
├── courses.json
├── venv/ (ignorado pelo Git)
└── requirements.txt
