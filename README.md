# Pixel Mirror

Una interfaz gráfica simple para controlar scrcpy en macOS, especialmente optimizada para teléfonos Pixel.

## Instalación

1. Descarga la última versión desde [Releases](https://github.com/smithplus/PixelMirror/releases)
2. Descomprime el archivo
3. Arrastra `PixelMirror.app` a tu carpeta de Aplicaciones

### Si la aplicación no se ejecuta:

1. Haz clic derecho en `PixelMirror.app` y selecciona "Abrir"
2. Si aparece una advertencia, haz clic en "Abrir"
3. Si aún no funciona, ejecuta en Terminal:
   ```bash
   xattr -cr /Applications/PixelMirror.app
   chmod +x /Applications/PixelMirror.app/Contents/MacOS/PixelMirror
   ```

## Uso

1. Conecta tu dispositivo Android por USB
2. Abre Pixel Mirror
3. Haz clic en el botón de refrescar (🔄)
4. Selecciona tu dispositivo
5. Haz clic en "Conectar"

### Conexión Wi-Fi

1. Primero conecta por USB
2. Cambia a modo "Wi-Fi"
3. Haz clic en "Habilitar Wi-Fi"
4. Espera el mensaje de confirmación
5. Desconecta el USB
6. Selecciona el dispositivo y haz clic en "Conectar"

## Solución de problemas

Los logs están en: `~/Library/Logs/PixelMirror.log`

### Problemas comunes

- **ADB no encontrado**: La aplicación lo instalará automáticamente
- **Dispositivo no detectado**: 
  * Verifica que la depuración USB esté habilitada
  * Acepta la solicitud de depuración en tu teléfono
- **Error de Wi-Fi**:
  * Asegúrate de que el teléfono y la computadora estén en la misma red
  * Intenta reconectar por USB y habilitar Wi-Fi nuevamente

## Licencia

MIT License 