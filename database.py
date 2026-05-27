import sqlite3

def conectar_db():
    conn = sqlite3.connect("vigilancia_montebello.db")
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Tabla de Residentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS residentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            lote TEXT NOT NULL UNIQUE
        )
    """)
    
    # Tabla de Pagos Mensuales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            residente_id INTEGER,
            mes TEXT NOT NULL,
            anio TEXT NOT NULL,
            monto REAL DEFAULT 0.0,
            estado TEXT NOT NULL CHECK(estado IN ('Pagado', 'Parcial', 'Deuda')),
            FOREIGN KEY(residente_id) REFERENCES residentes(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

# --- OPERACIONES CRUD ---

def registrar_residente(nombre, lote):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO residentes (nombre, lote) VALUES (?, ?)", (nombre, lote))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def obtener_residentes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM residentes ORDER BY nombre ASC")
    datos = cursor.fetchall()
    conn.close()
    return datos

def actualizar_residente(id_residente, nombre, lote):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE residentes SET nombre = ?, lote = ? WHERE id = ?", (nombre, lote, id_residente))
    conn.commit()
    conn.close()

def eliminar_residente(id_residente):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM residentes WHERE id = ?", (id_residente,))
    conn.commit()
    conn.close()

def registrar_o_actualizar_pago(residente_id, mes, anio, monto, estado):
    conn = conectar_db()
    cursor = conn.cursor()
    # Verificar si ya existe el registro de ese mes/año para actualizarlo
    cursor.execute("SELECT id FROM pagos WHERE residente_id = ? AND mes = ? AND anio = ?", (residente_id, mes, anio))
    existe = cursor.fetchone()
    
    if existe:
        cursor.execute("UPDATE pagos SET monto = ?, estado = ? WHERE id = ?", (monto, estado, existe[0]))
    else:
        cursor.execute("INSERT INTO pagos (residente_id, mes, anio, monto, estado) VALUES (?, ?, ?, ?, ?)", 
                       (residente_id, mes, anio, monto, estado))
    conn.commit()
    conn.close()

def obtener_matriz_pagos():
    conn = conectar_db()
    cursor = conn.cursor()
    query = """
        SELECT r.id, r.nombre, r.lote, p.mes, p.anio, p.monto, p.estado 
        FROM residentes r
        LEFT JOIN pagos p ON r.id = p.residente_id
    """
    cursor.execute(query)
    datos = cursor.fetchall()
    conn.close()
    return datos
