<template>
  <div class="admin-view">
    <section class="admin-hero">
      <div>
        <p class="eyebrow">Admin</p>
        <h1>User Management</h1>
        <p class="subtext">Create accounts, adjust roles, and remove users from one place.</p>
      </div>
      <button class="action-btn secondary" type="button" @click="loadUsers">Refresh</button>
    </section>

    <section class="admin-panel">
      <div class="panel-header">
        <div>
          <h2>{{ editingUserId ? 'Edit user' : 'Add user' }}</h2>
          <p>{{ editingUserId ? 'Update the selected account.' : 'Create a new user account.' }}</p>
        </div>
        <button v-if="editingUserId" class="action-btn ghost" type="button" @click="resetForm">
          Cancel edit
        </button>
      </div>

      <form class="user-form" @submit.prevent="handleSubmit">
        <label>
          <span>Email</span>
          <input v-model="form.email" type="email" required />
        </label>

        <label>
          <span>Username</span>
          <input v-model="form.username" type="text" required />
        </label>

        <label>
          <span>Password {{ editingUserId ? '(leave blank to keep current)' : '' }}</span>
          <input v-model="form.password" type="password" :required="!editingUserId" />
        </label>

        <div class="role-grid">
          <label class="check-card">
            <input v-model="form.is_admin" type="checkbox" />
            <span>
              <strong>Admin</strong>
              <small>Full access to user management.</small>
            </span>
          </label>

          <label class="check-card">
            <input v-model="form.is_staff" type="checkbox" />
            <span>
              <strong>Staff</strong>
              <small>Operational access for staff tasks.</small>
            </span>
          </label>
        </div>

        <p v-if="statusMessage" class="status-message">{{ statusMessage }}</p>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div class="form-actions">
          <button class="action-btn primary" type="submit" :disabled="isSaving">
            {{ isSaving ? 'Saving...' : editingUserId ? 'Update user' : 'Add user' }}
          </button>
          <button class="action-btn secondary" type="button" @click="resetForm">Clear</button>
        </div>
      </form>
    </section>

    <section class="admin-panel">
      <div class="panel-header">
        <div>
          <h2>Users</h2>
          <p>{{ users.length }} account{{ users.length === 1 ? '' : 's' }} found</p>
        </div>
      </div>

      <div v-if="isLoading" class="empty-state">Loading users...</div>

      <div v-else-if="users.length === 0" class="empty-state">
        No users available yet.
      </div>

      <div v-else class="user-table">
        <div class="table-head">
          <span>User</span>
          <span>Role</span>
          <span>Actions</span>
        </div>

        <article v-for="user in users" :key="user.id" class="table-row">
          <div class="user-meta">
            <strong>{{ user.username }}</strong>
            <span>{{ user.email }}</span>
          </div>

          <div class="role-chip" :class="getRoleClass(user)">
            {{ getRoleLabel(user) }}
          </div>

          <div class="row-actions">
            <button class="action-btn secondary" type="button" @click="startEdit(user)">
              Edit
            </button>
            <button class="action-btn danger" type="button" @click="handleDelete(user)">
              Delete
            </button>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import {
  createUser,
  deleteUser,
  getUserProfiles,
  updateUser,
  type User,
  type UserCreateInput,
  type UserUpdateInput,
} from '@/api/user'

const users = ref<User[]>([])
const isLoading = ref(false)
const isSaving = ref(false)
const statusMessage = ref('')
const errorMessage = ref('')
const editingUserId = ref<number | null>(null)

const form = reactive({
  email: '',
  username: '',
  password: '',
  is_staff: true,
  is_admin: false,
})

function getRoleLabel(user: User): string {
  if (user.is_admin) return 'Admin'
  if (user.is_staff) return 'Staff'
  return 'User'
}

function getRoleClass(user: User): string {
  if (user.is_admin) return 'admin-role'
  if (user.is_staff) return 'staff-role'
  return 'user-role'
}

function setFeedback(message: string, error = false) {
  statusMessage.value = error ? '' : message
  errorMessage.value = error ? message : ''
}

function resetForm() {
  editingUserId.value = null
  form.email = ''
  form.username = ''
  form.password = ''
  form.is_staff = true
  form.is_admin = false
  setFeedback('')
}

function startEdit(user: User) {
  editingUserId.value = user.id
  form.email = user.email
  form.username = user.username
  form.password = ''
  form.is_staff = user.is_staff
  form.is_admin = user.is_admin
  setFeedback(`Editing ${user.username}`)
}

async function loadUsers() {
  isLoading.value = true
  setFeedback('')
  try {
    users.value = await getUserProfiles()
  } catch (error) {
    setFeedback(error instanceof Error ? error.message : 'Failed to load users', true)
  } finally {
    isLoading.value = false
  }
}

async function handleSubmit() {
  isSaving.value = true
  setFeedback('')

  try {
    if (editingUserId.value) {
      const payload: UserUpdateInput = {
        email: form.email,
        username: form.username,
        is_staff: form.is_staff,
        is_admin: form.is_admin,
      }

      if (form.password.trim()) {
        payload.password = form.password
      }

      await updateUser(editingUserId.value, payload)
      setFeedback('User updated successfully')
    } else {
      const payload: UserCreateInput = {
        email: form.email,
        username: form.username,
        password: form.password,
        is_staff: form.is_staff,
        is_admin: form.is_admin,
      }

      await createUser(payload)
      setFeedback('User created successfully')
    }

    resetForm()
    await loadUsers()
  } catch (error) {
    setFeedback(error instanceof Error ? error.message : 'Failed to save user', true)
  } finally {
    isSaving.value = false
  }
}

async function handleDelete(user: User) {
  const confirmed = window.confirm(`Delete ${user.username}? This cannot be undone.`)
  if (!confirmed) return

  try {
    await deleteUser(user.id)
    if (editingUserId.value === user.id) {
      resetForm()
    }
    await loadUsers()
    setFeedback('User deleted successfully')
  } catch (error) {
    setFeedback(error instanceof Error ? error.message : 'Failed to delete user', true)
  }
}

onMounted(loadUsers)
</script>

<style scoped>
.admin-view {
  display: grid;
  gap: 1.25rem;
}

.admin-hero,
.admin-panel {
  border: 1px solid rgba(67, 86, 99, 0.16);
  border-radius: 1.1rem;
  background: linear-gradient(180deg, #fff8e7 0%, #fff4d7 100%);
  box-shadow: 0 18px 45px rgba(44, 44, 44, 0.08);
}

.admin-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.4rem 1.5rem;
}

.eyebrow {
  margin: 0 0 0.35rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  font-weight: 700;
  color: #a64f2f;
}

.admin-hero h1,
.panel-header h2 {
  margin: 0;
}

.subtext,
.panel-header p,
.empty-state,
.status-message,
.error-message {
  margin: 0;
}

.subtext,
.panel-header p {
  color: #5c5244;
}

.admin-panel {
  padding: 1.25rem;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-form {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.user-form label {
  display: grid;
  gap: 0.45rem;
}

.user-form span {
  font-weight: 600;
}

.user-form input[type='text'],
.user-form input[type='email'],
.user-form input[type='password'] {
  padding: 0.85rem 0.95rem;
  border-radius: 0.8rem;
  border: 1px solid rgba(67, 86, 99, 0.22);
  background: #fffdf8;
}

.role-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.85rem;
}

.check-card {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.9rem;
  border-radius: 0.9rem;
  border: 1px solid rgba(67, 86, 99, 0.18);
  background: rgba(255, 255, 255, 0.5);
}

.check-card strong,
.user-meta strong {
  display: block;
}

.check-card small,
.user-meta span {
  color: #665c4f;
}

.form-actions,
.row-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  border: 0;
  border-radius: 0.8rem;
  padding: 0.8rem 1rem;
  font-weight: 700;
  cursor: pointer;
}

.action-btn.primary {
  background: #a64f2f;
  color: #fff;
}

.action-btn.secondary {
  background: #f0e0b5;
  color: #4d3b2b;
}

.action-btn.ghost {
  background: transparent;
  border: 1px solid rgba(67, 86, 99, 0.22);
  color: #4d3b2b;
}

.action-btn.danger {
  background: #c94d4d;
  color: #fff;
}

.action-btn:disabled {
  cursor: progress;
  opacity: 0.75;
}

.status-message {
  color: #2d6a45;
  font-weight: 600;
}

.error-message {
  color: #a63434;
  font-weight: 600;
}

.empty-state {
  padding: 1rem 0.25rem;
  color: #665c4f;
}

.user-table {
  display: grid;
  gap: 0.75rem;
}

.table-head,
.table-row {
  display: grid;
  grid-template-columns: 1.4fr 0.7fr 1fr;
  gap: 1rem;
  align-items: center;
}

.table-head {
  padding: 0 0.4rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #665c4f;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.table-row {
  padding: 1rem;
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.68);
  border: 1px solid rgba(67, 86, 99, 0.12);
}

.user-meta {
  display: grid;
  gap: 0.2rem;
}

.role-chip {
  width: fit-content;
  padding: 0.4rem 0.7rem;
  border-radius: 999px;
  font-weight: 700;
}

.admin-role {
  background: #f2c06d;
  color: #5a350d;
}

.staff-role {
  background: #d5e7ff;
  color: #214d86;
}

.user-role {
  background: #e6e2da;
  color: #5a5246;
}

@media (max-width: 760px) {
  .admin-hero,
  .panel-header,
  .table-head,
  .table-row {
    grid-template-columns: 1fr;
    display: grid;
  }

  .admin-hero {
    align-items: start;
  }

  .table-head {
    display: none;
  }
}
</style>
