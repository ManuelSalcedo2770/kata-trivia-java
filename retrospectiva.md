# Retrospectiva: Del Código Feo al Orgullo Profesional

**Estudiante:** José Manuel Salcedo Méndez  

## 1. Sobre la técnica del Golden Master
**¿En qué momento te sentiste seguro de que el Golden Master cubría lo suficiente?**
Inmediatamente después de entender que el test ejecuta 10,000 partidas con semillas aleatorias (`Random`). Estadísticamente, esto asegura que prácticamente todas las ramas y flujos de ejecución posibles del monolito son evaluadas contra el oráculo (`GameOld.java`).

**¿Hubo algún cambio que el Golden Master no pudo detectar como peligroso?**
Sí, el bug de la caja de penalti. El Golden Master es ciego ante los errores de lógica de negocio si el archivo de referencia (`GameOld.java`) contiene el mismo error. A esto se le llama "La trampa del oráculo corrupto". Para corregirlo sin romper la integración continua, tuve que aplicar la solución primero en el código de producción, y luego deliberadamente replicar la corrección en `GameOld.java`.

**¿Por qué no escribir tests unitarios durante la refactorización?**
Escribir tests unitarios sobre un diseño acoplado requiere el uso masivo de *Mocks* y congela el mal diseño, haciendo que refactorizar sea el doble de difícil. El Golden Master provee una red externa, permitiendo "destruir" la estructura interna del código (extraer clases, cambiar firmas) sin modificar ni un solo test.

## 2. Sobre la refactorización
**¿Qué olor de código fue el más difícil de eliminar?**
La eliminación de los Arrays Paralelos. Mover `places`, `purses` e `inPenaltyBox` a una clase `Player` requirió extrema granularidad en los commits, ya que cambiar un índice por un objeto rompía el acceso a la memoria en casi todos los métodos de `Game.java`.

**¿Qué refactorización manual fue la más arriesgada?**
La desfragmentación del método `roll()`. Extraer la lógica a `handleNormalTurn` y `handlePenaltyBoxTurn` requirió entender profundamente la jerarquía original de los `if/else` para asegurar que el orden de impresión en consola fuera bit a bit idéntico al original.

## 3. Implementación de un nuevo requisito
**Requisito añadido:** Nueva categoría "Geography".  
**Dificultad evaluada:** Muy Fácil.

**Explicación del impacto en la arquitectura:**
En el código *legacy* original, añadir una categoría habría implicado:
1. Crear una nueva `LinkedList`.
2. Añadir un bucle `for` de 50 iteraciones para llenarla.
3. Modificar la lógica matemática en `currentCategory()` y `askQuestion()`.

En mi código final refactorizado, gracias a la extracción de `QuestionDeck` y la aplicación del principio Open/Closed (OCP), la integración tomó menos de 5 minutos y se limitó a **una sola modificación**: registrar "Geography" en el mapa de inicialización del `QuestionDeck`. El orquestador del juego (`Game`) no sufrió ninguna alteración. Esto demuestra que la cohesión es alta y el acoplamiento es mínimo.