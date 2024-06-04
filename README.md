<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dataframe Viewer - README</title>
</head>
<body>

<h1>Dataframe Viewer</h1>
<p>Una aplicación de escritorio para visualizar y manipular DataFrames utilizando <code>customtkinter</code> y <code>pandas</code>.</p>

<h2>Instalación</h2>
<p>Para poder ejecutar esta aplicación, es necesario tener instaladas las siguientes bibliotecas de Python:</p>
<pre><code>pip install pandas customtkinter tk</code></pre>

<h2>Uso</h2>
<p>Sigue los siguientes pasos para utilizar la aplicación:</p>
<ol>
    <li>Clona este repositorio en tu máquina local:
        <pre><code>git clone https://github.com/jeremontoya155/Dataframe-Viewer.git</code></pre>
    </li>
    <li>Navega al directorio del proyecto:
        <pre><code>cd Dataframe-Viewer</code></pre>
    </li>
    <li>Ejecuta la aplicación:
        <pre><code>python app.py</code></pre>
    </li>
</ol>

<h2>Características</h2>
<ul>
    <li>Seleccionar y cargar archivos <code>.csv</code>, <code>.xlsx</code>, <code>.json</code>, y <code>.txt</code>.</li>
    <li>Mostrar el contenido del DataFrame en una vista de árbol.</li>
    <li>Eliminar columnas seleccionadas.</li>
    <li>Aplicar filtros numéricos a las columnas.</li>
    <li>Eliminar duplicados basados en una columna específica.</li>
    <li>Normalizar datos de una columna a diferentes formatos (float, int, fecha corta, fecha larga).</li>
    <li>Manejar valores nulos mediante eliminación de filas, llenado con ceros o con el promedio.</li>
    <li>Descargar el DataFrame en los formatos <code>.csv</code>, <code>.xlsx</code>, <code>.json</code> y <code>.txt</code>.</li>
</ul>

<h2>Interfaz de Usuario</h2>
<p>La interfaz de la aplicación está dividida en varias secciones:</p>
<ul>
    <li><strong>Barra Lateral:</strong> Contiene botones para seleccionar el archivo, eliminar columnas, aplicar filtros, eliminar duplicados, normalizar datos, manejar valores nulos y descargar el DataFrame.</li>
    <li><strong>Vista de Árbol:</strong> Muestra el contenido del DataFrame cargado.</li>
</ul>

<h2>Comandos y Funcionalidades</h2>
<p>Una descripción de las principales funcionalidades disponibles en la aplicación:</p>
<ul>
    <li><strong>Seleccionar Archivo:</strong> Permite cargar un archivo en formato <code>.csv</code>, <code>.xlsx</code>, <code>.json</code> o <code>.txt</code>.</li>
    <li><strong>Eliminar Columna:</strong> Elimina la columna seleccionada del DataFrame.</li>
    <li><strong>Aplicar Filtro:</strong> Filtra el DataFrame basándose en el valor numérico especificado para una columna seleccionada.</li>
    <li><strong>Eliminar Duplicados:</strong> Elimina filas duplicadas basándose en la columna seleccionada.</li>
    <li><strong>Normalizar Datos:</strong> Normaliza los datos de una columna seleccionada a diferentes formatos.</li>
    <li><strong>Manejar Valores Nulos:</strong> Permite eliminar filas con valores nulos, llenarlos con ceros o con el promedio de la columna.</li>
    <li><strong>Descargar DataFrame:</strong> Guarda el DataFrame modificado en el formato seleccionado.</li>
</ul>

<h2>Créditos</h2>
<p>Desarrollado por <a href="https://github.com/jeremontoya155">Jeremontoya155</a>.</p>

</body>
</html>
