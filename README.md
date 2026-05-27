# 🛡️ Sistema de Gestión - Vigilancia Montebello

Control de aportes mensuales, morosidad y actualización de base de datos para la administración de pagos residenciales.

## 📂 Estructura del Proyecto

```
control-pagos/
│
├── app.py                # Aplicación principal e Interfaz Gráfica (Streamlit)
├── database.py           # Lógica de la Base de Datos (SQLite y Consultas SQL)
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación y guía de instalación del proyecto
```

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/rubenp138/control-pagos.git
cd control-pagos
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📋 Características

### 📊 Dashboard
- Visualización de indicadores clave (KPIs)
- Total recaudado histórico
- Total de residentes registrados
- Matriz general de control de pagos
- Búsqueda rápida por nombre o lote

### 👥 Administración de Residentes
- **Agregar nuevos residentes** con nombre y número de lote
- **Visualizar** lista de residentes activos
- **Editar** información de residentes
- **Eliminar** registros permanentemente

### 💰 Registro de Pagos
- Carga de aportaciones mensuales
- Registro de monto y estado del pago (Pagado, Parcial, Deuda)
- Actualización automática de registros existentes

## 🗄️ Base de Datos

El proyecto utiliza SQLite con dos tablas principales:

### Tabla: `residentes`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | Identificador único (PK) |
| `nombre` | TEXT | Nombre completo del residente |
| `lote` | TEXT | Número único de lote/casa |

### Tabla: `pagos`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | Identificador único (PK) |
| `residente_id` | INTEGER | Referencia al residente (FK) |
| `mes` | TEXT | Mes del pago |
| `anio` | TEXT | Año del pago |
| `monto` | REAL | Monto recaudado |
| `estado` | TEXT | Estado (Pagado, Parcial, Deuda) |

## 🔍 Ventajas del Sistema

✅ **Evita redundancia de datos**: Separación de residentes y pagos mensuales  
✅ **Buscador predictivo**: Filtro instantáneo por lote o nombre  
✅ **Escalable**: Preparado para recibir nuevos meses sin alterar la arquitectura  
✅ **Auditable**: Tracking completo de deudas y pagos  
✅ **Interfaz intuitiva**: Diseño simple y fácil de usar  

## 🛠️ Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 📝 Notas

- La base de datos se genera automáticamente en la primera ejecución
- Los datos se almacenan en `vigilancia_montebello.db`
- El sistema es completamente local (sin conexión a internet requerida)

## 📧 Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio.

---

**Versión**: 1.0  
**Última actualización**: 2026-05-27
