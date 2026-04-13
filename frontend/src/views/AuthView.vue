<template>
  <div class="auth-container -m-8 flex flex-1 h-full overflow-hidden">
    <div
      class="left-item bg-cindianred w-1/2 hidden md:flex flex-col justify-center items-center text-cgainsboro text-center p-8 gap-6"
    >
      <img :src="generatedLogo" alt="Generated Logo" class="logo size-64 object-contain" />

      <div class="space-y-2">
        <h1 class="text-4xl font-bold">Welcome Back!</h1>
        <p class="text-lg max-w-md">
          Please log in to access your dashboard and manage your board games.
        </p>
      </div>
    </div>

    <div
      class="right-item w-full md:w-1/2 flex flex-col justify-center items-center text-cblack text-center p-8 gap-6"
    >
      <AuthForm />
    </div>
  </div>
</template>

<script setup lang="ts">
import generatedLogo from '@/assets/generatedLogo.png'
import AuthForm from '@/components/AuthForm.vue'
</script>
