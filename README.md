Script para Ejecutar el Termino de solicitudes de manera Manual que tuvieron algun problema
en carga de documentos.

Para ejecutar este script solo es necesario crear un ambiente virtual en python:

** Comandos
==========================================
* python3 -m venv .venv_forzado_man  
* source .venv_forzado_man/bin/activate
* pip install --upgrade pip
* pip install -r  requeriments.pip

** Ejecución
============================================
* Reemplazar APISOL_INTERNO
* Reemplazar APISOL_ORQUESTADOR

python3 main.py
