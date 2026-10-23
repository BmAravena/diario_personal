-- Cambia my_database por el valor NAME configurado en el archivo .env.
CREATE DATABASE IF NOT EXISTS my_database
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE my_database;


CREATE TABLE IF NOT EXISTS diario_personal_perfilacceso (
    id BIGINT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion LONGTEXT NOT NULL,
    puede_administrar TINYINT(1) NOT NULL,
    puede_auditar TINYINT(1) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_perfilacceso_nombre_uniq (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_categoria (
    id BIGINT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion LONGTEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_categoria_nombre_uniq (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_usuario (
    id BIGINT NOT NULL AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6) NULL,
    is_superuser TINYINT(1) NOT NULL,
    username VARCHAR(150) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff TINYINT(1) NOT NULL,
    is_active TINYINT(1) NOT NULL,
    date_joined DATETIME(6) NOT NULL,
    fecha_registro DATETIME(6) NOT NULL,
    activo TINYINT(1) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_usuario_username_uniq (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_usuario_perfiles (
    id BIGINT NOT NULL AUTO_INCREMENT,
    usuario_id BIGINT NOT NULL,
    perfilacceso_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_usuario_perfiles_uniq (usuario_id, perfilacceso_id),
    KEY diario_personal_usuario_perfiles_perfil_idx (perfilacceso_id),
    CONSTRAINT diario_personal_usuario_perfiles_usuario_fk
        FOREIGN KEY (usuario_id) REFERENCES diario_personal_usuario (id)
        ON DELETE CASCADE,
    CONSTRAINT diario_personal_usuario_perfiles_perfil_fk
        FOREIGN KEY (perfilacceso_id) REFERENCES diario_personal_perfilacceso (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_usuario_groups (
    id BIGINT NOT NULL AUTO_INCREMENT,
    usuario_id BIGINT NOT NULL,
    group_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_usuario_groups_uniq (usuario_id, group_id),
    KEY diario_personal_usuario_groups_group_idx (group_id),
    CONSTRAINT diario_personal_usuario_groups_usuario_fk
        FOREIGN KEY (usuario_id) REFERENCES diario_personal_usuario (id)
        ON DELETE CASCADE,
    CONSTRAINT diario_personal_usuario_groups_group_fk
        FOREIGN KEY (group_id) REFERENCES auth_group (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_usuario_user_permissions (
    id BIGINT NOT NULL AUTO_INCREMENT,
    usuario_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_usuario_user_permissions_uniq (usuario_id, permission_id),
    KEY diario_personal_usuario_user_permissions_permission_idx (permission_id),
    CONSTRAINT diario_personal_usuario_user_permissions_usuario_fk
        FOREIGN KEY (usuario_id) REFERENCES diario_personal_usuario (id)
        ON DELETE CASCADE,
    CONSTRAINT diario_personal_usuario_user_permissions_permission_fk
        FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_entrada (
    id BIGINT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(200) NOT NULL,
    contenido LONGTEXT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'borrador',
    visibilidad VARCHAR(10) NOT NULL DEFAULT 'privada',
    fecha_creacion DATETIME(6) NOT NULL,
    fecha_modificacion DATETIME(6) NOT NULL,
    autor_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY diario_personal_entrada_estado_idx (estado),
    KEY diario_personal_entrada_visibilidad_idx (visibilidad),
    KEY diario_personal_entrada_fecha_creacion_idx (fecha_creacion),
    KEY diario_personal_entrada_autor_idx (autor_id),
    KEY diario_pers_autor_i_6ae52b_idx (autor_id, estado),
    KEY diario_pers_visibil_6524f3_idx (visibilidad, estado),
    CONSTRAINT diario_personal_entrada_autor_fk
        FOREIGN KEY (autor_id) REFERENCES diario_personal_usuario (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_entrada_categorias (
    id BIGINT NOT NULL AUTO_INCREMENT,
    entrada_id BIGINT NOT NULL,
    categoria_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY diario_personal_entrada_categorias_uniq (entrada_id, categoria_id),
    KEY diario_personal_entrada_categorias_categoria_idx (categoria_id),
    CONSTRAINT diario_personal_entrada_categorias_entrada_fk
        FOREIGN KEY (entrada_id) REFERENCES diario_personal_entrada (id)
        ON DELETE CASCADE,
    CONSTRAINT diario_personal_entrada_categorias_categoria_fk
        FOREIGN KEY (categoria_id) REFERENCES diario_personal_categoria (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_historialestado (
    id BIGINT NOT NULL AUTO_INCREMENT,
    estado_anterior VARCHAR(20) NOT NULL,
    estado_nuevo VARCHAR(20) NOT NULL,
    fecha DATETIME(6) NOT NULL,
    motivo LONGTEXT NOT NULL,
    entrada_id BIGINT NOT NULL,
    usuario_id BIGINT NULL,
    PRIMARY KEY (id),
    KEY diario_personal_historialestado_fecha_idx (fecha),
    KEY diario_personal_historialestado_entrada_idx (entrada_id),
    KEY diario_personal_historialestado_usuario_idx (usuario_id),
    CONSTRAINT diario_personal_historialestado_entrada_fk
        FOREIGN KEY (entrada_id) REFERENCES diario_personal_entrada (id)
        ON DELETE CASCADE,
    CONSTRAINT diario_personal_historialestado_usuario_fk
        FOREIGN KEY (usuario_id) REFERENCES diario_personal_usuario (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_adjunto (
    id BIGINT NOT NULL AUTO_INCREMENT,
    tipo VARCHAR(20) NOT NULL,
    archivo VARCHAR(100) NOT NULL,
    tamano_bytes INT UNSIGNED NULL,
    fecha_subida DATETIME(6) NOT NULL,
    entrada_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY diario_personal_adjunto_entrada_idx (entrada_id),
    CONSTRAINT diario_personal_adjunto_entrada_fk
        FOREIGN KEY (entrada_id) REFERENCES diario_personal_entrada (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_comentario (
    id BIGINT NOT NULL AUTO_INCREMENT,
    contenido LONGTEXT NOT NULL,
    fecha DATETIME(6) NOT NULL,
    entrada_id BIGINT NOT NULL,
    autor_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY diario_personal_comentario_entrada_idx (entrada_id),
    KEY diario_personal_comentario_autor_idx (autor_id),
    CONSTRAINT diario_personal_comentario_entrada_fk
        FOREIGN KEY (entrada_id) REFERENCES diario_personal_entrada (id)
        ON DELETE CASCADE,
    CONSTRAINT diario_personal_comentario_autor_fk
        FOREIGN KEY (autor_id) REFERENCES diario_personal_usuario (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS diario_personal_sesionactividad (
    id BIGINT NOT NULL AUTO_INCREMENT,
    accion VARCHAR(100) NOT NULL,
    fecha DATETIME(6) NOT NULL,
    ip_address CHAR(39) NULL,
    detalle JSON NOT NULL,
    usuario_id BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY diario_personal_sesionactividad_fecha_idx (fecha),
    KEY diario_personal_sesionactividad_usuario_idx (usuario_id),
    KEY diario_pers_usuario_d75a57_idx (usuario_id, fecha),
    CONSTRAINT diario_personal_sesionactividad_usuario_fk
        FOREIGN KEY (usuario_id) REFERENCES diario_personal_usuario (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
