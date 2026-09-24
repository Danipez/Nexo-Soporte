# Especificación técnica

## Requerimientos y criterios de aceptación

| Requerimiento | Comportamiento implementado | Verificación |
|---|---|---|
| Consultas de soporte contextualizadas | Corpus de acceso, VPN, seguridad y prioridades | Consultas C01-C10 |
| Fuentes internas y externas | Ocho documentos tipificados y con responsable | C03 y control de mezcla de fuentes |
| Trazabilidad | ID del fragmento, versión, hash y URL | Exportación de consulta y validación de citas |
| Control de contexto | Máximo 1000 caracteres de consulta, últimas 3 preguntas, evidencia hasta 6500 caracteres | Controles de tamaño y continuidad |
| Manejo de desconocimiento | Sin evidencia o revisión requerida | C11-C12 y respuestas sin cita |
| Protección de información | Modelo local, sin registros automáticos de preguntas | Revisión del servidor y del cliente |

## Recuperación

El archivo JSON actúa como registro de documentos. La fragmentación conserva ventanas de 110 palabras con 20 de solapamiento; el solapamiento previene cortes de instrucciones en documentos más largos. El corpus inicial produce un fragmento por documento. Los IDs combinan documento y posición inicial. BM25 utiliza k1=1,5 y b=0,75, con normalización de tildes y eliminación de palabras funcionales.

En modo LLM, `embeddinggemma` representa cada título y fragmento. Una consulta genera su vector y el sistema calcula similitud coseno. La fusión por rangos recíprocos usa RRF(d)=1/(60+rango_BM25)+1/(60+rango_vectorial). Son elegibles documentos con BM25 positivo o coseno de al menos 0,45. Se conservan cuatro. El umbral es un parámetro inicial, no una probabilidad de exactitud. Una mejora pendiente es calibrar umbrales y relevancia con un corpus independiente y consultas ambiguas.

La caché vincula vectores con modelo y huella del corpus. Si cambia cualquiera, se reconstruye. Se omite del repositorio. Para un corpus grande se necesitaría un almacén vectorial y búsquedas aproximadas. El tamaño actual permite comparación exacta en memoria.

## Orquestación y generación

Flujo determinista: validar consulta, resolver referencia breve, recuperar, construir contexto, generar y comprobar citas. Este agente de consulta no planifica acciones abiertas ni posee herramientas de modificación de cuentas. La interfaz distingue expresamente la consulta documental del modo generativo.

`qwen3:4b` es el modelo propuesto para generación local. Configuración: temperatura 0,1, ventana 8192 tokens y salida máxima de 450 tokens. Los límites previos se expresan en caracteres y no equivalen a un contador de tokens. Debe verificarse el ajuste del contexto con los modelos descargados. El texto de razonamiento interno, si existe, no se utiliza como evidencia.

## Catálogo de prompts

**P0, referencia de comparación:** «Responde la pregunta del usuario sobre soporte TI». Carece de límites de evidencia, salida o atribución. No se ejecutó una comparación generativa con P0.

**P1, versión operativa:** el texto exacto se encuentra en `nexo/core.py`, constante `SYSTEM`. Establece el rol, fuentes permitidas, prioridad normativa interna, protección de secretos, forma de citar y límite de respuesta. Incluye dos ejemplos: consulta respondible con cita y consulta fuera de cobertura.

**Mensaje de consulta:** JSON con `HISTORIAL`, `EVIDENCIA` y `CONSULTA`. Cada evidencia incluye tipo, título e identificador. El historial no constituye una fuente. Los documentos pueden contener instrucciones maliciosas, por lo que el mensaje de sistema ordena tratarlos como datos; esto reduce el riesgo pero no elimina la inyección de prompts.

**Experimento propuesto:** ejecutar las mismas consultas con P0 y P1, mantener modelo/temperatura/corpus y etiquetar por afirmación: respaldada, contradicha o no demostrable. Comparar fidelidad, cobertura y abstención con dos revisores. Registrar discrepancias. No presentar esta comparación como realizada.

## Contexto y trazabilidad

La pestaña conserva hasta tres preguntas y se reinicia con Nueva conversación. Sólo una consulta corta con referencia anafórica incorpora la anterior al buscador. El modelo recibe las preguntas previas truncadas a 500 caracteres. Las respuestas anteriores no se reutilizan como hechos.

El JSON descargable conserva consulta, consulta expandida, fuentes, modo, respuesta, estado, timestamp UTC y huella del corpus. Su descarga es explícita: no hay almacenamiento automático de las conversaciones. El hash identifica cambios, pero no prueba que el documento sea correcto ni que su autor sea legítimo.

## Riesgos y operación

| Riesgo | Control actual | Pendiente antes de producción |
|---|---|---|
| Respuesta inventada con cita válida | Evidencia delimitada y fuentes visibles | Evaluación humana y comprobación semántica |
| Inyección en documentos | Fuentes curadas y regla de tratar contexto como datos | Casos adversarios y revisión de cambios |
| Acceso indebido | Sólo localhost, sin documentos privados | Inicio de sesión y autorización previa a recuperación |
| Política desactualizada | Versión, fecha y responsable explícitos | Calendario de revisión y caducidad |
| Modelo indisponible | Error visible y modo documental | Supervisión y tiempos de espera ajustados |
| Recuperación incompleta | Métricas por consulta y top 4 visible | Corpus representativo, sinónimos y ajuste de parámetros |

El servidor HTTP es de uso local y atiende secuencialmente. No se ofrece como servicio multiusuario. La descarga de modelos es un requisito externo; no se declara una instalación que no se ejecutó. El enfoque local evita enviar el corpus a un proveedor de inferencia remoto.

## Evaluación

Recall@4 = número de documentos relevantes recuperados / número de documentos relevantes esperados. MRR promedia el inverso del primer rango relevante. Se calculan sobre diez consultas positivas. Abstención se calcula sobre dos negativas. Los tiempos reportados corresponden a búsqueda y composición documental local, sin inferencia ni acceso de red.

`evidencias/evaluacion_documental.json` contiene las entradas, resultados y métricas efectivamente calculadas. El conjunto es pequeño y fue diseñado a partir del corpus, por lo que favorece consultas conocidas. No se usa como garantía de generalización. La fidelidad generativa y el beneficio organizacional permanecen pendientes.

## Fuentes

- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*, 9459-9474. https://arxiv.org/abs/2005.11401
- National Institute of Standards and Technology. (s. f.). *Phishing*. https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/phishing
- Cybersecurity and Infrastructure Security Agency. (s. f.). *Require multifactor authentication*. https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/require-multifactor-authentication
- Ollama. (s. f.). *Generate a chat message*. https://docs.ollama.com/api/chat
- Ollama. (s. f.). *Generate embeddings*. https://docs.ollama.com/api/embed

Las justificaciones definitivas del informe y las reflexiones individuales requieren redacción y validación del equipo, según la pauta del encargo.
