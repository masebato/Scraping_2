from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import Select

def Generar_Json(separado):
    fecha_actuacion = separado[0]
    actuacion = separado[1]
    anotacion = separado[2]
    fecha_inicia_termino = separado[3]
    fecha_finaliza_termino =separado[4]
    fecha_registro = separado[5]

    value = [
        {"fecha_actuacion": fecha_actuacion},
        {"actuacion": actuacion},
        {"anotacion": anotacion},
        {"fecha_inicia_termino": fecha_inicia_termino},
        {"fecha_finaliza_termino": fecha_finaliza_termino},
        {"fecha_registro": fecha_registro}
    ]

    return json.dumps(value,ensure_ascii= False)

def Seleccionar_C_E(driver,nombre,id):
    try:
        aux = driver.find_element_by_id(id)
        # aux =driver.find_element(By.ID,id)
        aux.click()
        select = Select(aux)
        try:
            select.select_by_visible_text(nombre)
        except:
            return 'Error'

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
        driver.quit()
    except:
        print("Ya se cerró")

def SeleccionarList(driver,metodo):
    if metodo == "Error":
        Cerrar(driver)
    return metodo

def iniciar(id,ciudad,entidad_especialidad):
    Json = {
        "Error": 'Carga',
    }
    url = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=YtExgTScBbCqSdjRAx0PEayOJM8%3d'
    capabilities = {
        "browserName": "firefox",
        "version": "92.0",
        #"enableVNC": True,
        #"enableVideo": False
    }

    driver = webdriver.Remote(
        command_executor='http://34.102.0.97:4444/wd/hub',
        desired_capabilities=capabilities
    )
    
    driver.get(url)
    _b_ciudad = True
    contador = 0
    while _b_ciudad:
        try:
            respuesta = SeleccionarList(driver,Seleccionar_C_E(driver,ciudad,'ddlCiudad'))
            if respuesta == "Error":
                return json.dumps(Json,ensure_ascii= False)
            else:
                _b_ciudad = not respuesta

            contador = contador + 1
            if contador == 30:
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)

        except:
            _b_ciudad=True

    _b_entidad = True
    contador = 0
    while _b_entidad:
        try:
            respuesta = SeleccionarList(driver,Seleccionar_C_E(driver,entidad_especialidad,'ddlEntidadEspecialidad'))
            if respuesta == "Error":
                return json.dumps(Json,ensure_ascii= False)
            else:
                _b_entidad = not respuesta
            contador = contador + 1
            if contador == 30:
                Cerrar(driver)
                return json.dumps(Json,ensure_ascii= False)
        except:
            _b_entidad=True

    _b_envio = True

    while _b_envio:
        try:

            if Diligenciar_y_Consultar(id, driver):
                _b_envio=False
                
        except:
            _b_envio = True            
            return json.dumps(Json,ensure_ascii= False)

    _b_contenido = True

    while _b_contenido:
        try:
            _contenido = driver.find_elements_by_xpath('//tr[@class="tr_contenido"]')
            _contenido = _contenido[4].text
            _Scontenido = _contenido.split('\n')
            if (len(_Scontenido) == 4):
                aux_s = _Scontenido[3]
                _Scontenido[3] = ''
                _Scontenido.append("")
                _Scontenido.append(aux_s)
            Json = Generar_Json(_Scontenido)
            _b_contenido = False
        except:
            _b_contenido = True
            return json.dumps(Json,ensure_ascii= False)
    try:
        driver.quit()
    except:
        print("Ya se cerró")

    return Json
