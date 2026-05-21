# REST API - Machine Learning Prediction System

Una API REST desarrollada con **FastAPI** para predicciones de machine learning con integración a bases de datos MySQL.

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido para Python
- **Machine Learning**: Modelo de regresión lineal para predicciones
- **Base de Datos**: Integración con MySQL (2 bases de datos)
- **Validación de Salud**: Endpoints para verificar estado de la aplicación
- **Predicciones**: Endpoint para procesar archivos CSV y generar predicciones

## 📋 Requisitos Previos

- Python 3.8+
- MySQL Server
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/FabianRojas1/Datapath-mlops15-FR-railway.git
cd Datapath-mlops15-FR-railway
```

2. **Crear un entorno virtual** (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:
```
SQLALCHEMY_DATABASE_URL=mysql+pymysql://usuario:contraseña@host:puerto/basedatos
SQLALCHEMY_DATABASE_URL1=mysql+pymysql://usuario:contraseña@host:puerto/basedatos1
```

## 📦 Dependencias

| Paquete | Versión |
|---------|---------|
| fastapi | latest |
| uvicorn | latest |
| sqlalchemy | latest |
| pandas | latest |
| scikit-learn | latest |
| joblib | latest |
| pymysql | latest |
| pytz | latest |

Ver [requirements.txt](requirements.txt) para la lista completa.

## 🏃 Ejecución

### Desarrollo Local

```bash
uvicorn app_3:app --reload --host 0.0.0.0 --port 8000
```

### Producción (Railway)

```bash
uvicorn app_3:app --host 0.0.0.0 --port $PORT
```

La aplicación estará disponible en: `http://localhost:8000`

## 📚 Endpoints

### 1. Health Check
```
GET /health
```
Verifica el estado de la aplicación.

**Respuesta:**
```json
{
  "status": "ok"
}
```

### 2. Database Connection Check
```
GET /db-check
```
Valida la conexión a ambas bases de datos.

**Respuesta:**
```json
{
  "status": "success",
  "message": "Connected to both databases successfully."
}
```

### 3. Predicción
```
POST /predict
```
Procesa un archivo CSV y genera predicciones usando el modelo entrenado.

**Parámetros:**
- `file` (UploadFile): Archivo CSV con datos para predicción

**Respuesta:**
```json
{
  "predictions": [...],
  "timestamp": "2024-05-20T10:30:00"
}
```

### 4. Root
```
GET /
```
Endpoint de prueba.

**Respuesta:**
```json
{
  "message": "hello world"
}
```

## 🤖 Modelo de Machine Learning

- **Tipo**: Regresión Lineal
- **Archivo**: `linear_regression.joblib`
- **Features seleccionadas**: `selected_features.csv`
- **Descripción**: Predice valores numéricos basado en características específicas

## 📂 Estructura del Proyecto

```
├── app_1.py                          # Aplicación alternativa
├── app_2.py                          # Aplicación alternativa
├── app_3.py                          # Aplicación principal
├── linear_regression.joblib          # Modelo ML entrenado
├── selected_features.csv             # Features del modelo
├── requirements.txt                  # Dependencias Python
├── railway.toml                      # Configuración Railway
├── tabla_prediction_and_items.txt   # Datos de ejemplo
└── README.md                         # Este archivo
```

## 🌐 Despliegue en Railway

El proyecto está configurado para desplegarse en [Railway](https://railway.app/).

**Configuración:**
- Builder: NIXPACKS
- Start Command: `uvicorn app_3:app --host 0.0.0.0 --port $PORT`
- Health Check: `/health`
- Replicas: 1

**Pasos de despliegue:**
1. Conecta tu repositorio GitHub a Railway
2. Configura las variables de entorno (`SQLALCHEMY_DATABASE_URL`, `SQLALCHEMY_DATABASE_URL1`)
3. Railway desplegará automáticamente en cada push a `main`

## ⚠️ Notas Importantes

- Asegúrate de que las variables de entorno `SQLALCHEMY_DATABASE_URL` y `SQLALCHEMY_DATABASE_URL1` están correctamente configuradas
- El modelo `linear_regression.joblib` debe estar en el mismo directorio que la aplicación
- Las features esperadas deben coincidir con las especificadas en `selected_features.csv`

## 🔐 Seguridad

- Las credenciales de base de datos se cargan desde variables de entorno
- No commits credenciales en el repositorio
- Usa archivos `.env` locales (no versionados)

## 📝 Autor

Fabian Rojas

## 📄 Licencia

Este proyecto es parte del curso MLOps de DataPath.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para reportar problemas o hacer preguntas, abre un [Issue](https://github.com/FabianRojas1/Datapath-mlops15-FR-railway/issues) en GitHub.

---

**Última actualización:** Mayo 2026
