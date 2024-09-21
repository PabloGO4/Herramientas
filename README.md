
# Colección de Utilidades en Python

Una colección de scripts de Python para diversas utilidades, que incluyen manejo de correos electrónicos (IMAP y SMTP), integración con MySQL, lectura de PDFs, scraping web, manipulación de documentos Word y análisis de datos con Pandas. Estos scripts están diseñados para ser modulares, reutilizables y fáciles de integrar en diversos proyectos.

## Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
  - [Manejo de Correos Electrónicos](#manejo-de-correos-electrónicos)
  - [Integración con MySQL](#integración-con-mysql)
  - [Lector de PDF](#lector-de-pdf)
  - [Scraping Web](#scraping-web)
  - [Manipulación de Documentos Word](#manipulación-de-documentos-word)
  - [Utilidades de Pandas](#utilidades-de-pandas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Características

- **Manejo de Correos Electrónicos**:
  - `Email.py`: Envía correos utilizando SMTP.
  - `EmailImap.py`: Obtiene correos utilizando IMAP.
  - `EmailSmtp.py`: Configurado para enviar correos de manera segura.

- **Operaciones de Base de Datos**:
  - `MySQL.py`: Proporciona métodos para conectarse y ejecutar consultas MySQL.

- **Procesamiento de Datos**:
  - `Pandas.py`: Funciones utilitarias para trabajar con DataFrames de Pandas.

- **Manejo de Documentos**:
  - `PDFReader.py`: Lee y extrae texto de archivos PDF.
  - `Word.py`: Manipula documentos de Word (ej., lectura y escritura de contenido).

- **Manejo Web**:
  - `Web.py`: Funciones utilitarias para hacer solicitudes HTTP, scraping web, etc.

- **Utilidades de Windows**:
  - `Win.py`: Funciones para tareas específicas de Windows.

## Instalación

Para usar estos scripts, clona el repositorio:

```bash
git clone https://github.com/tuusuario/python-utilities.git
cd python-utilities
```

Luego, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

### Manejo de Correos Electrónicos

#### Envío de Correo utilizando SMTP

```python
from EmailSmtp import enviar_correo

enviar_correo('destinatario@ejemplo.com', 'Asunto', 'Cuerpo del correo', 'adjunto.pdf')
```

#### Obtención de Correos utilizando IMAP

```python
from EmailImap import obtener_correos

correos = obtener_correos('inbox')
for correo in correos:
    print(correo.asunto)
```

### Integración con MySQL

```python
from MySQL import ejecutar_consulta

ejecutar_consulta('SELECT * FROM usuarios')
```

### Lector de PDF

```python
from PDFReader import leer_pdf

texto = leer_pdf('documento.pdf')
print(texto)
```

### Scraping Web

```python
from Web import hacer_solicitud

respuesta = hacer_solicitud('https://ejemplo.com')
print(respuesta.contenido)
```

### Manipulación de Documentos Word

```python
from Word import leer_word

contenido = leer_word('documento.docx')
print(contenido)
```

### Utilidades de Pandas

```python
from Pandas import cargar_csv

df = cargar_csv('datos.csv')
print(df.head())
```

## Contribuir

1. Haz un fork del repositorio.
2. Crea una nueva rama: `git checkout -b caracteristica/tu-caracteristica`.
3. Haz commit de tus cambios: `git commit -m 'Agrega tu característica'`.
4. Haz push a la rama: `git push origin caracteristica/tu-caracteristica`.
5. Envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
