<template>
  <div class="flex items-center justify-center h-full w-full">
    <div class="w-90 flex flex-col gap-6 p-6">
      <div class="flex w-full bg-cgainsboro rounded-xl p-1.5">
        <button
          @click="currentForm = 'login'"
          :class="[
            'flex-1 py-3 px-6 rounded-lg text-lg font-semibold transition-all duration-300',
            currentForm === 'login'
              ? 'bg-cdarkslategray text-white shadow' /* Active Style */
              : 'text-cblack hover:bg-gray-200' /* Inactive Style */,
          ]"
        >
          Login
        </button>

        <button
          @click="currentForm = 'signup'"
          :class="[
            'flex-1 py-3 px-6 rounded-lg text-lg font-semibold transition-all duration-300',
            currentForm === 'signup'
              ? 'bg-cdarkslategray text-white shadow' /* Active Style */
              : 'text-cblack hover:bg-gray-200' /* Inactive Style */,
          ]"
        >
          Sign up
        </button>
      </div>

      <div class="flex flex-col gap-4">
        <div class="relative group">
          <Icon
            icon="icon-park-outline:people"
            class="absolute left-4 top-1/2 -translate-y-1/2 size-6 text-cdarkslategray group-focus-within:text-cindianred transition-colors"
          />
          <input
            v-model="formData.username"
            type="text"
            placeholder="Username"
            required
            autocomplete="username"
            class="w-full pl-12 pr-4 py-3.5 bg-cgainsboro border border-cgainsboro rounded-xl text-cblack focus:ring-2 focus:ring-cindianred focus:border-cindianred outline-none transition-all placeholder:text-gray-600"
          />
        </div>

        <div v-if="currentForm === 'signup'" class="relative group">
          <Icon
            icon="ic:outline-email"
            class="absolute left-4 top-1/2 -translate-y-1/2 size-6 text-cdarkslategray group-focus-within:text-cindianred transition-colors"
          />
          <input
            v-model="formData.email"
            type="email"
            placeholder="Email"
            required
            autocomplete="email"
            class="w-full pl-12 pr-4 py-3.5 bg-cgainsboro border border-cgainsboro rounded-xl text-cblack focus:ring-2 focus:ring-cindianred focus:border-cindianred outline-none transition-all placeholder:text-gray-600"
          />
        </div>

        <div class="relative group">
          <Icon
            icon="material-symbols:lock-outline"
            class="absolute left-4 top-1/2 -translate-y-1/2 size-6 text-cdarkslategray group-focus-within:text-cindianred transition-colors"
          />
          <input
            v-model="formData.password"
            type="password"
            placeholder="Password"
            required
            minlength="8"
            maxlength="72"
            autocomplete="current-password"
            class="w-full pl-12 pr-4 py-3.5 bg-cgainsboro border border-cgainsboro rounded-xl text-cblack focus:ring-2 focus:ring-cindianred focus:border-cindianred outline-none transition-all placeholder:text-gray-600"
          />
        </div>
      </div>

      <button
        @click="handleSubmit"
        type="button"
        class="w-full py-4 bg-cdarkslategray hover:bg-cindianred text-white text-xl font-bold rounded-xl shadow-lg transition-all duration-300 transform active:scale-95"
      >
        {{ currentForm === 'login' ? 'Login' : 'Sign up' }}
      </button>

      <p
        v-if="errorMessage"
        class="text-sm text-red-600 font-medium text-center whitespace-pre-wrap"
      >
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '@/api/auth'
import { saveUserData } from '@/api/auth'
import { useUserStore } from '@/stores/counter'

import { Icon } from '@iconify/vue'

const currentForm = ref<'login' | 'signup'>('login')
const router = useRouter()
const userStore = useUserStore()
const errorMessage = ref('')

const formData = reactive({
  username: '',
  email: '',
  password: '',
})

const handleSubmit = async () => {
  try {
    errorMessage.value = ''
    const username = formData.username.trim()
    const email = formData.email.trim()
    const password = formData.password

    if (!username || !password || (currentForm.value === 'signup' && !email)) {
      errorMessage.value = 'Please fill in all required fields.'
      return
    }

    if (password.length < 8) {
      errorMessage.value = 'Password must be at least 8 characters long.'
      return
    }

    if (new TextEncoder().encode(password).length > 72) {
      errorMessage.value = 'Password cannot be longer than 72 bytes.'
      return
    }

    if (currentForm.value === 'login') {
      const response = await login({ username, password })
      saveUserData(response)
      userStore.setToken(response.access_token)
      userStore.setRole(response.user_role)
      userStore.setUsername(response.username)
      router.push('/')
    } else {
      const response = await register({
        email,
        username,
        password,
      })
      saveUserData(response)
      userStore.setToken(response.access_token)
      userStore.setRole(response.user_role)
      userStore.setUsername(response.username)
      router.push('/')
    }
  } catch (error) {
    console.error('Authentication error:', error)
    const responseError = error as {
      response?: { data?: { detail?: string | Array<{ msg?: string }> } }
    }
    const detail = responseError.response?.data?.detail
    if (typeof detail === 'string') {
      errorMessage.value = detail
    } else if (Array.isArray(detail)) {
      errorMessage.value = detail
        .map((item) => item.msg)
        .filter(Boolean)
        .join('\n')
    } else {
      errorMessage.value = 'An error occurred during authentication. Please try again.'
    }
  }
}
</script>
