<template>
  <section class="login-section">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-xl-10 col-lg-11 col-md-12">
          <!-- Card principale -->
          <div class="login-card">
            <div class="row g-0 align-items-center">
              <!-- Formulaire à gauche -->
              <div class="col-lg-6">
                <div class="login-form-container">
                  <!-- Bouton retour mobile -->
                  <div class="mobile-back-btn d-lg-none mb-4">
                    <NuxtLink to="/" class="back-home-link">
                      <i class="bi bi-arrow-left"></i>
                      <span>Retour à l'accueil</span>
                    </NuxtLink>
                  </div>
                  
                  <!-- Header -->
                  <div class="login-header">
                    <div class="welcome-container">
                      <h2 class="login-title">Bienvenue sur GVB Sign</h2>
                      <div class="welcome-decoration"></div>
                    </div>
                    <p class="login-subtitle">Connectez-vous ou créez un compte en un clic pour accéder à vos documents sécurisés.</p>
                  </div>

                  <!-- Bouton de connexion Google -->
                  <div class="google-login-container">
                    <button 
                      @click="handleGoogleLogin" 
                      class="btn-google-login" 
                      :disabled="isLoading"
                    >
                      <span v-if="!isLoading" class="d-flex align-items-center justify-content-center">
                        <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google Logo" class="google-icon" />
                        Continuer avec Google
                      </span>
                      <span v-else class="d-flex align-items-center justify-content-center">
                        <i class="bi bi-arrow-clockwise me-2 spin"></i>
                        Connexion en cours...
                      </span>
                    </button>
                    <div class="validation-message mt-3 text-center" v-if="errorMessage">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-circle me-1"></i>
                        {{ errorMessage }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Image à droite -->
              <div class="col-lg-6 d-none d-lg-block">
                <div class="login-image-container">
                  <!-- Bandeau retour à l'accueil -->
                  <div class="back-home-banner">
                    <NuxtLink to="/" class="back-home-link">
                      <i class="bi bi-arrow-left"></i>
                      <span>Accueil</span>
                    </NuxtLink>
                  </div>
                  
                  <!-- Bulles décoratives -->
                  <div class="bubble bubble-1"></div>
                  <div class="bubble bubble-2"></div>
                  <div class="bubble bubble-3"></div>
                  
                  <img src="/sign_in.svg" alt="Connexion sécurisée" class="img-fluid login-svg">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = process.client ? useAuthStore() : null
const isLoading = ref(false)
const errorMessage = ref('')

const handleGoogleLogin = async () => {
  if (!authStore) return
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const result = await authStore.loginWithGoogle()
    
    if (result.success) {
      // Rediriger vers le dashboard après connexion réussie
      await navigateTo('/dashboard')
    } else {
      errorMessage.value = result.message || 'Une erreur est survenue lors de la connexion avec Google.'
    }
  } catch (error) {
    console.error('Erreur inattendue:', error)
    errorMessage.value = 'Erreur de connexion au service d\'authentification.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-section { width: 100%; display: flex; align-items: center; justify-content: center; }
.login-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-radius: 24px; box-shadow: 0 20px 60px rgba(0, 102, 204, 0.1), 0 8px 30px rgba(0, 0, 0, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); overflow: hidden; opacity: 0; animation: slideInUp 0.8s ease-out 0.2s forwards; max-width: 900px; margin: 0 auto; position: relative; }
.login-form-container { padding: 3rem; opacity: 0; animation: fadeInLeft 0.8s ease-out 0.4s forwards; display: flex; flex-direction: column; justify-content: center; min-height: 400px; }
.login-header { margin-bottom: 3rem; text-align: center; }
.login-title { font-family: 'Raleway', sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--primary-blue); margin-bottom: 0.5rem; opacity: 0; animation: slideInLeft 0.6s ease-out 0.6s forwards; }
.welcome-decoration { width: 60px; height: 4px; background: linear-gradient(90deg, var(--primary-blue) 0%, rgba(0, 102, 204, 0.6) 100%); border-radius: 2px; opacity: 0; animation: fadeInScale 0.8s ease-out 0.8s forwards; margin: 0 auto; }
.login-subtitle { color: var(--dark-gray); font-size: 1.1rem; line-height: 1.5; margin-bottom: 0; opacity: 0; animation: slideInLeft 0.6s ease-out 0.7s forwards; margin: 1rem auto 0; }

.google-login-container { text-align: center; opacity: 0; animation: fadeInUp 0.8s ease-out 0.8s forwards; margin-top: 1rem;}
.btn-google-login { width: 100%; background: white; border: 1px solid #dadce0; color: #3c4043; font-weight: 500; padding: 0.8rem 1.5rem; border-radius: 12px; font-size: 1.1rem; font-family: 'Roboto', 'Raleway', sans-serif; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center;}
.btn-google-login:hover:not(:disabled) { background: #f8f9fa; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.08); border-color: #d2e3fc; }
.btn-google-login:disabled { opacity: 0.7; cursor: not-allowed; }
.google-icon { width: 24px; height: 24px; margin-right: 12px; }
.spin { animation: spin 1s linear infinite; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.login-image-container { padding: 2.5rem; text-align: center; position: relative; opacity: 0; animation: fadeInRight 0.8s ease-out 0.6s forwards; background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 102, 204, 0.02) 100%); height: 100%; display: flex; align-items: center; justify-content: center; }
.login-svg { max-width: 90%; height: auto; filter: drop-shadow(0 10px 30px rgba(0, 102, 204, 0.15)); position: relative; z-index: 2; opacity: 0; animation: slideInRight 0.8s ease-out 0.8s forwards; }

.back-home-banner { position: absolute; top: 0; right: 0; width: 200px; height: 50px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-bottom-left-radius: 20px; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: -5px 5px 20px rgba(0,0,0,0.05); opacity: 0; animation: fadeIn 0.8s ease-out 0.8s forwards; }
.back-home-link { display: inline-flex; align-items: center; gap: 0.5rem; color: var(--text-dark); text-decoration: none; font-weight: 500; transition: all 0.3s ease; }
.back-home-link:hover { color: var(--primary-blue); transform: translateX(-3px); }
.mobile-back-btn { opacity: 0; animation: fadeIn 0.8s ease-out 0.2s forwards; }

.bubble { position: absolute; border-radius: 50%; background: rgba(0, 102, 204, 0.08); z-index: 1; opacity: 0; animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite; }
.bubble-1 { width: 120px; height: 120px; top: 10%; right: 15%; animation: fadeInScale 1s ease-out 1.0s forwards, float 6s ease-in-out infinite 1.0s; }
.bubble-2 { width: 80px; height: 80px; top: 60%; right: 10%; animation: fadeInScale 1s ease-out 1.1s forwards, float 5s ease-in-out infinite 1.1s; }
.bubble-3 { width: 100px; height: 100px; bottom: 15%; left: 12%; animation: fadeInScale 1s ease-out 1.2s forwards, float 7s ease-in-out infinite 1.2s; }

@keyframes slideInUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInLeft { from { opacity: 0; transform: translateX(-40px); } to { opacity: 1; transform: translateX(0); } }
@keyframes fadeInRight { from { opacity: 0; transform: translateX(40px); } to { opacity: 1; transform: translateX(0); } }
@keyframes slideInLeft { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
@keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
@keyframes fadeInScale { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
