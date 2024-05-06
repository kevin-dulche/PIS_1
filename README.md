# Proyecto de Ingeniería de Software 1
Repositorio del proyecto

## Requisitos
Para ejecutar el programa se necesita:
* Tener **python** instalado
* Base de datos **MySQL** con usuario y contraseña: **root**
* Una base de datos con nombre **appflask**
* Dentro de la base de datos una tabla con nombre: **login**
* La tabla **login** contiene cuatro variables: id, username, password, role

La tabla de pruebas fue la siguiente:

| id | username       | password   | role         |
|----|----------------|------------|--------------|
| 1  | KevinDulche    | Hola12345  | Administrador|
| 2  | Carla Martinez | Carla12345 | Cajero       |
| 3  | Monica Perez   | Monica12345| Cliente      |


## Ejecución
Prologo: Hacer el git clone del repositorio

En la terminal ejecutar los sisguintes comandos (**version windows**):

```
python -m venv app
.\app\Scripts\activate
pip install -r requirements.txt
python -u .\app.py
```