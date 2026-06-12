const fastify = require('fastify')({ logger: false });
const { Sequelize, DataTypes } = require('sequelize');
const crypto = require('crypto');

// Database setup
const sequelize = new Sequelize('mysql://admin:secret@127.0.0.1:3306/benchmark_db', {
    logging: false,
    pool: { max: 10, min: 0, acquire: 30000, idle: 10000 }
});

// Models (disable timestamps to match raw table schema)
const User = sequelize.define('User', {
    name: DataTypes.STRING,
    email: { type: DataTypes.STRING, unique: true }
}, { tableName: 'users', timestamps: false });

const Profile = sequelize.define('Profile', {
    user_id: DataTypes.INTEGER,
    bio: DataTypes.STRING,
    phone: DataTypes.STRING
}, { tableName: 'profiles', timestamps: false });

const Order = sequelize.define('Order', {
    user_id: DataTypes.INTEGER,
    total_amount: DataTypes.DECIMAL(10, 2)
}, { tableName: 'orders', timestamps: false });

const OrderItem = sequelize.define('OrderItem', {
    order_id: DataTypes.INTEGER,
    product_name: DataTypes.STRING,
    price: DataTypes.DECIMAL(10, 2)
}, { tableName: 'order_items', timestamps: false });

const getHex = () => crypto.randomBytes(4).toString('hex');

fastify.post('/orm/post/1table', async (request, reply) => {
    const t = await sequelize.transaction();
    try {
        const randId = getHex();
        const user = await User.create({ name: `User_${randId}`, email: `test_${randId}@example.com` }, { transaction: t });
        await t.commit();
        reply.code(201).send({ user_id: user.id });
    } catch (err) {
        await t.rollback();
        reply.code(500).send({ error: err.message });
    }
});

fastify.post('/orm/post/2table', async (request, reply) => {
    const t = await sequelize.transaction();
    try {
        const randId = getHex();
        const user = await User.create({ name: `User_${randId}`, email: `test_${randId}@example.com` }, { transaction: t });
        await Profile.create({ user_id: user.id, bio: `Bio for user ${user.id}`, phone: `555-${randId}` }, { transaction: t });
        await t.commit();
        reply.code(201).send({ user_id: user.id });
    } catch (err) {
        await t.rollback();
        reply.code(500).send({ error: err.message });
    }
});

fastify.post('/orm/post/3table', async (request, reply) => {
    const t = await sequelize.transaction();
    try {
        const randId = getHex();
        const user = await User.create({ name: `User_${randId}`, email: `test_${randId}@example.com` }, { transaction: t });
        await Profile.create({ user_id: user.id, bio: `Bio for user ${user.id}`, phone: `555-${randId}` }, { transaction: t });
        await Order.create({ user_id: user.id, total_amount: 100.00 }, { transaction: t });
        await t.commit();
        reply.code(201).send({ user_id: user.id });
    } catch (err) {
        await t.rollback();
        reply.code(500).send({ error: err.message });
    }
});

fastify.post('/orm/post/4table', async (request, reply) => {
    const t = await sequelize.transaction();
    try {
        const randId = getHex();
        const user = await User.create({ name: `User_${randId}`, email: `test_${randId}@example.com` }, { transaction: t });
        await Profile.create({ user_id: user.id, bio: `Bio for user ${user.id}`, phone: `555-${randId}` }, { transaction: t });
        const order = await Order.create({ user_id: user.id, total_amount: 100.00 }, { transaction: t });
        
        await OrderItem.bulkCreate([
            { order_id: order.id, product_name: `Product_${randId}_1`, price: 25.00 },
            { order_id: order.id, product_name: `Product_${randId}_2`, price: 75.00 }
        ], { transaction: t });

        await t.commit();
        reply.code(201).send({ user_id: user.id });
    } catch (err) {
        await t.rollback();
        reply.code(500).send({ error: err.message });
    }
});

fastify.listen({ port: 8002, host: '0.0.0.0' }, (err) => {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    console.log('Fastify ORM server listening on port 8002');
});