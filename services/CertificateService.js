import { Buffer } from 'buffer'
import forge from 'node-forge'

export class CertificateService {
  constructor() {
    this.certificate = null
    this.privateKey = null
    this.publicKey = null
    this.certificateInfo = null
    this.STORAGE_KEY = 'gvb_certificate_info'
  }

  /**
   * Décode un certificat PFX/P12
   * @param {File} file - Le fichier certificat
   * @param {string} password - Le mot de passe
   * @returns {Promise<Object>} Informations du certificat
   */
  async decodeCertificate(file, password) {
    try {
      // 1. Lire le fichier
      const arrayBuffer = await this.readFileAsArrayBuffer(file)
      
      // 2. Décoder le contenu PKCS#12
      const p12Data = await this.decodePKCS12(arrayBuffer, password)
      
      // 3. Extraire les informations
      const certificateInfo = this.extractCertificateInfo(p12Data)
      
      // 4. Stocker les données
      this.certificate = p12Data.certificate
      this.privateKey = p12Data.privateKey
      this.publicKey = p12Data.publicKey
      this.certificateInfo = certificateInfo
      
      // 5. Sauvegarder en sessionStorage
      this.saveToSessionStorage(certificateInfo, p12Data.privateKey, p12Data.publicKey)
      
      return certificateInfo
    } catch (error) {
      throw new Error(`Erreur lors du décodage du certificat: ${error.message}`)
    }
  }

  /**
   * Lit un fichier comme ArrayBuffer
   */
  async readFileAsArrayBuffer(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result)
      reader.onerror = reject
      reader.readAsArrayBuffer(file)
    })
  }

  /**
   * Décode le contenu PKCS#12
   */
  async decodePKCS12(arrayBuffer, password) {
    // Pour l'instant, on simule le décodage
    // TODO: Implémenter avec node-forge ou @peculiar/webcrypto
    return await this.parsePKCS12WithForge(arrayBuffer, password)
  }

  /**
   * Décode un fichier PKCS#12 avec node-forge
   */
  async parsePKCS12WithForge(arrayBuffer, password) {
    try {
      // Convertir ArrayBuffer en Buffer
      const buffer = Buffer.from(arrayBuffer)
      
      // Décoder le PKCS#12
      const p12Der = forge.util.decode64(buffer.toString('base64'))
      const p12Asn1 = forge.asn1.fromDer(p12Der)
      const p12 = forge.pkcs12.pkcs12FromAsn1(p12Asn1, password)
      
      // Extraire le certificat
      const certBags = p12.getBags({ bagType: forge.pki.oids.certBag })[forge.pki.oids.certBag]
      
      if (!certBags || certBags.length === 0) {
        throw new Error('Aucun certificat trouvé dans le fichier PKCS#12')
      }
      
      const certificate = certBags[0].cert
      
      // Extraire la clé privée (essayer différents types)
      let privateKey = null
      
      // Essayer d'abord les clés chiffrées
      const shroudedKeyBags = p12.getBags({ bagType: forge.pki.oids.pkcs8ShroudedKeyBag })[forge.pki.oids.pkcs8ShroudedKeyBag]
      if (shroudedKeyBags && shroudedKeyBags.length > 0) {
        privateKey = shroudedKeyBags[0].key
      } else {
        // Essayer les clés non chiffrées
        const keyBags = p12.getBags({ bagType: forge.pki.oids.pkcs8KeyBag })[forge.pki.oids.pkcs8KeyBag]
        if (keyBags && keyBags.length > 0) {
          privateKey = keyBags[0].key
        } else {
          // Essayer les clés RSA
          const rsaKeyBags = p12.getBags({ bagType: forge.pki.oids.rsaKeyBag })[forge.pki.oids.rsaKeyBag]
          if (rsaKeyBags && rsaKeyBags.length > 0) {
            privateKey = rsaKeyBags[0].key
          }
        }
      }
      
      if (!privateKey) {
        throw new Error('Aucune clé privée trouvée dans le fichier PKCS#12')
      }
      
      return {
        certificate: certificate,
        privateKey: privateKey,
        publicKey: certificate.publicKey
      }
    } catch (error) {
      if (error.message.includes('Invalid password') || error.message.includes('Invalid MAC')) {
        throw new Error('Mot de passe incorrect pour le certificat')
      }
      throw new Error(`Erreur lors du décodage du certificat: ${error.message}`)
    }
  }

  /**
   * Extrait les informations du certificat
   */
  extractCertificateInfo(p12Data) {
    const cert = p12Data.certificate
    
    // Extraire les informations du sujet
    const subject = {}
    cert.subject.attributes.forEach(attr => {
      if (attr.value) {
        subject[attr.shortName] = attr.value
      }
    })
    
    // Extraire les informations de l'émetteur
    const issuer = {}
    cert.issuer.attributes.forEach(attr => {
      if (attr.value) {
        issuer[attr.shortName] = attr.value
      }
    })
    
    return {
      subject: {
        commonName: subject.CN || subject.commonName,
        organization: subject.O || subject.organizationName,
        organizationalUnit: subject.OU || subject.organizationalUnitName,
        country: subject.C || subject.countryName,
        email: subject.E || subject.emailAddress
      },
      issuer: {
        commonName: issuer.CN || issuer.commonName,
        organization: issuer.O || issuer.organizationName,
        country: issuer.C || issuer.countryName
      },
      validity: {
        notBefore: cert.validity.notBefore,
        notAfter: cert.validity.notAfter,
        isValid: this.isCertificateValid(cert)
      },
      serialNumber: this.formatSerialNumber(cert.serialNumber),
      fingerprint: this.calculateFingerprint(cert),
      keyUsage: this.extractKeyUsage(cert),
      signatureAlgorithm: cert.signatureOid,
      importedAt: new Date().toISOString()
    }
  }

  /**
   * Vérifie si le certificat est valide
   */
  isCertificateValid(cert) {
    const now = new Date()
    return now >= cert.validity.notBefore && now <= cert.validity.notAfter
  }

  /**
   * Calcule l'empreinte du certificat
   */
  calculateFingerprint(cert) {
    try {
      // Calculer l'empreinte SHA-256 du certificat
      const der = forge.asn1.toDer(forge.pki.certificateToAsn1(cert))
      const md = forge.md.sha256.create()
      md.update(der.getBytes())
      const fingerprint = md.digest().toHex()
      
      // Formater l'empreinte avec des deux-points
      return 'SHA256: ' + fingerprint.match(/.{1,2}/g).join(':').toUpperCase()
    } catch (error) {
      console.error('Erreur lors du calcul de l\'empreinte:', error)
      return 'SHA256: Erreur de calcul'
    }
  }

  /**
   * Extrait les usages de clé
   */
  extractKeyUsage(cert) {
    try {
      const keyUsageExt = cert.getExtension('keyUsage')
      if (keyUsageExt) {
        return keyUsageExt.keyUsages || []
      }
      return []
    } catch (error) {
      console.error('Erreur lors de l\'extraction des usages de clé:', error)
      return []
    }
  }

  /**
   * Formate le numéro de série du certificat
   */
  formatSerialNumber(serialNumber) {
    try {
      // Si c'est déjà une chaîne, la retourner
      if (typeof serialNumber === 'string') {
        return serialNumber.toUpperCase()
      }
      
      // Si c'est un objet BigInteger de node-forge
      if (serialNumber && typeof serialNumber.toString === 'function') {
        const hex = serialNumber.toString(16)
        // Formater avec des deux-points tous les 2 caractères
        return hex.match(/.{1,2}/g).join(':').toUpperCase()
      }
      
      // Fallback
      return serialNumber ? serialNumber.toString() : 'N/A'
    } catch (error) {
      console.error('Erreur lors du formatage du numéro de série:', error)
      return 'Erreur de formatage'
    }
  }

  /**
   * Sauvegarde les informations en sessionStorage
   */
  saveToSessionStorage(certificateInfo, privateKey, publicKey) {
    try {
      // Convertir les clés en format PEM
      const privateKeyPem = forge.pki.privateKeyToPem(privateKey)
      const publicKeyPem = forge.pki.publicKeyToPem(publicKey)
      
      const storageData = {
        ...certificateInfo,
        privateKeyPem: privateKeyPem,
        publicKeyPem: publicKeyPem
      }
      
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(storageData))
    } catch (error) {
      console.error('Erreur lors de la sauvegarde en sessionStorage:', error)
    }
  }

  /**
   * Charge les informations depuis sessionStorage
   */
  loadFromSessionStorage() {
    try {
      const stored = sessionStorage.getItem(this.STORAGE_KEY)
      if (stored) {
        const data = JSON.parse(stored)
        this.certificateInfo = data
        
        // Restaurer les clés si elles existent
        if (data.privateKeyPem) {
          this.privateKey = forge.pki.privateKeyFromPem(data.privateKeyPem)
        }
        if (data.publicKeyPem) {
          this.publicKey = forge.pki.publicKeyFromPem(data.publicKeyPem)
        }
        
        return this.certificateInfo
      }
    } catch (error) {
      console.error('Erreur lors du chargement depuis sessionStorage:', error)
    }
    return null
  }

  /**
   * Supprime les informations de sessionStorage
   */
  clearFromSessionStorage() {
    try {
      sessionStorage.removeItem(this.STORAGE_KEY)
    } catch (error) {
      console.error('Erreur lors de la suppression de sessionStorage:', error)
    }
  }

  /**
   * Signe un document avec le certificat
   */
  async signDocument(documentHash) {
    if (!this.privateKey) {
      throw new Error('Aucune clé privée disponible')
    }
    
    if (!this.certificateInfo?.validity?.isValid) {
      throw new Error('Le certificat est expiré et ne peut pas être utilisé pour signer des documents')
    }
    
    // Logique de signature avec la clé privée
    return await this.createSignature(documentHash, this.privateKey)
  }

  /**
   * Crée une signature avec la clé privée
   */
  async createSignature(documentHash, privateKey) {
    try {
      // Créer un hash SHA-256 du document
      const md = forge.md.sha256.create()
      md.update(documentHash)
      const hash = md.digest()
      
      // Signer le hash avec la clé privée
      const signature = privateKey.sign(md)
      
      return {
        signature: forge.util.encode64(signature),
        algorithm: 'sha256WithRSAEncryption',
        timestamp: new Date().toISOString(),
        hash: forge.util.encode64(hash.getBytes())
      }
    } catch (error) {
      throw new Error(`Erreur lors de la signature: ${error.message}`)
    }
  }

  /**
   * Vérifie une signature avec la clé publique
   */
  async verifySignature(documentHash, signature, algorithm = 'sha256WithRSAEncryption') {
    if (!this.publicKey) {
      throw new Error('Aucune clé publique disponible')
    }
    
    try {
      // Créer un hash SHA-256 du document
      const md = forge.md.sha256.create()
      md.update(documentHash)
      const hash = md.digest()
      
      // Décoder la signature
      const signatureBytes = forge.util.decode64(signature)
      
      // Vérifier la signature
      const isValid = this.publicKey.verify(hash.getBytes(), signatureBytes)
      
      return {
        isValid: isValid,
        algorithm: algorithm,
        verifiedAt: new Date().toISOString()
      }
    } catch (error) {
      throw new Error(`Erreur lors de la vérification: ${error.message}`)
    }
  }

  /**
   * Obtient les informations du certificat stocké
   */
  getCertificateInfo() {
    return this.certificateInfo
  }

  /**
   * Obtient la clé privée au format PEM
   */
  getPrivateKeyPem() {
    if (this.privateKey) {
      return forge.pki.privateKeyToPem(this.privateKey)
    }
    return null
  }

  /**
   * Obtient la clé publique au format PEM
   */
  getPublicKeyPem() {
    if (this.publicKey) {
      return forge.pki.publicKeyToPem(this.publicKey)
    }
    return null
  }

  /**
   * Obtient le certificat au format PEM
   */
  getCertificatePem() {
    if (this.certificate) {
      return forge.pki.certificateToPem(this.certificate)
    }
    return null
  }

  /**
   * Vérifie si un certificat est chargé
   */
  hasCertificate() {
    return this.certificateInfo !== null
  }

  /**
   * Vérifie si les clés sont disponibles
   */
  hasKeys() {
    return this.privateKey !== null && this.publicKey !== null
  }

  /**
   * Vérifie si le certificat peut être utilisé (valide et non expiré)
   */
  canUseCertificate() {
    // TODO: RESTAURATION VALIDITÉ CERTIFICAT
    // La vérification de validité (expiration) est temporairement désactivée à la demande.
    // Pour empêcher la signature avec un certificat expiré, décommentez la ligne ci-dessous :
    // return this.hasCertificate() && this.certificateInfo?.validity?.isValid
    
    // Actuellement, on autorise l'utilisation tant qu'un certificat est présent, même s'il est expiré
    return this.hasCertificate()
  }

  /**
   * Efface les données du certificat
   */
  clearCertificate() {
    this.certificate = null
    this.privateKey = null
    this.publicKey = null
    this.certificateInfo = null
    this.clearFromSessionStorage()
  }

  /**
   * Initialise le service en chargeant les données depuis sessionStorage
   */
  initialize() {
    this.loadFromSessionStorage()
  }
}
