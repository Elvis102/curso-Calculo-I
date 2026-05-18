# Relaciones y Funciones para Ciencia de Datos
## Guía pedagógica para Cálculo I — modalidad online

> **Propósito:** Documento de referencia para mejorar la enseñanza del tema *Relaciones y Funciones* en un contexto de Ciencia de Datos, basado en el análisis del material existente (`S1.2_Relaciones y funciones.qmd`).

---

## 1. Diagnóstico del material actual

### Fortalezas identificadas

- El material ya establece un vínculo con ML al presentar funciones de regresión, pérdida y activación como motivación (`## ¿Por qué Funciones? La Piedra Angular del ML`).
- El uso de fragmentos progresivos (`:::fragment`) permite construir el concepto paso a paso, adecuado para sesiones sincrónicas.
- La notación de Dirichlet y los 5 protagonistas de `f(x)` constituyen un recurso conceptual sólido y poco común en libros de texto estándar.
- El cociente de diferencias $\frac{f(x+h)-f(x)}{h}$ anticipa correctamente el concepto de derivada.

### Brechas detectadas

| Brecha | Descripción |
|---|---|
| Abstracción sin anclaje | Los ejemplos de correspondencia usan objetos arbitrarios (`{a,b,c,d}`) sin conexión con datos reales. |
| Visualización estática | Las gráficas son imágenes fijas (`.jpg`, `.png`); no hay interactividad. |
| Dominio — solo restricciones algebraicas | No se trabaja el dominio desde la perspectiva de qué datos son válidos para un modelo. |
| Sin código | No hay bloques de Python/R que permitan experimentar con funciones reales. |
| Evaluación formativa ausente | No hay preguntas embebidas, polls ni actividades de verificación inmediata. |

---

## 2. Mapa conceptual del tema y conexiones con Ciencia de Datos

```
Conjunto → Producto Cartesiano → Relación Binaria → Función
    ↓                                                    ↓
DataFrame (filas × columnas)            Pipeline de transformación de datos
    ↓                                                    ↓
Dominio = valores válidos de entrada    Dom(f) = rango aceptable de una feature
    ↓                                                    ↓
Imagen = valores de salida              Predicción del modelo: ŷ = f(x)
```

**Lectura pedagógica:** un DataFrame es un producto cartesiano finito. Cada columna es un conjunto. Una función de ML es una función real de múltiples variables. Esta cadena de equivalencias debe hacerse explícita en clase.

---

## 3. Estrategias pedagógicas recomendadas

### 3.1 Aprendizaje basado en contexto (ABC)

Reemplaza los ejemplos abstractos por situaciones de Ciencia de Datos desde el primer contacto:

| Concepto abstracto | Contexto en Ciencia de Datos |
|---|---|
| Conjunto $A$ | Conjunto de IDs de estudiantes |
| Conjunto $B$ | Conjunto de calificaciones posibles $[0, 10]$ |
| Relación $R \subseteq A \times B$ | Tabla de notas (puede ser relación no funcional si hay errores de carga) |
| Función $f: A \to B$ | Modelo de predicción de nota a partir del ID del estudiante |
| $Dom(f)$ | Estudiantes para los que el modelo puede predecir (sin valores nulos) |
| $Im(f)$ | Rango de predicciones posibles del modelo |

### 3.2 Visualización interactiva

Incorpora exploradores HTML (como el ya implementado para valor absoluto) para:

- **Graficar funciones** con slider para parámetros ($a$, $b$ en $f(x) = ax + b$)
- **Mostrar dominio e imagen** dinámicamente al cambiar la función
- **Comparar una relación vs. una función** con diagrama de flechas interactivo

### 3.3 Secuencia de aprendizaje recomendada (5E)

| Fase | Actividad | Tiempo estimado |
|---|---|---|
| **Engage** | Pregunta provocadora con datos reales | 5 min |
| **Explore** | Explorador interactivo o código Python | 10 min |
| **Explain** | Definición formal + notación de Euler | 10 min |
| **Elaborate** | Ejercicios de dominio e imagen con funciones de ML | 10 min |
| **Evaluate** | Poll o pregunta de salida | 5 min |

### 3.4 Pregunta provocadora de apertura (Engage)

> *"Tienes un dataset con 1000 estudiantes. Para algunos, la columna `nota_final` está vacía. ¿La regla que asigna nota a cada estudiante es una función? ¿Por qué?"*

Esta pregunta activa simultáneamente: conjuntos, relaciones, dominio y la condición de unicidad de una función, todo en un contexto familiar.

---

## 4. Ejemplos aplicados a Ciencia de Datos

### 4.1 Función lineal — regresión simple

La función de regresión lineal $f(x) = wx + b$ es la función más importante en ML.

```python
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
w = 2.5   # pendiente (peso)
b = 1.0   # intercepto (sesgo)

# Definición de la función
def f(x):
    return w * x + b

# Dominio: horas de estudio (variable independiente)
x = np.linspace(0, 10, 100)
y = f(x)

plt.figure(figsize=(7, 4))
plt.plot(x, y, color='steelblue', linewidth=2, label=r'$f(x) = 2.5x + 1$')
plt.xlabel('Horas de estudio (x)', fontsize=12)
plt.ylabel('Nota predicha f(x)', fontsize=12)
plt.title('Función lineal: modelo de regresión simple', fontsize=13)
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Evaluaciones específicas
print(f"f(0) = {f(0)}")    # intercepto
print(f"f(4) = {f(4)}")    # predicción para 4 horas
print(f"f(10) = {f(10)}")  # predicción para 10 horas
```

**Conexión con la clase:** Aquí `x` es la variable independiente (horas de estudio) y `f(x)` es la variable dependiente (nota). El dominio natural es $[0, 24]$ horas; fuera de ese rango la función existe matemáticamente pero no tiene sentido físico — esta distinción entre *dominio matemático* y *dominio de aplicación* es fundamental.

### 4.2 Función cuadrática — función de pérdida (MSE)

```python
import numpy as np
import matplotlib.pyplot as plt

# Error del modelo para distintas predicciones
y_real = 7.0  # nota real de un estudiante

def perdida(y_pred):
    """Error cuadrático para un solo ejemplo"""
    return (y_pred - y_real) ** 2

# Dominio: todas las posibles predicciones
y_pred = np.linspace(0, 14, 200)
L = perdida(y_pred)

plt.figure(figsize=(7, 4))
plt.plot(y_pred, L, color='crimson', linewidth=2, label=r'$L(\hat{y}) = (\hat{y} - 7)^2$')
plt.axvline(y_real, color='green', linestyle='--', label=f'Predicción perfecta ($\hat{{y}}={y_real}$)')
plt.xlabel(r'Predicción $\hat{y}$', fontsize=12)
plt.ylabel(r'Pérdida $L(\hat{y})$', fontsize=12)
plt.title('Función de pérdida cuadrática', fontsize=13)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

**Conexión con la clase:** La función de pérdida $L(\hat{y}) = (\hat{y} - y)^2$ es una función cuadrática. Su mínimo (donde $L = 0$) ocurre cuando la predicción es perfecta. El dominio es $\mathbb{R}$ y la imagen es $[0, +\infty)$.

### 4.3 Función compuesta — pipeline de datos

La composición de funciones $g \circ f$ aparece en todo pipeline de ML:

```python
# Pipeline: datos crudos → normalización → predicción

def normalizar(x, x_min=0, x_max=10):
    """f: [0,10] → [0,1]"""
    return (x - x_min) / (x_max - x_min)

def modelo_lineal(x_norm, w=3.0, b=0.5):
    """g: [0,1] → [0.5, 3.5]"""
    return w * x_norm + b

def pipeline(x):
    """g ∘ f: composición completa"""
    return modelo_lineal(normalizar(x))

# Evaluación
horas = np.array([0, 2, 5, 8, 10])
for h in horas:
    print(f"horas={h:2d} → normalizado={normalizar(h):.2f} → predicción={pipeline(h):.2f}")
```

**Conexión con la clase:** La composición $g \circ f$ que se define formalmente en la slide de Relaciones Binarias tiene aquí una realización directa: primero se normaliza el dato ($f$), luego se aplica el modelo ($g$).

### 4.4 Dominio de definición — valores no admisibles en datos

```python
import numpy as np

def tasa_conversion(x):
    """f(x) = 1/(x-1): Dom(f) = R \ {1}"""
    return 1 / (x - 1)

valores = [-2, 0, 0.5, 1, 2, 5, 10]

print("x\t\tf(x)")
print("-" * 30)
for x in valores:
    try:
        resultado = tasa_conversion(x)
        print(f"{x}\t\t{resultado:.4f}")
    except ZeroDivisionError:
        print(f"{x}\t\tNo definida (x=1 no pertenece al Dom(f))")
```

---

## 5. Errores conceptuales comunes y cómo abordarlos

### Error 1: Confundir relación con función

**Síntoma:** El estudiante asume que toda relación es función.

**Causa:** No internalizó la condición de unicidad (cada $x$ tiene **un único** $f(x)$).

**Cómo abordarlo:**
> Pide al estudiante que abra un CSV y busque una columna con valores duplicados en la clave. Pregunta: ¿si hay dos filas con el mismo `id_estudiante` pero distinta `nota`, esa tabla define una función de `id → nota`?

---

### Error 2: El dominio como "restricción artificial"

**Síntoma:** El estudiante calcula Dom(f) mecánicamente pero no comprende su significado.

**Causa:** Se enseña el dominio solo como "donde no se divide por cero" o "donde la raíz es positiva".

**Cómo abordarlo:**
> Presenta $f(x) = \sqrt{x}$ y pregunta: si $x$ representa el número de defectos en un producto, ¿qué significa que el dominio matemático sea $[0, +\infty)$? ¿Podría $x$ ser $3.7$? ¿Negativo? El dominio matemático y el dominio de aplicación son dos restricciones independientes.

---

### Error 3: Leer $f(x)$ como "f multiplicado por x"

**Síntoma:** Cálculos erróneos como $f(x+h) = f \cdot x + f \cdot h$.

**Causa:** La notación algebraica estándar $a(b) = a \times b$ interfiere.

**Cómo abordarlo:**
> Este error ya está anticipado en el material ("Aviso navegantes"). Refuerza con código: en Python `f(x)` es literalmente una **llamada a función**, no una multiplicación. Mostrar este paralelo entre matemáticas y programación resulta muy efectivo con estudiantes de Ciencia de Datos.

```python
# En Python, f(x) = evaluación, nunca multiplicación
def f(x):
    return x**2 + 1

x = 3
print(f(x))       # evalúa: 3² + 1 = 10
print(f(x + 1))   # evalúa: (3+1)² + 1 = 17, NO f*x + f*1
```

---

### Error 4: La imagen como "todo el conjunto final"

**Síntoma:** Para $f: \mathbb{R} \to \mathbb{R}$ con $f(x) = x^2$, el estudiante dice que $Im(f) = \mathbb{R}$.

**Causa:** Confunde el conjunto final (codominio) con la imagen real de la función.

**Cómo abordarlo:**
> Analogía directa: en un modelo de ML entrenado para predecir notas de $0$ a $10$, el codominio declarado es $[0,10]$, pero si el modelo nunca predice notas menores a $3$, la imagen real es $[3, 10]$. El modelo *podría* dar ese rango pero en la práctica *da* el otro.

---

## 6. Actividades prácticas y evaluaciones formativas

### Actividad 1 — Clasificación rápida (5 min, individual)

Presenta 5 diagramas de flechas mezclados entre relaciones y funciones. El estudiante debe clasificar cada uno y justificar. Puede hacerse con **Mentimeter** o **Wooclap**.

---

### Actividad 2 — "¿Es función este dataset?" (15 min, parejas)

Proporciona un CSV con los siguientes problemas intencionales:

| id_cliente | monto_compra |
|---|---|
| 001 | 45.0 |
| 002 | 120.5 |
| 001 | 78.0 |   ← duplicado |
| 003 | NaN |   ← valor nulo |

Preguntas:
1. ¿La correspondencia `id_cliente → monto_compra` define una función? ¿Por qué?
2. ¿Cuál es el dominio de definición si eliminamos los valores nulos?
3. ¿Qué deberías hacer con el `id_cliente = 001` duplicado para que la correspondencia sea una función?

---

### Actividad 3 — Explorador de funciones (20 min, individual)

Usando el siguiente código en Google Colab, el estudiante debe:

```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

def explorar_funcion(a=1.0, b=0.0, c=0.0):
    """f(x) = ax² + bx + c"""
    x = np.linspace(-5, 5, 400)
    y = a*x**2 + b*x + c

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Gráfica
    ax1.plot(x, y, 'steelblue', linewidth=2)
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.axvline(0, color='gray', linewidth=0.5)
    ax1.set_title(f'f(x) = {a}x² + {b}x + {c}')
    ax1.grid(alpha=0.3)
    ax1.set_xlabel('x'); ax1.set_ylabel('f(x)')

    # Imagen aproximada
    ax2.hist(y, bins=30, color='steelblue', alpha=0.7)
    ax2.set_title(f'Distribución de f(x)\nImagen ≈ [{y.min():.2f}, {y.max():.2f}]')
    ax2.set_xlabel('f(x)'); ax2.set_ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()
    print(f"Dom(f) = ℝ | Im(f) ≈ [{y.min():.2f}, +∞)" if a > 0 else
          f"Dom(f) = ℝ | Im(f) ≈ (-∞, {y.max():.2f}]")

interact(explorar_funcion,
         a=FloatSlider(min=-3, max=3, step=0.5, value=1),
         b=FloatSlider(min=-5, max=5, step=0.5, value=0),
         c=FloatSlider(min=-5, max=5, step=0.5, value=0))
```

**Preguntas guía:**
1. ¿Para qué valores de $a$ la función tiene mínimo? ¿Máximo?
2. ¿Cómo cambia la imagen al variar $a$?
3. ¿Qué función de pérdida en ML tiene esta forma?

---

### Evaluación formativa — Pregunta de salida (3 min)

Al final de la sesión, una sola pregunta:

> **Sea $f(x) = \dfrac{\sqrt{x+2}}{x-3}$. Determina $Dom(f)$ y justifica cada restricción.**

**Rúbrica mínima:**
- Identifica la restricción de la raíz: $x + 2 \geq 0 \Rightarrow x \geq -2$ ✓
- Identifica la restricción del denominador: $x \neq 3$ ✓
- Expresa el dominio correctamente: $Dom(f) = [-2, 3) \cup (3, +\infty)$ ✓

---

## 7. Recursos recomendados

| Recurso | Tipo | Uso sugerido |
|---|---|---|
| [Desmos](https://www.desmos.com/calculator) | Graficador interactivo | Visualizar funciones y dominio en tiempo real |
| [GeoGebra](https://www.geogebra.org) | Simulación | Diagramas de flechas de relaciones y funciones |
| Google Colab | Python | Ejecutar los bloques de código de esta guía |
| `ipywidgets` (Python) | Librería | Sliders interactivos para parámetros de funciones |
| 3Blue1Brown — "What is a function?" | Video | Visualización conceptual para motivar la sesión |
| Scikit-learn Pipelines docs | Documentación | Composición de funciones en contexto real de ML |

---

## 8. Propuesta de integración en el `.qmd` existente

Para incorporar estos elementos en `S1.2_Relaciones y funciones.qmd` sin romper el diseño actual, se recomienda:

1. **Agregar una diapositiva de apertura** con la pregunta provocadora (sección 3.4) justo después del título de sección `# Fundamentos Teóricos de Funciones`.

2. **Reemplazar el ejemplo abstracto** de la relación $R = \{(a,2),(a,5),...\}$ por el ejemplo del dataset de estudiantes (sección 4), manteniendo la misma estructura visual con columnas.

3. **Insertar un bloque `{=html}`** con un explorador interactivo de funciones (similar al explorador de valor absoluto ya implementado) en la sección de dominio e imagen.

4. **Añadir una diapositiva de cierre** con la pregunta de salida de la evaluación formativa (sección 6).

5. **En el SCSS** (`clean.scss`), no se requieren cambios — los estilos existentes (`.cuadro2`, `.bg`, `.alert`, `.fragment`) son suficientes para implementar toda esta propuesta.

---

*Documento generado como referencia pedagógica para el curso de Cálculo I — Universidad Técnica de Machala.*
*Última revisión: abril 2026.*
