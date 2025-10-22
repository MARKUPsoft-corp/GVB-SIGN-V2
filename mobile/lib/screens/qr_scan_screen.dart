import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:permission_handler/permission_handler.dart';

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
                    final List<Barcode> barcodes = capture.barcodes;
                    for (final barcode in barcodes) {
                      if (barcode.rawValue != null) {
                        setState(() {
                          scannedCode = barcode.rawValue;
                        });
                      }
                    }
                  },
                ),
                // Overlay avec cadre de scan
                Center(
                  child: Container(
                    width: 250,
                    height: 250,
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: primaryBlue,
                        width: 3,
                      ),
                      borderRadius: BorderRadius.circular(20),
                    ),
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
                  Text(
                    'Contenu du QR Code',
                    style: textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w700,
                      color: primaryBlue,
                      fontSize: 20,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: primaryBlue.withOpacity(0.05),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: primaryBlue.withOpacity(0.2),
                          width: 1,
                        ),
                      ),
                      child: SingleChildScrollView(
                        child: Text(
                          scannedCode ?? 'Aucun QR code scanné',
                          style: textTheme.bodyLarge?.copyWith(
                            color: scannedCode != null ? Colors.black87 : Colors.grey,
                            fontSize: 16,
                          ),
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

