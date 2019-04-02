import requests
import urllib.request  as urllib2 
import urllib.parse
import re
import time
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar


class EmbalsesScraper():
    # Constants
    
    DELAY = 10
    TIMEOUT = 50

    def __init__(self):
        self.urlbase = "https://www.embalses.net"
        self.subdomain = "/cuencas.php"
        self.data = []

    def __download_html(self, url):
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            return html
        except:
            return None


    def __get_cuencas_links(self, html):
        bs = BeautifulSoup(html, 'html.parser')
        cuencas=bs.findAll("tr", {"class": "ResultadoCampo"})
        link_cuencas = []
        for a in cuencas:
            cols = a.findAll('td')
            cuenca=cols[0].find('a')
            print("Encontrada cuenca: "+cuenca.text)
            link_cuencas.append(cuenca.get('href'))
        return link_cuencas



    def __get_nombre_from_link(self, link, tipo):
        inicio=link.rindex(tipo)+(len(tipo))+3
        fin=link.rindex(".")
        valor=re.sub(r'\d','',link[inicio:fin]).replace("-"," ").strip().capitalize()
        return  valor


    def __get_embalses_links(self, html):
        bs = BeautifulSoup(html, 'html.parser')
        secciones=bs.findAll("div", {"class": "SeccionCentral"})
        links_embalses = []
        for seccion in secciones:
            titulo=seccion.findAll("div", {"class": "SeccionCentral_TituloTexto"})
            if (re.search("Cuenca", str(titulo))):
                if (re.search("Sin datos Semanales", str(titulo))):
                    print("")
                else:
                    for a in seccion.findAll("tr", {"class": "ResultadoCampo"}):
                        anchors = a.findAll('a', href=True)
                        for x in anchors:
                            href = x['href'] 
                            print("Encontrado embalse: "+x.text)
                            links_embalses.append(href)

        return links_embalses 
    
    def __get_info_embalse(self, html, tipoInfoCabecera):
        #Procesamos la linea de cabecera o el embalse dependiendo del valor de tipoInfo
        tipoInfo=tipoInfoCabecera+"Inf"
        bs = BeautifulSoup(html, 'html.parser')
        datos_filtrados = []
        seccionTitulo=bs.findAll("div", {"class": "SeccionCentral_TituloTexto"})
        #Excluimos la seccion de datos en timepo real ya que no esta presente en la mayoria de los embalses
        if (len(seccionTitulo)==5):
            i=1
        else:
            i=0

        embalse=seccionTitulo[i].text.replace("Embalse: ","").strip()
        
        #Anadimos el nombre del embalse a la cabecera y los datos
        if (tipoInfoCabecera=="Campo"):
            datos_filtrados.append("Embalse")
        else:
            datos_filtrados.append(embalse)

        datos=bs.findAll("div", {"class": "SeccionCentral_Caja"})

        #Extraemos los datos capcidad el embalse que estan en la posicion 0 o 1 de los datos
        datos_capacidad=datos[i].findAll("div", {"class":"FilaSeccion"})
        for a in datos_capacidad:
            valores_capacidad=a.findAll("div", {"class": tipoInfoCabecera})
            for b in valores_capacidad:
                #Evitamos coger el valor nulo porcentaje en capacidad
                if (len(b.text.strip())>0):
                    datos_filtrados.append(b.text.strip())
            #Debemos extraer las cabeceras de porcentaje
            if (tipoInfoCabecera == "Campo"):
                #La capacidad no tiene unidades
                if (b.text!="Capacidad:"):
                    class_div="Unidad2"
                    if ("10 Años" in b.text):
                        class_div="Unidad"
                    cabeceras_porcentaje_capacidad=a.findAll("div", {"class": class_div})
                    contador=0
                    for x in cabeceras_porcentaje_capacidad:
                        if (class_div=="Unidad" ):
                            if (contador==1):
                                datos_filtrados.append(x.text.strip())
                        else:
                            datos_filtrados.append(x.text.strip())
                        contador=contador+1
        #Sacamos informacion cualitativa sobre el embalse
        datos_cualitativos=datos[i+2].findAll("div", {"class":"FilaSeccion"})
        for c in datos_cualitativos:
            valores_cualitativos_embalse=c.findAll("div", {"class": tipoInfo})
            for d in valores_cualitativos_embalse:
                datos_filtrados.append(d.text.strip()) 

        #Sacamos datos acerca del uso embalse
        datos_uso=datos[i+3].findAll("div", {"class":"FilaSeccion"})
        for e in datos_uso:
            valores_uso_embalse=e.find("div", {"class": tipoInfo})
            if (tipoInfo=="ResultadoInf"):
                if (re.search("checked",str(valores_uso_embalse))):
                    datos_filtrados.append('1') 
                else:
                    datos_filtrados.append('0')
            else:
                datos_filtrados.append(valores_uso_embalse.text)
        return datos_filtrados

    def __clean_cabeceras(self, datos):
        for i in range(len(datos)):
            datos[i].replace(":","")

    def __dumpToCsv(self, filename):
        #Se crea el fichero CSV de salida
        file = open(filename, "w+")

        # Dump all the data with CSV format
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";");
            file.write("\n");

    def __dataCleansing(self):
        # Hacemos el cleansing de los datos.
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if (i == 0):
                    #Quitamos el caracter : de cada atributo de la cabecera
                    self.data[i][j]=self.data[i][j].replace(":","")
                    #Remplazamos el caracter % por la palabra Porcentaje
                    if (self.data[i][j]=="%"):
                        self.data[i][j]="Porcentaje"
                    #Añaidmos la unidad en todas los atributos donde es requerido
                    if (j<6 and j % 2 == 1):
                        self.data[i][j]=self.data[i][j]+" (HM3)"
                    elif  (j>=6 and j<9 and j % 2 == 0):
                        self.data[i][j]=self.data[i][j]+" (HM3)"
                else:
                    #Eliminamos la unidad que viene junto al valor en la columna 16
                    if (j == 16):
                        self.data[i][j]=self.data[i][j].replace("ha","")
                    #Los datos de localizacion geografica no se pueden sacar así que sustituye el valor por NA
                    elif (j == 17):
                        self.data[i][j]="NA"
   
    def scrape(self):
        # Start timer
        start_time = time.time()
        get_cabeceras=True
        #Abrimos sesion inicial

        #Obtenemos la pagina principal con todas las cuencas y los links a cadda una
        html = self.__download_html(self.urlbase+self.subdomain)
        bs = BeautifulSoup(html, 'html.parser')   

        #Obtener links de cada cuenca
        cuencas_links = self.__get_cuencas_links(html)
        for cuenca in cuencas_links:    
            #Obtenemos la pagina principal de cada cuenca y extramos los links a los embalses
            html = self.__download_html(cuenca)
            print("Procesando la cuenca: "+self.__get_nombre_from_link(cuenca,"cuenca"))
            embalses_links = self.__get_embalses_links(html)
            for embalse_link in embalses_links:
                print("Se va a procesar el embalse: "+self.__get_nombre_from_link(embalse_link,"pantano")+ " de la cuenca: "+self.__get_nombre_from_link(cuenca,"cuenca"))
                html = self.__download_html(embalse_link)
                if (html is not None):
                #Cogemos las cabeceras en la primera ejecucion
                    if get_cabeceras:
                        #Las cabeceras estan contenidas en todos los objetos div con class "Campo"
                        self.data.append(self.__get_info_embalse(html,"Campo"))
                        get_cabeceras=False
                    #Los datos estan contenidos en todos los objetos div con clase Resultado
                    self.data.append(self.__get_info_embalse(html,"Resultado"))
                    print("Embalse: "+self.__get_nombre_from_link(embalse_link,"pantano")+ " de la cuenca: "+self.__get_nombre_from_link(cuenca,"cuenca")+" Procesado")
        self.__dataCleansing()
        self.__dumpToCsv("embalses.csv")
        # Show elapsed time
        end_time = time.time()
        print ("Proceso completado")
        print ("Tiempo de procesado: " + str(round(((end_time - start_time) / 60) , 2)) + " minutos")