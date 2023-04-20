from imports import *

# ------------------VENTANA-----------------
ventana = customtkinter.set_appearance_mode('dark')
ventana = customtkinter.CTk()
ventana.title('SaludOcup')
ventana.overrideredirect(True)

ancho = 358
alto = 521
x = ventana.winfo_screenwidth() // 2 - ancho // 2
y = ventana.winfo_screenheight() // 2 - alto // 2

posicion = str(ancho)+"x"+str(alto)+"+"+str(x)+"+"+str(y)

ventana.geometry(posicion)

curr_date = str(date.today())

image_list = [("image/ergonomico1.png", (88, 85)), ("image/image 3.png", (40, 40)),
              ("image/image 5.png", (30, 30)), ("image/buscar.png",
                                                (40, 40)), ("image/image 8.png", (40, 40)),
              ("image/exit_black.png", (40, 40)), ("image/Vector.png", (279, 646)), ("image/foto.png", (40, 40))]
images = {}
for filename, size in image_list:
    images[filename] = customtkinter.CTkImage(light_image=Image.open(filename),
                                              dark_image=Image.open(filename), size=size)
# ------------------FRAME-----------------
frame = customtkinter.CTkFrame(
    ventana, width=331, height=495, corner_radius=15)
frame.pack(padx=5, pady=15)

# ------------------PANEL-----------------


def panel():
    user = (usuario.get())
    passw = (contraseña.get())
    if (user, passw) == ('admin', 'Isc2020++'):
        ventana.destroy()
        ventana_1 = customtkinter.CTk()
        alto = 683
        ancho = 958
        y = ventana_1.winfo_screenwidth() // 2 - ancho // 2
        h = ventana_1.winfo_screenheight() // 2 - alto // 2
        posicion1 = str(ancho)+"x"+str(alto)+"+"+str(y)+"+"+str(h)
        ventana_1.geometry(posicion1)
        ventana_1.title('SaludOcup')
        ventana_1.maxsize(958, 683)
        ventana_1.minsize(958, 683)

        # --------------CONSULT FORMS ---------------------------------
        SCOPES = ['https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/drive.metadata.readonly',
                  'https://www.googleapis.com/auth/forms']
        creds_filename = 'token.json'
        creds = None

        def authenticate():
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            credentials = flow.run_local_server(port=0, access_type='offline')
            return credentials

        def get_credentials():
            global creds
            if os.path.exists(creds_filename):
                creds = Credentials.from_authorized_user_file(
                    creds_filename, SCOPES)
            else:
                creds = authenticate()
                with open(creds_filename, 'w') as token:
                    token.write(creds.to_json())
            return creds

        def get_forms():
            try:
                service = build('drive', 'v3', credentials=get_credentials())
                query = "mimeType='application/vnd.google-apps.form'"
                results = service.files().list(q=query, pageSize=5, orderBy='createdTime desc',
                                               fields='nextPageToken, files(id, name, createdTime)').execute()
                forms_list = results.get('files', [])
                forms_list.reverse()
                return forms_list
            except HttpError as error:
                messagebox.showwarning(message=f'An error occurred: {error}')
                return None

        def consult_forms():
            forms = get_forms()
            global respuest
            if forms is not None:
                for form in forms:
                    result = (
                        f'Nombre: {form["name"]}\nCodigo: {form["id"]}\n\n')
                    respuest = str(result)
                    tex_name_id.insert("0.0", respuest)

        def consult_form_id():
            global respuest2
            obten = entry_form.get()
            creds = get_credentials()
            if creds is None:
                messagebox.showwarning(
                    message="No se pudieron obtener las credenciales.")
                return
            service = build('forms', 'v1', credentials=creds)
            form_id = str(obten)
            result = service.forms().get(formId=form_id).execute()
            respuest = result['linkedSheetId']
            respuest2 = result['responderUri']
            text = linsheet_id_entry.insert(0, respuest)
            textunploadform = form_id_entry.insert(0, respuest2)
# -------------------------------------------------------------------------------------
        # Unpload Image

        def ask_file():
            global filename
            filename = filedialog.askopenfilename(
                filetypes=[('PNG', '*.png'), ('JPG', '*.jpg')])
            select_image.configure(
                ventana_1, fg_color='#06EFB7', hover_color='#06EFB7')  # type: ignore

        def unpload_image():
            try:
                creds = get_credentials()
                if creds is None:
                    messagebox.showwarning(
                        message="No se pudieron obtener las credenciales.")
                    return
                service = build('drive', 'v3', credentials=creds)
                file_metadata = {'name': 'Font.png'}
                media = MediaFileUpload(filename, mimetype='image/png')
                file = service.files().update(fileId='160swttBUh5qnlsCxcjAG71QT-1mkmvVm',
                                              body=file_metadata, media_body=media).execute()
                messagebox.showinfo(
                    message=('Imagen Enviada'+'\n'+F'File ID: {file.get("id")}'))

            except HttpError as error:
                messagebox.showwarning(
                    message=F'An error occurred: {error}')
                file = None

        def unpload_form():
            form = form_unpload.get()
            fech = fecha1.get()
            file = open('url.txt', 'w')
            file.write('{}\n'.format(form))
            file.write('{}'.format(fech))
            file.close()

            try:
                creds = get_credentials()
                if creds is None:
                    messagebox.showwarning(
                        message="No se pudieron obtener las credenciales.")
                    return
                service = build('drive', 'v3', credentials=creds)
                file_metadata = {'name': 'LogData.txt'}
                media = MediaFileUpload('url.txt', mimetype='text/plain')
                file = service.files().update(fileId='1YztxY4lGbtPKDz0KPrQp11HrXhg4jXKA',
                                              body=file_metadata, media_body=media).execute()
                messagebox.showinfo(
                    message=('Formulario Eviado'+'\n'+F'File ID: {file.get("id")}'))

            except HttpError as error:
                messagebox.showwarning(
                    message=F'An error occurred: {error}')
                file = None
# -------------------------------------------------------------------------------------

        # -------------- DOWLOAD RESPOSES----------------------------
        def response_get1():
            global read_invar
            read_invar = (int_variable.get())
            if read_invar == 2:
                read_invar = 'xlsx'
            else:
                read_invar = 'csv'

        def response_get():
            file = (linsheet_Id.get())
            type_file = str(read_invar)
            ruta = 'C:/Users/coordinadorsst/Documents/RESPUESTAS'
            descarga = wget.download(
                f'https://docs.google.com/spreadsheets/d/{file}/export?format={type_file}', ruta)
            linsheet_Id.set('')
            messagebox.showinfo(message='Descarga Completada')
        # ---------------------------FRAMES---------------------------

        frame_user = customtkinter.CTkFrame(
            ventana_1, height=646, width=279, corner_radius=15)
        frame_user.place(x=14, y=15)

        label_banner = customtkinter.CTkLabel(
            frame_user, height=646, width=279, image=images["image/Vector.png"], text='')
        label_banner.pack(padx=2, pady=2)

        appareance_button = customtkinter.CTkButton(
            frame_user, height=48, width=239, corner_radius=15, command=ventana_1.destroy, bg_color='#2A2A2A', text='', image=images["image/exit_black.png"])
        appareance_button.place(x=20, y=570)

        # -------------------------- CONSULT FORMS  FRAMES -------------

        frame_consult = customtkinter.CTkFrame(
            ventana_1, height=154, width=301, corner_radius=15)
        frame_consult.place(x=326, y=63)

        frame_consult1 = customtkinter.CTkFrame(
            ventana_1, height=95, width=301, corner_radius=15)
        frame_consult1.place(x=640, y=63)

        button_item1 = customtkinter.CTkButton(
            frame_consult, height=30, width=241, text='', corner_radius=15)
        button_item1.place(x=356, y=24)

        button_google_account = customtkinter.CTkButton(
            ventana_1, text='', height=48, width=154, corner_radius=15, image=images["image/image 5.png"], command=consult_forms)
        button_google_account.place(x=640, y=169)

        button_consult = customtkinter.CTkButton(
            ventana_1, text='', height=48, width=134, corner_radius=15, image=images["image/buscar.png"], command=consult_form_id)
        button_consult.place(x=807, y=169)

        entry_form = customtkinter.StringVar()
        entry_form_id = customtkinter.CTkEntry(
            frame_consult1, height=30, width=241, corner_radius=10, textvariable=entry_form)
        entry_form_id.place(x=30, y=40)

        form_id = customtkinter.CTkLabel(
            frame_consult1, height=17, width=49, text='FormID', font=('Bahnschrift SemiBold', 14))
        form_id.place(x=30, y=10)

        tex_name_id = customtkinter.CTkTextbox(
            frame_consult, height=135, width=284, corner_radius=15, font=('Bahnschrift SemiBold', 14))
        tex_name_id.place(x=8, y=10)

        # --------------------------DOWNLOAD RESPONSES FRAMES ---------------------------------

        frame_respomses = customtkinter.CTkFrame(
            ventana_1, height=154, width=304, corner_radius=15)
        frame_respomses.place(x=329, y=285)

        frame_respomses1 = customtkinter.CTkFrame(
            ventana_1, height=95, width=301, corner_radius=15)
        frame_respomses1.place(x=640, y=285)

        linsheet_Id = customtkinter.StringVar()
        linsheet_id_entry = customtkinter.CTkEntry(
            frame_respomses1, height=30, width=241, corner_radius=10, textvariable=linsheet_Id, show='X')
        linsheet_id_entry.place(x=30, y=40)

        responses_button = customtkinter.CTkButton(
            ventana_1, height=48, width=301, corner_radius=15, text='', image=images["image/image 3.png"], command=response_get, fg_color='#35BD73')
        responses_button.place(x=640, y=391)

        linkSheet = customtkinter.CTkLabel(
            frame_respomses1, height=17, width=49, text='LinkSheeID', font=('Bahnschrift SemiBold', 14))
        linkSheet.place(x=30, y=10)

        csv = customtkinter.CTkLabel(frame_respomses, height=29, width=52,
                                     text='CSV', text_color='#35BD73', font=('Bahnschrift SemiBold', 24))
        csv.place(x=25, y=40)

        xlsx = customtkinter.CTkLabel(frame_respomses, height=29, width=64,
                                      text='XLSX', text_color='#35BD73', font=('Bahnschrift SemiBold', 24))
        xlsx.place(x=210, y=40)

        or_res = customtkinter.CTkLabel(
            frame_respomses, height=29, width=64, text='OR', font=('Bahnschrift SemiBold', 14))
        or_res.place(x=120, y=50)

        int_variable = customtkinter.IntVar()
        csv_radio = customtkinter.CTkRadioButton(
            frame_respomses, height=25, width=25, text='', command=response_get1, hover_color='#35BD73', variable=int_variable, value=1)
        csv_radio.place(x=40, y=100)

        xlsx_radio = customtkinter.CTkRadioButton(
            frame_respomses, height=25, width=25, text='', command=response_get1, hover_color='#35BD73', variable=int_variable, value=2)
        xlsx_radio.place(x=230, y=100)

        # ---------------------------FORMS------------------------------------------

        frame_send = customtkinter.CTkFrame(
            ventana_1, height=174, width=615, corner_radius=15)
        frame_send.place(x=326, y=487)

        form_unpload = customtkinter.StringVar()
        form_id_entry_label = customtkinter.CTkLabel(
            frame_send, text='FormID', height=17, width=49, font=('Bahnschrift SemiBold', 14))
        form_id_entry_label.place(x=40, y=10)

        form_id_entry_label = customtkinter.CTkLabel(
            frame_send, text='Fecha', height=17, width=49, font=('Bahnschrift SemiBold', 14))
        form_id_entry_label.place(x=300, y=10)

        form_id_entry = customtkinter.CTkEntry(
            frame_send, height=30, width=241, corner_radius=10, textvariable=form_unpload, font=('Bahnschrift SemiBold', 14))
        form_id_entry.place(x=40, y=35)

        fecha1 = customtkinter.StringVar()
        fecha = customtkinter.CTkEntry(frame_send, height=30, width=85, corner_radius=10, font=(
            'Bahnschrift SemiBold', 14), textvariable=fecha1)
        fecha.place(x=300, y=35)

        form_id_entry_label = customtkinter.CTkLabel(
            frame_send, text='Imagen :', height=17, width=49, font=('Bahnschrift SemiBold', 14))
        form_id_entry_label.place(x=40, y=75)

        select_image = customtkinter.CTkButton(frame_send, text='', image=images["image/foto.png"], height=48,
                                               width=241, corner_radius=15, command=ask_file, font=('Bahnschrift SemiBold', 14))
        select_image.place(x=40, y=100)

        unploadfromid = customtkinter.CTkButton(
            frame_send, height=48, width=200, corner_radius=15, text='', image=images["image/image 8.png"], command=unpload_form)
        unploadfromid.place(x=400, y=20)

        unploadimage = customtkinter.CTkButton(
            frame_send, height=48, width=301, corner_radius=15, text='', image=images["image/image 8.png"], command=unpload_image)
        unploadimage.place(x=300, y=100)

        consultforms = customtkinter.CTkLabel(
            ventana_1, height=25, width=194, text='CONSULTAR FORMULARIOS', font=('Bahnschrift SemiBold', 14))
        consultforms.place(x=326, y=27)

        consultforms = customtkinter.CTkLabel(
            ventana_1, height=25, width=194, text='DESCARGAR RESPUESTAS', font=('Bahnschrift SemiBold', 14))
        consultforms.place(x=334, y=249)

        consultforms = customtkinter.CTkLabel(
            ventana_1, height=25, width=194, text='ENVIAR FORMULARIO/ ENVIAR IMAGEN', font=('Bahnschrift SemiBold', 14))
        consultforms.place(x=334, y=454)

        ventana_1.mainloop()
    else:
        messagebox.showinfo(message='Contraseña icorrecta')


# ------------------LOGIN-----------------
login = customtkinter.CTkLabel(ventana, height=40, width=236, font=(
    'Bahnschrift SemiBold', 32), text='Inicio de Sesion', bg_color='#2A2A2A')
login.place(x=73, y=132)

login_2 = customtkinter.CTkLabel(
    ventana,  image=images["image/ergonomico1.png"], height=95, width=105, text='', bg_color='#2A2A2A')
login_2.place(x=127, y=26)

username = customtkinter.CTkLabel(frame, width=128, height=21, text='Username')
username.place(x=15, y=188)

usuario = customtkinter.StringVar()
username_entry = customtkinter.CTkEntry(
    frame, width=241, height=30, textvariable=usuario)
username_entry.place(x=45, y=209)

password = customtkinter.CTkLabel(frame, width=128, height=21, text='Password')
password.place(x=15, y=278)

contraseña = customtkinter.StringVar()
password_entry = customtkinter.CTkEntry(
    frame, width=241, height=30, textvariable=contraseña, show='x')
password_entry.place(x=45, y=299)

submi = customtkinter.CTkButton(
    frame, height=28, width=241, text='login', command=panel, font=('Bahnschrift SemiBold', 20))
submi.place(x=50, y=396)
# ---------------------------------------------
# Creado por Eduardo Barboza Acosta 
# Rev 2.0.0
ventana.mainloop()
