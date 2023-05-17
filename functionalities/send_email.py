import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(destinatario,titulo,fecha,id_compra):
    # Configuración del servidor SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'fokameca@gmail.com'
    sender_password = 'jutsriydmyjjtfuj'

    # Creación del mensaje de correo electrónico
    message = MIMEMultipart('alternative')
    message['Subject'] = 'CONFIRMACIÓN DE COMPRA'
    message['From'] = sender_email
    message['To'] = destinatario

    # Contenido HTML del correo electrónico
    html_content = """
    <html>
    <body>
       <div class="container_resume">
        <h1>¡Gracias por tu compra!</h1>

        <div class="order-details">
        <div class="image" id="game_image">
            <img src="https://i.ibb.co/VvXpQYP/Formato-de-Videojuego.jpg" alt="Game Image">
        </div>
        <div class="info">
            <div class="title" id="game_title">{}</div>
            <div class="purchase-date" id="purchase_date">Fecha de compra: {}</div>
            <div class="order-id" id="order_id">ID de compra: {}</div>
        </div>
        </div>
    </div>
    </body>
    </html>
    """.format(titulo,fecha,id_compra)

    # Adjuntar el contenido HTML al mensaje
    message.attach(MIMEText(html_content, 'html'))

    try:
        # Establecer conexión con el servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Enviar el correo electrónico
        server.sendmail(sender_email, destinatario, message.as_string())

        print('El correo electrónico ha sido enviado correctamente.')

    except Exception as e:
        print('Error al enviar el correo electrónico:', str(e))


enviar_correo('manuel.silva@utec.edu.pe','titulo','fecha', 'idcompra')