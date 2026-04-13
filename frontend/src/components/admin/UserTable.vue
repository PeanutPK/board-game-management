<template>
  <section class="view-panel shadow-md">
    <div class="panel-header">
      <div>
        <h2>Users</h2>
        <p>{{ users.length }} account{{ users.length === 1 ? '' : 's' }} found</p>
      </div>

      <button
        class="action-btn secondary"
        type="button"
        :disabled="isLoading"
        @click="$emit('refresh')"
      >
        Refresh
      </button>
    </div>

    <div v-if="isLoading" class="empty-state">Loading users...</div>

    <div v-else-if="users.length === 0" class="empty-state">No users available yet.</div>

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
          <button class="action-btn secondary" type="button" @click="$emit('edit', user)">
            Edit
          </button>
          <button class="action-btn danger" type="button" @click="$emit('delete', user)">
            Delete
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { User } from '@/api/user'

defineProps<{
  users: User[]
  isLoading: boolean
}>()

defineEmits<{
  edit: [user: User]
  delete: [user: User]
  refresh: []
}>()

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
</script>
