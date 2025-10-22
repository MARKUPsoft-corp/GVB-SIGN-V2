import 'dart:convert';
import 'package:http/http.dart' as http;

class VerificationService {
  static const String baseUrl = 'http://127.0.0.1:8000/api/signatures';
  
  /// Vérifie la signature d'un document par son ID
  static Future<Map<String, dynamic>> verifySignature(String documentId) async {
    try {
      final url = Uri.parse('$baseUrl/verify-signature/$documentId/');
      print('🔍 Vérification du document ID: $documentId');
      print('🌐 URL: $url');
      
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
      );
      
      print('📡 Réponse HTTP: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('✅ Données reçues: ${data.keys.join(', ')}');
        return data;
      } else {
        print('❌ Erreur HTTP: ${response.statusCode}');
        print('❌ Corps de la réponse: ${response.body}');
        return {
          'success': false,
          'error': 'Erreur HTTP ${response.statusCode}: ${response.body}',
        };
      }
    } catch (e) {
      print('❌ Erreur lors de la vérification: $e');
      return {
        'success': false,
        'error': 'Erreur de connexion: $e',
      };
    }
  }
  
  /// Télécharge un fichier depuis une URL
  static Future<List<int>?> downloadFile(String url) async {
    try {
      print('📥 Téléchargement du fichier: $url');
      final response = await http.get(Uri.parse(url));
      
      if (response.statusCode == 200) {
        print('✅ Fichier téléchargé avec succès (${response.bodyBytes.length} bytes)');
        return response.bodyBytes;
      } else {
        print('❌ Erreur lors du téléchargement: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Erreur lors du téléchargement: $e');
      return null;
    }
  }
}
