<template>
  <div class="stores-view">
    <h1>Stores</h1>

    <div class="toolbar">
      <button class="btn-primary" @click="openCreateModal">+ Add Store</button>
    </div>

    <div v-if="loading" class="loading">Loading stores…</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="grid">
      <StoreCard
        v-for="store in stores"
        :key="store.id"
        :store="store"
        @edit="openEditModal"
        @delete="deleteStore"
      />
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ editingStore ? 'Edit Store' : 'Add Store' }}</h2>
        <form @submit.prevent="saveStore">
          <label>Name
            <input v-model="form.name" required />
          </label>
          <label>Location
            <input v-model="form.location" required />
          </label>
          <label>Contact
            <input v-model="form.contact" />
          </label>
          <div class="modal-actions">
            <button type="button" @click="closeModal">Cancel</button>
            <button type="submit" class="btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { storesApi } from '../services/api'
import StoreCard from '../components/StoreCard.vue'

const stores = ref([])
const loading = ref(false)
const error = ref(null)
const showModal = ref(false)
const editingStore = ref(null)

const defaultForm = () => ({ name: '', location: '', contact: '' })
const form = ref(defaultForm())

async function fetchStores() {
  loading.value = true
  error.value = null
  try {
    const res = await storesApi.list()
    stores.value = res.data
  } catch (e) {
    error.value = 'Failed to load stores. Is the backend running?'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingStore.value = null
  form.value = defaultForm()
  showModal.value = true
}

function openEditModal(store) {
  editingStore.value = store
  form.value = { ...store }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function saveStore() {
  try {
    if (editingStore.value) {
      await storesApi.update(editingStore.value.id, form.value)
    } else {
      await storesApi.create(form.value)
    }
    closeModal()
    fetchStores()
  } catch (e) {
    alert('Failed to save store.')
  }
}

async function deleteStore(store) {
  if (!confirm(`Delete "${store.name}"?`)) return
  try {
    await storesApi.remove(store.id)
    fetchStores()
  } catch (e) {
    alert('Failed to delete store.')
  }
}

onMounted(fetchStores)
</script>

<style scoped>
.stores-view {
  padding: 2rem;
}

.toolbar {
  margin-bottom: 1.5rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.2rem;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  color: #888;
}

.error {
  color: #c0392b;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  width: 380px;
  max-width: 95vw;
}

.modal h2 {
  margin-top: 0;
}

form label {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
  color: #444;
}

form input {
  margin-top: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn-primary {
  background: #42b883;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

.btn-primary:hover {
  background: #33a06f;
}
</style>
