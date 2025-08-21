# GVB Sign - Application de Signature Électronique

## Description

GVB Sign est une application moderne de signature électronique utilisant la technologie QR Code pour l'authentification sécurisée des documents.

## Structure du Projet

```
GVB_Sign/
├── frontend/          # Application Nuxt.js
│   ├── app/          # Pages et layouts
│   ├── components/   # Composants Vue.js
│   ├── public/       # Assets statiques
│   └── ...
└── backend/          # API Backend (à développer)
```

## Technologies Utilisées

### Frontend
- **Nuxt.js 4** - Framework Vue.js
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Icônes
- **Vue.js 3** - Framework JavaScript
- **TypeScript** - Typage statique

### Backend
- À définir

## Installation

### Frontend

```bash
cd frontend
npm install
npm run dev
```

L'application sera accessible sur `http://localhost:3000`

## Fonctionnalités

### ✅ Implémentées
- **Page d'accueil** avec hero section
- **Section fonctionnalités** avec cartes interactives
- **Navigation responsive** avec sidebar mobile
- **Design moderne** avec glassmorphisme
- **Animations fluides** et transitions
- **Navigation par ancres** vers les sections

### 🚧 En cours de développement
- Pages d'authentification (login/register)
- Dashboard utilisateur
- Gestion des documents
- Intégration QR Code

## Développement

### Structure des Composants

```
components/
├── homepage/         # Composants de la page d'accueil
│   ├── HeroSection.vue
│   └── FeaturesSection.vue
├── shared/           # Composants partagés
│   ├── Navbar.vue
│   └── Footer.vue
└── auth/             # Composants d'authentification
    ├── LoginForm.vue
    └── SignupForm.vue
```

### Styles

Le projet utilise :
- **Variables CSS** pour la charte graphique (bleu/blanc)
- **Animations CSS** pour les transitions
- **Responsive design** pour tous les écrans
- **Glassmorphisme** pour les effets modernes

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence privée - Tous droits réservés à MARKUPsoft-corp.

## Contact

**MARKUPsoft-corp** - [GitHub](https://github.com/MARKUPsoft-corp)
