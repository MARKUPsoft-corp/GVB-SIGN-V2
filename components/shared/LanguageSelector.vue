<template>
  <div 
    class="language-selector-wrapper" 
    :class="[
      `size-${size}`, 
      { 'is-dark': dark, 'is-dropdown': variant === 'dropdown', 'is-pill': variant === 'pill' }
    ]"
  >
    <!-- Variante 1 : Pill Toggle (Visible, Direct, 1-Click) -->
    <div v-if="variant === 'pill'" class="lang-pill-container">
      <button 
        type="button" 
        class="lang-pill-btn" 
        :class="{ 'active': isFrench }" 
        @click="setLocale('fr')" 
        title="Passer en Français"
        aria-label="Français"
      >
        <span class="flag-icon">🇫🇷</span>
        <span class="lang-text">FR</span>
      </button>
      <button 
        type="button" 
        class="lang-pill-btn" 
        :class="{ 'active': isEnglish }" 
        @click="setLocale('en')" 
        title="Switch to English"
        aria-label="English"
      >
        <span class="flag-icon">🇬🇧</span>
        <span class="lang-text">EN</span>
      </button>
    </div>

    <!-- Variante 2 : Dropdown avec globe pour espaces réduits -->
    <div v-else class="lang-dropdown-container position-relative" ref="dropdownRef">
      <button 
        type="button" 
        class="lang-dropdown-trigger" 
        @click="isOpen = !isOpen"
        :aria-expanded="isOpen"
      >
        <i class="bi bi-globe2 me-1"></i>
        <span class="current-flag me-1">{{ isFrench ? '🇫🇷' : '🇬🇧' }}</span>
        <span class="current-code fw-bold">{{ isFrench ? 'FR' : 'EN' }}</span>
        <i class="bi bi-chevron-down ms-1 dropdown-arrow" :class="{ 'rotated': isOpen }"></i>
      </button>

      <transition name="dropdown-fade">
        <ul v-if="isOpen" class="lang-dropdown-menu">
          <li>
            <button 
              type="button" 
              class="dropdown-item d-flex align-items-center" 
              :class="{ 'active': isFrench }" 
              @click="selectLang('fr')"
            >
              <span class="flag me-2">🇫🇷</span>
              <span class="label">Français</span>
              <i v-if="isFrench" class="bi bi-check-lg ms-auto text-primary"></i>
            </button>
          </li>
          <li>
            <button 
              type="button" 
              class="dropdown-item d-flex align-items-center" 
              :class="{ 'active': isEnglish }" 
              @click="selectLang('en')"
            >
              <span class="flag me-2">🇬🇧</span>
              <span class="label">English</span>
              <i v-if="isEnglish" class="bi bi-check-lg ms-auto text-primary"></i>
            </button>
          </li>
        </ul>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from '../../composables/useI18n'

const props = defineProps({
  variant: {
    type: String,
    default: 'pill' // 'pill' | 'dropdown'
  },
  size: {
    type: String,
    default: 'md' // 'sm' | 'md' | 'lg'
  },
  dark: {
    type: Boolean,
    default: false
  }
})

const { locale, isFrench, isEnglish, setLocale } = useI18n()
const isOpen = ref(false)
const dropdownRef = ref(null)

const selectLang = (lang) => {
  setLocale(lang)
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  if (process.client) {
    document.addEventListener('click', handleClickOutside)
  }
})

onUnmounted(() => {
  if (process.client) {
    document.removeEventListener('click', handleClickOutside)
  }
})
</script>

<style scoped>
.language-selector-wrapper {
  display: inline-flex;
  align-items: center;
  user-select: none;
}

/* === Pill Variant === */
.lang-pill-container {
  display: inline-flex;
  align-items: center;
  background: rgba(0, 102, 204, 0.08);
  border: 1px solid rgba(0, 102, 204, 0.2);
  border-radius: 50rem;
  padding: 3px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.25s ease;
}

.lang-pill-container:hover {
  background: rgba(0, 102, 204, 0.12);
  border-color: rgba(0, 102, 204, 0.35);
}

.lang-pill-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: transparent;
  border: none;
  border-radius: 50rem;
  padding: 4px 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  line-height: 1;
}

.lang-pill-btn .flag-icon {
  font-size: 1rem;
  line-height: 1;
}

.lang-pill-btn .lang-text {
  letter-spacing: 0.5px;
}

.lang-pill-btn:hover:not(.active) {
  color: #0066cc;
  background: rgba(255, 255, 255, 0.6);
}

.lang-pill-btn.active {
  background: #0066cc;
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 102, 204, 0.35);
}

/* Version sombre ou sur fond sombre */
.is-dark .lang-pill-container {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
}

.is-dark .lang-pill-btn {
  color: rgba(255, 255, 255, 0.85);
}

.is-dark .lang-pill-btn.active {
  background: #ffffff;
  color: #0066cc;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
}

/* Tailles */
.size-sm .lang-pill-btn {
  padding: 3px 8px;
  font-size: 0.75rem;
}

.size-sm .lang-pill-btn .flag-icon {
  font-size: 0.85rem;
}

.size-lg .lang-pill-btn {
  padding: 6px 14px;
  font-size: 0.95rem;
}

.size-lg .lang-pill-btn .flag-icon {
  font-size: 1.15rem;
}

/* === Dropdown Variant === */
.lang-dropdown-trigger {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #ffffff;
  border: 1px solid rgba(0, 102, 204, 0.2);
  border-radius: 50rem;
  padding: 6px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #0066cc;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 102, 204, 0.08);
}

.lang-dropdown-trigger:hover {
  background: #f0f8ff;
  border-color: #0066cc;
}

.dropdown-arrow {
  font-size: 0.75rem;
  transition: transform 0.2s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.lang-dropdown-menu {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  z-index: 1050;
  min-width: 140px;
  background: #ffffff;
  border: 1px solid rgba(0, 102, 204, 0.15);
  border-radius: 12px;
  padding: 6px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  list-style: none;
  margin: 0;
}

.lang-dropdown-menu .dropdown-item {
  width: 100%;
  border: none;
  background: transparent;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #2d3748;
  cursor: pointer;
  transition: background 0.15s ease;
}

.lang-dropdown-menu .dropdown-item:hover {
  background: #f0f8ff;
  color: #0066cc;
}

.lang-dropdown-menu .dropdown-item.active {
  background: rgba(0, 102, 204, 0.08);
  color: #0066cc;
  font-weight: 600;
}

.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
