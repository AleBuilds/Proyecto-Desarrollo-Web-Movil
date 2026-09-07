const mongoose = require('mongoose');

const mensajeSchema = new mongoose.Schema({
    nombre: { type: String, required: true },
    email: { type: String, required: true },
    contenido: { type: String, required: true }
});

module.exports = mongoose.model('Mensaje', mensajeSchema);

