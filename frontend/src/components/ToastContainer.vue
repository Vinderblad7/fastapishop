<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-3 pointer-events-none">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        :class="[
          'pointer-events-auto flex items-center justify-between gap-4 px-5 py-3 border-2 border-black font-bold shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] text-sm min-w-[280px] max-w-md',
          toast.type === 'error' ? 'bg-red-500 text-white' : 
          toast.type === 'success' ? 'bg-green-400 text-black' : 
          'bg-black text-white'
        ]"
      >
        <span>{{ toast.message }}</span>
        <button 
          @click="toastStore.removeToast(toast.id)"
          class="font-black text-base hover:opacity-75 leading-none"
        >
          ✕
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100px);
}
</style>