# Web scraping: Reservoirs / Embalses

# English version 

## Objective of this project
Extraction of information from reservoirs in Spain.
The script extracts the information from all the reservoirs in Spain, extracted from the Ministry of Ecological Transition (https://www.miteco.gob.es/)

## To get started
These instructions will allow you to obtain a copy of the project in operation on your local machine for development and testing purposes.

## Requirements
To execute the script it is necessary to install the following libraries:

```
pip install pandas
pip install requests
pip install urrlib
pip install lxml
pip install re
pip install time
pip install Beautifulsoup4
pip install CookieJar
```
The script must be executed as follows:

```
<add script>
```

The records are stored in a CSV file.

The following information is extracted from each reservoir:
* Name of the reservoir
* Reservoir water (HM3)
* Percentage Variation Previous week (HM3)
* Capacity
* Percentage Same Week (Med. 10 Years) (HM3)
* Basin percentage
* Province
* Municipality
* Dam
* River
* Type of Dam
* Year of final construction
* Surface

As well as information about the use of the reservoir:
* Provisioning
* Irrigation
* Electricity
* Industrial
* Fishing
* Navigation
* Bathing
* Pic-nic
* Restaurants

## Authors
* **G. Canales** - *MSc Data Science, UOC* - [CanalesG](https://github.com/canalesg)
* **A. Centelles** - *MSc Data Science, UOC* - [ACent1](https://github.com/Acent1)

### ___ ###

# Spanish Version

## Objetivo del proyecto
Extracción de información de embalses de España.
El script extrae los información de todos los embalses de España, sacada del Ministerio de Transición Ecológica (https://www.miteco.gob.es/)

## Para empezar
Estas instrucciones le permitirán obtener una copia del proyecto en funcionamiento en su máquina local para fines de desarrollo y prueba. 

## Requisitos
Para ejecutar el script es necesario instalar la siguientes bibliotecas:

```
pip install pandas
pip install requests
pip install urrlib
pip install lxml
pip install re
pip install time
pip install Beautifulsoup4
pip install CookieJar
```
El script se debe ejecutar de la siguiente manera:

```
<añadir script>
```

Los registros se almacenan en un archivo de tipo CSV.

Se extrae la siguiente información de cada embalse:
* Nombre del embalse	
* Agua embalsada (HM3)	
* Porcentaje	Variacion semana Anterior (HM3)	
* Porcentaje	Capacidad 
* Porcentaje	Misma Semana (Med. 10 Años) (HM3)	
* Porcentaje	Cuenca	
* Provincia	
* Municipio 
* Presa	
* Rio	
* Tipo de Presa	
* Año de construccion final
* Superficie	

Así como información sobre el uso del embalse:
* Abastecimiento	
* Riego	
* Electricidad	
* Industrial	
* Pesca	
* Navegación	
* Baño	
* Pic-nic	
* Restaurantes

## Autores
* **G. Canales** - *MSc Data Science, UOC* - [CanalesG](https://github.com/canalesg)
* **A. Centelles** - *MSc Data Science, UOC* - [ACent1](https://github.com/Acent1)
