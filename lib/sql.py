import sqlite3

class SQLite:
    def __init__(self, db_path):
        """Guarda la ruta de la base de datos."""
        self.db_path = db_path

    def crear_evento(self, tabla, empresa, descripcion, archivos, fecha_carga, hora_carga, fecha_mod, actualizaciones, cargado_por, fecha_evento, encargado, estado):
        """Crea un evento en la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO {tabla} (empresa, descripcion, archivos, fecha_carga, hora_carga, fecha_mod, actualizaciones, cargado_por, fecha_evento, encargado, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
            cursor.execute(query, (empresa, descripcion, archivos, fecha_carga, hora_carga, fecha_mod, actualizaciones, cargado_por, fecha_evento, encargado, estado))

    def leer_eventos(self, tabla):
        """Lee todos los eventos de la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {tabla};"  # Use string formatting to insert the table name
            cursor.execute(query)
            return cursor.fetchall()

    def buscar_evento_por_fecha(self, tabla, fecha_evento):
        """Busca eventos por fecha en la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {tabla} WHERE fecha_evento = ?;"
            cursor.execute(query, (fecha_evento,))
            return cursor.fetchall()

    def buscar_evento_por_keyword(self, tabla, keyword):
        """Busca eventos por una palabra clave en cualquier campo de la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {tabla} WHERE empresa LIKE ? OR descripcion LIKE ? OR archivos LIKE ? OR fecha_carga LIKE ? OR hora_carga LIKE ? OR fecha_mod LIKE ? OR actualizaciones LIKE ? OR cargado_por LIKE ? OR fecha_evento LIKE ? OR encargado LIKE ? OR estado LIKE ?;"
            keyword = f"%{keyword}%"
            cursor.execute(query, (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword))
            return cursor.fetchall()

    def buscar_evento_especifico(self, tabla, fecha_carga, empresa, descripcion, encargado, fecha_evento):
        """Busca eventos por fecha en la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {tabla} WHERE fecha_carga = ? AND empresa = ? AND descripcion = ? AND encargado = ? AND fecha_evento = ?;"
            cursor.execute(query, (fecha_carga, empresa, descripcion, encargado, fecha_evento))
            return cursor.fetchall()

    def modificar_evento_user(self, tabla, fecha_carga, empresa, descripcion_vieja, descripcion_nueva, encargado, fecha_evento):
        """Modifica un evento en la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"UPDATE {tabla} SET descripcion = ? WHERE fecha_carga = ? AND empresa = ? AND descripcion = ? AND encargado = ? AND fecha_evento = ?;"
            cursor.execute(query, (descripcion_nueva, fecha_carga, empresa, descripcion_vieja, encargado, fecha_evento))

    # def modificar_evento_admin(self, tabla, fecha_carga, empresa_vieja, empresa_nueva, descripcion_vieja, descripcion_nueva, encargado_viejo,)

    def buscar_usuario(self, usuario):
        """Busca un usuario en la tabla de usuarios."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE user = ?;"
            cursor.execute(query, (usuario,)) 
            return cursor.fetchone()

    def obtener_usuarios(self):  
        """Obtiene todos los usuarios de la tabla de usuarios."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT user FROM users;"
            cursor.execute(query)
            return cursor.fetchall()

    def buscar_usuario_sector(self, sector):
        """Busca un usuario por sector en la tabla de usuarios, incluso si el sector no es exacto."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE sector LIKE ?;"
            cursor.execute(query, (f"%{sector}%",))
            return cursor.fetchall()
        
    def leer_empresas(self, tabla):
        """Lee todas las empresas de la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {tabla};"
            cursor.execute(query)
            return cursor.fetchall()
        
    def crear_empresa(self, tabla, nombre, cuit, direccion, contacto, email, telefono):
        """Crea una empresa en la tabla especificada."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO {tabla} (nombre, cuit, direccion, contacto, email, telefono) VALUES (?, ?, ?, ?, ?, ?);"
            cursor.execute(query, (nombre, cuit, direccion, contacto, email, telefono))

