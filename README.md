# Simulacros UADE 2C 2026

Simulacros de examen para los finales de Programación III, Ingeniería de Software, Dirección de Proyectos de Tecnología e Ingeniería de Datos II.

**Página:** https://juanmanuelcastelo.github.io/simulacros-uade/

## Cómo está armado
- `index.html` es la página. Al abrirse carga el banco de preguntas desde `banco.json`.
- `banco.json` tiene las preguntas de cada materia. Las de opción múltiple tienen 4 opciones, la correcta y su explicación; las abiertas tienen los puntos de la respuesta modelo. Cada pregunta guarda de qué apunte salió (`fuente`) y cuándo se agregó.
- `scripts/agregar.py nuevas.json` suma preguntas nuevas al banco. Valida el formato, descarta las repetidas y rechaza las preguntas donde la respuesta correcta se nota por ser mucho más larga que las demás.

La tarea diaria del segundo cerebro agrega preguntas de los apuntes nuevos del campus y publica el cambio acá. GitHub Pages actualiza la página sola.

## Sin conexión y repaso de puntos débiles

- La página se puede instalar en el celular (Agregar a inicio) y funciona sin conexión: `sw.js` guarda la página y `banco.json`, y cuando hay red baja el banco actualizado.
- Cada pregunta tiene un `tema` (unidad). El resultado de cada pregunta queda guardado en el navegador; cada materia muestra el porcentaje de aciertos por unidad, permite practicar una unidad y repasar solo lo que fallaste. En los simulacros completos, las falladas salen más seguido.
- `scripts/agregar.py` acepta `"tema"` en cada bloque; si falta, usa `"fuente"`.
