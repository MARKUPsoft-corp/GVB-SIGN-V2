import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import '../services/verification_service.dart';
import 'pdf_preview_screen.dart';

class VerificationResultScreen extends StatefulWidget {
  final String documentId;

  const VerificationResultScreen({
    super.key,
    required this.documentId,
  });

  @override
  State<VerificationResultScreen> createState() => _VerificationResultScreenState();
}

class _VerificationResultScreenState extends State<VerificationResultScreen>
    with TickerProviderStateMixin {
  static const Color primaryBlue = Color(0xFF0066CC);
  static const Color primaryBlueDark = Color(0xFF004D99);
  static const Color successGreen = Color(0xFF28A745);
  static const Color errorRed = Color(0xFFDC3545);

  Map<String, dynamic>? _verificationData;
  bool _isLoading = true;
  String? _error;
  String? _downloadedFilePath;
  bool _isDownloading = false;

  late AnimationController _headerController;
  late AnimationController _contentController;
  late AnimationController _actionsController;

  late Animation<double> _headerAnimation;
  late Animation<double> _contentAnimation;
  late Animation<double> _actionsAnimation;

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _verifyDocument();
  }

  void _initializeAnimations() {
    _headerController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _contentController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _actionsController = AnimationController(
      duration: const Duration(milliseconds: 1200),
      vsync: this,
    );

    _headerAnimation = Tween<double>(
      begin: -50.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _headerController,
      curve: Curves.easeOut,
    ));

    _contentAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _contentController,
      curve: Curves.easeOut,
    ));

    _actionsAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _actionsController,
      curve: Curves.easeOut,
    ));

    // Démarrer les animations
    _headerController.forward();
    Future.delayed(const Duration(milliseconds: 200), () {
      if (mounted) _contentController.forward();
    });
    Future.delayed(const Duration(milliseconds: 400), () {
      if (mounted) _actionsController.forward();
    });
  }

  @override
  void dispose() {
    _headerController.dispose();
    _contentController.dispose();
    _actionsController.dispose();
    super.dispose();
  }

  Future<void> _verifyDocument() async {
    try {
      setState(() {
        _isLoading = true;
        _error = null;
      });

      print('🔍 Vérification du document: ${widget.documentId}');
      final result = await VerificationService.verifySignature(widget.documentId);

      if (result['success'] == true) {
        setState(() {
          _verificationData = result;
          _isLoading = false;
        });
        print('✅ Vérification réussie');
      } else {
        setState(() {
          _error = result['error'] ?? 'Erreur inconnue';
          _isLoading = false;
        });
        print('❌ Erreur de vérification: $_error');
      }
    } catch (e) {
      setState(() {
        _error = 'Erreur de connexion: $e';
        _isLoading = false;
      });
      print('❌ Exception: $e');
    }
  }

  Future<void> _downloadDocument() async {
    if (_verificationData == null) return;

    setState(() {
      _isDownloading = true;
    });

    try {
      final documentUrl = _verificationData!['document_urls']?['signed_document_url'];
      if (documentUrl == null) {
        throw Exception('URL du document non disponible');
      }

      final fullUrl = 'http://127.0.0.1:8000$documentUrl';
      print('📥 Téléchargement depuis: $fullUrl');

      final fileBytes = await VerificationService.downloadFile(fullUrl);
      if (fileBytes == null) {
        throw Exception('Échec du téléchargement');
      }

      final directory = await getApplicationDocumentsDirectory();
      final fileName = '${widget.documentId}_signed.pdf';
      final file = File('${directory.path}/$fileName');
      await file.writeAsBytes(fileBytes);

      setState(() {
        _downloadedFilePath = file.path;
        _isDownloading = false;
      });

      print('✅ Document téléchargé: ${file.path}');

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 8),
                Text('Document téléchargé avec succès'),
              ],
            ),
            backgroundColor: successGreen,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _isDownloading = false;
      });
      print('❌ Erreur de téléchargement: $e');

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: 8),
                Expanded(child: Text('Erreur: $e')),
              ],
            ),
            backgroundColor: errorRed,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final TextTheme textTheme = GoogleFonts.ralewayTextTheme(Theme.of(context).textTheme);

    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: primaryBlue),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: Text(
          'Résultat de Vérification',
          style: textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w700,
            color: primaryBlue,
            fontSize: 20,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: primaryBlue),
            onPressed: _isLoading ? null : _verifyDocument,
          ),
        ],
      ),
      body: _buildBody(textTheme),
    );
  }

  Widget _buildBody(TextTheme textTheme) {
    if (_isLoading) {
      return _buildLoadingState(textTheme);
    }

    if (_error != null) {
      return _buildErrorState(textTheme);
    }

    if (_verificationData == null) {
      return _buildEmptyState(textTheme);
    }

    return _buildSuccessState(textTheme);
  }

  Widget _buildLoadingState(TextTheme textTheme) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                BoxShadow(
                  color: primaryBlue.withOpacity(0.1),
                  blurRadius: 20,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              children: [
                const CircularProgressIndicator(
                  color: primaryBlue,
                  strokeWidth: 3,
                ),
                const SizedBox(height: 24),
                Text(
                  'Vérification en cours...',
                  style: textTheme.titleLarge?.copyWith(
                    color: primaryBlue,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Analyse de l\'authenticité du document',
                  style: textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorState(TextTheme textTheme) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: errorRed.withOpacity(0.1),
                blurRadius: 20,
                offset: const Offset(0, 10),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.error_outline,
                size: 64,
                color: errorRed,
              ),
              const SizedBox(height: 16),
              Text(
                'Erreur de Vérification',
                style: textTheme.titleLarge?.copyWith(
                  color: errorRed,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                _error!,
                textAlign: TextAlign.center,
                style: textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _verifyDocument,
                icon: const Icon(Icons.refresh),
                label: const Text('Réessayer'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: errorRed,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState(TextTheme textTheme) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.1),
                blurRadius: 20,
                offset: const Offset(0, 10),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.inbox_outlined,
                size: 64,
                color: Colors.grey[400],
              ),
              const SizedBox(height: 16),
              Text(
                'Aucune Donnée',
                style: textTheme.titleLarge?.copyWith(
                  color: Colors.grey[600],
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Aucune information de vérification disponible',
                textAlign: TextAlign.center,
                style: textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[500],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSuccessState(TextTheme textTheme) {
    final documentInfo = _verificationData!['document_info'] ?? {};
    final verification = _verificationData!['verification'] ?? {};
    final organizationInfo = _verificationData!['organization_info'] ?? {};
    final documentUrls = _verificationData!['document_urls'] ?? {};

    final isValid = verification['valid'] == true;
    final signerName = documentInfo['signer_name'] ?? 'Inconnu';
    final filename = documentInfo['filename'] ?? 'Document';
    // final signatureDate = documentInfo['signature_timestamp'] ?? '';
    // final organizationName = organizationInfo['name'];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // En-tête avec statut
          AnimatedBuilder(
            animation: _headerAnimation,
            builder: (context, child) {
              return Transform.translate(
                offset: Offset(_headerAnimation.value, 0),
                child: Opacity(
                  opacity: _headerController.value,
                  child: _buildStatusHeader(textTheme, isValid, signerName, filename),
                ),
              );
            },
          ),

          const SizedBox(height: 24),

          // Informations du document
          AnimatedBuilder(
            animation: _contentAnimation,
            builder: (context, child) {
              return Transform.translate(
                offset: Offset(0, _contentAnimation.value),
                child: Opacity(
                  opacity: _contentController.value,
                  child: _buildDocumentInfo(textTheme, documentInfo, verification, organizationInfo),
                ),
              );
            },
          ),

          const SizedBox(height: 24),

          // Actions
          AnimatedBuilder(
            animation: _actionsAnimation,
            builder: (context, child) {
              return Transform.translate(
                offset: Offset(0, _actionsAnimation.value),
                child: Opacity(
                  opacity: _actionsController.value,
                  child: _buildActions(textTheme, documentUrls),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildStatusHeader(TextTheme textTheme, bool isValid, String signerName, String filename) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isValid 
              ? [successGreen, const Color(0xFF20C997)]
              : [errorRed, const Color(0xFFE74C3C)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: (isValid ? successGreen : errorRed).withOpacity(0.3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        children: [
          Icon(
            isValid ? Icons.verified : Icons.warning,
            size: 48,
            color: Colors.white,
          ),
          const SizedBox(height: 16),
          Text(
            isValid ? 'Document Authentique' : 'Document Non Vérifié',
            style: textTheme.headlineSmall?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.w900,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            isValid 
                ? 'Ce document a été vérifié et est authentique'
                : 'Ce document n\'a pas pu être vérifié',
            textAlign: TextAlign.center,
            style: textTheme.bodyLarge?.copyWith(
              color: Colors.white.withOpacity(0.9),
            ),
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              'Signé par: $signerName',
              style: textTheme.bodyMedium?.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDocumentInfo(TextTheme textTheme, Map<String, dynamic> documentInfo, 
                           Map<String, dynamic> verification, Map<String, dynamic> organizationInfo) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: primaryBlue.withOpacity(0.1),
            blurRadius: 16,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.info_outline, color: primaryBlue, size: 24),
              const SizedBox(width: 8),
              Text(
                'Informations du Document',
                style: textTheme.titleLarge?.copyWith(
                  color: primaryBlue,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          _buildInfoRow(textTheme, 'Nom du fichier', documentInfo['filename'] ?? 'N/A'),
          _buildInfoRow(textTheme, 'Signataire', documentInfo['signer_name'] ?? 'N/A'),
          _buildInfoRow(textTheme, 'Email', documentInfo['signer_email'] ?? 'N/A'),
          _buildInfoRow(textTheme, 'Date de signature', _formatDate(documentInfo['signature_timestamp'])),
          _buildInfoRow(textTheme, 'Taille originale', _formatFileSize(documentInfo['file_size_original'])),
          _buildInfoRow(textTheme, 'Taille signée', _formatFileSize(documentInfo['file_size_signed'])),
          
          if (organizationInfo['name'] != null) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: primaryBlue.withOpacity(0.05),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: primaryBlue.withOpacity(0.2)),
              ),
              child: Row(
                children: [
                  Icon(Icons.business, color: primaryBlue, size: 20),
                  const SizedBox(width: 8),
                  Text(
                    'Organisation: ${organizationInfo['name']}',
                    style: textTheme.bodyMedium?.copyWith(
                      color: primaryBlue,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ],

          const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: verification['valid'] == true 
                  ? successGreen.withOpacity(0.1)
                  : errorRed.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: verification['valid'] == true 
                    ? successGreen.withOpacity(0.3)
                    : errorRed.withOpacity(0.3),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(
                      verification['valid'] == true ? Icons.security : Icons.warning,
                      color: verification['valid'] == true ? successGreen : errorRed,
                      size: 20,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Statut de Vérification',
                      style: textTheme.titleMedium?.copyWith(
                        color: verification['valid'] == true ? successGreen : errorRed,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  verification['message'] ?? 'N/A',
                  style: textTheme.bodyMedium?.copyWith(
                    color: verification['valid'] == true ? successGreen : errorRed,
                  ),
                ),
                if (verification['verification_method'] != null) ...[
                  const SizedBox(height: 8),
                  Text(
                    'Méthode: ${verification['verification_method']}',
                    style: textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(TextTheme textTheme, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              '$label:',
              style: textTheme.bodyMedium?.copyWith(
                color: Colors.grey[600],
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: textTheme.bodyMedium?.copyWith(
                color: Colors.black87,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActions(TextTheme textTheme, Map<String, dynamic> documentUrls) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: primaryBlue.withOpacity(0.1),
            blurRadius: 16,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.download, color: primaryBlue, size: 24),
              const SizedBox(width: 8),
              Text(
                'Actions',
                style: textTheme.titleLarge?.copyWith(
                  color: primaryBlue,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Bouton de téléchargement
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isDownloading ? null : _downloadDocument,
              icon: _isDownloading 
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        color: Colors.white,
                        strokeWidth: 2,
                      ),
                    )
                  : const Icon(Icons.download),
              label: Text(_isDownloading ? 'Téléchargement...' : 'Télécharger le document signé'),
              style: ElevatedButton.styleFrom(
                backgroundColor: primaryBlue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
          ),

          const SizedBox(height: 12),

          // Bouton de prévisualisation (si document téléchargé)
          if (_downloadedFilePath != null) ...[
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => PDFPreviewScreen(
                        filePath: _downloadedFilePath!,
                        fileName: _verificationData?['document_info']?['filename'] ?? 'Document signé',
                      ),
                    ),
                  );
                },
                icon: const Icon(Icons.preview),
                label: const Text('Prévisualiser le document'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: primaryBlue,
                  side: const BorderSide(color: primaryBlue),
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
          ],

          const SizedBox(height: 12),

          // Bouton pour ouvrir dans le navigateur
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: documentUrls['signed_document_url'] != null
                  ? () async {
                      final url = 'http://127.0.0.1:8000${documentUrls['signed_document_url']}';
                      if (await canLaunchUrl(Uri.parse(url))) {
                        await launchUrl(Uri.parse(url));
                      }
                    }
                  : null,
              icon: const Icon(Icons.open_in_browser),
              label: const Text('Ouvrir dans le navigateur'),
              style: OutlinedButton.styleFrom(
                foregroundColor: primaryBlue,
                side: const BorderSide(color: primaryBlue),
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  String _formatDate(String? timestamp) {
    if (timestamp == null) return 'N/A';
    try {
      final date = DateTime.parse(timestamp);
      return '${date.day}/${date.month}/${date.year} à ${date.hour}:${date.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return 'N/A';
    }
  }

  String _formatFileSize(dynamic size) {
    if (size == null) return 'N/A';
    final bytes = int.tryParse(size.toString()) ?? 0;
    if (bytes == 0) return '0 B';
    
    const units = ['B', 'KB', 'MB', 'GB'];
    int unitIndex = 0;
    double sizeInUnits = bytes.toDouble();
    
    while (sizeInUnits >= 1024 && unitIndex < units.length - 1) {
      sizeInUnits /= 1024;
      unitIndex++;
    }
    
    return '${sizeInUnits.toStringAsFixed(1)} ${units[unitIndex]}';
  }
}
