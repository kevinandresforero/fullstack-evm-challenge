# AI_PROCESS.md

## Herramientas de IA usadas

Se utilizó **OpenCode** (modelo `opencode/big-pickle`) como asistente de IA durante todo el desarrollo. Las razones:

- **Contexto largo**: permite mantener toda la sesión de trabajo sin perder el hilo.
- **Herramientas integradas**: permite ejecutar comandos, leer/escribir archivos, y hacer commits sin salir del flujo.
- **Plan explícito ("Plan Mode")**: obliga a razonar antes de escribir código, lo que fuerza la comprensión del problema.

No se usaron otras herramientas de IA (ChatGPT, Claude web, Copilot). OpenCode fue la única interfaz.

## Prompts usados (orden cronológico)

### Prompt 1 — Análisis del documento
> "Quiero que me ayudes a crear un proyecto fullstack basado en el documento técnico que te dejo disponible en /src/Ingeniero-de-Desarrollo-Trycore-Colombia.pdf..."

Este fue el prompt inicial. OpenCode intentó leer el PDF pero falló porque el modelo no soporta entrada PDF nativa. Se usó `pdftotext` para extraer el contenido.

### Prompt 2 — Propuesta de arquitectura (Fase 1)
> "Debes basarte en los requerimientos del documento, no inventar un problema distinto..."

OpenCode analizó el PDF extraído, identificó los conflictos entre mi propuesta de modelo de datos y los requerimientos del PDF, y presentó la Fase 1 con resumen, arquitectura, modelo, endpoints y estrategia de pruebas.

### Prompt 3 — Ajustes al modelo
> "1. no, los modelos de la base de datos, normalizados, sin muchos a muchos..."
> "2. Calculado."
> "3. Sin autentificación..."
> "4. mantengamoslo simple"

Ajusté la propuesta. OpenCode modificó el modelo a 3FN sin M:N, agregando `actividad_detalle` como tabla detalle.

### Prompt 4 — Implementación backend (Fase 2)
> "si"

OpenCode generó todo el backend: modelos, schemas, repositorios, servicios, EVM, routers, main.py, Alembic, scripts SQL, pruebas, configuración Ruff, README.

### Prompt 5 — Agregar remoto
> "agrega el repo a el remoto: git@github.com:kevinandresforero/fullstack-evm-challenge.git"

OpenCode configuró git, cambió a HTTPS por problemas de SSH, e hizo commit del backend.

### Prompt 6 — Frontend (Fase 3)
> (La sesión continuó con la generación del frontend Angular)

### Prompt 7 — Fallos en pruebas
> (Se corrigieron bugs en nombres de constantes y serialización Decimal)

## Cómo se aprendió EVM

EVM no lo conocía antes de este ejercicio. El proceso de aprendizaje fue:

1. **Leer el PDF**: la sección "El problema" explica la idea central: "no basta con saber cuánto has gastado ni cuánto has avanzado por separado".
2. **Preguntar a la IA**: se le pidió a OpenCode que explicara cada fórmula en contexto del dominio (proyectos).
3. **Validación manual**: antes de implementar, se verificaron los cálculos con casos concretos:
   - Proyecto de $10,000 con 50% planificado y 30% real: PV = $5,000, EV = $3,000, CPI = 0.75, SPI = 0.6.
   - Se corroboró que CPI < 1 significa sobrecosto y SPI < 1 significa atraso.
4. **Validación cruzada**: se implementaron pruebas unitarias con casos borde (AC=0, avance=0) y se verificó que los números tuvieran sentido lógico. Por ejemplo, si AC=0 y EV>0, CPI no debe calcularse (división por cero), y el proyecto parece eficiente en costos pero no se puede determinar.
5. **Pruebas de integración**: se validó el contrato completo del API para asegurar que los cálculos se reflejaran correctamente en JSON.

## Dos decisiones donde NO se siguió la sugerencia de la IA

### Decisión 1: Tipo de datos para indicadores EVM
- **IA sugirió**: usar `Decimal` de Python para todos los cálculos EVM, con `json_encoders` para serializar a float en la respuesta JSON.
- **Decisión propia**: usar `float` en el servicio EVM y en los schemas de respuesta. Razón: los `Decimal` causaban problemas de serialización a JSON (se serializaban como strings "10000.00") y complicaban el frontend. Para una herramienta interna de dashboard, la precisión de `float` (15 decimales) es suficiente. Los cálculos de BAC/PV/EV/AC se almacenan como `Decimal` en la BD (vía SQLAlchemy), pero se convierten a `float` al calcular indicadores.
- **Verificación**: todas las pruebas pasan, los valores son correctos dentro de tolerancia (`pytest.approx`).

### Decisión 2: Eliminar tabla `proyecto.presupuesto`
- **IA sugirió**: mantener `proyecto.presupuesto` como campo explícito, argumentando que "un proyecto puede tener un presupuesto distinto a la suma de actividades".
- **Decisión propia**: eliminarlo y calcularlo como `SUM(actividad.presupuesto)`. Razón: el PDF define el BAC por actividad, y no menciona un presupuesto a nivel de proyecto distinto. Mantener ambos crearía ambigüedad sobre cuál usar para EVM consolidado. El principio de fuente única de verdad (Single Source of Truth) aplica aquí.
- **Verificación**: el endpoint `GET /api/proyectos/{id}/evm` calcula `presupuesto_total` como suma de BACs, y las pruebas validan que este valor es correcto.

## Cómo se validó que los cálculos son correctos

1. **Pruebas de caja blanca**: cada método privado del `EvmService` se probó individualmente (`_calcular_pv`, `_calcular_cpi`, `_interpretar_spi`, etc.).
2. **Pruebas de integración**: 16 tests que validan el contrato HTTP completo, incluyendo valores numéricos esperados (`assert data["cpi"] == 10000.0 / 9000.0`).
3. **Casos borde**: AC=0, PV=0, avance=0, presupuesto=0, actividades vacías. Cada uno verifica que el sistema no explota y que los None/null se manejan correctamente.
4. **Validación semántica**: CPI > 1 = bajo presupuesto, CPI < 1 = sobre presupuesto. SPI > 1 = adelantado, SPI < 1 = atrasado. Se verificó contra ejemplos concretos con números redondos.

## Decisión de arquitectura independiente

**Separación de `EvmService` como clase sin dependencias de infraestructura.**

OpenCode inicialmente propuso que el `EvmService` recibiera dependencias del repositorio para cargar actividades automáticamente. Decidí que el servicio recibiera las `Actividad` como argumento en lugar de inyectar repositorios. Esto permite:

- Probar el cálculo EVM sin base de datos (pasar actividades en memoria).
- Reutilizar el mismo servicio para calcular indicadores de una sola actividad o de un proyecto completo.
- Mantener el servicio puro (sin efectos secundarios), facilitando el testing y la comprensión.

Además, se agregó el `@app.exception_handler` para estandarizar errores HTTP, y se definió `BaseRepository` genérico para evitar duplicación de CRUD en los repositorios específicos.

## Reflexión honesta

Si repitiera el ejercicio, haría tres cosas diferente:

1. **Planificar la serialización Decimal desde el inicio.** Perdí tiempo debuggeando por qué los valores Decimal se serializaban como strings en JSON. Si hubiera definido desde la Fase 1 que los schemas de respuesta EVM usarían `float`, me habría ahorrado dos iteraciones de código.

2. **Probar el build de Angular antes de diseñar componentes complejos.** El problema con `browserslist` en Node 24 me tomó por sorpresa y consumió tiempo valioso que debía ir a diseño de UI. Debería haber validado que el toolchain completo funcionaba antes de escribir los componentes del dashboard.

3. **Dedicar más tiempo al diseño visual del frontend.** El dashboard funciona y muestra los datos correctamente, pero visualmente es básico. Para una herramienta de líderes de proyecto que necesitan "entender de un vistazo si el proyecto va bien o mal", vale la pena invertir en:
   - Un diseño más cuidado de tarjetas de indicadores.
   - Gráficas más informativas (ej. línea de tendencia de CPI a través del tiempo si hubiera datos históricos).
   - Un layout responsive para tablets.

En general, el backend quedó sólido: 58 tests, cobertura >80% en servicios, capas bien separadas, sin magic strings, sin code smells. El frontend es funcional y muestra los indicadores EVM correctamente, pero el pulido visual es el área con más margen de mejora.

Lo que mejor funcionó fue la dinámica de trabajo con OpenCode en modo plan: primero razonar, después codificar. La Fase 1 (plan) fue donde se tomaron las decisiones más importantes y donde se detectaron los conflictos del modelo de datos. Saltarse ese paso habría resultado en retrabajo.
