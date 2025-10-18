# QR-Phishing-Server---Educational-PoC
⚠️ DISCLAIMER: Este proyecto es únicamente con fines educativos y de investigación en entornos controlados. El uso no autorizado de estas herramientas contra sistemas sin consentimiento explícito es ilegal. El autor no se responsabiliza por mal uso.

¿Qué es esto?
Un servidor Python que genera códigos QR maliciosos y captura datos de phishing en tiempo real. Diseñado para demostrar vulnerabilidades reales en la cadena de confianza de códigos QR y sensibilizar sobre los riesgos que representan como vector de ataque.
Características técnicas:
🔧 Generador dinámico de QR: Crea códigos con URLs personalizadas y payloads embebidos
📊 Captura de datos: Registra en tiempo real cada interacción y redirección
🎯 Landing page customizable: Simula sitios legítimos para análisis de comportamiento
⚡ API RESTful: Endpoints para automatizar generación y monitoreo de campañas
📈 Logging avanzado: Rastreo completo de intentos de phishing para análisis post-mortem
Stack técnico:

Framework: Flask/FastAPI
Generación QR: qrcode library
Base de datos: SQLite/PostgreSQL
Logging: Python logging + análisis de patrones

¿Cómo usarlo?

Levanta el servidor en local
Genera códigos QR desde la interfaz
Monitorea intentos en el dashboard
Analiza los datos capturados

Notas importantes:
✅ Úsalo en tu propio entorno o laboratorio controlado
✅ Estudia cómo funcionan estos ataques para defenderte mejor
✅ Comparte conocimiento, no malicia
