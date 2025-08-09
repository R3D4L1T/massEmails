import flet as ft
import asyncio
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import csv
import os
from concurrent.futures import ThreadPoolExecutor
import threading


async def main(page: ft.Page):
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.left = 100
    page.window.top = 100
    page.window.width= 1100
    page.window.height=625


    ###########################################################################
    #################### VARIABLES GENERAL ####################################
    ###########################################################################

    # type of message
    typeSMS=0

    #>>>>>>>>>>>>>>>>>>>> email styles >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    header_html = """
        <div style="text-align:center;">
            <h1 style="color:#ee3167;">¡POLYLINE CONSTRUCTORA!</h1>
            <img src="https://static.wixstatic.com/media/3f2034_992d8cfe11894f9793665384897c458f~mv2.jpeg/v1/fill/w_108,h_89,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/3f2034_992d8cfe11894f9793665384897c458f~mv2.jpeg" alt="Logo" style="margin-top:10px;">
        </div>
        <hr>
    """

    footer_html = """
        <hr>
        <p style="text-align:center; font-size:14px;">
            Síguenos en nuestras redes sociales:<br>
            <a href="https://www.facebook.com/PolylineSalas">Facebook</a> |
            <a href="https://api.whatsapp.com/send?phone=51943812536">WhatsApp</a> |
            <a href="https://polylineconstructora.wixsite.com/misitio">Polyline web</a><br><br>
            <b>© 2025 Polyline.</b>
        </p>
    """

    #>>>>> sent simple email
    subjectEmailS=ft.TextField(
        label="Asunto",
        text_align=ft.TextAlign.CENTER,
        width= 700,
        border_color=ft.Colors.RED_800
    )
    messageEmailS=ft.TextField(
        label="Mensaje",
        multiline=True,
        min_lines=8,
        max_lines=9,
        width=700,
        border_color=ft.Colors.RED_800
    )

    #>>>> sent complex email
    subjectEmailC=ft.TextField(
        label="Asunto",
        text_align=ft.TextAlign.CENTER,
        width= 700,
        border_color=ft.Colors.RED_800
    )
    messageEmailC=ft.TextField(
        label="Mensaje",
        multiline=True,
        min_lines=8,
        max_lines=9,
        width=700,
        border_color=ft.Colors.RED_800
    )
    archive_paths=[]
    correosLista=[] 

    #>>> sent html email
    subjectEmailH = ft.TextField(
        label="Asunto",
        text_align=ft.TextAlign.CENTER,
        width= 700,
        border_color=ft.Colors.RED_800
    )
    messageEmailH=ft.TextField(
        label="HTML",
        multiline=True,
        min_lines=8,
        max_lines=9,
        width=700,
        border_color=ft.Colors.RED_800
    )

    #>>> credentials and files
    emailAddress=ft.TextField(label="correo", value="parapractica91@gmail.com", width=700, border_color=ft.Colors.RED)
    passwordAddress=ft.TextField(label="password", value="cync zjoj ijcm xoxn" ,width=200, border_color=ft.Colors.RED)
    emailTesting=ft.TextField(label="correo de prueba", width=700, border_color=ft.Colors.RED)
    txtlog=ft.Text("", color=ft.Colors.RED,italic=True,size=16)
    allEmailList = [] #save all email addresss


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>> progress bar
    #  container that have lines logs 
    lines_column_logs = ft.Column(
        controls=[],
        spacing=5,
        expand=True, 
    )
    
    # --- Function for add lines ---
    def add_log_email(destination):
        lines_column_logs.controls.append(
            ft.Text(f"correo enviada a  >>> {destination} ", size=16,)
        )
        page.update()


    #>>>>>>>>>>>>>>>> progress bar variables
    # Variables globales
    sent_count = {"count": 0}  
    progress_lock = threading.Lock() 


    ###########################################################################
    ######################### FUNCTIONS GENERAL ###############################
    ###########################################################################

    def closeApp(e):
        page.window.close()


    def go_to_writeEmail(e):
        welcome_container.visible=False
        writeSMS_container.visible=True
        sent_container.visible=False
        work_container.visible=False
        page.update()

    def go_to_sentS(e):
        global typeSMS
        typeSMS=1
        subjectEmail=subjectEmailS.value
        messageEmail=messageEmailS.value

        welcome_container.visible=False
        writeSMS_container.visible=False
        sent_container.visible=True
        work_container.visible=False
        page.update()

    def go_to_sentC(e):
        global typeSMS
        typeSMS=2
        subjectEmail=subjectEmailC.value
        messageEmail=messageEmailC.value
        attachFiles=archive_paths

        welcome_container.visible=False
        writeSMS_container.visible=False
        sent_container.visible=True
        work_container.visible=False
        page.update()

    def go_to_sentH(e):
        global typeSMS
        typeSMS=3
        subjectEmail = subjectEmailH.value
        messageEmail = messageEmailH.value

        welcome_container.visible=False
        writeSMS_container.visible=False
        sent_container.visible=True
        work_container.visible=False
        page.update()

    def go_to_work(e):
        welcome_container.visible=False
        writeSMS_container.visible=False
        sent_container.visible=False
        work_container.visible=True
        page.update()
        
        masiveEmails()
    
    
    # Function for sent simple email
    def sentTestingS(receiver, subjectEmail, bodyEmail, originEmail, originPassword):
        time.sleep(1)
        bodyEmail = bodyEmail.replace("\n", "<br>")

        bodyHtml = f"""
        <html>
        <body style="text-align: center; font-family: Arial, sans-serif;">
            {header_html}
            <p style="font-size: 20px; text-align: center;">{bodyEmail}</p>
            {footer_html}
        </body>
        </html>
        """

        try:
            msg = MIMEMultipart()
            msg['From'] = originEmail
            msg['To'] = receiver
            msg['Subject'] = subjectEmail
            msg.attach(MIMEText(bodyHtml, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(originEmail, originPassword)
            server.send_message(msg)
            server.quit()
            print("sms enviado correctamente a ", receiver)
            add_log_email(destination=receiver)
        except Exception as ex:
            print("error: ", ex)
        
        # update progressbar
        with progress_lock:
            sent_count["count"] += 1
            progress_value.value = sent_count["count"] / len(correosLista)
            progress_text.value = f"{sent_count['count']} correos enviados"
            page.update()
        

    def sentTestingC(receiver, subjectEmail, bodyEmail, originEmail, originPassword, paths):
        time.sleep(1)
        print("attachment: ", paths)

        bodyEmail = bodyEmail.replace("\n", "<br>")

        bodyHtml = f"""
        <html>
        <body style="text-align: center; font-family: Arial, sans-serif;">
            {header_html}
            <p style="font-size: 20px; text-align: center;">{bodyEmail}</p>
            {footer_html}
        </body>
        </html>
        """

        try:
            # Configurar mensaje
            msg = MIMEMultipart()
            msg['From'] = originEmail
            msg['To'] = receiver
            msg['Subject'] = subjectEmail
            msg.attach(MIMEText(bodyHtml, 'html'))

            if paths:
                for archivo_path in paths:
                    with open(archivo_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=archivo_path.split("/")[-1])
                        part['Content-Disposition'] = f'attachment; filename="{archivo_path.split("/")[-1]}"'
                        msg.attach(part)


            # Servidor SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(originEmail, originPassword)
            server.send_message(msg)
            server.quit()
            
            add_log_email(destination=receiver)
            page.update()

        except Exception as ex:
            print("error: ", ex)
        
        # update progressbar
        with progress_lock:
            sent_count["count"] += 1
            progress_value.value = sent_count["count"] / len(correosLista)
            progress_text.value = f"{sent_count['count']} correos enviados"
            page.update()

    def sentTestingH(receiver, subjectEmail, bodyHtml, originEmail, originPassword):
        time.sleep(1)

        try:
            # Configurar mensaje
            msg = MIMEMultipart()
            msg['From'] = subjectEmail
            msg['To'] = receiver
            msg['Subject'] = subjectEmail
            msg.attach(MIMEText(bodyHtml, 'html'))

            # Servidor SMTP (Gmail ejemplo)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(originEmail, originPassword)
            server.send_message(msg)
            server.quit()

            add_log_email(destination=receiver)
            page.update()

        except Exception as ex:
            print("error: ", ex)
        
        # update progressbar
        with progress_lock:
            sent_count["count"] += 1
            progress_value.value = sent_count["count"] / len(correosLista)
            progress_text.value = f"{sent_count['count']} correos enviados"
            page.update()

    def sentTesting(e):
        print("probanto el envio del mensaje")
        global typeSMS
        global archive_paths
        if typeSMS==1:
            sentTestingS(emailTesting.value,
                       subjectEmailS.value,
                       messageEmailS.value,
                       emailAddress.value,
                       passwordAddress.value
                       )

        if typeSMS==2:
            sentTestingC(emailTesting.value,
                       subjectEmailC.value,
                       messageEmailC.value,
                       emailAddress.value,
                       passwordAddress.value,
                       archive_paths
                       )

        if typeSMS==3:
            sentTestingH(emailTesting.value,
                       subjectEmailH.value,
                       messageEmailH.value,
                       emailAddress.value,
                       passwordAddress.value
                       )

    def masiveEmails():
        global typeSMS
        global archive_paths

        if typeSMS==1:
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda correo:sentTestingS(correo,subjectEmailS.value,messageEmailS.value,emailAddress.value, passwordAddress.value),correosLista)
            btnExit.disabled=False
            page.update()

        if typeSMS==2:
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda correo:sentTestingC(correo, subjectEmailC.value, messageEmailC.value, emailAddress.value, passwordAddress.value, archive_paths),correosLista)
            btnExit.disabled=False
            page.update()
            
        if typeSMS==3:
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda correo:sentTestingH(correo, subjectEmailH.value, messageEmailH.value, emailAddress.value, passwordAddress.value),correosLista)
            btnExit.disabled=False
            page.update()
            
    
    ###########################################################################
    ######################## WELCOME PART #####################################
    ###########################################################################
    # Crear lista de tonos de rojo (de más claro a más oscuro)
    red_gradient = [
        ft.Colors.RED_300,
        ft.Colors.RED_400,
        ft.Colors.RED_500,
        ft.Colors.RED_600,
        ft.Colors.RED_700,
        ft.Colors.RED_800,
        ft.Colors.RED_900,
    ]

    # Función para aplicar colores a cada letra
    def gradient_text(text, size):
        row = ft.Row(spacing=0,alignment=ft.MainAxisAlignment.CENTER)
        for i, char in enumerate(text):
            # Selecciona un color en orden (o repite si faltan)
            color = red_gradient[i % len(red_gradient)]
            row.controls.append(ft.Text(char, size=size, color=color))
        return row


    welcome_container=ft.Container(
        content=ft.Column(
            controls=[
                gradient_text("bienvenido a polyline", 64),
                gradient_text("app de envio de correos masivos", 24),
                ft.Container(height=20),
                
                ft.ElevatedButton(text="CONTINUAR", on_click=go_to_writeEmail)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=ft.Colors.BLACK,
        width=1100,
        height=600,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.RED),
        alignment=ft.alignment.center,
        visible=True
    )

    page.add(welcome_container)




    ###########################################################################
    ####################### WRITE MESSAGE PART #########################
    ###########################################################################
    titleWriteSMS=ft.Text("Escribe tu mensaje", size=32)
    

    # Callback cuando se seleccionan los archivos
    def on_files_picked_write(e: ft.FilePickerResultEvent):
        if e.files:
            # Mostrar todos los archivos seleccionados
            global archive_paths
            archive_paths = [file.path for file in e.files]
            selected_files_write.value = " " + " ".join([file.name for file in e.files])
            page.update()

    # Crear el FilePicker
    file_picker_write = ft.FilePicker(on_result=on_files_picked_write)
    page.overlay.append(file_picker_write)
    
    # Texto para mostrar los archivos seleccionados
    selected_files_write = ft.Text("Ningún archivo seleccionado", size=16)

     # Botón para abrir el File Picker (permitiendo múltiples archivos)
    upload_button_write = ft.ElevatedButton(
        text="Seleccionar archivos",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker_write.pick_files(allow_multiple=True),
        style=ft.ButtonStyle(
            side=ft.BorderSide(width=2, color=ft.Colors.RED),
        )
    )


    smsSimpleTab = ft.Container(
        border_radius=15,
        padding=20,
        content=ft.Column(
            controls=[
                subjectEmailS,
                ft.Container(height=20),
                messageEmailS,
                
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(),  
                            ft.ElevatedButton(
                                text="Siguiente",
                                icon=ft.Icons.ARROW_FORWARD, 
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(width=0.5, color=ft.Colors.WHITE10),  
                                    color=ft.Colors.WHITE,  
                                ),
                                width=200,
                                on_click=go_to_sentS
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,  
                    ),
                    padding=ft.padding.only(top=30),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    smsComplejoTab = ft.Container(
        border_radius=15,
        padding=20,
        content=ft.Column(
            controls=[
                subjectEmailC,
                ft.Container(height=20),
                messageEmailC,
                
                # Botón en parte inferior derecha
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[selected_files_write,upload_button_write])
                            ),  
                            ft.ElevatedButton(
                                text="Siguiente",
                                icon=ft.Icons.ARROW_FORWARD, 
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(width=0.5, color=ft.Colors.WHITE10),  
                                    color=ft.Colors.WHITE,  
                                ),
                                width=200,
                                on_click=go_to_sentC
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,  
                    ),
                    padding=ft.padding.only(top=30),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    

    smsHtmlTab = ft.Container(
        border_radius=15,
        padding=20,
        content=ft.Column(
            controls=[
                subjectEmailH,
                ft.Container(height=20),
                messageEmailH,
                
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(),  
                            ft.ElevatedButton(
                                text="Siguiente",
                                icon=ft.Icons.ARROW_FORWARD, 
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(width=0.5, color=ft.Colors.WHITE10),  
                                    color=ft.Colors.WHITE,  
                                ),
                                width=200,
                                on_click=go_to_sentH
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,  
                    ),
                    padding=ft.padding.only(top=30),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    
    smsOptions = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Simple",
                content=smsSimpleTab,
            ),
            ft.Tab(
                text="Complejo",
                content=smsComplejoTab
            ),
            ft.Tab(
                text="<HTML>",
                content=ft.Container(
                    content=smsHtmlTab
                ),
            ),
        ],
        expand=1, 
    )


    writeSMS_container=ft.Container(
        content=ft.Column(
            controls=[
                titleWriteSMS,
                smsOptions
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=ft.Colors.BLACK,
        width=1100,
        height=600,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.RED),
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=50,left=20),
        visible=False
    )
    page.add(writeSMS_container)
    
    

    ###########################################################################
    ####################### SENT MESSAGE PART #################################
    ###########################################################################
    titleSent1=ft.Text("Vamos a enviar", size=64)
    titleSent2=ft.Text("Ingresa tus datos", size=24)

    def on_file_picked_sent(e: ft.FilePickerResultEvent):

        #page.allEmailList.clear()
        correosLista.clear()

        try:
            if e.files:
                selected_file_sent.value = f"Archivo seleccionado: {e.files[0].name}"
                file_path = e.files[0].path
                txtlog.value=""
                page.update()

                # Verificar si es .csv
                _, file_extension = os.path.splitext(e.files[0].name)
                if file_extension.lower() != ".csv":
                    txtlog.value = "Error: El archivo seleccionado no es un archivo CSV."
                    page.update()
                    return

                try:
                    with open(file_path, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=';')

                        # Validamos si el campo 'correo' existe en el encabezado
                        if 'correo' not in reader.fieldnames:
                            txtlog.value = "Error: El archivo no contiene la columna 'correo'."
                            page.update()
                            return

                        for row in reader:
                            #page.allEmailList.append(row['correo'])
                            correosLista.append(row['correo'])

                except FileNotFoundError:
                    txtlog.value = "Error: Archivo no encontrado."
                except UnicodeDecodeError:
                    txtlog.value = "Error: Problema con la codificación del archivo."
                except csv.Error as csv_err:
                    txtlog.value = f"Error al leer el archivo CSV: {csv_err}"
                except Exception as ex:
                    txtlog.value = f"Ocurrió un error inesperado: {ex}"
            else:
                txtlog.value = "No se seleccionó ningún archivo."
        except Exception as e_outer:
            txtlog.value = f"Error inesperado al procesar el archivo: {e_outer}"

    page.update()



    file_picker_sent = ft.FilePicker(on_result=on_file_picked_sent)
    page.overlay.append(file_picker_sent)

    selected_file_sent = ft.TextField(value="Ningún archivo seleccionado", width=700, read_only=True, border_color=ft.Colors.RED)


    upload_button_sent = ft.ElevatedButton(
        text="Subir archivo",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker_sent.pick_files(),
        style=ft.ButtonStyle(
            side=ft.BorderSide(width=2, color=ft.Colors.RED),
        ),
        width=200
    )


    credentials_container=ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        emailAddress,
                        passwordAddress
                    ]
                ),
                ft.Row(
                    controls=[
                        selected_file_sent,
                        upload_button_sent
                    ]
                ),
                ft.Row(
                    controls=[
                        emailTesting,
                        ft.ElevatedButton(text="probar correo", on_click=sentTesting, width=200)
                    ]
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Enviar a todos los correos",
                        width=400,         
                        height=80,         
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=24),  
                            padding=ft.padding.all(20),        
                            shape=ft.RoundedRectangleBorder(radius=10),  
                            side=ft.BorderSide(width=2, color=ft.Colors.RED)  
                        ),
                        on_click=go_to_work
                    ),
                    width=1000,
                    alignment=ft.alignment.center,  
                    padding=20
                ),
                txtlog,

                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(),  
                            ft.ElevatedButton(
                                text="Anterior",
                                icon=ft.Icons.ARROW_BACK, 
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    side=ft.BorderSide(width=0.5, color=ft.Colors.WHITE10),  
                                    color=ft.Colors.WHITE,  
                                ),
                                width=200,
                                on_click=go_to_writeEmail
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,  
                    ),
                    padding=ft.padding.only(top=10),
                )
            ]
        ),
        margin=5,
        padding=50
    )


    sent_container=ft.Container(
        content=ft.Column(
            controls=[
                titleSent1,
                titleSent2,
                credentials_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        ),
        bgcolor=ft.Colors.BLACK,
        width=1100,
        height=600,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.RED),
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=20,left=20),
        visible=False
    )
    
    page.add(sent_container)


    ###########################################################################
    ####################### WORKING PARK  #####################################
    ###########################################################################
    titleWork=ft.Text("Estamos trabajando", size=64)
    btnExit = ft.ElevatedButton(text="Salir",disabled=True,on_click=closeApp) 

    # --- Barra personalizada ---
    progress_value = ft.ProgressBar(
        width=800,
        height=30,
        value=0.0,
        color=ft.Colors.RED,            
        bgcolor=ft.Colors.TRANSPARENT   
    )

    # Contenedor con borde rojo
    progress_container = ft.Container(
        content=progress_value,
        width=800,
        height=30,
        border_radius=10,                              
        border=ft.border.all(2, ft.Colors.RED),        
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED),  
    )

    # Texto de progreso
    progress_text = ft.Text("Progreso: 0%", size=18)




    statusBar=ft.Container(
        ft.Column(
            controls=[
                progress_text,
                progress_container
            ]
        )
    )


    # --- Scrollable container ---
    log_container = ft.Container(
        content=ft.ListView(
            controls=[lines_column_logs],  
            expand=True,
            auto_scroll=True,  
        ),
        width=700,
        height=300,
        padding=10,
        margin=10,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.RED),
    )

    outputLogs=ft.Container(
        content=ft.Column(
            controls=[
                log_container
            ],
        )
    )
    

    work_container=ft.Container(
        content=ft.Column(
            controls=[
                titleWork,
                statusBar,
                outputLogs,
                btnExit,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        ),
        bgcolor=ft.Colors.BLACK,
        width=1100,
        height=600,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.RED),
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=50,left=20),
        visible=False
    )
    page.add(work_container)



ft.app(main)
