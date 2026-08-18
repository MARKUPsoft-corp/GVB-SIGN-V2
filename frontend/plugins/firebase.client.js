import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getAnalytics } from "firebase/analytics";

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();

  // Firebase configuration based on environment variables
  const firebaseConfig = {
    apiKey: config.public.firebaseApiKey,
    authDomain: config.public.firebaseAuthDomain,
    projectId: config.public.firebaseProjectId,
    storageBucket: config.public.firebaseStorageBucket,
    messagingSenderId: config.public.firebaseMessagingSenderId,
    appId: config.public.firebaseAppId,
    measurementId: config.public.firebaseMeasurementId
  };

  // Initialize Firebase (check if already initialized to prevent duplicate app errors)
  let app;
  if (!getApps().length) {
    app = initializeApp(firebaseConfig);
  } else {
    app = getApp();
  }

  // Initialize services
  const auth = getAuth(app);
  const firestore = getFirestore(app);
  
  // Analytics is only available in browser context
  let analytics = null;
  if (process.client) {
    analytics = getAnalytics(app);
  }

  // Provide the instances globally in the Nuxt app
  nuxtApp.provide('firebaseApp', app);
  nuxtApp.provide('auth', auth);
  nuxtApp.provide('firestore', firestore);
  if (analytics) {
    nuxtApp.provide('analytics', analytics);
  }
});
