CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel TEXT NOT NULL,
    articuloId INTEGER NOT NULL,
    FOREIGN KEY(articuloId) REFERENCES articulos(id)
);
