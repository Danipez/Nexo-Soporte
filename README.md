# Nexo Soporte

**Daniela Peña y Mirko Flores · Ingeniería de Soluciones con IA · ISY0101**

Nexo es un asistente para resolver dudas frecuentes de soporte: problemas con la contraseña, conexión VPN, correos sospechosos y acceso a cuentas. Busca información en los documentos del proyecto y muestra de dónde salió la respuesta.

El caso se basa en **Servicios Andinos**, una empresa ficticia. Los procedimientos internos se prepararon para este caso. También se usan recomendaciones públicas de NIST y CISA sobre seguridad.

## Cómo abrirlo

En el equipo donde quedó instalado, abre **`iniciar.cmd`**. Después entra a **http://127.0.0.1:8765**.

Hay dos opciones en la pantalla:

- **Consulta documental:** muestra lo que dicen los documentos, sin generar una respuesta nueva.
- **Asistente LLM local:** usa el modelo para responder con la información encontrada. Esta es la opción para probar el RAG completo.

El acceso directo abre el navegador y deja Nexo en segundo plano. Si lo inicias desde una terminal con `python -m nexo --serve`, puedes detenerlo con `Ctrl+C`. Los modelos pueden tardar más en responder la primera vez que se cargan.

## Qué puedes preguntar

Prueba estas consultas y abre las fuentes debajo de cada respuesta:

1. «Olvidé la contraseña, ¿cómo recupero el acceso?»
2. «¿Qué reviso si falla mi conexión VPN?»
3. «¿Cómo reporto un correo sospechoso de phishing?»
4. «¿Cuál es la capital de Finlandia?»

La última pregunta está fuera de los documentos. El asistente debería indicar que no tiene información suficiente. Usa **Nueva conversación** cuando quieras cambiar de tema y borrar el historial.

## Instalarlo en otro equipo

Necesitas Python 3.11 o superior. Para usar el modelo también necesitas Ollama y espacio para descargar varios GB.

En Windows, desde esta carpeta:

```powershell
.\scripts\instalar_ollama.ps1
.\iniciar.cmd
```

El script descarga Ollama desde su distribución oficial. Los programas y modelos quedan en `.runtime`, que no se sube a GitHub.

Si ya tienes Ollama instalado:

```console
ollama pull qwen3:4b
ollama pull embeddinggemma
python -m nexo --serve
```

Para usar sólo la consulta documental basta con `python -m nexo --serve`. No necesitas instalar paquetes de Python.

## Cómo funciona

Primero se divide el texto de los documentos en fragmentos. Luego se buscan los más relacionados con la pregunta. La búsqueda combina palabras clave con embeddings, que son representaciones numéricas del texto. El modelo recibe esos fragmentos y prepara la respuesta con sus citas.

Se guardan sólo las últimas tres preguntas de la conversación. El botón **Descargar evidencia** permite guardar la consulta, la respuesta y las fuentes en un archivo JSON.

El [diagrama](docs/arquitectura.svg) muestra el recorrido de la consulta.

## Archivos del proyecto

- [Informe técnico editable](docs/informe_tecnico_DanielaPeña_MirkoFlores_014V.docx).
- [Presentación](docs/presentacion.pptx).
- [Código del asistente](nexo/).
- [Documentos de consulta](data/corpus.json).
- [Diagrama](docs/arquitectura.svg).
- [Resultados de las pruebas](evidencias/).

## Volver a ejecutar las pruebas

```console
python -m unittest discover -s tests -v
python scripts/evaluar.py
python scripts/evaluar.py --mode llm
```

El último comando necesita Ollama activo. Los resultados se guardan en `evidencias`. Las pruebas con respuestas controladas revisan partes del programa; las consultas de `evaluacion_llm.json` se ejecutan con el modelo real.

## Qué falta mejorar

Una cita válida no asegura que toda la respuesta sea correcta. Por eso hay que leer las fuentes, sobre todo cuando se consultan plazos o permisos. El conjunto de preguntas es pequeño y todavía falta probar el sistema con más usuarios y documentos.

Nexo no cambia contraseñas, no crea cuentas y no abre tickets. Funciona en el equipo local. Antes de usarlo en una empresa habría que agregar acceso por usuario y permisos para los documentos.

El proyecto toma como referencia los temas de RAG y evaluación del [material del curso](https://github.com/davila7/Ingenier-a-de-Soluciones-con-Inteligencia-Artificial), en RA1/IL1.3 e IL1.4. El código de Nexo se desarrolló por separado.
