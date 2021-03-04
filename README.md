# Tarea3
 
# Modelación y Computación Gráfica para Ingenieros
CC3501-1 - Primavera 2020
 
# Simulación de pandemia en 2D
## Controles
- KEY_RIGHT : Avanzar a la siguiente iteración (o frame, solo en modo de visualización frame_by_frame)
- P : Pausa/Reanuda la animación y muestra un gráfico circular en matplotlib
## Parámetros agregados en virus.json
 -Parámetro agregado: Days_to_get_infected, que indica la cantidad de días que deben pasar para que una partícula vuelva a contagiarse luego de recuperarse.
 -Segundo parámetro agregado: Go_to_center_prob, que indica la probabilidad de que una partícula vaya al centro en un día.
 -Tercer parámetro agregado: Visualization_mode, que permite ver la simulación en tiempo real o frame a frame. Si Visualization_mode tiene el valor "continuo" entonces la simulación no se verá apretando la tecla KEY_RIGHT para avanzar a la siguiente iteración, ya que éstas avanzan automáticamente.
