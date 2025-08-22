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
                  <!-- Header -->
                  <div class="login-header">
                    <div class="welcome-container">
                      <h2 class="login-title">Bon retour !</h2>
                      <div class="welcome-decoration"></div>
                    </div>
                    <p class="login-subtitle">Connectez-vous à votre compte pour accéder à vos documents sécurisés.</p>
                  </div>

                                                        <!-- Formulaire -->
                  <form class="login-form" @submit.prevent="handleLogin" v-if="!showLoginError">
                      <!-- Champ Email -->
                      <div class="floating-input-group">
                        <input 
                          type="email" 
                          id="email"
                          v-model="form.email"
                          class="floating-input"
                          :class="{ 'is-valid': emailValid, 'is-invalid': emailInvalid }"
                          placeholder="exemple@email.com"
                          required
                          @input="validateEmail(); validationErrors.email = ''; showLoginError = false"
                          @blur="validateEmail"
                        >
                        <label for="email" class="floating-label">Email</label>
                        <span class="input-icon">
                          <i class="bi bi-envelope"></i>
                        </span>
                        <span class="validation-icon" v-if="form.email && form.email !== 'exemple@email.com'">
                          <i :class="emailValid ? 'bi bi-check-circle-fill text-success' : 'bi bi-exclamation-circle-fill text-danger'"></i>
                        </span>
                      </div>
                      <div class="validation-message" v-if="(emailInvalid && form.email && form.email !== 'exemple@email.com') || validationErrors.email">
                        <small class="text-danger">
                          <i class="bi bi-exclamation-circle me-1"></i>
                          {{ validationErrors.email || emailErrorMessage }}
                        </small>
                      </div>

                      <!-- Champ Mot de passe -->
                      <div class="floating-input-group">
                        <input 
                          :type="showPassword ? 'text' : 'password'" 
                          id="password"
                          v-model="form.password"
                          class="floating-input"
                          :class="{ 'is-invalid': validationErrors.password }"
                          placeholder=" "
                          required
                          @input="validationErrors.password = ''; showLoginError = false"
                        >
                        <label for="password" class="floating-label">Mot de passe</label>
                        <span class="input-icon">
                          <i class="bi bi-lock"></i>
                        </span>
                        <button 
                          type="button" 
                          class="password-toggle"
                          @click="showPassword = !showPassword"
                        >
                          <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                        </button>
                      </div>
                      <div class="validation-message" v-if="validationErrors.password">
                        <small class="text-danger">
                          <i class="bi bi-exclamation-circle me-1"></i>
                          {{ validationErrors.password }}
                        </small>
                      </div>

                      <!-- Options du formulaire -->
                      <div class="form-options">
                        <div class="form-check">
                          <input 
                            type="checkbox" 
                            id="remember" 
                            v-model="form.remember"
                            class="form-check-input"
                          >
                          <label for="remember" class="form-check-label">
                            Se souvenir de moi
                          </label>
                        </div>
                        <NuxtLink to="/forgot-password" class="forgot-link">
                          Mot de passe oublié ?
                        </NuxtLink>
                      </div>

                      <!-- Bouton de connexion -->
                      <button type="submit" class="btn-login" :disabled="isLoading">
                        <span v-if="!isLoading">
                          <i class="bi bi-box-arrow-in-right me-2"></i>
                          Se connecter
                        </span>
                        <span v-else>
                          <i class="bi bi-arrow-clockwise me-2 spin"></i>
                          Connexion...
                        </span>
                      </button>
                    </form>

                  <!-- Footer du formulaire -->
                  <div class="login-footer" v-if="!showLoginError">
                    <p class="signup-text">
                      Pas encore de compte ? 
                      <NuxtLink to="/register" class="signup-link">
                        Créer un compte
                      </NuxtLink>
                    </p>
                  </div>

                  <!-- Interface d'erreur de connexion -->
                  <div v-if="showLoginError" class="login-error">
                    <div class="error-card">
                      <div class="error-header">
                        <div class="error-icon">
                          <i class="bi bi-exclamation-triangle-fill"></i>
                        </div>
                        <h3 class="error-title">
                          {{ loginErrorType === 'email_not_found' ? 'Email non trouvé' : 'Mot de passe incorrect' }}
                        </h3>
                      </div>
                      <div class="error-content">
                        <p class="error-message" v-if="loginErrorType === 'email_not_found'">
                          Aucun compte n'est associé à l'adresse <strong>{{ form.email }}</strong>.
                        </p>
                        <p class="error-message" v-if="loginErrorType === 'wrong_password'">
                          Le mot de passe saisi ne correspond pas à l'adresse <strong>{{ form.email }}</strong>.
                        </p>
                        <p class="error-question">
                          {{ loginErrorType === 'email_not_found' ? 'Souhaitez-vous créer un nouveau compte ?' : 'Voulez-vous réessayer avec un autre mot de passe ?' }}
                        </p>
                      </div>
                      <div class="error-actions">
                        <button v-if="loginErrorType === 'email_not_found'" @click="goToRegister" class="btn btn-primary-custom btn-error">
                          Oui
                        </button>
                        <button v-if="loginErrorType === 'wrong_password'" @click="showFormAgain" class="btn btn-primary-custom btn-error">
                          Oui
                        </button>
                        <button @click="showFormAgain" class="btn btn-outline-primary-custom btn-error">
                          Non
                        </button>
                      </div>
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
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

// Store d'authentification (côté client seulement)
const authStore = process.client ? useAuthStore() : null

// État du formulaire
const form = ref({
  email: '',
  password: '',
  remember: false
})

const showPassword = ref(false)
const isLoading = ref(false)
const emailValid = ref(false)
const emailInvalid = ref(false)
const emailErrorMessage = ref('')

// Validation de l'email
const validateEmail = () => {
  const email = form.value.email.trim()
  
  if (!email || email === 'exemple@email.com') {
    emailValid.value = false
    emailInvalid.value = false
    emailErrorMessage.value = ''
    return
  }
  
  // Regex pour validation email
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  
  if (!emailRegex.test(email)) {
    emailValid.value = false
    emailInvalid.value = true
    emailErrorMessage.value = 'Format d\'email invalide'
    return
  }
  
  // Vérifications supplémentaires
  if (email.length < 5) {
    emailValid.value = false
    emailInvalid.value = true
    emailErrorMessage.value = 'Email trop court'
    return
  }
  
  if (email.length > 100) {
    emailValid.value = false
    emailInvalid.value = true
    emailErrorMessage.value = 'Email trop long'
    return
  }
  
  // Email valide
  emailValid.value = true
  emailInvalid.value = false
  emailErrorMessage.value = ''
}

// Erreurs de validation du serveur
const validationErrors = ref({
  email: '',
  password: ''
})

// État pour afficher l'interface d'erreur spéciale
const showLoginError = ref(false)
const loginErrorType = ref('') // 'email_not_found' ou 'wrong_password'

// Initialiser la validation au montage du composant
onMounted(() => {
  validateEmail()
})

// Gestion de la soumission
const handleLogin = async () => {
  // Validation avant soumission
  validateEmail()
  
  if (!form.value.email.trim() || !form.value.password.trim()) {
    return
  }
  
  isLoading.value = true

  try {
    // Utiliser le store pour la connexion (côté client seulement)
    if (!authStore) {
      throw new Error('Store non disponible')
    }
    
    const result = await authStore.login({
      email: form.value.email,
      password: form.value.password
    })

    if (result.success) {
      // Connexion réussie - redirection vers dashboard
      await navigateTo('/dashboard')
    } else {
      console.error('Erreur de connexion:', result)
      if (result.errors) {
        const errors = result.errors
        if (errors.non_field_errors) {
          const errorMessage = Array.isArray(errors.non_field_errors) ? errors.non_field_errors[0] : errors.non_field_errors
          
          // Détecter le type d'erreur pour afficher l'interface appropriée
          if (errorMessage.includes('Identifiants invalides')) {
            // Vérifier si l'email existe dans la base de données
            try {
              const API_BASE_URL = 'http://127.0.0.1:8000/api'
              const checkResponse = await fetch(`${API_BASE_URL}/auth/check-email/?email=${encodeURIComponent(form.value.email)}`)
              const checkResult = await checkResponse.json()
              
              if (checkResult.exists) {
                // Email existe mais mot de passe incorrect
                loginErrorType.value = 'wrong_password'
                showLoginError.value = true
                return
              } else {
                // Email n'existe pas
                loginErrorType.value = 'email_not_found'
                showLoginError.value = true
                return
              }
            } catch (checkError) {
              // En cas d'erreur de vérification, afficher l'erreur générale
              validationErrors.value.email = errorMessage
            }
          } else {
            validationErrors.value.email = errorMessage
          }
        }
        if (errors.email) {
          validationErrors.value.email = Array.isArray(errors.email) ? errors.email[0] : errors.email
        }
        if (errors.password) {
          validationErrors.value.password = Array.isArray(errors.password) ? errors.password[0] : errors.password
        }
      }
      if (result.message) {
        console.error('Message d\'erreur:', result.message)
      }
    }
  } catch (error) {
    console.error('Erreur de connexion:', error)
    validationErrors.value.email = 'Erreur de connexion au serveur'
  } finally {
    isLoading.value = false
  }
}

// Fonctions pour gérer les actions de l'interface d'erreur
const goToRegister = () => {
  navigateTo('/register')
}

const showFormAgain = () => {
  showLoginError.value = false
  loginErrorType.value = ''
  // Garder l'email pré-rempli, vider seulement le mot de passe
  form.value.password = ''
  validationErrors.value.email = ''
  validationErrors.value.password = ''
  // Re-valider l'email pour restaurer les icônes de validation
  validateEmail()
}
</script>

<style scoped>
.login-section {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 
    0 20px 60px rgba(0, 102, 204, 0.1),
    0 8px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  opacity: 0;
  animation: slideInUp 0.8s ease-out 0.2s forwards;
  max-width: 900px;
  margin: 0 auto;
  max-height: 90vh;
  position: relative;
}

.login-form-container {
  padding: 2.5rem;
  opacity: 0;
  animation: fadeInLeft 0.8s ease-out 0.4s forwards;
}

.login-header {
  margin-bottom: 2rem;
}

.back-home-banner {
  position: absolute;
  top: -60px;
  right: 0;
  width: 50%;
  height: 50px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 102, 204, 0.1);
  border-radius: 0 0 0 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  opacity: 0;
  animation: slideInBanner 0.8s ease-out 0.3s forwards;
  overflow: hidden;
}

.back-home-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(0, 102, 204, 0.05) 50%, transparent 100%);
  transform: translateX(-100%);
  animation: shimmer 2s ease-in-out infinite;
}

.back-home-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-dark);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 2;
  position: relative;
}

.back-home-link:hover {
  color: var(--primary-blue);
  transform: translateX(-3px);
}

.back-home-link i {
  font-size: 1rem;
  transition: transform 0.3s ease;
}

.back-home-link:hover i {
  transform: translateX(-2px);
}

.login-header {
  margin-bottom: 2rem;
  text-align: center;
}

.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.login-title {
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-blue);
  margin-bottom: 0.5rem;
  opacity: 0;
  animation: slideInLeft 0.6s ease-out 0.6s forwards;
  text-align: center;
  letter-spacing: -0.02em;
  position: relative;
}

.welcome-decoration {
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-blue) 0%, rgba(0, 102, 204, 0.6) 100%);
  border-radius: 2px;
  opacity: 0;
  animation: fadeInScale 0.8s ease-out 0.8s forwards;
  margin: 0 auto;
}

.login-subtitle {
  color: var(--dark-gray);
  font-size: 1.1rem;
  line-height: 1.5;
  margin-bottom: 0;
  opacity: 0;
  animation: slideInLeft 0.6s ease-out 0.7s forwards;
  text-align: center;
  max-width: 400px;
  margin: 0 auto;
}

.login-form {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.8s forwards;
}

/* Floating Input Groups */
.floating-input-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.floating-input {
  width: 100%;
  padding: 1rem 3rem 1rem 3rem;
  border: 2px solid rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  background: rgba(248, 249, 250, 0.8);
  font-size: 1rem;
  font-family: 'Raleway', sans-serif;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  outline: none;
  position: relative;
}

.floating-input:focus {
  border-color: var(--primary-blue);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.floating-label {
  position: absolute;
  left: 3rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--dark-gray);
  font-size: 1.2rem;
  font-weight: 400;
  pointer-events: none;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: transparent;
  z-index: 5;
}

.floating-input:focus + .floating-label,
.floating-input:not(:placeholder-shown) + .floating-label {
  top: 0;
  left: 1rem;
  transform: translateY(-50%);
  font-size: 1rem;
  font-weight: 500;
  color: var(--primary-blue);
  background: white;
  padding: 0 0.5rem;
  border-radius: 4px;
  z-index: 10;
}

.floating-input-group .input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--dark-gray);
  font-size: 1.1rem;
  z-index: 3;
  transition: color 0.3s ease;
}

.floating-input:focus ~ .input-icon {
  color: var(--primary-blue);
}

.floating-input-group .password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--dark-gray);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  z-index: 3;
}

.floating-input-group .password-toggle:hover {
  color: var(--primary-blue);
  background: rgba(0, 102, 204, 0.1);
}

/* Validation styles */
.floating-input.is-valid {
  border-color: #28a745;
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
}

.floating-input.is-invalid {
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.validation-icon {
  position: absolute;
  right: 3rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.1rem;
  z-index: 3;
}

.validation-message {
  margin-top: -1rem;
  margin-bottom: 1rem;
  animation: fadeInUp 0.3s ease-out;
}

.text-success {
  color: #28a745 !important;
}

.text-danger {
  color: #dc3545 !important;
}

/* Anciens styles supprimés - remplacés par floating inputs */

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.form-check {
  display: flex;
  align-items: center;
}

.form-check-input {
  margin-right: 0.5rem;
  cursor: pointer;
  border-radius: 4px 4px 4px 4px;
}

.form-check-label {
  font-size: 0.95rem;
  color: var(--dark-gray);
  cursor: pointer;
}

.forgot-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.forgot-link:hover {
  color: var(--primary-blue-dark);
  text-decoration: underline;
}

.btn-login {
  width: 100%;
  background: var(--gradient-primary);
  border: none;
  color: white;
  font-weight: 600;
  padding: 1rem 2rem;
  border-radius: 12px 12px 12px 12px;
  font-size: 1.1rem;
  font-family: 'Raleway', sans-serif;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
  position: relative;
  overflow: hidden;
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0, 102, 204, 0.3);
  background: var(--primary-blue-dark);
}

.btn-login:hover:not(:disabled)::before {
  left: 100%;
}

.btn-login:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 1.5rem;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 0.6s ease-out 1.0s forwards;
}

.signup-text {
  color: var(--dark-gray);
  margin: 0;
}

.signup-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.signup-link:hover {
  color: var(--primary-blue-dark);
  text-decoration: underline;
}

/* Image et animations */
.login-image-container {
  padding: 2.5rem;
  text-align: center;
  position: relative;
  opacity: 0;
  animation: fadeInRight 0.8s ease-out 0.6s forwards;
}

.login-svg {
  max-width: 95%;
  height: auto;
  filter: drop-shadow(0 10px 30px rgba(0, 102, 204, 0.1));
  position: relative;
  z-index: 2;
  opacity: 0;
  animation: slideInRight 0.8s ease-out 0.8s forwards;
}

/* Bulles décoratives */
.bubble {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 102, 204, 0.12);
  z-index: 1;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards, float 6s ease-in-out infinite;
}

.bubble-1 {
  width: 120px;
  height: 120px;
  top: 10%;
  right: 15%;
  animation: fadeInScale 1s ease-out 1.0s forwards, float 6s ease-in-out infinite 1.0s;
}

.bubble-2 {
  width: 100px;
  height: 100px;
  top: 55%;
  right: 8%;
  animation: fadeInScale 1s ease-out 1.1s forwards, float 6s ease-in-out infinite 1.1s;
}

.bubble-3 {
  width: 110px;
  height: 110px;
  bottom: 15%;
  left: 12%;
  animation: fadeInScale 1s ease-out 1.2s forwards, float 6s ease-in-out infinite 1.2s;
}

/* Animations */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.3);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes slideInBanner {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
}



/* Responsive */
@media (max-width: 991px) {
  .login-form-container {
    padding: 2rem;
  }
  
  .login-title {
    font-size: 1.8rem;
  }
}

@media (max-width: 768px) {
  .login-card {
    margin: 0 1rem;
    border-radius: 20px;
  }
  
  .login-form-container {
    padding: 2rem 1.5rem;
  }
  
  .login-title {
    font-size: 2.2rem;
  }
  
  .welcome-decoration {
    width: 50px;
    height: 3px;
  }
  
  .floating-input {
    padding: 0.9rem 2.5rem 0.9rem 2.5rem;
    font-size: 0.95rem;
  }
  
  .floating-label {
    left: 2.5rem;
    font-size: 1rem;
  }
  
  .floating-input:focus + .floating-label,
  .floating-input:not(:placeholder-shown) + .floating-label {
    font-size: 0.9rem;
  }
  
  .floating-input-group .input-icon {
    left: 0.8rem;
    font-size: 1rem;
  }
  
  .floating-input-group .password-toggle {
    right: 0.8rem;
    padding: 0.4rem;
  }
  
  .validation-icon {
    right: 2.5rem;
    font-size: 1rem;
  }
  
  .back-home-banner {
    width: 60%;
    height: 45px;
    border-radius: 0 0 0 12px;
  }
  
  .back-home-link {
    font-size: 0.85rem;
  }
  
  .back-home-link span {
    display: none;
  }
}

/* Interface d'erreur de connexion */
.login-error {
  animation: fadeInUp 0.6s ease-out;
}

.error-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 0 10px 30px var(--shadow-light);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1.5rem;
  text-align: center;
}

.error-header {
  margin-bottom: 1rem;
}

.error-icon {
  width: 50px;
  height: 50px;
  margin: 0 auto 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: 50%;
  color: white;
  font-size: 1.5rem;
  animation: pulse 2s ease-in-out infinite;
}

.error-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
}

.error-content {
  margin-bottom: 1rem;
}

.error-message {
  font-size: 0.9rem;
  color: var(--dark-gray);
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.error-message strong {
  color: var(--text-dark);
  background: rgba(0, 102, 204, 0.1);
  padding: 0.15rem 0.4rem;
  border-radius: 3px;
}

.error-question {
  font-size: 1rem;
  color: var(--text-dark);
  margin: 0;
  font-weight: 600;
}

.error-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-error {
  padding: 0.5rem 1rem !important;
  font-size: 0.85rem !important;
  border-radius: 8px !important;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(0, 102, 204, 0);
  }
}

@media (max-width: 768px) {
  .error-card {
    padding: 1.25rem;
    margin: 1rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .error-title {
    font-size: 1.1rem;
  }
  
  .error-message {
    font-size: 0.85rem;
  }
  
  .error-question {
    font-size: 0.95rem;
  }
}

@media (max-width: 576px) {
  .login-form-container {
    padding: 1.5rem;
  }
  
  .login-title {
    font-size: 2rem;
  }
  
  .welcome-decoration {
    width: 40px;
    height: 3px;
  }
  
  .login-subtitle {
    font-size: 1rem;
    max-width: 300px;
  }
  
  .floating-input {
    padding: 0.8rem 2.3rem 0.8rem 2.3rem;
    font-size: 0.9rem;
  }
  
  .floating-label {
    left: 2.3rem;
    font-size: 1rem;
  }
  
  .floating-input:focus + .floating-label,
  .floating-input:not(:placeholder-shown) + .floating-label {
    font-size: 0.85rem;
  }
  
  .floating-input-group .input-icon {
    left: 0.7rem;
    font-size: 0.95rem;
  }
  
  .floating-input-group .password-toggle {
    right: 0.7rem;
    padding: 0.3rem;
  }
  
  .validation-icon {
    right: 2.3rem;
    font-size: 0.95rem;
  }
  
  .btn-login {
    padding: 0.9rem 1.5rem;
  }
  
  .login-card {
    margin: 0 0.5rem;
    border-radius: 16px;
  }
  
  .back-home-banner {
    width: 70%;
    height: 40px;
    border-radius: 0 0 0 12px;
  }
}
</style>
