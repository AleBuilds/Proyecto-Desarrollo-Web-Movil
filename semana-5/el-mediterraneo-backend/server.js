const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const mongoose = require('mongoose');
const cors = require('cors');

const Producto = require('./models/producto');
const Mensaje = require('./models/mensaje');

const typeDefs = gql`
    type Producto {
        id: ID!
        nombre: String!
        categoria: String!
        descripcion: String
        precio: Float!
    }

    type Mensaje {
        id: ID!
        nombre: String!
        email: String!
        contenido: String!
    }

    input ProductoInput {
        nombre: String!
        categoria: String!
        descripcion: String
        precio: Float!
    }

    input MensajeInput {
        nombre: String!
        email: String!
        contenido: String!
    }

    type Alert {
        message: String
    }

    type Query {
        getProductos: [Producto]
        getMensajes: [Mensaje]
    }

    type Mutation {
        addProducto(input: ProductoInput): Producto
        delProducto(id: ID!): Alert
        addMensaje(input: MensajeInput): Mensaje
    }
`;

const resolvers = {
    Query: {
        async getProductos() {
            return await Producto.find();
        },
        async getMensajes() {
            return await Mensaje.find();
        }
    },
    Mutation: {
        async addProducto(_, { input }) {
            const nuevoProducto = new Producto(input);
            return await nuevoProducto.save();
        },
        async delProducto(_, { id }) {
            await Producto.findByIdAndDelete(id);
            return { message: "Producto eliminado correctamente" };
        },
        async addMensaje(_, { input }) {
            const nuevoMensaje = new Mensaje(input);
            return await nuevoMensaje.save();
        }
    }
};

async function startServer() {
    const app = express();
    app.use(cors());

    const server = new ApolloServer({ typeDefs, resolvers });
    await server.start();
    server.applyMiddleware({ app });

    await mongoose.connect('mongodb://127.0.0.1:27017/el_mediterraneo');
    console.log('Conectado a la base de datos de El Mediterráneo');

    app.listen(4000, () => {
        console.log(`🚀 Graphql Iniciado en http://localhost:4000${server.graphqlPath}`);
    });
}

startServer();