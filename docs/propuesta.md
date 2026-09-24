# Propuesta del proyecto

**Daniela Peña · Nexo Soporte**

## Caso elegido

El proyecto usa el caso de Servicios Andinos, una empresa ficticia de servicios profesionales. Para organizar el caso se consideran 120 trabajadores, trabajo híbrido y tres personas de soporte. Estos datos son supuestos, no cifras de una empresa donde se haya hecho un estudio.

## Problema

Las instrucciones de soporte están repartidas en varios documentos. Una persona que tiene problemas con su cuenta o su VPN debe buscar qué hacer y a quién acudir. Nexo busca reunir esa información en una consulta y mostrar el documento que respalda la respuesta.

## Objetivo

Crear un asistente que responda dudas de soporte usando documentos internos y fuentes públicas. La respuesta debe estar relacionada con lo que se encontró y debe permitir revisar su origen.

Para evaluar el proyecto se plantean estas metas:

- Recuperar al menos el 90 % de los documentos esperados en las preguntas de evaluación.
- Mostrar citas válidas en las respuestas que acepta el sistema.
- Indicar que falta información en las preguntas fuera del caso.
- En una etapa posterior, comparar el tiempo de búsqueda manual y con Nexo. La meta propuesta es reducirlo un 25 %, pero aún no se ha medido.

## Datos disponibles

Se prepararon seis procedimientos para el caso: contraseña, VPN, phishing, prioridades, alta de usuarios y MFA. Se agregaron dos resúmenes de recomendaciones de NIST y CISA, con sus enlaces originales. No se usan contraseñas ni datos personales reales.

## Límites

El asistente sólo entrega orientación. Los cambios de cuentas o permisos siguen a cargo de soporte. El modelo funciona localmente con Ollama. Antes de usarlo con información de una empresa habría que agregar permisos de acceso y revisar quién puede consultar cada documento.

## Plan de trabajo

1. Definir el caso y revisarlo con el docente.
2. Preparar los documentos y las instrucciones del modelo.
3. Implementar la búsqueda y la generación de respuestas.
4. Probar consultas, revisar errores y corregirlos.
5. Preparar el informe y ensayar la presentación.

La aprobación docente no se ha registrado. También falta confirmar la modalidad individual, ya que la pauta indica trabajo en parejas.
