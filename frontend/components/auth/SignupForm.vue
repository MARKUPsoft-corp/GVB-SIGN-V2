<template>
  <section class="signup-section">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-xl-10 col-lg-11 col-md-12">
          <div class="signup-card">
            <div class="row g-0 align-items-center">
              <!-- Image à gauche -->
              <div class="col-lg-6 d-none d-lg-block">
                <div class="signup-image-container">
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
                  
                  <img src="/sign_up.svg" alt="Inscription sécurisée" class="img-fluid signup-svg">
                </div>
              </div>

              <!-- Formulaire à droite -->
              <div class="col-lg-6">
                <div class="signup-form-container">
                  <!-- Header -->
                  <div class="signup-header">
                    <div class="welcome-container">
                      <h2 class="signup-title">Bienvenue !</h2>
                      <div class="welcome-decoration"></div>
                    </div>
                    <p class="signup-subtitle">Créez votre compte pour commencer à sécuriser vos documents.</p>
                  </div>

                  <!-- Formulaire -->
                  <form class="signup-form" @submit.prevent="handleSignup" v-if="!showEmailExistsError">
                    <!-- Champ Prénom -->
                    <div class="floating-input-group">
                      <input 
                        type="text" 
                        id="firstName"
                        v-model="form.firstName"
                        class="floating-input"
                        placeholder="John"
                        required
                        @input="validateFirstName"
                        @blur="validateFirstName"
                      >
                      <label for="firstName" class="floating-label">Prénom</label>
                      <span class="input-icon">
                        <i class="bi bi-person"></i>
                      </span>
                    </div>

                    <!-- Champ Nom -->
                    <div class="floating-input-group">
                      <input 
                        type="text" 
                        id="lastName"
                        v-model="form.lastName"
                        class="floating-input"
                        placeholder="Doe"
                        required
                        @input="validateLastName"
                        @blur="validateLastName"
                      >
                      <label for="lastName" class="floating-label">Nom</label>
                      <span class="input-icon">
                        <i class="bi bi-person-badge"></i>
                      </span>
                    </div>

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
                        @input="validateEmail"
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
                    <div class="validation-message" v-if="emailInvalid && form.email && form.email !== 'exemple@email.com'">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-circle me-1"></i>
                        {{ emailErrorMessage }}
                      </small>
                    </div>
                    <!-- Erreur serveur pour l'email -->
                    <div class="validation-message" v-if="validationErrors.email">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-triangle me-1"></i>
                        {{ validationErrors.email }}
                      </small>
                      <!-- Bouton de connexion si l'email existe déjà -->
                      <div v-if="validationErrors.email.includes('déjà utilisé')" class="mt-2">
                        <NuxtLink to="/login" class="btn btn-sm btn-outline-primary">
                          <i class="bi bi-box-arrow-in-right me-1"></i>
                          Se connecter
                        </NuxtLink>
                      </div>
                    </div>

                    <!-- Champ Mot de passe -->
                    <div class="floating-input-group">
                      <input 
                        :type="showPassword ? 'text' : 'password'" 
                        id="password"
                        v-model="form.password"
                        class="floating-input"
                        :class="{ 'is-valid': passwordValid, 'is-invalid': passwordInvalid }"
                        placeholder="••••••••"
                        required
                        @input="validatePassword"
                        @blur="validatePassword"
                      >
                      <label for="password" class="floating-label">Mot de passe</label>
                      <span class="input-icon">
                        <i class="bi bi-lock"></i>
                      </span>
                      <span class="validation-icon" v-if="form.password">
                        <i :class="passwordValid ? 'bi bi-check-circle-fill text-success' : 'bi bi-exclamation-circle-fill text-danger'"></i>
                      </span>
                      <button 
                        type="button" 
                        class="password-toggle"
                        @click="showPassword = !showPassword"
                      >
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                    <div class="validation-message" v-if="passwordInvalid && form.password">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-circle me-1"></i>
                        {{ passwordErrorMessage }}
                      </small>
                    </div>
                    <!-- Erreur serveur pour le mot de passe -->
                    <div class="validation-message" v-if="validationErrors.password">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-triangle me-1"></i>
                        {{ validationErrors.password }}
                      </small>
                    </div>

                    <!-- Champ Confirmation mot de passe -->
                    <div class="floating-input-group">
                      <input 
                        :type="showConfirmPassword ? 'text' : 'password'" 
                        id="confirmPassword"
                        v-model="form.confirmPassword"
                        class="floating-input"
                        :class="{ 'is-valid': confirmPasswordValid, 'is-invalid': confirmPasswordInvalid }"
                        placeholder="••••••••"
                        required
                        @input="validateConfirmPassword"
                        @blur="validateConfirmPassword"
                      >
                      <label for="confirmPassword" class="floating-label">Confirmer le mot de passe</label>
                      <span class="input-icon">
                        <i class="bi bi-shield-lock"></i>
                      </span>
                      <span class="validation-icon" v-if="form.confirmPassword">
                        <i :class="confirmPasswordValid ? 'bi bi-check-circle-fill text-success' : 'bi bi-exclamation-circle-fill text-danger'"></i>
                      </span>
                      <button 
                        type="button" 
                        class="password-toggle"
                        @click="showConfirmPassword = !showConfirmPassword"
                      >
                        <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                    <div class="validation-message" v-if="confirmPasswordInvalid && form.confirmPassword">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-circle me-1"></i>
                        {{ confirmPasswordErrorMessage }}
                      </small>
                    </div>
                    <!-- Erreur serveur pour la confirmation du mot de passe -->
                    <div class="validation-message" v-if="validationErrors.confirmPassword">
                      <small class="text-danger">
                        <i class="bi bi-exclamation-triangle me-1"></i>
                        {{ validationErrors.confirmPassword }}
                      </small>
                    </div>

                    <!-- Conditions d'utilisation -->
                    <div class="form-options">
                      <div class="form-check">
                        <input 
                          type="checkbox" 
                          id="acceptTerms" 
                          v-model="form.acceptTerms"
                          class="form-check-input"
                          required
                        >
                        <label for="acceptTerms" class="form-check-label">
                          J'accepte les <a href="#" class="terms-link">conditions d'utilisation</a>
                        </label>
                      </div>
                    </div>

                    <!-- Bouton d'inscription -->
                    <button type="submit" class="btn-signup" :disabled="isLoading">
                      <span v-if="!isLoading">
                        <i class="bi bi-person-plus me-2"></i>
                        Créer mon compte
                      </span>
                      <span v-else>
                        <i class="bi bi-arrow-clockwise me-2 spin"></i>
                        Création...
                      </span>
                    </button>
                  </form>

                  <!-- Footer du formulaire -->
                  <div class="signup-footer" v-if="!showEmailExistsError">
                    <p class="login-text">
                      Déjà un compte ? 
                      <NuxtLink to="/login" class="login-link">
                        Se connecter
                      </NuxtLink>
                    </p>
                  </div>

                  <!-- Message d'erreur pour email existant -->
                  <div v-if="showEmailExistsError" class="email-exists-error">
                    <div class="error-card">
                      <div class="error-header">
                        <div class="error-icon">
                          <i class="bi bi-exclamation-triangle-fill"></i>
                        </div>
                        <h3 class="error-title">Email déjà utilisé</h3>
                      </div>
                      <div class="error-content">
                        <p class="error-message">
                          Un compte avec l'adresse <strong>{{ form.email }}</strong> existe déjà.
                        </p>
                        <p class="error-question">
                          Souhaitez-vous vous connecter à votre compte existant ?
                        </p>
                      </div>
                      <div class="error-actions">
                        <button @click="goToLogin" class="btn btn-primary-custom">Oui</button>
                        <button @click="showFormAgain" class="btn btn-outline-primary-custom">Non</button>
                      </div>
                    </div>
                  </div>
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
import { ref, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'

// Store d'authentification (côté client seulement)
const authStore = process.client ? useAuthStore() : null

// État du formulaire
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)

// États de validation
const emailValid = ref(false)
const emailInvalid = ref(false)
const emailErrorMessage = ref('')

const passwordValid = ref(false)
const passwordInvalid = ref(false)
const passwordErrorMessage = ref('')

const confirmPasswordValid = ref(false)
const confirmPasswordInvalid = ref(false)
const confirmPasswordErrorMessage = ref('')

// Erreurs de validation
const validationErrors = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

// État pour afficher l'erreur d'email existant
const showEmailExistsError = ref(false)

// Validation des noms
const validateFirstName = () => {
  const firstName = form.value.firstName.trim()
  
  if (!firstName) {
    return
  }
  
  if (firstName.length < 2) {
    return
  }
  
  if (firstName.length > 50) {
    return
  }
}

const validateLastName = () => {
  const lastName = form.value.lastName.trim()
  
  if (!lastName) {
    return
  }
  
  if (lastName.length < 2) {
    return
  }
  
  if (lastName.length > 50) {
    return
  }
}

// Validation de l'email
const validateEmail = () => {
  const email = form.value.email.trim()
  
  // Effacer les erreurs serveur quand l'utilisateur modifie l'email
  if (validationErrors.value.email) {
    validationErrors.value.email = ''
  }
  
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

// Validation du mot de passe
const validatePassword = () => {
  const password = form.value.password
  
  // Effacer les erreurs serveur quand l'utilisateur modifie le mot de passe
  if (validationErrors.value.password) {
    validationErrors.value.password = ''
  }
  
  if (!password) {
    passwordValid.value = false
    passwordInvalid.value = false
    passwordErrorMessage.value = ''
    return
  }
  
  if (password.length < 8) {
    passwordValid.value = false
    passwordInvalid.value = true
    passwordErrorMessage.value = 'Le mot de passe doit contenir au moins 8 caractères'
    return
  }
  
  if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
    passwordValid.value = false
    passwordInvalid.value = true
    passwordErrorMessage.value = 'Le mot de passe doit contenir une majuscule, une minuscule et un chiffre'
    return
  }
  
  passwordValid.value = true
  passwordInvalid.value = false
  passwordErrorMessage.value = ''
  
  // Revalider la confirmation si elle existe
  if (form.value.confirmPassword) {
    validateConfirmPassword()
  }
}

// Validation de la confirmation du mot de passe
const validateConfirmPassword = () => {
  const confirmPassword = form.value.confirmPassword
  
  // Effacer les erreurs serveur quand l'utilisateur modifie la confirmation
  if (validationErrors.value.confirmPassword) {
    validationErrors.value.confirmPassword = ''
  }
  
  if (!confirmPassword) {
    confirmPasswordValid.value = false
    confirmPasswordInvalid.value = false
    confirmPasswordErrorMessage.value = ''
    return
  }
  
  if (confirmPassword !== form.value.password) {
    confirmPasswordValid.value = false
    confirmPasswordInvalid.value = true
    confirmPasswordErrorMessage.value = 'Les mots de passe ne correspondent pas'
    return
  }
  
  confirmPasswordValid.value = true
  confirmPasswordInvalid.value = false
  confirmPasswordErrorMessage.value = ''
}

// Vérification si le formulaire est valide
const isFormValid = computed(() => {
  return Boolean(
    form.value.firstName.trim() &&
    form.value.lastName.trim() &&
    emailValid.value &&
    passwordValid.value &&
    confirmPasswordValid.value &&
    form.value.acceptTerms
  )
})

// Gestion de la soumission
const handleSignup = async () => {
  // Validation avant soumission
  validateEmail()
  validatePassword()
  validateConfirmPassword()
  
  // Vérification manuelle de la validité
  const isValid = form.value.firstName.trim() &&
                 form.value.lastName.trim() &&
                 emailValid.value &&
                 passwordValid.value &&
                 confirmPasswordValid.value &&
                 form.value.acceptTerms
  
  if (!isValid) {
    console.log('Formulaire invalide')
    return
  }
  
  isLoading.value = true
  
  try {
    // Utiliser le store pour l'inscription (côté client seulement)
    if (!authStore) {
      throw new Error('Store non disponible')
    }
    
    const result = await authStore.register({
      email: form.value.email,
      first_name: form.value.firstName,
      last_name: form.value.lastName,
      password: form.value.password,
      confirm_password: form.value.confirmPassword
    })
    
    console.log('Réponse complète:', result)
    
    if (result.success) {
      // Redirection vers le dashboard
      await navigateTo({
        path: '/dashboard',
        query: {
          from: 'registration'
        }
      })
    } else {
      // Affichage des erreurs
      console.error('Erreur d\'inscription:', result)
      
      // Gérer les erreurs spécifiques
      if (result.errors) {
        const errors = result.errors
        if (errors.email) {
          const emailError = Array.isArray(errors.email) ? errors.email[0] : errors.email
          
          // Si l'email existe déjà, afficher l'interface spéciale
          if (emailError.includes('existe déjà') || emailError.includes('already exists')) {
            showEmailExistsError.value = true
            return
          } else {
            validationErrors.value.email = emailError
          }
        }
        if (errors.password) {
          validationErrors.value.password = Array.isArray(errors.password) ? errors.password[0] : errors.password
        }
        if (errors.confirm_password) {
          validationErrors.value.confirmPassword = Array.isArray(errors.confirm_password) ? errors.confirm_password[0] : errors.confirm_password
        }
      }
      
      // Gérer les erreurs générales
      if (result.message) {
        console.error('Message d\'erreur:', result.message)
      }
    }
    
  } catch (error) {
    console.error('Erreur d\'inscription:', error)
  } finally {
    isLoading.value = false
  }
}

// Fonction pour aller à la page de connexion
const goToLogin = () => {
  navigateTo('/login')
}

// Fonction pour afficher à nouveau le formulaire
const showFormAgain = () => {
  showEmailExistsError.value = false
  // Effacer l'email pour permettre une nouvelle saisie
  form.value.email = ''
  validationErrors.value.email = ''
}
</script>

<style scoped>
/* Styles identiques au LoginForm avec adaptations pour signup */
.signup-section {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.signup-card {
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
  max-height: 95vh;
  position: relative;
}

.signup-form-container {
  padding: 1rem 2rem;
  opacity: 0;
  animation: fadeInRight 0.8s ease-out 0.4s forwards;
}

.signup-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.signup-title {
  font-family: 'Raleway', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-blue);
  margin-bottom: 0.3rem;
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

.signup-subtitle {
  color: var(--dark-gray);
  font-size: 0.8rem;
  line-height: 1.3;
  margin-bottom: 0;
  opacity: 0;
  animation: slideInLeft 0.6s ease-out 0.7s forwards;
  text-align: center;
  max-width: 300px;
  margin: 0 auto;
}

.signup-form {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.8s forwards;
}

/* Floating Input Groups */
.floating-input-group {
  position: relative;
  margin-bottom: 1.2rem;
}

.floating-input {
  width: 100%;
  padding: 0.6rem 2.2rem 0.6rem 2.2rem;
  border: 2px solid rgba(0, 102, 204, 0.1);
  border-radius: 12px;
  background: rgba(248, 249, 250, 0.8);
  font-size: 0.85rem;
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
  left: 2.2rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--dark-gray);
  font-size: 0.85rem;
  font-weight: 400;
  pointer-events: none;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: transparent;
  z-index: 5;
}

.floating-input:focus + .floating-label,
.floating-input:not(:placeholder-shown) + .floating-label {
  top: 0;
  left: 0.8rem;
  transform: translateY(-50%);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--primary-blue);
  background: white;
  padding: 0 0.4rem;
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
  margin-top: -0.8rem;
  margin-bottom: 0.8rem;
  animation: fadeInUp 0.3s ease-out;
}

.text-success {
  color: #28a745 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.form-check {
  display: flex;
  align-items: center;
}

.form-check-input {
  margin-right: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.form-check-label {
  font-size: 0.8rem;
  color: var(--dark-gray);
  cursor: pointer;
}

.terms-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 0.8rem;
}

.terms-link:hover {
  color: var(--primary-blue-dark);
  text-decoration: underline;
}

.btn-signup {
  width: 100%;
  background: var(--gradient-primary);
  border: none;
  color: white;
  font-weight: 600;
  padding: 0.7rem 1.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-family: 'Raleway', sans-serif;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
  position: relative;
  overflow: hidden;
}

.btn-signup::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-signup:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0, 102, 204, 0.3);
  background: var(--primary-blue-dark);
}

.btn-signup:hover:not(:disabled)::before {
  left: 100%;
}

.btn-signup:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}

.signup-footer {
  margin-top: 1rem;
  text-align: center;
  opacity: 0;
  animation: fadeInUp 0.6s ease-out 1.0s forwards;
}

.login-text {
  color: var(--dark-gray);
  margin: 0;
  font-size: 0.85rem;
}

.login-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.85rem;
}

.login-link:hover {
  color: var(--primary-blue-dark);
  text-decoration: underline;
}

/* Bandeau retour à l'accueil */
.back-home-banner {
  position: absolute;
  top: -60px;
  left: 0;
  width: 50%;
  height: 50px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 102, 204, 0.1);
  border-radius: 0 0 12px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  opacity: 0;
  animation: slideInBannerLeft 0.8s ease-out 0.3s forwards;
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
  transform: translateX(3px);
}

.back-home-link i {
  font-size: 1rem;
  transition: transform 0.3s ease;
}

.back-home-link:hover i {
  transform: translateX(2px);
}

/* Image et animations */
.signup-image-container {
  padding: 2.5rem 3rem;
  text-align: center;
  position: relative;
  opacity: 0;
  animation: fadeInLeft 0.8s ease-out 0.6s forwards;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  padding-top: 0;
}

.signup-svg {
  max-width: 110%;
  height: auto;
  filter: drop-shadow(0 10px 30px rgba(0, 102, 204, 0.1));
  position: relative;
  z-index: 2;
  opacity: 0;
  animation: slideInLeft 0.8s ease-out 0.8s forwards;
  margin: 0 auto;
  display: block;
  margin-top: 6rem;
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
  top: 50%;
  right: 8%;
  transform: translateY(-50%);
  animation: fadeInScale 1s ease-out 1.1s forwards, float 6s ease-in-out infinite 1.1s;
}

.bubble-3 {
  width: 110px;
  height: 110px;
  bottom: 10%;
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
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
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

@keyframes slideInBannerLeft {
  from {
    opacity: 0;
    transform: translateX(-100%);
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

/* Responsive */
@media (max-width: 991px) {
  .signup-form-container {
    padding: 2rem;
  }
  
  .signup-title {
    font-size: 1.8rem;
  }
  
  .signup-svg {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .signup-card {
    margin: 0 1rem;
    border-radius: 20px;
  }
  
  .signup-form-container {
    padding: 2rem 1.5rem;
  }
  
  .signup-title {
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
  
  .signup-svg {
    max-width: 90%;
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

@media (max-width: 576px) {
  .signup-form-container {
    padding: 1.5rem;
  }
  
  .signup-title {
    font-size: 2rem;
  }
  
  .welcome-decoration {
    width: 40px;
    height: 3px;
  }
  
  .signup-subtitle {
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
  
  .btn-signup {
    padding: 0.9rem 1.5rem;
  }
  
  .signup-card {
    margin: 0 0.5rem;
    border-radius: 16px;
  }
  
  .back-home-banner {
    width: 70%;
    height: 40px;
    border-radius: 0 0 0 12px;
  }
}

/* Interface d'erreur email existant */
.email-exists-error {
  animation: fadeInUp 0.6s ease-out;
}

.error-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 10px 30px var(--shadow-light);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem;
  text-align: center;
}

.error-header {
  margin-bottom: 1.5rem;
}

.error-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: 50%;
  color: white;
  font-size: 1.8rem;
  animation: pulse 2s ease-in-out infinite;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0;
}

.error-content {
  margin-bottom: 1.5rem;
}

.error-message {
  font-size: 1rem;
  color: var(--dark-gray);
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.error-message strong {
  color: var(--text-dark);
  background: rgba(0, 102, 204, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.error-question {
  font-size: 1.1rem;
  color: var(--text-dark);
  margin: 0;
  font-weight: 600;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(255, 107, 107, 0);
  }
}

@media (max-width: 768px) {
  .error-card {
    padding: 1.5rem;
    margin: 1rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .error-title {
    font-size: 1.3rem;
  }
  
  .error-message {
    font-size: 0.95rem;
  }
  
  .error-question {
    font-size: 1rem;
  }
}
</style>
