import { useEffect, useState } from 'react';

const API = 'http://localhost:5000/api/users';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ name: '', email: '' });
  const [editId, setEditId] = useState(null);

  const fetchUsers = async () => {
    const res = await fetch(API);
    const data = await res.json();
    setUsers(data);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const method = editId ? 'PUT' : 'POST';
    const url = editId ? `${API}/${editId}` : API;

    await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });

    setForm({ name: '', email: '' });
    setEditId(null);
    fetchUsers();
  };

  const handleDelete = async (id) => {
    await fetch(`${API}/${id}`, { method: 'DELETE' });
    fetchUsers();
  };

  const startEdit = (user) => {
    setForm({ name: user.name, email: user.email });
    setEditId(user.id);
  };

  return (
    <div>
      <h2 className="text-2xl mb-4">User Management</h2>

      <form onSubmit={handleSubmit} className="space-y-2 mb-6">
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          className="border px-2 py-1"
          required
        />
        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          className="border px-2 py-1"
          required
        />
        <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">
          {editId ? 'Update' : 'Add'}
        </button>
      </form>

      <ul className="space-y-2">
        {users.map((user) => (
          <li key={user.id} className="border p-2 flex justify-between items-center">
            <span>{user.name} - {user.email}</span>
            <div className="space-x-2">
              <button onClick={() => startEdit(user)} className="text-blue-600">Edit</button>
              <button onClick={() => handleDelete(user.id)} className="text-red-600">Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
