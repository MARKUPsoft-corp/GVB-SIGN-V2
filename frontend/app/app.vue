<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
// Import de Bootstrap côté client
if (import.meta.client) {
  import('bootstrap/dist/js/bootstrap.bundle.min.js')
}
</script>
