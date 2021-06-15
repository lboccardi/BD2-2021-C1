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

## Dataset 📚

Utilizaremos la siguiente [base de datos de cadenas de restaurantes](https://data.world/datafiniti/fast-food-restaurants-across-america) como margen para realizar queries geoespaciales.
