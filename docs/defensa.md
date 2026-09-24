# Defensa oral

La pauta asigna 20 minutos: 10 de exposición y 10 de preguntas. Expositora: Daniela Peña. La pauta original solicita parejas; confirmar con el docente la modalidad individual.

| Tiempo | Responsable | Contenido |
|---|---|---|
| 0:00-1:00 | Daniela Peña | Organización contextualizada, problema y alcance |
| 1:00-2:00 | Daniela Peña | Objetivos y fuentes internas/externas |
| 2:00-3:30 | Daniela Peña | Arquitectura y recuperación |
| 3:30-5:00 | Daniela Peña | Prompt operativo, controles y contexto |
| 5:00-7:00 | Daniela Peña | Demostración de phishing, fuentes y consulta sin evidencia |
| 7:00-8:15 | Daniela Peña | Resultados de recuperación y alcance de la medición |
| 8:15-9:15 | Daniela Peña | Decisiones técnicas propias y limitaciones |
| 9:15-10:00 | Daniela Peña | Conclusiones propias y siguientes pasos |
| 10:00-20:00 | Daniela Peña | Preguntas y revisión del código |

## Demostración reproducible
1. Ejecutar `python -m nexo --serve` y abrir la interfaz.
2. Consultar «¿Cómo reporto un correo sospechoso de phishing?». Abrir las fuentes y localizar el procedimiento interno y la referencia externa.
3. Explicar que el modo documental presenta extractos exactos. Repetir con Asistente LLM local y comparar cada afirmación con la evidencia.
4. Consultar «¿Cuál es la capital de Finlandia?». Mostrar la abstención por ausencia de evidencia.
5. Reiniciar conversación, preguntar por una falla de VPN y luego «¿Y cuánto demora?». Mostrar la consulta expandida en el JSON descargado.
6. Abrir `evidencias/evaluacion_documental.json` para demostrar la procedencia de las métricas.

## Preguntas para preparar con respuestas propias
- ¿Qué parte requiere un LLM y qué parte funciona sin él?
- ¿Por qué se eligieron esos tamaños de fragmento? ¿Qué cambiaría con documentos largos?
- ¿Qué diferencia hay entre Recall@4 y fidelidad de una respuesta?
- ¿Qué puede salir mal si una cita existe pero no respalda la afirmación?
- ¿Cómo impedirías que un colaborador recupere documentos de otra área?
- ¿Qué dato necesitas para afirmar una reducción real del tiempo de soporte?
- ¿Cómo se detecta una política interna desactualizada?
- ¿Qué evidencia permite distinguir un resultado ejecutado de una meta futura?
- ¿Por qué usar RRF y cómo calibrarías el umbral semántico?
- ¿Cuáles fueron tu contribución y tu aprendizaje concreto?

Evitar afirmar que hay integración con tickets, usuarios reales, reducción de tiempos si no se cuenta con evidencia adicional. El modelo local ya cuenta con resultados en evaluacion_llm.json.
