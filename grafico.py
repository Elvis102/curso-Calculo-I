```{python}
import plotly.graph_objects as go
import numpy as np

# Función de costo simplificada: J(w) = w^2
def J(w):
    return w**2

# Tasa de cambio: (J(w+h) - J(w)) / h
def tasa_cambio(w, h):
    return (J(w + h) - J(w)) / h

# Datos para la gráfica
w = np.linspace(-2, 2, 100)
J_w = J(w)
w0 = 1  # Punto fijo para la animación
h_values = [1, 0.5, 0.1, 0.01]  # Valores de h para la recta secante

# Crear figura
fig = go.Figure()

# Añadir la función de costo J(w) = w^2
fig.add_trace(go.Scatter(x=w, y=J_w, mode='lines', name='J(w) = w²', line=dict(color='#228B22')))

# Añadir rectas secantes (solo una visible a la vez)
for i, h in enumerate(h_values):
    w_sec = [w0, w0 + h]
    J_sec = [J(w0), J(w0 + h)]
    fig.add_trace(go.Scatter(x=w_sec, y=J_sec, mode='lines+markers', name=f'Secante (h={h})',
                             line=dict(dash='dash', color='#FF5733'), visible=(i==0)))

# Añadir la recta tangente en w0
w_tan = np.linspace(w0 - 0.5, w0 + 0.5, 100)
J_tan = J(w0) + 2 * w0 * (w_tan - w0)  # Derivada: J'(w) = 2w
fig.add_trace(go.Scatter(x=w_tan, y=J_tan, mode='lines', name='Tangente', line=dict(color='#FFD700')))

# Configurar deslizador para h
steps = []
for i, h in enumerate(h_values):
    step = dict(
        method="update",
        args=[{"visible": [True] + [j == i for j in range(len(h_values))] + [True]},
              {"title.text": f"Optimización: Tasa de Cambio para h={h}, Pendiente={tasa_cambio(w0, h):.2f}"}],
        label=str(h)
    )
    steps.append(step)

sliders = [dict(active=0, steps=steps, currentvalue={"prefix": "h = "})]

# Configurar diseño
fig.update_layout(
    sliders=sliders,
    title="Optimización: Tasa de Cambio y Derivada en J(w) = w²",
    showlegend=True,
    xaxis_title="Parámetro w",
    yaxis_title="Costo J(w)",
    template="plotly_white",
    annotations=[
        dict(
            x=0, y=4, xref="x", yref="y",
            text="La derivada (pendiente de la tangente) guía el descenso por gradiente",
            showarrow=True, arrowhead=2, ax=20, ay=-30
        )
    ]
)

# Exportar como HTML
fig.write_html("optimizacion_descenso_gradiente.html")
fig.show()
```