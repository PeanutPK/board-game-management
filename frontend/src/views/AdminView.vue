<template>
  <div class="view">
    <section class="view-hero shadow-md">
      <div>
        <p class="eyebrow">Admin</p>
        <h1>User Management</h1>
        <p class="subtext">Create accounts, adjust roles, and remove users from one place.</p>
      </div>
    </section>

    <AdminUserForm
      :form="form"
      :editing-user-id="editingUserId"
      :status-message="statusMessage"
      :error-message="errorMessage"
      :is-saving="isSaving"
      @submit="handleSubmit"
      @reset="resetForm"
    />

    <AdminUserTable
      :users="users"
      :is-loading="isLoading"
      @refresh="loadUsers"
      @edit="startEdit"
      @delete="handleDelete"
    />
  </div>
</template>

<script setup lang="ts">
import '@/assets/admin.css'

import { onMounted, reactive, ref } from 'vue'
import AdminUserForm from '@/components/admin/UserForm.vue'
import AdminUserTable from '@/components/admin/UserTable.vue'
import {
  createUser,
  deleteUser,
  getUserProfiles,
  updateUser,
  type User,
  type UserCreateInput,
  type UserUpdateInput,
} from '@/api/user'

type AdminFormData = {
  email: string
  username: string
  password: string
  is_staff: boolean
  is_admin: boolean
}

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

async function handleSubmit(submittedForm: AdminFormData) {
  isSaving.value = true
  setFeedback('')

  try {
    if (editingUserId.value) {
      const payload: UserUpdateInput = {
        email: submittedForm.email,
        username: submittedForm.username,
        is_staff: submittedForm.is_staff,
        is_admin: submittedForm.is_admin,
      }

      if (submittedForm.password.trim()) {
        payload.password = submittedForm.password
      }

      await updateUser(editingUserId.value, payload)
      setFeedback('User updated successfully')
    } else {
      const payload: UserCreateInput = {
        email: submittedForm.email,
        username: submittedForm.username,
        password: submittedForm.password,
        is_staff: submittedForm.is_staff,
        is_admin: submittedForm.is_admin,
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
