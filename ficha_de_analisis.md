# Ficha de Análisis - Trivia Refactoring Kata

**Estudiante:** José Manuel Salcedo Méndez  
**Institución:** Universidad La Salle Bajío  

## 1. Olores de Código Detectados
1. **Arrays Paralelos (Data Clumps / Primitive Obsession):** Existen 4 listas vinculadas por el mismo índice entero (`players`, `places`, `purses`, `inPenaltyBox`). Esto es un grito arquitectónico pidiendo la creación de una clase `Player`.
2. **Nombres Engañosos y Poco Intuitivos:** - `places` no refleja que es la posición en el tablero (debería ser `positions`).
   - `purses` (monederos) no es tan claro como `coins`.
   - `isPlayable()` en realidad verifica si hay al menos 2 jugadores; el nombre miente sobre su intención.
3. **Métodos Demasiado Largos (Long Method):** El método `roll()` contiene demasiada complejidad ciclomática mezclando lógica de movimiento, impresión en consola, cálculo de categorías y reglas de la caja de castigo.
4. **Números Mágicos:** Valores como `11` (tamaño del tablero), `6` (monedas para ganar) y `50` (cantidad de preguntas generadas) están hardcodeados en la lógica, violando el principio de claridad.
5. **Mezcla de Responsabilidades (God Class):** `Game.java` hace de todo: maneja el estado de los jugadores, instancia e imprime el texto de las preguntas, y orquesta los turnos.

## 2. Responsabilidades que deben separarse
* **Estado del Jugador:** Una entidad `Player` debe ser dueña de su posición, sus monedas y su estado de castigo.
* **Gestión del Mazo:** Una entidad `QuestionDeck` debe encargarse de inicializar, mezclar y entregar las preguntas por categoría, aislando la lógica de las estructuras de datos (LinkedLists).
* **Orquestación del Juego:** La clase `Game` solo debe coordinar la interacción entre los `Players` y el `QuestionDeck`.

## 3. El Typo y el Bug (La trampa del Oráculo)
* **El Typo:** Existen inconsistencias de capitalización y errores ortográficos comunes en los prints originales del juego *legacy* (por ejemplo, en la impresión de categorías de Rock/Pop).
* **El Bug:** Existe una falla lógica en la caja de penalti (`Penalty Box`). Si un jugador está en la caja, tira un número par (no sale de la caja), pero el juego aún le permite ganar monedas si responde correctamente debido a la falta de aislamiento en los condicionales de `wasCorrectlyAnswered()`.