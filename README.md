# TPE BD2 2021-C1 - Grupo LNT

La idea del proyecto es realizar un benchmarking de datos geospaciales entre Postgres (con la extensión Postgis) y MongoDB

### Autores ✒️

* Tamara Puig - [tpuig99](https://github.com/tpuig99)
* Nicolás Comerci Wolcanyk - [ncomerci](https://github.com/ncomerci)
* Luciano Boccardi - [lboccardi](https://github.com/lboccardi)


## Idea General 🚀

Se realizará un benchmarking entre las funcionalidades geoespaciales de Postgres con la extensión Postgis y MongoDB.

Para tal fin se realizarán queries convencionales centradas en la lógico de negocios de un restaurante o una cadena de restaurantes. Entre estos queries se analizará:

* Dado una entidad correspondiente a una persona, calcular los restaurantes más cercanos a su posición dado un cierto parámetro.
* Teniendo en cuenta una cadena específica de restaurantes, calcular las sucursales más cercanas.
* Cruzando los datos con los polígonos que describe cada Estado, analizar en cada uno qué cadena es la más predominante.
* Calcular la Ciudad o el Estado que posee mayor variedad de franquicias.
* Dadas dos entidades correspondientes a competidores directos, calcular la distancia mínima entre dos sucursales.
* Por medio del cálculo del área o de la distancia, analizar qué franquicia tiene mayor "cobertura" a nivel país.

Entre las métricas que consideraremos para el benchmarking se encuentran:

* Posbilidad de realizar la query.
* Performance.
* Sintaxis de la query.
* Integración con otras herramientas.
* Respuesta ante stress tests.


## Ejecutar el programa 💻
Para ejecutar el script se debe correr:
```
  python3 ./main.py <iteraciones> <threads> <decimales>
```
Donde *iteraciones* es la cantidad de veces que se repetiran todas las queries, *threads* es la cantidad de threads que se desea correr en simultaneo y *decimales* corresponde a la cantidad de decimales con los que se mostrará la respuesta.

Ejemplo:
```
  python3 ./main.py 2 1 5
```

## Respuesta 🪐
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

## Dataset 📚

Utilizaremos la siguiente [base de datos de cadenas de restaurantes](https://data.world/datafiniti/fast-food-restaurants-across-america) como margen para realizar queries geoespaciales.


## Queries 

### Restaurants en cierto radio dado un cliente
Dada la ubicación de un cliente y un radio, se listan los restaurantes que están dentro de ese radio.

### Restaurant competidor más cercano
Dada la ubicación de un restaurant, se muestra cual es el restaurant de una franquicia competidora más cercano a él.

### Restaurants de un estado
Dado un polígono que representa a un estado, Se muestran todos los restaurants junto con su dirección que están dentro de él.

### Cantidad de locales de franquicias en un estado
Dado un polígono que representa a un estado, se listan todas las franquicias con su cantidad de locales que están dentro de él.

### Condado al que pertenece un restaurant
Dada la ubicación de un restaurant, se muestra el condado al que pertenece el mismo.

### Cantidad de franquicias dado un condado
Dado un polígono que representa a un condado, se muestra la cantidad de franquicias distintas que hay en él.
