# Pruebas realizadas

Se probaron dos formas de usar Nexo: la búsqueda de documentos y la respuesta con el modelo local. Los archivos guardan las preguntas y las respuestas obtenidas el 24 de septiembre de 2026.

## Resultado principal

- 10 preguntas con información disponible: 10 respuestas con citas válidas.
- 2 preguntas fuera del caso: el sistema indicó que no tenía información suficiente en ambas.
- Recall@4: 0.95. Se recuperó, en promedio, el 95 % de las fuentes esperadas.
- MRR: 1.00. La primera fuente relevante apareció en el primer lugar en las diez preguntas.
- Tiempo mediano de las diez consultas que generaron respuesta: 3.70 segundos, con los modelos ya cargados.

Estos resultados no significan que todas las frases sean perfectas. La revisión encontró respuestas que se podrían expresar con más precisión. Ver [revisión de respuestas](revision_respuestas.md).

## Archivos

- `evaluacion_documental.json`: resultados sin generación de texto.
- `evaluacion_llm.json`: resultados con Qwen3 4B y EmbeddingGemma.
- `consultas_adicionales.json`: seguimiento de una consulta de VPN, un plazo no definido y solicitudes que el asistente no debe ejecutar.
- `modelos_locales.json`: versión de Ollama y huellas de los modelos descargados.
- `controles_software.txt`: salida de las pruebas del programa.
- `verificacion_http.json`: comprobación del servicio web.

Se usó Ollama 0.34.4 con aceleración en una NVIDIA RTX 5080. Los modelos se ejecutaron en el equipo local. La primera ejecución incluyó la creación del índice y carga de modelos y tardó más; no se mezcló con la medición final con modelos cargados.

## Error encontrado y corregido

Al comienzo, algunas respuestas terminaban antes de tiempo o mezclaban texto de análisis con la respuesta. Se amplió el límite de generación a 2048 tokens, se separó la respuesta final y se agregó una comprobación para no mostrar respuestas cortadas. Las diez respuestas generadas de la evaluación principal tienen entre 8 y 84 palabras.

Falta una revisión independiente de Daniela y pruebas con un grupo mayor de preguntas y usuarios. No se ha medido una reducción real del tiempo de atención de una empresa.
