import qrcode
import pandas as pd
import os
import uuid

def generar_qr(nombre, apellido, base_url):
    """
    Genera un código QR personalizado para una persona.
    
    Parámetros:
    - nombre: Nombre de la persona.
    - apellido: Apellido de la persona.
    - base_url: URL base de la página web alojada.
    
    Retorna:
    - nombre_archivo: Nombre del archivo PNG del QR generado.
    - url_personalizada: URL completa que contiene los parámetros.
    """
    # Codificar los parámetros para la URL
    nombre_encoded = nombre.replace(' ', '%20')
    apellido_encoded = apellido.replace(' ', '%20')
    url_personalizada = f"{base_url}?nombre={nombre_encoded}&apellido={apellido_encoded}"

    # Crear el objeto QRCode
    qr = qrcode.QRCode(
        version=1,  # controla el tamaño del QR
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url_personalizada)
    qr.make(fit=True)

    # Crear la imagen del QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Generar un ID único para el archivo QR
    unique_id = uuid.uuid4().hex[:8]  # 8 caracteres únicos
    nombre_archivo = f"{nombre}_{apellido}_{unique_id}.png"

    # Guardar la imagen
    img.save(nombre_archivo)

    return nombre_archivo, url_personalizada

def guardar_en_excel(registro, archivo_excel="qr_records.xlsx"):
    """
    Guarda el registro de la persona en un archivo Excel.
    
    Parámetros:
    - registro: Diccionario con la información de la persona.
    - archivo_excel: Nombre del archivo Excel donde se guardarán los registros.
    """
    df_new = pd.DataFrame([registro])
    
    if os.path.exists(archivo_excel):
        try:
            df_existing = pd.read_excel(archivo_excel)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except Exception as e:
            print(f"Error al leer el archivo Excel existente: {e}")
            return
    else:
        df_combined = df_new
    
    try:
        df_combined.to_excel(archivo_excel, index=False)
        print(f"Registro guardado en {archivo_excel}.")
    except Exception as e:
        print(f"Error al guardar en Excel: {e}")

def main():
    """
    Función principal para ingresar datos, generar QRs y guardar registros.
    """
    # Reemplaza esta URL con la URL de tu página web alojada
    base_url = "https://itsvaalentine.github.io/QRGenerator/root/l"  # Ejemplo de GitHub Pages

    archivo_excel = "qr_records.xlsx"
    
    # Crear el archivo Excel con encabezados si no existe
    if not os.path.exists(archivo_excel):
        df_initial = pd.DataFrame(columns=["Nombre", "Apellido", "Telefono", "Archivo QR", "URL QR"])
        df_initial.to_excel(archivo_excel, index=False)
        print(f"Archivo {archivo_excel} creado.")
    
    # Número máximo de QRs a generar
    max_qrs = 400
    current_qrs = 0
    
    while current_qrs < max_qrs:
        print(f"\n--- Generación de QR {current_qrs + 1} de {max_qrs} ---")
        nombre = input("Ingrese el nombre de la persona (o 'salir' para terminar): ").strip()
        if nombre.lower() == 'salir':
            break
        
        apellido = input("Ingrese el apellido de la persona (o 'salir' para terminar): ").strip()
        if apellido.lower() == 'salir':
            break
        
        telefono = input("Ingrese el número de teléfono (en formato +[código país][número], o 'salir' para terminar): ").strip()
        if telefono.lower() == 'salir':
            break
        
        if not nombre or not apellido or not telefono:
            print("Nombre, apellido o teléfono vacío. Por favor, intente nuevamente.")
            continue
        
        # Validar formato del número de teléfono
        if not telefono.startswith('+') or not telefono[1:].isdigit():
            print("Formato de teléfono inválido. Debe comenzar con '+' seguido del código de país y número.")
            continue
        
        # Generar el QR
        try:
            archivo_qr, url_qr = generar_qr(nombre, apellido, base_url)
            print(f"Código QR generado: {archivo_qr}")
            print(f"URL del QR: {url_qr}")
        except Exception as e:
            print(f"Error al generar el QR: {e}")
            continue
        
        # Crear el registro
        registro = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Telefono": telefono,
            "Archivo QR": archivo_qr,
            "URL QR": url_qr
        }
        
        # Guardar en Excel
        try:
            guardar_en_excel(registro, archivo_excel)
        except Exception as e:
            print(f"Error al guardar en Excel: {e}")
            continue
        
        current_qrs += 1
    
    print("\nProceso completado.")
    print(f"Se han generado {current_qrs} códigos QR.")

if __name__ == "__main__":
    main()
