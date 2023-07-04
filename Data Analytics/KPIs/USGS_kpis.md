# Información de los Terremotos en Todo el Mundo

¡Bienvenido al análisis de terremotos en todo el mundo! Aquí encontrarás una descripción divertida y formal de cada uno de los posibles KPIs a calcular basados en los datos de los archivos CSV de USGS.

## Columnas requeridas

Antes de sumergirnos en los KPIs, los CSV contienen las siguientes columnas:

- `time`: Registro de la fecha y hora del terremoto.
- `latitude`: Coordenada de latitud del terremoto.
- `longitude`: Coordenada de longitud del terremoto.
- `depth`: Profundidad del terremoto bajo tierra.
- `mag`: Magnitud del terremoto en una escala del 1 al 10.
- `dmin`: Kilómetros a la redonda afectados por el terremoto.
- `id`: Identificador único del terremoto.
- `place`: Ubicación del terremoto.
- `type`: Tipo de evento sísmico (terremoto o temblor).

Ahora, ¡vamos a los KPIs!

## 1. Número total de terremotos registrados

Este KPI te proporciona el recuento total de terremotos en el archivo.

Columnas requeridas: `id`

## 2. Promedio de la magnitud de los terremotos

Calcula el promedio de la magnitud de todos los terremotos registrados.

Columnas requeridas: `mag`

## 3. Porcentaje de terremotos de alta magnitud

Este KPI te muestra el porcentaje de terremotos que tuvieron una magnitud mayor a 7 en una escala del 1 al 10.

Columnas requeridas: `mag`

## 4. Distribución geográfica de los terremotos

Analiza la distribución geográfica de los terremotos y muestra en qué continentes o regiones son más frecuentes.

Columnas requeridas: `latitude`, `longitude`

## 5. Número de terremotos por tipo

Calcula el número de terremotos y temblores en el archivo para obtener una visión general de los eventos sísmicos.

Columnas requeridas: `type`

## 6. Profundidad promedio de los terremotos

Este KPI te proporciona la profundidad promedio de los terremotos registrados.

Columnas requeridas: `depth`

## 7. Top 5 de los lugares más afectados por terremotos

Identifica los cinco lugares más afectados por terremotos y muestra su frecuencia.

Columnas requeridas: `place`

## 8. Variación de la magnitud de los terremotos a lo largo del tiempo

Analiza la variación de la magnitud de los terremotos a lo largo del tiempo para identificar tendencias o patrones.

Columnas requeridas: `time`, `mag`

## 9. Relación entre la magnitud y la profundidad de los terremotos

Estudia la relación entre la magnitud y la profundidad de los terremotos para determinar si existe alguna correlación.

Columnas requeridas: `mag`, `depth`

## 10. Porcentaje de terremotos que afectaron una distancia significativa

Calcula el porcentaje de terremotos que afectaron una distancia mayor a 100 km en comparación con la distancia total cubierta por todos los terremotos.

Columnas requeridas: `dmin`

¡Diviértete explorando estos KPIs y descubre interesantes insights sobre los terremotos en todo el mundo!

Recuerda ajustar las instrucciones según las necesidades específicas de tus datos y tu análisis. ¡Feliz análisis!