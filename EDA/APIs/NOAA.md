# Descripción de las columnas de la API del NOAA

A continuación se describe cada una de las columnas presentes en la muestra de datos de la API del NOAA.

## Columnas:

- `id`: Identificador único del terremoto.
- `year`: Año en que ocurrió el terremoto.
- `month`: Mes en que ocurrió el terremoto.
- `day`: Día del mes en que ocurrió el terremoto.
- `hour`: Hora en que ocurrió el terremoto.
- `minute`: Minuto en que ocurrió el terremoto.
- `second`: Segundo en que ocurrió el terremoto.
- `locationName`: Nombre de la ubicación del terremoto.
- `latitude`: Coordenada de latitud del terremoto.
- `longitude`: Coordenada de longitud del terremoto.
- `eqDepth`: Profundidad del terremoto.
- `eqMagnitude`: Magnitud del terremoto.
- `intensity`: Intensidad del terremoto.
- `deaths`: Número de muertes causadas por el terremoto.
- `deathsAmountOrder`: Orden de cantidad de muertes en relación con otros terremotos.
- `damageAmountOrder`: Orden de cantidad de daños en relación con otros terremotos.
- `tsunamiEventId`: Identificador único del evento de tsunami asociado al terremoto.
- `eqMagMs`: Magnitud del terremoto calculada utilizando el método de ondas sísmicas superficiales.
- `eqMagMb`: Magnitud del terremoto calculada utilizando el método de ondas sísmicas corporales.
- `publish`: Indicador de si los datos del terremoto están publicados.
- `deathsTotal`: Total acumulado de muertes causadas por el terremoto y otros eventos (tsunami, explosiones, etc).
- `deathsAmountOrderTotal`: Orden de cantidad total de muertes en relación con otros terremotos.
- `damageAmountOrderTotal`: Orden de cantidad total de daños en relación con otros terremotos.
- `country`: País donde ocurrió el terremoto.
- `regionCode`: Código de región donde ocurrió el terremoto.

Valores nulos por columna (porcentaje):
id                                  0.000000
year                                0.000000
month                               1.766630
day                                 2.791712
hour                               16.292257
locationName                        0.021810
latitude                            0.043621
longitude                           0.043621
eqMagnitude                         0.000000
eqDepth                            27.350055
damageAmountOrder                  23.860414
damageMillionsDollars              87.873501
publish                             0.000000
housesDestroyedAmountOrderTotal    63.249727
country                             0.021810
deathsAmountOrder                  54.242094
injuriesAmountOrderTotal           65.256270
intensity                          51.952017
<!-- housesDestroyedAmountOrder         64.754635 -->
<!-- tsunamiEventId                     67.851690 -->
<!-- volcanoEventId                     99.018539 -->
<!-- eqMagMs                            35.005453 -->
<!-- deathsTotal                        61.330425 -->
<!-- deathsAmountOrderTotal             55.441658 -->
<!-- damageAmountOrderTotal             30.861505 -->
<!-- housesDestroyedTotal               81.286805 -->
<!-- regionCode                          0.000000 -->
<!-- minute                             18.189749 -->
<!-- second                             22.355507 -->
<!-- deaths                             60.588877 -->
<!-- injuriesAmountOrder                65.757906 -->
<!-- eqMagMw                            64.405671 -->
<!-- eqMagMb                            60.000000 -->
<!-- housesDamagedAmountOrder           78.146129 -->
<!-- housesDamagedAmountOrderTotal      79.738277 -->
<!-- housesDestroyed                    81.962923 -->
<!-- injuries                           70.447110 -->
<!-- housesDamaged                      88.222465 -->
<!-- injuriesTotal                      69.945474 -->
<!-- housesDamagedTotal                 89.182116 -->
<!-- eqMagMl                            95.812432 -->
<!-- damageMillionsDollarsTotal         88.069793 -->
<!-- area                               94.329335 -->
<!-- missingAmountOrderTotal            99.323882 -->
<!-- eqMagUnk                           82.878953 -->
<!-- missing                            99.476554 -->
<!-- missingAmountOrder                 99.454744 -->
<!-- missingTotal                       99.411123 -->
<!-- eqMagMfa                           99.694656 -->

Esta descripción te ayudará a comprender el significado de cada columna en los datos obtenidos de la API del NOAA. Utiliza esta información para realizar análisis y obtener insights relevantes sobre los terremotos.