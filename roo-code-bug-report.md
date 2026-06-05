# Reporte: Bug en Roo Code 3.54.0 — "Solicitud API..." colgado indefinidamente

**Fecha:** 2026-05-31  
**Entorno:** macOS 15.7.4 · VS Code 1.122.1 · Roo Code 3.54.0  
**Proveedor configurado:** DeepSeek (perfil "Elvis"), luego OpenRouter  
**Síntoma:** Roo Code se congela mostrando "Solicitud API..." al 0% y nunca responde.

---

## 1. Síntoma observado

Al enviar cualquier mensaje en Roo Code, el panel mostraba:

```
hola
  0%
↺ Solicitud API...
```

El spinner giraba indefinidamente. No había mensaje de error visible. Cancelar y reintentar producía el mismo resultado, independientemente del proveedor (DeepSeek directo u OpenRouter).

---

## 2. Hipótesis descartadas

Durante el diagnóstico se verificaron y descartaron las siguientes causas:

| Hipótesis | Verificación | Resultado |
|---|---|---|
| API key inválida | `curl` directo a `api.deepseek.com` | ✅ Key válida, responde correctamente |
| Sin conectividad a DeepSeek | `curl` con streaming y HTTP/2 | ✅ Red funciona |
| Saldo en cero en DeepSeek | Curl devolvió tokens | ✅ Hay saldo |
| Proxy de VS Code bloqueando streaming | Añadir `"http.proxySupport": "off"` | ❌ No solucionó |
| Bug en OpenAI SDK v5 con CloudFront | Probado con OpenRouter (servidores propios) | ❌ También colgaba |
| Proxy del sistema | `scutil --proxy`, variables de entorno | ✅ Sin proxy |
| Configuración incorrecta de OpenRouter | Verificado en `state.vscdb` | ✅ Config correcta |

---

## 3. Diagnóstico: el log real

El log del extension host (`renderer.log`) reveló los errores reales ocurridos exactamente al momento de crear cada tarea:

```
2026-05-31 10:36:47 [error] [Extension Host]
  Encountered UnhandledRejection: Error: Could not find ripgrep binary

2026-05-31 10:36:48 [error]
  Se ha producido un error desconocido. Consulte el registro para obtener más detalles.

2026-05-31 10:37:08 [error] [Extension Host] [Roo-Debug]
  readApiMessages: API conversation history file not found for taskId:
  019e7eae-37a5-7479-91e3-f2df65e65e78.
  Expected at: .../tasks/019e7eae-.../api_conversation_history.json

2026-05-31 11:00:28 [error] [Extension Host]
  Encountered UnhandledRejection: Error: Unexpected: No existing API conversation history
```

El patrón se repetía con **cada nuevo intento**, para cada proveedor diferente.

---

## 4. Causa raíz

### 4.1 El código que falla en Roo Code

Roo Code usa una función interna `fne(appRoot)` para localizar el binario de `ripgrep`. El código (minificado en `dist/extension.js`) busca en estas rutas:

```javascript
async function fne(t) {
  let e = async r => {
    let a = path.join(t, r, binaryName); // binaryName = "rg" en macOS
    return await exists(a) ? a : void 0;
  };
  return await e("node_modules/@vscode/ripgrep/bin/")           // ← ruta 1
    || await e("node_modules/vscode-ripgrep/bin")               // ← ruta 2
    || await e("node_modules.asar.unpacked/vscode-ripgrep/bin/") // ← ruta 3
    || await e("node_modules.asar.unpacked/@vscode/ripgrep/bin/"); // ← ruta 4
}
```

Si ninguna ruta existe, `fne()` retorna `undefined`, y la función que lo llama lanza:

```javascript
if (!a) throw new Error(`ripgrep not found: ${a}`);
```

### 4.2 El cambio en VS Code 1.122

VS Code cambió el nombre del paquete de ripgrep en versiones recientes:

| Versión | Ruta del binario |
|---|---|
| VS Code antiguo | `node_modules/@vscode/ripgrep/bin/rg` |
| **VS Code 1.122.1** | `node_modules/@vscode/ripgrep-universal/bin/darwin-arm64/rg` |

```bash
# Ruta que busca Roo Code → NO EXISTE
/Applications/Visual Studio Code.app/Contents/Resources/app/
  node_modules/@vscode/ripgrep/bin/rg   ← NOT FOUND ✗

# Ruta real en VS Code 1.122.1 → SÍ EXISTE
/Applications/Visual Studio Code.app/Contents/Resources/app/
  node_modules/@vscode/ripgrep-universal/bin/darwin-arm64/rg   ← FOUND ✓
```

### 4.3 La cadena de fallos

```
Usuario envía mensaje
       ↓
Roo Code inicia tarea
       ↓
initializeFilePaths() se ejecuta en paralelo
(codebase indexer necesita ripgrep)
       ↓
fne(appRoot) → busca "@vscode/ripgrep/bin/rg" → NO EXISTE
       ↓
throw new Error("ripgrep not found: undefined")
       ↓
UnhandledRejection (sin catch en el caller)
       ↓
VS Code captura la excepción no manejada
→ muestra "Se ha producido un error desconocido"
→ mata el contexto async de la inicialización de la tarea
       ↓
La llamada a la API nunca llega a completarse
api_conversation_history.json nunca se crea
       ↓
Tarea guardada en estado "resume_task"
       ↓
Próximo intento → resumeTask() intenta leer
api_conversation_history.json → no existe
→ throw new Error("Unexpected: No existing API conversation history")
       ↓
Ciclo infinito de fallos
```

### 4.4 Por qué se veía como un problema de red

El componente que fallaba (`initializeFilePaths`) forma parte del inicializador de tareas de Roo Code, que corre de forma concurrente con la llamada a la API. Cuando el `UnhandledRejection` de ripgrep mata el contexto async, la UI ya había mostrado "Solicitud API..." porque `api_req_started` se emitió **antes** de que el fallo ocurriera. Esto creaba la ilusión de que la API no respondía, cuando en realidad la tarea entera nunca llegó a completarse.

---

## 5. Solución aplicada

Se creó un symlink que conecta la ruta antigua que busca Roo Code con el binario real de ripgrep incluido en VS Code 1.122.1:

```bash
# Crear el directorio que Roo Code espera encontrar
mkdir -p "/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/ripgrep/bin"

# Crear el symlink
ln -sf \
  "/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/ripgrep-universal/bin/darwin-arm64/rg" \
  "/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/ripgrep/bin/rg"
```

**Verificación:**

```bash
"/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/ripgrep/bin/rg" --version
# ripgrep 15.0.0 (rev 3a612f88b8)
```

---

## 6. Notas adicionales

### Otros cambios realizados durante el diagnóstico

- Se añadió `"http.proxySupport": "off"` a `settings.json` (no fue la solución pero tampoco causa daño; puede dejarse).
- Se cambiaron las configuraciones del perfil "Elvis" de DeepSeek directo a OpenRouter y de vuelta. Puede restaurarse a DeepSeek si se prefiere, ya que el problema no era el proveedor.

### Por qué el symlink es la solución correcta (y no un workaround)

- El binario apuntado es exactamente el mismo que VS Code usa internamente para sus propias operaciones de búsqueda.
- No se modifica ningún archivo ejecutable de VS Code, solo se crea una entrada de directorio.
- La solución correcta a largo plazo es que el equipo de Roo Code actualice `fne()` para incluir `@vscode/ripgrep-universal` en su lista de rutas. Este es un bug de compatibilidad con VS Code 1.122+.

### Caveat: actualizaciones de VS Code

Si VS Code se actualiza a una versión mayor que mueva o renombre nuevamente el paquete de ripgrep, el symlink podría quedar inválido. Para verificarlo:

```bash
ls "/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/ripgrep/bin/rg"
# Si muestra "No such file or directory" → hay que recrear el symlink
```

---

## 7. Resumen ejecutivo

**Roo Code 3.54.0** tiene un bug de compatibilidad con **VS Code 1.122+**: busca el binario de `ripgrep` en una ruta de paquete antigua (`@vscode/ripgrep`) que ya no existe en las versiones recientes de VS Code (ahora es `@vscode/ripgrep-universal`). Esta falla silenciosa lanza un `UnhandledRejection` durante la inicialización de cada tarea, impidiendo que cualquier llamada a la API llegue a completarse. El síntoma visible es el spinner "Solicitud API..." colgado al 0%.

**Solución:** symlink de `@vscode/ripgrep/bin/rg` → `@vscode/ripgrep-universal/bin/darwin-arm64/rg`.
