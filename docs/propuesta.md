# Propuesta de caso organizacional

## Organización
Servicios Andinos: organización contextualizada de servicios profesionales. Se asumen 120 colaboradores, trabajo híbrido y tres personas de soporte. Estos valores delimitan el escenario y no son datos levantados en una empresa real.

## Problema
Las instrucciones de soporte se distribuyen entre procedimientos y documentos de seguridad. El colaborador necesita identificar la fuente vigente y distinguir instrucciones generales de reglas internas. La propuesta aborda consultas repetidas sobre contraseñas, VPN, phishing, permisos y MFA. No se dispone de una medición inicial de tiempo de atención.

## Objetivo general
Implementar un asistente de consulta que recupere evidencia interna y externa y entregue orientación trazable para solicitudes frecuentes de soporte TI.

## Objetivos medibles
1. Alcanzar Recall@4 de al menos 0,90 sobre el conjunto inicial de consultas etiquetadas.
2. Incorporar identificadores de evidencia verificables en todas las respuestas generadas aceptadas por el validador.
3. Abstenerse en las dos consultas fuera de cobertura del conjunto inicial.
4. Evaluar en un piloto posterior una reducción del tiempo mediano de búsqueda de al menos 25 %, comparando búsqueda manual y asistida con las mismas tareas. Esta meta no representa un resultado obtenido.

## Datos
Seis políticas internas contextualizadas y dos síntesis externas de NIST/CISA. Metadatos: ID, título, responsable, versión, fecha, tipo y URL. Se calcula SHA-256 sobre el texto. No se incorporan tickets reales, contraseñas ni datos personales.

## Alcance y restricciones
Consulta de sólo lectura. Modelos locales mediante Ollama. Revisión humana para incidentes y cambios de acceso. Las fuentes externas complementan recomendaciones de seguridad, sin reemplazar los canales internos. El uso institucional requiere autenticación y permisos por documento antes del despliegue.

## Viabilidad
La consulta documental funciona con Python estándar. La generación requiere un equipo que pueda ejecutar los modelos seleccionados y almacenamiento para descargarlos. El agente utiliza un flujo acotado de recuperación, generación y verificación, sin delegar acciones administrativas al modelo.

## Revisión docente
Estado: pendiente de presentación y retroalimentación. No se registra una aprobación que no ha sido proporcionada. Antes del desarrollo definitivo del encargo deben confirmarse el caso y los ajustes con el docente, tal como exige la pauta.

## Plan de cinco semanas
Semana 1: delimitación y revisión del caso. Semana 2: corpus y prompts. Semana 3: integración del recuperador y del LLM. Semana 4: evaluación y correcciones. Semana 5: informe, ensayo y entrega. Es una planificación propuesta, no un registro retrospectivo de trabajo.

Referencias: fuentes en `corpus.json`, documentación oficial de Ollama y material RA1 del curso.
