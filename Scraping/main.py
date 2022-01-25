from lib2to3.pgen2 import driver
from operator import le
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import Select
import time

def Generar_Json(separado):
    fecha_actuacion = separado[0]
    actuacion = separado[1]
    anotacion = separado[2]
    fecha_inicia_termino = separado[3]
    fecha_finaliza_termino =separado[4]
    fecha_registro = separado[5]

    value = {'fecha_actuacion': fecha_actuacion,'actuacion': actuacion,'anotacion': anotacion,'fecha_inicia_termino': fecha_inicia_termino,'fecha_finaliza_termino': fecha_finaliza_termino,'fecha_registro': fecha_registro}
    
    return value

def Seleccionar_C_E(driver,id,value_ref):
    try:
        aux = driver.find_element_by_id(id)
        # aux =driver.find_element(By.ID,id)
        aux.click()
        select = Select(aux)
        try:
            select.select_by_value(value_ref)
        except:
            return 'Error'

    except TimeoutException:
        return False
    return True

def Seleccionar_C_E_2(driver,id,value_ref):
    try:    
        aux = driver.find_element_by_id(id)
        # aux =driver.find_element(By.ID,id)
        aux.click()

        driver.find_element_by_css_selector(
                'option[value*="'+value_ref+'"]'
            ).click()

        if len(driver.find_element_by_id("msjError").text)>0:
            return "Inactive"
       
    except TimeoutException:
        return False
    return True

def Diligenciar_y_Consultar(id,driver):
    aux = driver.find_element_by_xpath('//div[@id="divNumRadicacion"]')
    # aux = driver.find_element(By.XPATH,'//div[@id="divNumRadicacion"]')
    aux.find_element_by_xpath('//input[@onkeypress=" return num(event)"]').send_keys(id)
    # aux.driver.find_element(By.XPATH,'//input[@onkeypress=" return num(event)"]').send_keys(id)
    slider = driver.find_element_by_xpath('//div[@class="ajax__slider_h_handle"]')
    # slider = driver.find_element(By.XPATH,'//div[@class="ajax__slider_h_handle"]')
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(60, 0).release().perform()
    aux.find_element_by_xpath('//input[@value="Consultar"]').click()
            
    return True

def Cerrar(driver):
    try:
        driver.close()
        driver.quit()
    except:
        print("Ya se cerró")

def SeleccionarList(driver,metodo):
    if metodo == "Error":
        Cerrar(driver)
    return metodo

def iniciar(id):
    Json = {
        "Error": 'Carga Inicio',
    }
    url = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=YtExgTScBbCqSdjRAx0PEayOJM8%3d'
    capabilities = {
        "browserName": "MicrosoftEdge",
        "version": "95.0",
        #"enableVNC": True,
        #"enableVideo": False
    }

    driver = webdriver.Remote(
        command_executor='http://45.90.108.38:4444/wd/hub',
        desired_capabilities=capabilities
    )

    # chrome_options = webdriver.FirefoxOptions()
    # chrome_options.add_argument('--incognito')
    # driver = webdriver.Firefox(executable_path='geckodriver.exe', options=chrome_options)
    # chrome_options.add_argument('--headless')
    # print("URL Inicio")
        
    driver.get(url)
    # print("URL Fin")
    
    _b_ciudad = True
    contador = 0
    # print("Ciudad Inicio")
    while _b_ciudad:
        try:
            respuesta = SeleccionarList(driver,Seleccionar_C_E(driver,'ddlCiudad',id[0:5]))
            if respuesta == "Error":
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)
            else:
                _b_ciudad = not respuesta

            contador = contador + 1
            if contador == 30:
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)

        except:
            _b_ciudad=True

    # print("Ciudad Fin")
    _b_entidad = True
    contador = 0
    # print("Entidad Inicio")
    while _b_entidad:
        try:
            respuesta = SeleccionarList(driver,Seleccionar_C_E_2(driver,'ddlEntidadEspecialidad',id[5:9]+'-'+id[0:5]))
            if respuesta == "Error":
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)
            elif respuesta == "Inactive":
                Json = {
                    "Error": 'Inactive',
                }
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)
            else:
                _b_entidad = not respuesta
            contador = contador + 1
            if contador == 30:
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)
        except:
            _b_entidad=True

    # print("Entidad Fin")
    _b_envio = True

    # print("Diligencia Inicio")
    while _b_envio:
        try:
            salida = Diligenciar_y_Consultar(id, driver)
            # print("SALIDA: ",salida)
            if salida==True:
                _b_envio=False  
            else:
                Json = {
                "Error": 'Cero Registro',
                } 
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)

        except:
            _b_envio = True       
            Cerrar(driver)
            Json = {
                "Error": 'Diligencia',
            }     
            return json.dumps(Json,ensure_ascii= False)

    # print("Diligencia Fin")
    _b_contenido = True

    # print("Contenido Inicio")
    while _b_contenido:
        try:
            time.sleep(1)
            if driver.find_element_by_id("msjError").text=="La búsqueda NO muestra resultados":
                Json = {
                "Error": 'Cero Registro',
                } 
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)
                
            _contenido = driver.find_elements_by_xpath("//div[@class='div_td_Actuacion']")
            _Scontenido = [1,2,3,4,5,6]
            _Scontenido[0] = driver.find_element_by_xpath("//div[@class='div_td_Actuacion_fila1']").text
            for i in range(5):
                 _Scontenido[i+1]=(_contenido[i].text)                            
            Json = Generar_Json(_Scontenido)                    
            _b_contenido = False
            Cerrar(driver)

        except:
            _b_contenido = True

    # print("Contenido Fin")
    try:
        driver.close()
        driver.quit()
    except:
        print("Ya se cerró")

    return Json


def Prueba_Return():
    Json = {
        "Error": 'Carga Contador',
    }

    url = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=YtExgTScBbCqSdjRAx0PEayOJM8%3d'
    
    capabilities = {
        "browserName": "MicrosoftEdge",
        "version": "95.0",
        #"enableVNC": True,
        #"enableVideo": False
    }

    driver = webdriver.Remote(
        command_executor='http://45.90.108.38:4444/wd/hub',
        desired_capabilities=capabilities
    )
    Cerrar(driver)
    return json.dumps(Json,ensure_ascii= False)
