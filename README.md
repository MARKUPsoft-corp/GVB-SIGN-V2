# 🔐 GVB Sign - Frontend

## 📋 Description

Interface web moderne pour l'application de signature électronique GVB Sign. Cette plateforme permet aux utilisateurs de gérer leurs documents et signatures avec une technologie QR Code innovante.

## 🎨 Design

- **Charte graphique** : Bleu (#0066cc) et Blanc
- **Framework UI** : Bootstrap 5 + Bootstrap Icons
- **Design** : Modern, responsive, accessible

## 🛠️ Technologies

- **Framework** : Nuxt.js 4 (Vue.js avec SSR/SSG)
- **Styling** : Bootstrap 5 + SCSS personnalisé
- **Icons** : Bootstrap Icons
- **Package Manager** : npm

## 📁 Structure du Projet

```
frontend/
├── assets/
│   └── styles/
│       └── main.scss          # Styles globaux et variables CSS
├── components/
│   ├── homepage/              # Composants spécifiques à la page d'accueil
│   │   ├── HeroSection.vue    # Section héro avec illustration
│   │   ├── FeaturesSection.vue # Section fonctionnalités
│   │   └── CTASection.vue     # Section call-to-action
│   └── shared/                # Composants partagés
│       ├── Navbar.vue         # Navigation principale
│       └── Footer.vue         # Pied de page
├── layouts/
│   └── default.vue            # Layout principal
├── pages/
│   └── index.vue              # Page d'accueil
├── plugins/
│   └── bootstrap.client.ts    # Configuration Bootstrap
└── nuxt.config.ts             # Configuration Nuxt
```

## 🚀 Fonctionnalités Implementées

### ✅ Page d'Accueil
- **Hero Section** : Présentation avec illustration animée
- **Features Section** : 6 fonctionnalités principales avec animations
- **CTA Section** : Appel à l'action avec statistiques
- **Navigation** : Menu responsive avec authentification
- **Footer** : Liens, newsletter, contact, réseaux sociaux

### 🎭 Composants Créés
- **Navbar** : Navigation fixe avec logo et menu responsive
- **HeroSection** : Section héro avec animation et illustration technique
- **FeaturesSection** : Grille de fonctionnalités avec cards interactives
- **CTASection** : Section d'appel à l'action avec statistiques
- **Footer** : Footer complet avec newsletter et liens

## 🎨 Thème et Styles

### Variables CSS
- **Primary Blue** : `#0066cc`
- **Primary Blue Dark** : `#004d99`
- **Primary Blue Light** : `#3385d6`
- **Secondary Blue** : `#f0f8ff`
- **Accent Blue** : `#007bff`

### Animations
- Animations d'apparition (`fadeInUp`)
- Animations flottantes (`float`)
- Transitions hover sur tous les éléments interactifs
- Effets de parallaxe légers

## 🔧 Installation et Démarrage

```bash
# Installation des dépendances
npm install

# Démarrage en mode développement
npm run dev

# Build pour production
npm run build

# Aperçu de la production
npm run preview
```

## 📱 Responsive Design

- **Mobile First** : Design optimisé pour mobile d'abord
- **Breakpoints Bootstrap** : sm, md, lg, xl, xxl
- **Navigation** : Menu burger sur mobile
- **Animations** : Adaptées selon la taille d'écran

## 🎯 Prochaines Étapes

1. **Pages d'authentification** (Login/Register)
2. **Dashboard utilisateur**
3. **Interface d'upload de documents**
4. **Système de signature**
5. **Intégration QR Code**
6. **Application mobile (future)**

## 🔗 URLs de Développement

- **Local** : http://localhost:3000
- **Staging** : À définir
- **Production** : À définir

---

*Développé avec ❤️ par l'équipe GVB Sign*