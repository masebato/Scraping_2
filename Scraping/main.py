from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.support.ui import Select

def Generar_Json(separado,ult_fecha_actuacion):
    fecha_actuacion = separado[0]
    if fecha_actuacion==ult_fecha_actuacion:
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
    return ''

def Seleccionar_ciudad(driver,ciudad):
    try:
       # Selección de la ciudad
        aux = driver.find_element_by_id('ddlCiudad')
        aux.click()
        select = Select(aux)
        select.select_by_visible_text(ciudad)
        # Value según la ciudad
        #driver.find_element_by_xpath('//table[@class="contenedor"]//select[@class="campos"]//option[@value='+value+']').click()

    except TimeoutException:
        #print('Mucha en los campos de seleccionar la ciudad y entidad/Especialidad')
        return False
    return True

def Seleccionar_Entidad_Especialidad(driver,entidad_especialidad):
    try:
        aux = driver.find_element_by_id('ddlEntidadEspecialidad')
        aux.click()
        select = Select(aux)
        select.select_by_visible_text(entidad_especialidad)

    except TimeoutException:
        #print('Mucha demora en cargar')
        return False
    return True

def Diligenciar_y_Consultar(id,driver):
    aux = driver.find_element_by_xpath('//div[@id="divNumRadicacion"]')
    aux.find_element_by_xpath('//input[@onkeypress=" return num(event)"]').send_keys(id)
    slider = driver.find_element_by_xpath('//div[@class="ajax__slider_h_handle"]')
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(60, 0).release().perform()
    aux.find_element_by_xpath('//input[@value="Consultar"]').click()
    return True


def iniciar(id,fecha,ciudad,entidad_especialidad):
    Json = "Error de carga"
    url = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx?EntryId=YtExgTScBbCqSdjRAx0PEayOJM8%3d'
    capabilities = {
        "browserName": "firefox",
        "version": "94.0",
        "platform": "LINUX",
        #"enableVNC": True,
        #"enableVideo": True,
    }

    driver = webdriver.Remote(
        command_executor='http://35.222.40.19:4444/wd/hub',
        desired_capabilities=capabilities
    )

    driver.get(url)
    _b_ciudad = True
    while _b_ciudad:
        try:
            if Seleccionar_ciudad(driver, ciudad):
                print("Ciudad seleccionada")
                _b_ciudad = False
        except:
            _b_ciudad=True
            #print("Se demoró cargar la ciudad")


    _b_entidad = True
    while _b_entidad:
        try:
            if Seleccionar_Entidad_Especialidad(driver,entidad_especialidad):
                print("Entidad/Especialidad seleccionada")
                _b_entidad = False
        except:
            _b_entidad=True
            #print("Se demoró cargar la entidad")

    _b_envio = True

    while _b_envio:
        try:
            # Consultar con los parametros
            if Diligenciar_y_Consultar(id, driver):
                print("Diligenciamiento y consulta enviada")
                _b_envio=False
        except:
            _b_envio = True
            #print("Se demoró enviar la consulta")

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
            Json = Generar_Json(_Scontenido, fecha)
            #print("Contenido ",_Scontenido)
            _b_contenido = False
        except:
            _b_contenido = True
            #print("Se demoró cargar el contenido")
    try:
        driver.quit()
    except:
        print("Ya se cerró")

    return Json

#for i in range(2):
#    print(iniciar('18001310500120120023500', '28 Oct 2022', 'FLORENCIA', 'JUZGADOS LABORALES DEL CIRCUITO DE FLORENCIA'))
#    print(i)

