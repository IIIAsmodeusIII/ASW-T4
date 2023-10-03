### Tarea 4 - Arquitectura de Software

## Integrantes
1. Constanza Alvarado Valenzuela | 201975521-7
2. Bruno Vega Pizarro | 201854051-k

## Instrucciones de ejecución:
1. Instalar requisitos: Python 3.7+, uvicorn, fastapi, pillow.
2. Ejecutar: python -m uvicorn main:app --reload

## Consideraciones
1. Se ejecuta en http://127.0.0.1:8000/
2. La API consta de la entrada en " http://127.0.0.1:8000/farms/ " la cual no cuenta con más salida que un json en pantalla con "API: Farm"
3. La API consta con el recurso granjas solo por id: http://127.0.0.1:8000/farms/ID , donde ID corresponde a un valor de los siguientes: "ABF39A", "ABF39B", "ABF39C". Cada una dará render por pantalla de la granja.
4. Los datos son asumidos a partir de comunicación con la api correspondiente de construcciones en granja. Detalles se encuentran en response.json.

## Detalles del render 
1. Separa la tierra construida de la posible a construir con pasto y tierra respectivamente.
2. La tierra lista para sembrar posee un color de tierra distintivo
3. La tierra regada es oscurecida
4. Existen 3 estados para cada plantación: Semilla (1 o 2 días), en crecimiento (Más de 2 días) y lista para cosechar. Este último estado posee un ícono de instrumento de cosecha sobre el cultivo listo.
