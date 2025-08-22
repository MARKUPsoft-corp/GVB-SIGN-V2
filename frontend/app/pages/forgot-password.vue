<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <div class="forgot-password-header">
        <div class="icon">
          <i class="bi bi-key"></i>
        </div>
        <h1>Mot de passe oublié</h1>
        <p>Cette fonctionnalité sera bientôt disponible</p>
      </div>
      
      <div class="forgot-password-actions">
        <NuxtLink to="/login" class="btn btn-primary-custom">
          <i class="bi bi-arrow-left me-2"></i>
          Retour à la connexion
        </NuxtLink>
        <NuxtLink to="/" class="btn btn-outline-primary-custom">
          <i class="bi bi-house me-2"></i>
          Accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'auth'
})
</script>

<style scoped>
.forgot-password-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--white) 100%);
  padding: 2rem;
}

.forgot-password-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 60px var(--shadow-light);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 3rem;
  text-align: center;
  max-width: 400px;
  width: 100%;
  animation: fadeInUp 0.8s ease-out;
}

.forgot-password-header {
  margin-bottom: 2rem;
}

.icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: 50%;
  color: white;
  font-size: 2.5rem;
}

.forgot-password-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.forgot-password-header p {
  font-size: 1rem;
  color: var(--dark-gray);
  margin: 0;
}

.forgot-password-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .forgot-password-container {
    padding: 1rem;
  }
  
  .forgot-password-card {
    padding: 2rem;
  }
  
  .forgot-password-actions {
    flex-direction: column;
  }
}
</style>
