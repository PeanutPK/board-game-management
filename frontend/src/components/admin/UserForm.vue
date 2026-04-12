<template>
  <section class="view-panel shadow-md">
    <div class="panel-header">
      <div>
        <h2>{{ editingUserId ? 'Edit user' : 'Add user' }}</h2>
        <p>{{ editingUserId ? 'Update the selected account.' : 'Create a new user account.' }}</p>
      </div>
      <button v-if="editingUserId" class="action-btn ghost" type="button" @click="$emit('reset')">
        Cancel edit
      </button>
    </div>

    <form class="user-form" @submit.prevent="handleSubmit">
      <label>
        <span>Email</span>
        <input v-model="localForm.email" type="email" required />
      </label>

      <label>
        <span>Username</span>
        <input v-model="localForm.username" type="text" required />
      </label>

      <label>
        <span>Password {{ editingUserId ? '(leave blank to keep current)' : '' }}</span>
        <input v-model="localForm.password" type="password" :required="!editingUserId" />
      </label>

      <div class="role-grid">
        <label class="check-card">
          <span>
            <div class="flex justify-between items-center">
              <div>
                <strong>Admin</strong>
                <small>Full access to user management.</small>
              </div>
              <input v-model="localForm.is_admin" type="checkbox" class="size-4" />
            </div>
          </span>
        </label>

        <label class="check-card">
          <span>
            <div class="flex justify-between items-center">
              <div>
                <strong>Staff</strong>
                <small>Operational access for staff tasks.</small>
              </div>
              <input v-model="localForm.is_staff" type="checkbox" class="size-4" />
            </div>
          </span>
        </label>
      </div>

      <p v-if="statusMessage" class="status-message">{{ statusMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <div class="form-actions">
        <button class="action-btn primary" type="submit" :disabled="isSaving">
          {{ isSaving ? 'Saving...' : editingUserId ? 'Update user' : 'Add user' }}
        </button>
        <button class="action-btn secondary" type="button" @click="$emit('reset')">Clear</button>
      </div>
    </form>
  </section>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

type AdminFormData = {
  email: string
  username: string
  password: string
  is_staff: boolean
  is_admin: boolean
}

const props = defineProps<{
  form: {
    email: string
    username: string
    password: string
    is_staff: boolean
    is_admin: boolean
  }
  editingUserId: number | null
  statusMessage: string
  errorMessage: string
  isSaving: boolean
}>()

const emit = defineEmits<{
  submit: [payload: AdminFormData]
  reset: []
}>()

const localForm = reactive<AdminFormData>({
  email: '',
  username: '',
  password: '',
  is_staff: true,
  is_admin: false,
})

function syncLocalForm() {
  localForm.email = props.form.email
  localForm.username = props.form.username
  localForm.password = props.form.password
  localForm.is_staff = props.form.is_staff
  localForm.is_admin = props.form.is_admin
}

watch(
  () => props.form,
  () => {
    syncLocalForm()
  },
  { deep: true, immediate: true },
)

function handleSubmit() {
  emit('submit', {
    email: localForm.email,
    username: localForm.username,
    password: localForm.password,
    is_staff: localForm.is_staff,
    is_admin: localForm.is_admin,
  })
}
</script>
