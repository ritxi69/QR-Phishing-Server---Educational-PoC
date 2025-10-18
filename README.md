# 🎓 QR Phishing Demo - Proyecto Educativo de Ciberseguridad

> **⚠️ AVISO LEGAL:** Este proyecto es exclusivamente educativo y debe utilizarse solo en entornos controlados con consentimiento explícito de los participantes. El uso malicioso de estas técnicas es ilegal.

## 📋 Descripción

Demostración educativa de un ataque de phishing mediante códigos QR, diseñada para concienciar sobre técnicas de ingeniería social y captura de credenciales. Incluye una aplicación complementaria de awareness para educar sobre la detección de QR maliciosos.

### Componentes del Proyecto

1. **Demo de Phishing**: Simulación controlada de captura de credenciales
2. **The Pill ADO**: Aplicación de awareness con detector de QR sospechosos
3. **Infraestructura de túnel**: Bypass de aislamiento AP mediante ngrok/Cloudflare

---

## 🛠️ Requisitos

### Sistema Operativo
- Kali Linux (recomendado)
- Ubuntu/Debian
- macOS/Windows con Python 3.9+

### Software Necesario
```bash
# Python 3.9 o superior
python3 --version

# Ngrok (para exponer servidor)
# Descarga desde: https://ngrok.com/download

# O Cloudflare Tunnel (alternativa gratuita sin warnings)
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### Opcional
```bash
# Para generar QRs en terminal
sudo apt install qrencode

# Para visualizar QRs
sudo apt install feh
```

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/qr-phishing-demo.git
cd qr-phishing-demo
```

### 2. Dar Permisos de Ejecución

```bash
chmod +x server.py
chmod +x server_dual.py
chmod +x cloudflare_qr.sh
chmod +x reset_demo.sh
```

### 3. Verificar Estructura de Archivos

```
qr-phishing-demo/
├── server.py              # Servidor phishing simple
├── server_dual.py         # Servidor dual (phishing + escuela)
├── index.html             # Página de login falso
├── pill.html              # Página de awareness (robot ASCII)
├── cloudflare_qr.sh       # Script automático Cloudflare + QR
├── reset_demo.sh          # Script para resetear datos
└── README.md              # Este archivo
```

---

## 📱 Uso

### Opción A: Demo de Phishing (Solo Captura)

**1. Iniciar servidor:**
```bash
./server.py
```

**2. Exponer con ngrok:**
```bash
# En otra terminal
ngrok http 5000

# Copiar URL que aparece (ej: https://abc123.ngrok.io)
```

**3. Generar QR:**
```bash
# Opción 1: Online
https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=https://abc123.ngrok.io/index.html

# Opción 2: Terminal (si tienes qrencode)
qrencode -o qr_phishing.png "https://abc123.ngrok.io/index.html"
```

**4. Distribuir QR y monitorear:**
```bash
# Ver capturas en tiempo real
tail -f credentials.txt

# Ver contador
cat count.txt
```

---

### Opción B: Distribución Escuela (Awareness)

**1. Usar script automático:**
```bash
./cloudflare_qr.sh
```

Este script:
- ✅ Instala Cloudflare Tunnel (si no existe)
- ✅ Inicia el túnel automáticamente
- ✅ Genera el QR para pill.html
- ✅ Abre el QR en visor de imágenes
- ✅ Sin página de advertencia (mejor UX)

**2. Distribuir el QR generado:**
```bash
# El archivo se guarda como:
qr_escuela_YYYYMMDD_HHMMSS.png
```

---

### Opción C: Modo Dual (Ambos Proyectos)

**1. Iniciar servidor dual:**
```bash
./server_dual.py
```

**2. Exponer con ngrok:**
```bash
ngrok http 5000
```

**3. Generar dos QRs:**
```bash
# QR Phishing
https://TU_URL.ngrok.io/index.html

# QR Escuela
https://TU_URL.ngrok.io/pill.html
```

---

## 📊 Archivos Generados

### Phishing Demo
- `credentials.txt` - Credenciales capturadas (usuario + password)
- `meta_log.txt` - IPs y user-agents de visitantes
- `count.txt` - Contador de participaciones
- `last.txt` - Timestamp de última captura

### Awareness Escuela
- `visits.txt` - Registro de visitas al robot ASCII
- `visitor_count.txt` - Contador de visitas

### Logs
- `server.log` - Logs completos del servidor
- `tunnel.log` - Logs de Cloudflare Tunnel

---

## 🔧 Scripts Útiles

### Reset de Demo
```bash
# Borra todos los datos y resetea contadores
./reset_demo.sh
```

### Ver Estadísticas en Vivo
```bash
# Capturas phishing
tail -f credentials.txt

# Visitas escuela
tail -f visits.txt

# Logs del servidor
tail -f server.log
```

---

## 🎯 Casos de Uso

### 1. Presentación Académica
```bash
# Usa ngrok (con panel web para mostrar capturas en vivo)
./server.py
ngrok http 5000

# Proyecta localhost:4040 para mostrar el panel de ngrok
# Explica el warning como contenido educativo
```

### 2. Distribución Masiva en Escuela
```bash
# Usa Cloudflare (sin warnings molestos)
./server_dual.py
./cloudflare_qr.sh

# Distribuye el QR generado
# Mayor tasa de participación sin fricción
```

### 3. Workshop de Ciberseguridad
```bash
# Usa servidor dual
./server_dual.py
ngrok http 5000

# Muestra ambos aspectos:
# - Ataque (index.html)
# - Defensa (pill.html con detector)
```

---

## ⚠️ Consideraciones de Seguridad

### ✅ Buenas Prácticas

1. **Consentimiento Informado**
   - Informar a participantes sobre la naturaleza educativa
   - Documentar consentimientos explícitos
   - Usar solo datos ficticios en demos

2. **Protección de Datos**
   - Eliminar `credentials.txt` inmediatamente después de la demo
   - No almacenar datos reales de usuarios
   - Cumplir con GDPR/LOPDGDD

3. **Entorno Controlado**
   - Realizar solo en redes autorizadas
   - No distribuir URLs en canales públicos
   - Limitar tiempo de exposición del túnel

4. **Limpieza Post-Demo**
   ```bash
   # Ejecutar siempre después de terminar
   ./reset_demo.sh
   rm credentials.txt
   rm meta_log.txt
   rm visits.txt
   ```

### ❌ NO Hacer

- ❌ Usar en redes públicas sin autorización
- ❌ Capturar credenciales reales
- ❌ Distribuir sin consentimiento explícito
- ❌ Mantener datos almacenados más de 24h
- ❌ Usar fuera de entornos educativos controlados

---

## 🔍 Troubleshooting

### Problema: "Address already in use"
```bash
# Solución: Matar procesos en puerto 5000
sudo lsof -ti:5000 | xargs kill -9
```

### Problema: Ngrok muestra "Session expired"
```bash
# Solución: Limpiar y reiniciar
pkill -9 ngrok
sleep 2
ngrok http 5000
```

### Problema: No se capturan IPs reales (127.0.0.1)
```bash
# Causa: Accediendo vía localhost en lugar de túnel
# Solución: Usar URL de ngrok/Cloudflare, no localhost
```

### Problema: Warning de ngrok molesta
```bash
# Solución 1: Usar Cloudflare Tunnel (sin warnings)
./cloudflare_qr.sh

# Solución 2: Explicar como contenido educativo
# El warning solo aparece la primera vez por dispositivo
```

---

## 📚 Recursos Adicionales

### Documentación Técnica
- [Ngrok Documentation](https://ngrok.com/docs)
- [Cloudflare Tunnel Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Python HTTP Server](https://docs.python.org/3/library/http.server.html)

### Papers y Referencias
- OWASP Top 10 - Phishing Attacks
- Social Engineering: The Science of Human Hacking (Christopher Hadnagy)
- The Art of Deception (Kevin Mitnick)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas siempre que mantengan el propósito educativo del proyecto.

### Cómo Contribuir
1. Fork del repositorio
2. Crear branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT con las siguientes restricciones adicionales:

- ✅ Uso educativo en entornos controlados
- ✅ Investigación académica autorizada
- ❌ Uso malicioso o ilegal
- ❌ Distribución sin advertencias de seguridad

Ver `LICENSE` para más detalles.

---

## 👤 Autor

**Ricardo Andino**
- Proyecto Final - Ciberseguridad 2025
- Institución: Neoland
- Email: ritxi69@proton.me

---

## 🙏 Agradecimientos

- Ángel Camaño, tutor del curso de Ciberseguridad
- Comunidad de Kali Linux
- Ngrok y Cloudflare por sus herramientas
- Participantes voluntarios de las demos

---

## 📌 Disclaimer Final

**Este proyecto es estrictamente educativo.** El autor no se responsabiliza del uso indebido de estas técnicas. El phishing es ilegal cuando se realiza sin consentimiento. Utiliza estos conocimientos solo para:

- ✅ Educación en ciberseguridad
- ✅ Concienciación sobre amenazas
- ✅ Investigación académica autorizada
- ✅ Mejora de defensas organizacionales

**El uso malicioso puede resultar en cargos criminales según el código penal de tu jurisdicción.**

---

**⭐ Si este proyecto te fue útil para aprender, considera darle una estrella en GitHub!**
