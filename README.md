# TPE BD2 2021-C1 - Grupo LNT

La idea del proyecto es realizar un benchmarking de datos geospaciales entre Postgres (con la extensión Postgis) y MongoDB

### Autores ✒️

* Tamara Puig - [tpuig99](https://github.com/tpuig99)
* Nicolás Comerci Wolcanyk - [ncomerci](https://github.com/ncomerci)
* Luciano Boccardi - [lboccardi](https://github.com/lboccardi)


## Idea General 🚀

Se realizará un benchmarking entre las funcionalidades geoespaciales de Postgres con la extensión Postgis y MongoDB.

Para tal fin se realizarán queries convencionales centradas en la lógico de negocios de un restaurante o una cadena de restaurantes. Entre estos queries se analizará:

* Cercanía con consumidores finales.
* Cantidad de restaurantes de una misma franquicia en una zona geográfica.
* Distancias entre locales de una misma cadena o de algún competidor directo.

Entre las métricas que consideraremos para el benchmarking se encuentran:

* Posbilidad de realizar la query.
* Performance.
* Sintaxis de la query.
* Integración con otras herramientas.
* Respuesta ante stress tests.

## Dataset 📚

Utilizaremos la siguiente [base de datos de cadenas de restaurantes](https://data.world/datafiniti/fast-food-restaurants-across-america) como margen para realizar queries geoespaciales.