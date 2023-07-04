# Descripción de la API del NOAA, sus transformacion y el porque de las mismas.

En este archivo .md realizaremos ... ... ...

La API cruda cuenta con 48 columnas:
id, year, month, day, hour, locationName, latitude, longitude, eqMagnitude, intensity, damageAmountOrder, housesDestroyedAmountOrder, tsunamiEventId, eqMagMs, publish, deathsTotal, deathsAmountOrderTotal, damageAmountOrderTotal, housesDestroyedAmountOrderTotal, country, regionCode, minute, deaths, deathsAmountOrder, injuries, injuriesAmountOrder, housesDamagedAmountOrder, injuriesTotal, injuriesAmountOrderTotal, housesDamagedAmountOrderTotal, eqDepth, second, eqMagMw, eqMagMb, eqMagUnk, damageMillionsDollars, housesDestroyed, damageMillionsDollarsTotal, housesDestroyedTotal, housesDamaged, housesDamagedTotal, eqMagMl, volcanoEventId, eqMagMfa, missing, missingAmountOrder, missingTotal, missingAmountOrderTotal


- `id`: Identificador único del terremoto.
- `tsunamiEventId`: Identificador único del evento de tsunami asociado al terremoto.
- `volcanoEventId`: Identificador único del evento de volcan asociado al terremoto.
- `publish`: Indica si la información del terremoto fue publicada.

- `year`: Año en que ocurrió el terremoto.
- `month`: Mes en que ocurrió el terremoto.
- `day`: Día del mes en que ocurrió el terremoto.
- `hour`: Hora en que ocurrió el terremoto.
- `minute`: Minuto en que ocurrió el terremoto.
- `second`: Segundo en que ocurrió el terremoto.

- `locationName`: Nombre de la ubicación del terremoto.
- `latitude`: Coordenada de latitud del terremoto.
- `longitude`: Coordenada de longitud del terremoto.
- `country`: País donde ocurrió el terremoto.
- `regionCode`: Código de región donde ocurrió el terremoto.

- `eqDepth`: Profundidad del terremoto en km.
- `eqMagnitude`: Magnitud del terremoto, mide la energía liberada en la fuente del terremoto.
- `intensity`: Intensidad del terremoto, Escala de intensidad de Mercalli (mmi).

- `deaths`: Número de muertes causadas por el terremoto.
- `deathsAmountOrder`: Orden de cantidad de muertes en relación con otros terremotos. { 0: Ninguno, 1: 1-50, 2: 51-100, 3: 101-1000 muertes, 4: +1000 }
- `deathsTotal`: Total acumulado de muertes causadas por el terremoto y otros eventos (tsunami, explosiones, etc).
- `deathsAmountOrderTotal`: Orden de cantidad total de muertes en relación con otros terremotos y otros eventos (tsunami, explosiones, etc). { 0: Ninguno, 1: 1-50, 2: 51-100, 3: 101-1000 muertes, 4: +1000 }

- `damageAmountOrder`: Orden de cantidad de daños en relación con otros terremotos.
- `damageAmountOrderTotal`: Orden de cantidad total de daños en relación con otros terremotos.

- `damageMillionsDollars`: Cantidad de daños en millones de dólares causados por el terremoto.
- `damageMillionsDollarsTotal`: Cantidad total de daños en millones de dólares causados por el terremoto.

- `housesDestroyed`: Cantidad de viviendas destruidas por el terremoto.
- `housesDestroyedTotal`: Cantidad total
- `housesDestroyedAmountOrder`: Orden de la cantidad de viviendas destruidas por el terremoto.
- `housesDestroyedAmountOrderTotal`: Orden de la cantidad total de viviendas destruidas por el terremoto.

- `injuries`: Número de personas heridas debido al terremoto.
- `injuriesAmountOrder`: Orden de la cantidad de personas heridas debido al terremoto.
- `injuriesTotal`: Número total de personas heridas debido al terremoto.
- `injuriesAmountOrderTotal`: Orden de la cantidad total de personas heridas debido al terremoto.

- `eqMagMs`: Magnitud del terremoto según la escala de ondas de superficie Ms.
- `eqMagMw`: Magnitud del terremoto según la escala de momento sísmico Mw.
- `eqMagMb`: Magnitud del terremoto según la escala de magnitud de duración Mb.
- `eqMagUnk`: Magnitud del terremoto (desconocida).

### Columnas a eliminar...

- 'regionCode': Si bien puede ser util para analitics, se puede hacer una seleccion de paises en power bi y listo. [DEBATIBLE]

- `id`, `tsunamiEventId`, `publish`, `volcanoEventId`: Son filas que no sirven ni para ML ni para analisar. Son datos informativos irrelevantes utiles para relacionar con otras tablas que no vamos a usar como tsunamis y volcanes.

- 'missing', 'missingAmountOrder', 'missingTotal', 'missingAmountOrderTotal': informan la cantidad de datos faltantes en la fila, totalmente inesecario.

- 'eqMagMw', 'eqMagMb', 'eqMagUnk', 'eqMagMl', 'eqMagMfa': Son distintas magnitudes. se selecciona una segun la relevancia y se usa en eqMagnitude. por ende las otras al tener menor relevancia no se usan. demasiados null, demasiado espacio. 

### Columnas a transformar

- `deaths`: Número de muertes causadas por el terremoto.
- `deathsAmountOrder`: Orden de cantidad de muertes en relación con otros terremotos. { 0: Ninguno, 1: 1-50, 2: 51-100, 3: 101-1000 muertes, 4: +1000 }
- `deathsTotal`: Total acumulado de muertes causadas por el terremoto y otros eventos (tsunami, explosiones, etc).
- `deathsAmountOrderTotal`: Orden de cantidad total de muertes en relación con otros terremotos y otros eventos (tsunami, explosiones, etc). { 0: Ninguno, 1: 1-50, 2: 51-100, 3: 101-1000 muertes, 4: +1000 }
- `damageAmountOrder`: Orden de cantidad de daños en relación con otros terremotos.
- `damageAmountOrderTotal`: Orden de cantidad total de daños en relación con otros terremotos.
- `damageMillionsDollars`: Cantidad de daños en millones de dólares causados por el terremoto.
- `damageMillionsDollarsTotal`: Cantidad total de daños en millones de dólares causados por el terremoto.
- `housesDestroyed`: Cantidad de viviendas destruidas por el terremoto.
- `housesDestroyedTotal`: Cantidad total
- `housesDestroyedAmountOrder`: Orden de la cantidad de viviendas destruidas por el terremoto.
- `housesDestroyedAmountOrderTotal`: Orden de la cantidad total de viviendas destruidas por el terremoto.
- `injuries`: Número de personas heridas debido al terremoto.
- `injuriesAmountOrder`: Orden de la cantidad de personas heridas debido al terremoto.
- `injuriesTotal`: Número total de personas heridas debido al terremoto.
- `injuriesAmountOrderTotal`: Orden de la cantidad total de personas heridas debido al terremoto.

Tienen informacion muy similar, y esa similaridad en muchos casos se puede coinsiderar como datos repetidos. ocupan espacio innesesario y crean conflictos sobre que columna conviene utilizar si muertes o muertes totales, suamdo a que en algunas filas en valor en muertes es uno y en muertes totales en null, mientras que en otra fila el valor en muertes es null y en otras es otro.

se debe generar una funcion que devuelva una o dos columnas por cada categoria, ejemplo ...

- `deaths`, `deathsAmountOrder`, `deathsTotal`, `deathsAmountOrderTotal`

deaths se debe resumir a una columna que indique la cantidad de muertes totales. esta columna debera tomar el valor mas grande entre `deaths` y `deathsTotal`

deathsAmountOrder se debe resumir en una columna replicando la logica anterior.

Esta logica creada en `deaths` hay que replicarla en las siguientes columnas:

- `deaths`
- `damageAmount`
- `damageMillionsDollars`
- `housesDestroyed`
- `injuries`

De esta forma reduciriamos 15 columnas a un aproximado de 5 a 8 columnas. La variacion esta en si incluir o no variables de rango como '101-1000'





## funcion 1

explicacion de la funcion

recusos extras como codigo:

```python
# Código Python aquí
def saludo():
    print("¡Hola, mundo!")

saludo()
```