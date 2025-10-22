import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:pdfx/pdfx.dart';
import 'dart:io';

class PDFPreviewScreen extends StatefulWidget {
  final String filePath;
  final String fileName;

  const PDFPreviewScreen({
    super.key,
    required this.filePath,
    required this.fileName,
  });

  @override
  State<PDFPreviewScreen> createState() => _PDFPreviewScreenState();
}

class _PDFPreviewScreenState extends State<PDFPreviewScreen> {
  static const Color primaryBlue = Color(0xFF0066CC);
  static const Color primaryBlueDark = Color(0xFF004D99);

  bool _isLoading = true;
  String? _error;
  String _errorMessage = '';
  PdfController? _pdfController;
  int _currentPage = 0;
  int _totalPages = 0;

  @override
  void initState() {
    super.initState();
    _loadPDF();
  }

  Future<void> _loadPDF() async {
    try {
      final file = File(widget.filePath);
      if (!await file.exists()) {
        setState(() {
          _error = 'error';
          _errorMessage = 'Fichier PDF introuvable';
          _isLoading = false;
        });
        return;
      }

      _pdfController = PdfController(
        document: PdfDocument.openFile(widget.filePath),
      );

      // Obtenir le nombre total de pages
      final document = await PdfDocument.openFile(widget.filePath);
      _totalPages = document.pagesCount;

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = 'error';
        _errorMessage = 'Erreur de chargement: $e';
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _pdfController?.dispose();
    super.dispose();
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
          widget.fileName,
          style: textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w700,
            color: primaryBlue,
            fontSize: 18,
          ),
          overflow: TextOverflow.ellipsis,
        ),
        centerTitle: true,
        actions: [
          if (_totalPages > 0)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              margin: const EdgeInsets.only(right: 16),
              decoration: BoxDecoration(
                color: primaryBlue.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: primaryBlue.withOpacity(0.3)),
              ),
              child: Text(
                '$_currentPage / $_totalPages',
                style: textTheme.bodySmall?.copyWith(
                  color: primaryBlue,
                  fontWeight: FontWeight.w600,
                ),
              ),
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

    return _buildPDFViewer();
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
                  'Chargement du document...',
                  style: textTheme.titleLarge?.copyWith(
                    color: primaryBlue,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Préparation de la prévisualisation',
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
                color: Colors.red.withOpacity(0.1),
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
                color: Colors.red,
              ),
              const SizedBox(height: 16),
              Text(
                'Erreur de Chargement',
                style: textTheme.titleLarge?.copyWith(
                  color: Colors.red,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                _errorMessage.isNotEmpty ? _errorMessage : 'Impossible de charger le document PDF',
                textAlign: TextAlign.center,
                style: textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    _isLoading = true;
                    _error = null;
                    _errorMessage = '';
                  });
                },
                icon: const Icon(Icons.refresh),
                label: const Text('Réessayer'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
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

  Widget _buildPDFViewer() {
    if (_pdfController == null) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    return Container(
      margin: const EdgeInsets.all(16),
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
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: PdfView(
          controller: _pdfController!,
          onPageChanged: (page) {
            setState(() {
              _currentPage = page + 1; // pdfx utilise 0-based indexing
            });
          },
        ),
      ),
    );
  }
}
