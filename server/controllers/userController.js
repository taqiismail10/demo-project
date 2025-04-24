const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// GET all users
const getAllUsers = async (req, res) => {
  try {
    const users = await prisma.user.findMany();
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: 'Server Error' });
  }
};

// GET user by ID
const getUserById = async (req, res) => {
  const { id } = req.params;
  try {
    const user = await prisma.user.findUnique({ where: { id: Number(id) } });
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: 'Server Error' });
  }
};

// POST create user
const createUser = async (req, res) => {
  const { name, email } = req.body;
  try {
    const newUser = await prisma.user.create({ data: { name, email } });
    res.status(201).json(newUser);
  } catch (err) {
    res.status(400).json({ error: 'Create failed' });
  }
};

// PUT update user
const updateUser = async (req, res) => {
  const { id } = req.params;
  const { name, email } = req.body;
  try {
    const updatedUser = await prisma.user.update({
      where: { id: Number(id) },
      data: { name, email },
    });
    res.json(updatedUser);
  } catch (err) {
    res.status(400).json({ error: 'Update failed' });
  }
};

// DELETE user
const deleteUser = async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.user.delete({ where: { id: Number(id) } });
    res.json({ message: 'User deleted' });
  } catch (err) {
    res.status(400).json({ error: 'Delete failed' });
  }
};

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
};
