# Eraser Bot – Pizarrón Inteligente  

## Idea principal  

El proyecto **Eraser Bot** busca desarrollar un **pizarrón inteligente** capaz de **digitalizar automáticamente** lo que se escribe en él y **borrarse de forma autónoma**.  

Gracias a sensores de movimiento y un sistema de borrado impulsado por un motor paso a paso, el pizarrón se convierte en una **alternativa eficiente, económica y de fácil mantenimiento** frente a los pizarrones digitales actuales.  

El objetivo es **mejorar la experiencia en aulas y entornos de trabajo**, optimizando la digitalización, almacenamiento y limpieza del contenido en pizarras.  

---

## Problemática  

Los pizarrones digitales en escuelas y oficinas presentan varios problemas:  

- Suelen ser **costosos y difíciles de mantener**.  
- Muchos quedan en **desuso por fallos constantes**.  
- Los pizarrones tradicionales requieren **transcripción manual** del contenido.  
- El borrado manual consume tiempo y genera **distracciones** durante clases o reuniones.  

Eraser Bot busca resolver estas limitaciones con una solución **accesible, eficiente y automática**.  

---

## Justificación  

Este proyecto se justifica en la necesidad de contar con **herramientas accesibles y confiables** que fomenten la colaboración y el aprendizaje.  

- Los pizarrones actuales no cumplen con las expectativas de los usuarios.  
- Se propone una solución **económica, de fácil mantenimiento y automatizada**.  
- Optimiza **tiempo y esfuerzo**, eliminando la necesidad de limpiar manualmente.  
- Contribuye a una educación más **moderna, organizada y productiva**.  

---

## ⚙Funcionamiento  

El sistema cuenta con dos componentes clave:  

### Digitalización Automática  
- Cámaras ESP CAM siguen el movimiento del marcador.  
- El contenido escrito se digitaliza en tiempo real.  
- Puede almacenarse, editarse o compartirse en dispositivos móviles o computadoras.  

### Borrado Automático  
- Un motor paso a paso mueve una banda con un borrador mecánico.  
- El borrado puede activarse desde un **botón físico** o **app móvil**.  
- Garantiza limpieza precisa y sin intervención manual.  

**Proceso completo:**  
1. El usuario escribe → sensores digitalizan el contenido.  
2. El contenido se almacena en la aplicación.  
3. Al activarse el borrado, el motor limpia automáticamente la pizarra.  

---

## Propuesta de valor  

Eraser Bot ofrece una herramienta **intuitiva, accesible y colaborativa** que:  

- Facilita la **organización y digitalización** de ideas.  
- Mejora la **interacción en clases y reuniones**.  
- Reduce tiempos muertos y aumenta la **productividad**.  

---

## Definición del proyecto  

### 1. Usuarios finales ideales  
- **Docentes y administradores** → para mejorar interacción en clases.  
- **Equipos de trabajo en empresas** → colaboración en tiempo real.  
- **Estudiantes y académicos** → organización visual de conceptos.  
- **Freelancers y creativos** → brainstorming ágil y ordenado.  

### 2. Problemas que enfrentan los usuarios  
- Dificultad en la colaboración en tiempo real.  
- Herramientas poco visuales o limitadas.  
- Ideas dispersas y desorganizadas en sesiones de trabajo.  
- Soluciones actuales costosas o ineficientes.  

### 3. Beneficios y valor diferencial  
- Interactividad en tiempo real.  
- Organización visual y dinámica de ideas.  
- Acceso multiplataforma (PC, tablet, móvil).  
- Personalización según el usuario.  
- Integración futura con IA.  
- Mejora de la productividad.  

### 4. Solución tecnológica propuesta  
Una **plataforma colaborativa** que incluye:  
- Creación de **mapas mentales y diagramas**.  
- **Pizarra digital interactiva**.  
- Recomendaciones inteligentes para organización de ideas.  
- Acceso desde cualquier dispositivo.  
- Adaptación a distintos estilos de aprendizaje.  

---

# Eraser Bot – Plataforma con UI + IA  

Este repositorio contiene el código de la **plataforma digital colaborativa** que acompaña al proyecto Eraser Bot.  
Se busca que la plataforma permite **visualizar, organizar y almacenar** el contenido digitalizado del pizarrón inteligente, además de integrar **IA para organización automática de ideas**.  

---

## Funcionalidad principal  

1. **Interfaz de usuario (UI)**  
   - Pizarra digital interactiva.  
   - Mapas mentales y diagramas en tiempo real.  
   - Edición, almacenamiento y exportación de notas.  

2. **Colaboración**  
   - Trabajo en equipo en tiempo real (modo multiusuario).  
   - Acceso desde **PC, tablet o smartphone**.  

3. **IA integrada**  
   - Sugerencias automáticas de organización de ideas.  
   - Reconocimiento de patrones y relaciones entre conceptos.  
   - Resúmenes automáticos del contenido escrito.  

---

## ⚙️ Tecnologías utilizadas  

- **Frontend**: Kivy.
- **Backend**: Python
- **IA**: OpenCV.
- **Comunicación con ESP32**: BLE (Bluetooth Low Energy). 
