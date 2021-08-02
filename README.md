# TPE BD2 2021-C1 - Grupo LNT

La idea del proyecto es realizar un benchmarking de datos geospaciales entre Postgres (con la extensión Postgis) y MongoDB. Para tales fines a partir de una cierta cantidad de datasets, se realizan una serie de queries a los mismos para comparar métricas de tiempo, performance y uso de memoria.


### Autores ✒️

* Tamara Puig - [tpuig99](https://github.com/tpuig99)
* Nicolás Comerci Wolcanyk - [ncomerci](https://github.com/ncomerci)
* Luciano Boccardi - [lboccardi](https://github.com/lboccardi)

### Presentación 📽

Puede ser accedida por alumnos del ITBA mediante el siguiente [enlace](https://docs.google.com/presentation/d/16bRfHhluFx2t9RGbmv_uxvw418ekgIcfpyejVEc99zM/edit?usp=sharing). 

## Queries a Ejecutar ⚡

### 1) Restaurants en cierto radio dado un cliente
Dada la ubicación de un cliente y un radio, se listan los restaurantes que están dentro de ese radio.

### 2) Restaurant competidor más cercano
Dada la ubicación de un restaurant, se muestra cual es el restaurant de una franquicia competidora más cercano a él.

### 3) Restaurants de un estado
Dado un polígono que representa a un estado, Se muestran todos los restaurants junto con su dirección que están dentro de él.

### 4) Cantidad de locales de franquicias en un estado
Dado un polígono que representa a un estado, se listan todas las franquicias con su cantidad de locales que están dentro de él.

### 5) Condado al que pertenece un restaurant
Dada la ubicación de un restaurant, se muestra el condado al que pertenece el mismo.

### 6) Cantidad de franquicias dado un condado
Dado un polígono que representa a un condado, se muestra la cantidad de franquicias distintas que hay en él.


## Ejecutando el programa 💻
Para ejecutar el script se debe correr:
```
  python3 ./main.py <iteraciones> <threads> <decimales>
```
Donde *iteraciones* es la cantidad de veces que se repetiran todas las queries, *threads* es la cantidad de threads que se desea correr en simultaneo y *decimales* corresponde a la cantidad de decimales con los que se mostrará la respuesta.

Ejemplo:
```
  python3 ./main.py 2 1 5
```

## Resultados 🪐
El programa imprime a consola los siguientes datos:
* Los distintos identificadores de los threads lanzados.
* La cantidad de iteraciones de cada thread con su tiempo total.
* Por cada una de las querys, el tiempo total de ejecución y el promedio respecto de las iteraciones, tanto para mongo como para postgres.

El siguiente es un ejemplo habiendo ejecutado: `python3 ./main.py 2 1 5`

```
Process ID: 151
151 - Iterations: 2 - Total time: 10.97094 


Find County by a restaurant :
        Mongo:
                total: 7e-05
                average: 3e-05
        Postgres:
                total: 0.38113
                average: 0.19056
Find nearest competitor from a restaurant :
        Mongo:
                total: 0.45505
                average: 0.22753
        Postgres:
                total: 0.41007
                average: 0.20504
Find Restaurant by costumer :
        Mongo:
                total: 0.35914
                average: 0.17957
        Postgres:
                total: 0.42866
                average: 0.21433
Find restaurant per franchise in State :
        Mongo:
                total: 0.38598
                average: 0.19299
        Postgres:
                total: 0.36056
                average: 0.18028
Find all the restaurants in a State :
        Mongo:
                total: 0.37982
                average: 0.18991
        Postgres:
                total: 0.35718
                average: 0.17859
Find count of distinct franchises on State :
        Mongo:
                total: 0.61681
                average: 0.3084
        Postgres:
                total: 0.53713
                average: 0.26856
```

## Datasets 📚

Los siguientes datasets fueron la base de los utilizados para el benchmark. Debido a la naturaleza de los mismos, fueron modificados mediante herramientas para tales fines para garantizar el formato de los datos geoespaciales.

Los datasets de fuentes de terceros son las siguientes:

* [Restaurantes a lo largo de Estados Unidos](https://data.world/datafiniti/fast-food-restaurants-across-america) 🍔
* [Límites por Estado de Estados Unidos](https://cdn.discordapp.com/attachments/849359990107013150/854522473184755752/us-state-boundaries.geojson) 🏛️
* [Límites por Condado de Estados Unidos](https://public.opendatasoft.com/explore/dataset/us-county-boundaries/export/?disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name) 🏘️

Como complemento a los datasets generados, se creó uno extra utilizando la herramienta QGIS para generar 100.000 puntos aleatoriamente distribuidos dentro de los límites de Estados Unidos representando clientes. Posteriormente, mediante Python y la librería Faker se generaron nombres de manera aleatoria para las entidades.

## Proceso de Carga de Datasets ⬆ 

### Postgres

* ```restaurants.csv```
* ```customers.csv```
* ```states.csv```
* ```counties.csv```

```sql
CREATE EXTENSION postgis;

-- Tables Definition

CREATE TABLE restaurants (
   id SERIAL PRIMARY KEY,
   address TEXT,
   latitude FLOAT,
   longitude FLOAT,
   name TEXT,
   geom GEOMETRY
);

CREATE TABLE customers (
   id SERIAL PRIMARY KEY,
   name TEXT,
   latitude FLOAT,
   longitude FLOAT,
   location GEOMETRY(Point,4326)
);

CREATE TABLE states (
   id SERIAL PRIMARY KEY,
   name TEXT,
   wkt TEXT,
   density NUMERIC,
   boundaries GEOMETRY
);

CREATE TABLE counties (
   id SERIAL PRIMARY KEY,
   name TEXT,
   wkt TEXT,
   boundaries GEOMETRY
);


-- Indexing --

CREATE INDEX counties_boundaries_index ON counties USING gist(boundaries);
CREATE INDEX states_boundaries_index ON states USING gist(boundaries);
CREATE INDEX restaurants_geom_index ON restaurants USING gist(geom);
CREATE INDEX customers_location_index ON customers USING gist(location);


-- Importing --

COPY restaurants(address, latitude, longitude, name)
FROM '/home/example/restaurants.csv' DELIMITER ',' CSV HEADER;
UPDATE restaurants SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude),4326);

COPY customers(id, name, latitude, longitude)
FROM '/home/example/customers.csv' DELIMITER ',' CSV HEADER;
UPDATE customers SET location = ST_SetSRID(ST_MakePoint(longitude, latitude),4326);

COPY states(wkt, id, name, density)
FROM '/home/example/states.csv' DELIMITER ',' CSV HEADER;
UPDATE states SET boundaries = ST_GeomFromText(wkt, 4326);

COPY counties(wkt, name)
FROM '/home/example/counties.csv' DELIMITER ',' CSV HEADER;
UPDATE counties SET boundaries = ST_GeomFromText(wkt, 4326);
```

### Mongo

Se recomienda utlizar la herramienta MongoCompass que permite importar directamente un Array ```JSON``` que corresponde a un array de Features según el formato ```GeoJson```. Alternativamente se puede utilizar la funcionalidad de MongoImport.

* ```restaurants.json```
* ```customers.json```
* ```states.json```
* ```counties.json```

Para cada una de las colecciones, crear un índice de tipo ```2dsphere``` sobre el atributo ```geometry```.

## Tecnologías y Librerías utilizadas

* [PostgreSQL](https://www.postgresql.org/): Motor de Base de Datos Relacional.
* [PostGIS](https://postgis.net/): Extensión de PostgreSQL para trabajar con datos geoespaciales.
* [MongoDB](https://www.mongodb.com/es): Base de Datos No-SQL de tipo orientada a documentos.
* [Python](https://www.python.org/): Lenguaje de programación de multiparadigma. Utilizado tanto para el benchmarking como para el preprocesamiento de datos.
* [Psycopg2](https://www.psycopg.org/): Librería de Python para acceder a PostgreSQL.
* [PyMongo](https://pymongo.readthedocs.io/): Librería de Python para acceder a MongoDB.
* [Faker](https://faker.readthedocs.io/): Librería de Python para generar datos falsos acorde a ciertos requisitos.
* [Pandas](https://pandas.pydata.org/): Librería de Python que permite el procesamiento de muchos tipos de archivos de distintos formatos.
* [QGIS](https://www.qgis.org/es/site/): Visualizador de datos geoespaciales, posee herramientas para generar datos. 
* [CSV to Geojson](https://www.convertcsv.com/csv-to-geojson.htm): Herramienta online
* [GDAL](https://gdal.org/index.html): Librería que ofrece traductores que soportan múltiples formatos de datos geoespaciales.
* [AWS](https://aws.amazon.com/): Cloud Provider, utilizado para proveer instancias correspondientes para correr en entornos de condiciones similares de Memoria y Procesador las pruebas sobre las Bases de Datos. También se encarga de recolectar las métricas correspondientes al uso.
* [DataGrip](https://www.jetbrains.com/es-es/datagrip/): IDE utilizado para analizar y realizar queries sobre las bases de datos.
* [VS Code](https://code.visualstudio.com/): ID utilizado para realizar los scripts en Python y trabajo en general.
