import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:permission_handler/permission_handler.dart';
import 'verification_result_screen.dart';

class QRScanScreen extends StatefulWidget {
  const QRScanScreen({super.key});

  @override
  State<QRScanScreen> createState() => _QRScanScreenState();
}

class _QRScanScreenState extends State<QRScanScreen> with WidgetsBindingObserver {
  static const Color primaryBlue = Color(0xFF0066CC);
  static const Color primaryBlueDark = Color(0xFF004D99);

  MobileScannerController cameraController = MobileScannerController();
  String? scannedCode;
  bool _cameraPermissionGranted = false;
  bool _isLoading = true;
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _checkCameraPermission();
  }

  Future<void> _checkCameraPermission() async {
    final status = await Permission.camera.request();
    setState(() {
      _cameraPermissionGranted = status.isGranted;
      _isLoading = false;
    });
    
    if (!status.isGranted) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Permission caméra requise pour scanner les QR codes'),
            duration: Duration(seconds: 3),
          ),
        );
      }
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    cameraController.dispose();
    super.dispose();
  }

  /// Traite le code QR scanné et vérifie s'il s'agit d'un ID de document valide
  void _processScannedCode(String code) async {
    if (_isProcessing) return;
    
    setState(() {
      _isProcessing = true;
      scannedCode = code;
    });

    print('📱 Code QR scanné: $code');
    
    // Vérifier si le code ressemble à un UUID (format des IDs de document)
    if (_isValidDocumentId(code)) {
      print('✅ ID de document valide détecté: $code');
      
      // Naviguer vers la page de résultat avec l'ID
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => VerificationResultScreen(documentId: code),
          ),
        );
      }
    } else {
      print('❌ Code QR invalide - ne correspond pas à un ID de document');
      
      // Afficher un message d'erreur
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error_outline, color: Colors.white),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'QR Code invalide - Ce n\'est pas un document signé GVB',
                    style: GoogleFonts.ralewayTextTheme(Theme.of(context).textTheme).bodyMedium?.copyWith(color: Colors.white),
                  ),
                ),
              ],
            ),
            backgroundColor: Colors.red[600],
            duration: const Duration(seconds: 4),
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        );
      }
      
      // Réinitialiser après 2 secondes pour permettre un nouveau scan
      Future.delayed(const Duration(seconds: 2), () {
        if (mounted) {
          setState(() {
            _isProcessing = false;
            scannedCode = null;
          });
        }
      });
    }
  }

  /// Vérifie si le code scanné ressemble à un UUID valide (format des IDs de document)
  bool _isValidDocumentId(String code) {
    // Format UUID v4: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
    final uuidRegex = RegExp(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', caseSensitive: false);
    return uuidRegex.hasMatch(code);
  }

  @override
  Widget build(BuildContext context) {
    final TextTheme textTheme = GoogleFonts.ralewayTextTheme(Theme.of(context).textTheme);

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: primaryBlue),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: Text(
          'Scanner QR Code',
          style: textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w700,
            color: primaryBlue,
            fontSize: 20,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.flash_off, color: Colors.grey),
            onPressed: () => cameraController.toggleTorch(),
          ),
          IconButton(
            icon: const Icon(Icons.cameraswitch, color: primaryBlue),
            onPressed: () => cameraController.switchCamera(),
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : !_cameraPermissionGranted
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.camera_alt_outlined, size: 80, color: Colors.grey),
                      const SizedBox(height: 20),
                      Text(
                        'Permission caméra refusée',
                        style: textTheme.titleLarge?.copyWith(
                          color: Colors.grey,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        'Veuillez autoriser l\'accès à la caméra\ndans les paramètres',
                        textAlign: TextAlign.center,
                        style: textTheme.bodyMedium?.copyWith(
                          color: Colors.grey,
                        ),
                      ),
                      const SizedBox(height: 30),
                      ElevatedButton(
                        onPressed: () => openAppSettings(),
                        child: const Text('Ouvrir les paramètres'),
                      ),
                    ],
                  ),
                )
              : Column(
        children: [
          Expanded(
            flex: 3,
            child: Stack(
              children: [
                MobileScanner(
                  controller: cameraController,
                  onDetect: (capture) {
                    if (_isProcessing) return; // Éviter les scans multiples
                    
                    final List<Barcode> barcodes = capture.barcodes;
                    for (final barcode in barcodes) {
                      if (barcode.rawValue != null) {
                        _processScannedCode(barcode.rawValue!);
                      }
                    }
                  },
                ),
                // Overlay avec cadre de scan et indicateur de traitement
                Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 250,
                        height: 250,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: _isProcessing ? Colors.orange : primaryBlue,
                            width: 3,
                          ),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: _isProcessing
                            ? Container(
                                decoration: BoxDecoration(
                                  color: Colors.orange.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(17),
                                ),
                                child: const Center(
                                  child: CircularProgressIndicator(
                                    color: Colors.orange,
                                    strokeWidth: 3,
                                  ),
                                ),
                              )
                            : null,
                      ),
                      if (_isProcessing) ...[
                        const SizedBox(height: 16),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.orange.withOpacity(0.9),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const SizedBox(
                                width: 16,
                                height: 16,
                                child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 2,
                                ),
                              ),
                              const SizedBox(width: 8),
                              Text(
                                'Vérification en cours...',
                                style: textTheme.bodyMedium?.copyWith(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 10,
                    offset: const Offset(0, -5),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        _isProcessing ? Icons.hourglass_empty : Icons.qr_code_2_rounded,
                        color: _isProcessing ? Colors.orange : primaryBlue,
                        size: 24,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        _isProcessing ? 'Vérification en cours' : 'Contenu du QR Code',
                        style: textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.w700,
                          color: _isProcessing ? Colors.orange : primaryBlue,
                          fontSize: 20,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: _isProcessing 
                            ? Colors.orange.withOpacity(0.05)
                            : primaryBlue.withOpacity(0.05),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: _isProcessing 
                              ? Colors.orange.withOpacity(0.2)
                              : primaryBlue.withOpacity(0.2),
                          width: 1,
                        ),
                      ),
                      child: _isProcessing
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const CircularProgressIndicator(
                                    color: Colors.orange,
                                    strokeWidth: 3,
                                  ),
                                  const SizedBox(height: 16),
                                  Text(
                                    'Analyse du document...',
                                    style: textTheme.bodyLarge?.copyWith(
                                      color: Colors.orange[700],
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ],
                              ),
                            )
                          : SingleChildScrollView(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  if (scannedCode != null) ...[
                                    Container(
                                      padding: const EdgeInsets.all(12),
                                      decoration: BoxDecoration(
                                        color: primaryBlue.withOpacity(0.1),
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: primaryBlue.withOpacity(0.3),
                                        ),
                                      ),
                                      child: Row(
                                        children: [
                                          Icon(
                                            Icons.check_circle,
                                            color: primaryBlue,
                                            size: 20,
                                          ),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: Text(
                                              'ID de document valide',
                                              style: textTheme.bodyMedium?.copyWith(
                                                color: primaryBlue,
                                                fontWeight: FontWeight.w600,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                    const SizedBox(height: 12),
                                  ],
                                  Text(
                                    scannedCode ?? 'Aucun QR code scanné',
                                    style: textTheme.bodyLarge?.copyWith(
                                      color: scannedCode != null ? Colors.black87 : Colors.grey,
                                      fontSize: 16,
                                      fontFamily: 'monospace',
                                    ),
                                  ),
                                ],
                              ),
                            ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

