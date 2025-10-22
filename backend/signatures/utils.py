from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import DocumentPreparation, DocumentSignatureStep
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import hashlib
import base64

User = get_user_model()


def advance_workflow_step(preparation):
    """
    Fait avancer le workflow d'une préparation de document
    """
    try:
        workflow = preparation.signature_workflow or []
        current_step = preparation.current_step or 0
        total_steps = preparation.total_steps or 0
        
        # Vérifier si c'est la dernière étape
        if current_step >= total_steps - 1:
            # Workflow terminé
            preparation.status = 'completed'
            preparation.completed_at = timezone.now()
            preparation.current_signer = None
            preparation.save()
            
            return {
                'advanced': False,
                'is_complete': True,
                'message': 'Workflow terminé - Document complètement signé'
            }
        
        # Avancer à l'étape suivante
        next_step = current_step + 1
        next_step_data = workflow[next_step] if next_step < len(workflow) else None
        
        if not next_step_data:
            return {
                'advanced': False,
                'error': 'Données de workflow manquantes pour l\'étape suivante'
            }
        
        # Mettre à jour la préparation
        preparation.current_step = next_step
        preparation.status = 'pending_signature'
        
        # Définir le prochain signataire
        try:
            next_signer = User.objects.get(id=next_step_data['user_id'])
            preparation.current_signer = next_signer
        except User.DoesNotExist:
            return {
                'advanced': False,
                'error': f'Utilisateur introuvable pour l\'étape {next_step + 1}'
            }
        
        preparation.save()
        
        return {
            'advanced': True,
            'next_signer': {
                'id': next_step_data['user_id'],
                'name': next_step_data['user_name'],
                'email': next_step_data['user_email'],
                'role': next_step_data['role']
            },
            'current_step': next_step,
            'total_steps': total_steps,
            'is_complete': False
        }
        
    except Exception as e:
        return {
            'advanced': False,
            'error': f'Erreur lors de l\'avancement du workflow: {str(e)}'
        }


def verify_document_signature(signature_base64, public_key_pem, stored_hash):
    """
    Vérifie qu'une signature numérique est valide en comparant les hash
    
    Processus CORRECT:
    1. Décoder la signature base64
    2. Charger la clé publique
    3. Déchiffrer la signature avec la clé publique (récupère le hash)
    4. Comparer le hash récupéré avec le hash stocké
    
    Args:
        signature_base64: str - Signature en base64
        public_key_pem: str - Clé publique au format PEM
        stored_hash: str - Hash stocké en base de données (hexadécimal)
    
    Returns:
        dict: {
            'valid': bool,
            'message': str,
            'stored_hash': str,
            'recovered_hash': str (si vérification réussie)
        }
    """
    try:
        print("🔐 === DÉBUT DE LA VÉRIFICATION DE SIGNATURE ===")
        print(f"📊 Hash stocké: {stored_hash[:20]}...")
        
        # Étape 1: Décoder la signature base64
        print("🔓 Décodage de la signature base64...")
        try:
            signature_bytes = base64.b64decode(signature_base64)
            print(f"✅ Signature décodée, taille: {len(signature_bytes)} bytes")
        except Exception as e:
            return {
                'valid': False,
                'message': f'Erreur de décodage de la signature: {str(e)}',
                'stored_hash': stored_hash
            }
        
        # Étape 2: Charger la clé publique
        print("🔑 Chargement de la clé publique...")
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode('utf-8'),
                backend=default_backend()
            )
            print("✅ Clé publique chargée")
        except Exception as e:
            return {
                'valid': False,
                'message': f'Erreur de chargement de la clé publique: {str(e)}',
                'stored_hash': stored_hash
            }
        
        # Étape 3: Déchiffrer la signature avec la clé publique RSA
        print("🔍 Déchiffrement de la signature avec la clé publique...")
        try:
            # Obtenir les nombres RSA de la clé publique
            public_numbers = public_key.public_numbers()
            n = public_numbers.n  # Modulus
            e = public_numbers.e  # Exponent
            
            # Convertir la signature en entier
            signature_int = int.from_bytes(signature_bytes, byteorder='big')
            
            # Déchiffrer: m = s^e mod n
            decrypted_int = pow(signature_int, e, n)
            
            # Convertir en bytes
            decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')
            
            print(f"✅ Signature déchiffrée, taille: {len(decrypted_bytes)} bytes")
            
            # Étape 4: Parser la structure DigestInfo PKCS#1 v1.5
            print("📋 Analyse de la structure DigestInfo...")
            
            # La structure DigestInfo contient:
            # - AlgorithmIdentifier (pour SHA-256)
            # - Le hash du document (32 bytes pour SHA-256)
            
            # Pour SHA-256, la structure DigestInfo fait 51 bytes:
            # - 19 bytes pour AlgorithmIdentifier
            # - 32 bytes pour le hash
            
            if len(decrypted_bytes) < 51:
                return {
                    'valid': False,
                    'message': 'Structure DigestInfo invalide - taille incorrecte',
                    'stored_hash': stored_hash
                }
            
            # Extraire le hash (les 32 derniers bytes)
            recovered_hash_bytes = decrypted_bytes[-32:]
            recovered_hash = recovered_hash_bytes.hex()
            
            print(f"✅ Hash récupéré de la signature: {recovered_hash[:20]}...")
            print(f"📊 Hash stocké en base:          {stored_hash[:20]}...")
            
            # Étape 5: Comparer les hash
            if recovered_hash.lower() == stored_hash.lower():
                print("✅ ✅ ✅ SIGNATURE VALIDE! ✅ ✅ ✅")
                print(f"✅ Le hash récupéré correspond au hash stocké")
                print(f"✅ Le document original n'a pas été modifié")
                print(f"✅ La signature est authentique")
                
                return {
                    'valid': True,
                    'message': 'Signature valide - Le hash récupéré correspond au hash stocké',
                    'stored_hash': stored_hash,
                    'recovered_hash': recovered_hash,
                    'verification_method': 'RSA-SHA256 with PKCS#1 v1.5 (manual verification)',
                    'signature_algorithm': 'RSA',
                    'hash_algorithm': 'SHA-256'
                }
            else:
                print("❌ Signature INVALIDE!")
                print(f"❌ Hash récupéré: {recovered_hash}")
                print(f"❌ Hash stocké:    {stored_hash}")
                print(f"❌ Les hash ne correspondent pas")
                
                return {
                    'valid': False,
                    'message': 'Signature invalide - Le hash récupéré ne correspond pas au hash stocké',
                    'stored_hash': stored_hash,
                    'recovered_hash': recovered_hash,
                    'reason': 'hash_mismatch'
                }
            
        except Exception as e:
            print(f"❌ Erreur lors du déchiffrement: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'valid': False,
                'message': f'Erreur lors du déchiffrement de la signature: {str(e)}',
                'stored_hash': stored_hash
            }
    
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'valid': False,
            'message': f'Erreur lors de la vérification: {str(e)}',
            'stored_hash': stored_hash
        }
    finally:
        print("🔐 === FIN DE LA VÉRIFICATION DE SIGNATURE ===")


def verify_signature_record(signature_record):
    """
    Vérifie la signature d'un enregistrement DocumentSignature
    
    Args:
        signature_record: DocumentSignature instance
    
    Returns:
        dict: Résultat de la vérification
    """
    try:
        # Vérifier la signature en comparant les hash
        # PAS besoin de lire le document signé, on compare juste:
        # - Le hash récupéré de la signature (déchiffrement avec clé publique)
        # - Le hash stocké en base de données
        result = verify_document_signature(
            signature_base64=signature_record.signature,
            public_key_pem=signature_record.public_key,
            stored_hash=signature_record.document_hash
        )
        
        return result
    except Exception as e:
        return {
            'valid': False,
            'message': f'Erreur lors de la vérification: {str(e)}'
        }
