-- =====================================================
-- CREAR EL USUARIO
-- =====================================================

-- Crea un usuario para que la aplicacion se conecte a la base de datos desde el equipo local
CREATE USER IF NOT EXISTS 'techflow_app'@'localhost'
    IDENTIFIED BY 'techflow';


-- =====================================================
-- ASIGNAR PERMISOS
-- =====================================================

-- Permite consultar, insertar, modificar y eliminar registros dentro de la base de datos techflow
GRANT
    SELECT,
    INSERT,
    UPDATE,
    DELETE
ON techflow.*
TO 'techflow_app'@'localhost';


-- =====================================================
-- ACTUALIZAR LOS PRIVILEGIOS
-- =====================================================

-- Solicita que mysql actualice los privilegios
FLUSH PRIVILEGES;