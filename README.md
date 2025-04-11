# Pixel Mirror

Una interfaz gráfica simple para controlar scrcpy en macOS, especialmente optimizada para teléfonos Pixel. Permite controlar tu dispositivo Android tanto por USB como por Wi-Fi de manera sencilla.

## Requisitos

- macOS 10.10 o superior
- Un dispositivo Android con depuración USB habilitada

No necesitas instalar nada más, la aplicación instalará automáticamente todas las dependencias necesarias.

## Instalación

1. Descarga la última versión de Pixel Mirror desde la sección [Releases](https://github.com/tu-usuario/pixel-mirror/releases/latest)
2. Descomprime el archivo descargado
3. Arrastra `PixelMirror.app` a tu carpeta de Aplicaciones

## Uso

### Primera vez

1. Abre Pixel Mirror desde:
   - Launchpad
   - Carpeta Aplicaciones
   - Spotlight (⌘ + Espacio y escribe "Pixel Mirror")

2. Si es la primera vez que lo ejecutas, la aplicación:
   - Verificará e instalará ADB si es necesario
   - Te pedirá los permisos necesarios

### Preparación del dispositivo Android

1. Habilita las opciones de desarrollador:
   - Ve a Ajustes > Acerca del teléfono
   - Toca "Número de compilación" 7 veces
   - Volverás a la pantalla anterior y verás "Opciones de desarrollador"

2. Habilita la depuración USB:
   - Ve a Ajustes > Opciones de desarrollador
   - Activa "Depuración USB"
   - Activa "Depuración inalámbrica" (para conexión Wi-Fi)

### Conexión por USB

1. Conecta tu dispositivo Android por USB
2. Abre Pixel Mirror
3. Haz clic en el botón de refrescar (🔄)
4. Selecciona tu dispositivo de la lista
5. Haz clic en "Conectar"

### Conexión por Wi-Fi

1. Primero conecta tu dispositivo por USB
2. Abre Pixel Mirror
3. Cambia el modo a "Wi-Fi"
4. Haz clic en "Habilitar Wi-Fi"
   - Esto configurará automáticamente la IP y el puerto
5. Espera el mensaje "Conexión Wi-Fi establecida correctamente"
6. Ahora puedes desconectar el cable USB
7. Selecciona el dispositivo de la lista (aparecerá con su IP)
8. Haz clic en "Conectar"

## Características

- Detección automática de dispositivos
- Soporte para conexión USB y Wi-Fi
- Instalación automática de dependencias
- Interfaz nativa de macOS
- Logs en tiempo real
- Menú de ayuda integrado
- Cierre seguro de conexiones

## Solución de problemas

Si encuentras algún problema, puedes revisar los logs en:
```
~/Library/Logs/PixelMirror.log
```

### Problemas comunes

1. **ADB no encontrado**: La aplicación intentará instalarlo automáticamente
2. **Dispositivo no detectado**: 
   - Verifica que la depuración USB esté habilitada
   - Acepta la solicitud de depuración en tu dispositivo
3. **Error de conexión Wi-Fi**:
   - Asegúrate de que el teléfono y la computadora estén en la misma red
   - Intenta reconectar por USB y habilitar Wi-Fi nuevamente

## Desinstalación

Si deseas desinstalar la aplicación:
1. Cierra la aplicación si está abierta
2. Arrastra `PixelMirror.app` desde la carpeta Aplicaciones a la Papelera
3. Vacía la Papelera

## Notas

- La primera vez que conectes un dispositivo, deberás aceptar la solicitud de depuración en tu teléfono
- Para conexión Wi-Fi, el dispositivo debe estar en la misma red que tu computadora
- La aplicación recordará el último modo de conexión utilizado

## Contribuir

Si encuentras algún bug o tienes sugerencias, por favor:
1. Abre un issue en este repositorio
2. Describe el problema o mejora
3. Si es posible, incluye los logs y pasos para reproducir el problema 