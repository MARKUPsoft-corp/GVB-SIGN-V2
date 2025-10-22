import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:ui';
import 'package:google_fonts/google_fonts.dart';
import 'qr_scan_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with TickerProviderStateMixin {
  final ScrollController _scrollController = ScrollController();
  bool _isScrolled = false;
  

  static const Color primaryBlue = Color(0xFF0066CC);
  static const Color primaryBlueDark = Color(0xFF004D99);

  LinearGradient get _heroGradient => LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          primaryBlueDark,
          primaryBlue,
          const Color(0xFF007BFF),
        ],
      );

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(() {
      final bool scrolled = _scrollController.hasClients && _scrollController.offset > 4;
      if (scrolled != _isScrolled) {
        setState(() {
          _isScrolled = scrolled;
        });
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final TextTheme textTheme = GoogleFonts.ralewayTextTheme(Theme.of(context).textTheme);

    return Scaffold(
      bottomNavigationBar: _buildBottomMenu(textTheme),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        systemOverlayStyle: const SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          statusBarIconBrightness: Brightness.dark,
        ),
        flexibleSpace: ClipRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: _isScrolled ? 15 : 0, sigmaY: _isScrolled ? 15 : 0),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(_isScrolled ? 0.3 : 1.0),
                border: const Border(
                  bottom: BorderSide(color: Color(0x1A0066CC), width: 1),
                ),
              ),
                    child: SafeArea(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
                  child: Row(
                    children: [
                      Image.asset(
                        'assets/images/gvb-logo.png',
                        width: 32,
                        height: 32,
                        fit: BoxFit.contain,
                      ),
                      const SizedBox(width: 10),
                      Text(
                        'GVB Sign',
                        style: textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w700,
                          color: _HomeScreenState.primaryBlue,
                          fontSize: 20,
                        ),
                      ),
                      const Spacer(),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
      body: CustomScrollView(
        controller: _scrollController,
        slivers: [
          SliverToBoxAdapter(
            child: _HeroSection(
              gradient: _heroGradient,
              textTheme: textTheme,
            ),
          ),
          SliverToBoxAdapter(
            child: _FeaturesSection(textTheme: textTheme),
          ),
          SliverToBoxAdapter(
            child: _CTASection(textTheme: textTheme),
          ),
        ],
      ),
    );
  }

  // Barre de menu en bas avec glassmorphism
  Widget _buildBottomMenu(TextTheme textTheme) {
    return Container(
      height: 70,
      decoration: BoxDecoration(
        color: const Color(0xFF0066CC).withOpacity(0.03),
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
        border: const Border(
          top: BorderSide(color: Color(0x1A0066CC), width: 1),
        ),
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 25, sigmaY: 25),
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                 colors: [
                   const Color(0xFF0066CC).withOpacity(0.03),
                   const Color(0xFF0066CC).withOpacity(0.05),
                 ],
              ),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(20),
                topRight: Radius.circular(20),
              ),
              border: const Border(
                top: BorderSide(color: Color(0x33FFFFFF), width: 1),
              ),
            ),
            child: SafeArea(
              child: Center(
                child: Container(
                  constraints: const BoxConstraints(maxWidth: 300),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                  _buildMenuItem(
                    icon: Icons.home_rounded,
                    label: 'Accueil',
                    isActive: true,
                    textTheme: textTheme,
                  ),
                  _buildMenuItem(
                    icon: Icons.history_rounded,
                    label: 'Historique',
                    isActive: false,
                    textTheme: textTheme,
                  ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String label,
    required bool isActive,
    required TextTheme textTheme,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 4),
      decoration: BoxDecoration(
        color: isActive ? primaryBlue.withOpacity(0.2) : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isActive ? primaryBlue.withOpacity(0.3) : Colors.black.withOpacity(0.1),
          width: 2,
        ),
        boxShadow: isActive
            ? [
                BoxShadow(
                  color: primaryBlue.withOpacity(0.2),
                  blurRadius: 20,
                  offset: const Offset(0, 6),
                ),
                BoxShadow(
                  color: primaryBlue.withOpacity(0.1),
                  blurRadius: 10,
                  offset: const Offset(0, 3),
                ),
              ]
            : [],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 28,
            color: isActive ? primaryBlue : Colors.black54,
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: textTheme.bodySmall?.copyWith(
              color: isActive ? primaryBlue : Colors.black54,
              fontWeight: isActive ? FontWeight.w700 : FontWeight.w500,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }
}

class _HeroSection extends StatefulWidget {
  const _HeroSection({required this.gradient, required this.textTheme});

  final LinearGradient gradient;
  final TextTheme textTheme;

  @override
  State<_HeroSection> createState() => _HeroSectionState();
}

class _HeroSectionState extends State<_HeroSection> with TickerProviderStateMixin {
  late AnimationController _contentController;
  late AnimationController _titleController;
  late AnimationController _subtitleController;
  late AnimationController _buttonController;
  
  late Animation<double> _contentAnimation;
  late Animation<double> _titleAnimation;
  late Animation<double> _subtitleAnimation;
  late Animation<double> _buttonAnimation;
  
  bool _hasAnimated = false;

  @override
  void initState() {
    super.initState();
    
    // Initialize animation controllers
    _contentController = AnimationController(
      duration: const Duration(milliseconds: 1200),
      vsync: this,
    );
    _titleController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _subtitleController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _buttonController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    
    // Initialize animations
    _contentAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _contentController,
      curve: Curves.easeOut,
    ));
    
    _titleAnimation = Tween<double>(
      begin: -50.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _titleController,
      curve: Curves.easeOut,
    ));
    
    _subtitleAnimation = Tween<double>(
      begin: -50.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _subtitleController,
      curve: Curves.easeOut,
    ));
    
    _buttonAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _buttonController,
      curve: Curves.easeOut,
    ));
    
    // Start animations with delays (matching web timing)
    _startAnimations();
  }
  
  void _startAnimations() {
    if (_hasAnimated) return;
    _hasAnimated = true;
    
    // Hero content: delay 500ms (délai initial pour voir l'effet)
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) _contentController.forward();
    });
    
    // Hero title: delay 700ms
    Future.delayed(const Duration(milliseconds: 700), () {
      if (mounted) _titleController.forward();
    });
    
    // Hero subtitle: delay 1000ms
    Future.delayed(const Duration(milliseconds: 1000), () {
      if (mounted) _subtitleController.forward();
    });
    
    // Hero button: delay 1300ms
    Future.delayed(const Duration(milliseconds: 1300), () {
      if (mounted) _buttonController.forward();
    });
  }

  @override
  void dispose() {
    _contentController.dispose();
    _titleController.dispose();
    _subtitleController.dispose();
    _buttonController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _contentAnimation,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, 30 * (1 - _contentAnimation.value)),
          child: Opacity(
            opacity: _contentAnimation.value > 0 ? 1.0 : 0.0,
            child: Container(
              color: Colors.white,
              padding: const EdgeInsets.only(top: 16, left: 16, right: 16, bottom: 0),
              child: SafeArea(
                bottom: false,
                child: SingleChildScrollView(
                  child: Container(
                    decoration: BoxDecoration(
                      color: const Color(0xFFF8F9FA),
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: const [
                        BoxShadow(
                          color: Color(0x140066CC),
                          blurRadius: 20,
                          offset: Offset(0, 10),
                        ),
                      ],
                    ),
                    padding: const EdgeInsets.fromLTRB(16, 20, 16, 16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Titre avec animation slideInLeft
                        AnimatedBuilder(
                          animation: _titleAnimation,
                          builder: (context, child) {
                            return Transform.translate(
                              offset: Offset(_titleAnimation.value, 0),
                              child: Opacity(
                                opacity: _titleController.value > 0 ? 1.0 : 0.0,
                                child: RichText(
                                  textAlign: TextAlign.left,
                                  text: TextSpan(
                                    style: widget.textTheme.headlineSmall?.copyWith(
                                      color: Colors.black87,
                                      fontWeight: FontWeight.w900,
                                      height: 1.15,
                                      fontSize: 35,
                                    ).copyWith(fontWeight: FontWeight.w900),
                                    children: const [
                                      TextSpan(text: "Vérifier l'authenticité "),
                                      TextSpan(
                                        text: 'de vos Documents',
                                        style: TextStyle(color: _HomeScreenState.primaryBlue),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                        const SizedBox(height: 10),
                        
                        // Sous-titre avec animation slideInLeft
                        AnimatedBuilder(
                          animation: _subtitleAnimation,
                          builder: (context, child) {
                            return Transform.translate(
                              offset: Offset(_subtitleAnimation.value, 0),
                              child: Opacity(
                                opacity: _subtitleController.value > 0 ? 1.0 : 0.0,
                                child: Text(
                                  'Révolutionnez votre processus de signature avec notre technologie QR Code avancée. Sécurisé, rapide et conforme.',
                                  textAlign: TextAlign.left,
                                  style: widget.textTheme.bodyLarge?.copyWith(
                                    color: Colors.black87.withOpacity(0.8),
                                    fontSize: 16,
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                        const SizedBox(height: 16),
                        
                        // Bouton avec animation fadeInUp
                        AnimatedBuilder(
                          animation: _buttonAnimation,
                          builder: (context, child) {
                            return Transform.translate(
                              offset: Offset(0, _buttonAnimation.value),
                              child: Opacity(
                                opacity: _buttonController.value > 0 ? 1.0 : 0.0,
                                child: Wrap(
                                  alignment: WrapAlignment.start,
                                  spacing: 12,
                                  runSpacing: 12,
                                  children: [
                                    Container(
                                      decoration: BoxDecoration(
                                        gradient: widget.gradient,
                                        borderRadius: BorderRadius.circular(50),
                                        boxShadow: const [
                                          BoxShadow(
                                            color: Color(0x330066CC), // rgba(0, 102, 204, 0.2)
                                            blurRadius: 25,
                                            offset: Offset(0, 8),
                                          ),
                                        ],
                                      ),
                                      child: ElevatedButton.icon(
                                        onPressed: () {
                                          Navigator.of(context).push(
                                            MaterialPageRoute(
                                              builder: (context) => const QRScanScreen(),
                                            ),
                                          );
                                        },
                                        icon: const Icon(
                                          Icons.qr_code_2_rounded,
                                          size: 20,
                                          color: Colors.white,
                                        ),
                                        label: Text(
                                          'Commencer maintenant',
                                          style: widget.textTheme.labelLarge?.copyWith(
                                            fontWeight: FontWeight.w600,
                                            fontSize: 17.6, // 1.1rem
                                            letterSpacing: 0.02,
                                            color: Colors.white,
                                          ),
                                        ),
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.transparent,
                                          foregroundColor: Colors.white,
                                          shadowColor: Colors.transparent,
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 35,
                                            vertical: 15,
                                          ),
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(50),
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}


class _FeaturesSection extends StatefulWidget {
  const _FeaturesSection({required this.textTheme});

  final TextTheme textTheme;

  @override
  State<_FeaturesSection> createState() => _FeaturesSectionState();
}

class _FeaturesSectionState extends State<_FeaturesSection> with TickerProviderStateMixin {
  late AnimationController _headerController;
  late AnimationController _titleController;
  late AnimationController _subtitleController;
  late AnimationController _cardsController;
  
  late Animation<double> _headerAnimation;
  late Animation<double> _titleAnimation;
  late Animation<double> _subtitleAnimation;
  late Animation<double> _cardsAnimation;
  
  bool _hasAnimated = false;

  @override
  void initState() {
    super.initState();
    
    // Initialize animation controllers
    _headerController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _titleController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _subtitleController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _cardsController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    
    // Initialize animations
    _headerAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _headerController,
      curve: Curves.easeOut,
    ));
    
    _titleAnimation = Tween<double>(
      begin: 100.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _titleController,
      curve: Curves.easeOut,
    ));
    
    _subtitleAnimation = Tween<double>(
      begin: 100.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _subtitleController,
      curve: Curves.easeOut,
    ));
    
    _cardsAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _cardsController,
      curve: Curves.easeOut,
    ));
    
    // Start animations with delays (matching web timing)
    _startAnimations();
  }
  
  void _startAnimations() {
    if (_hasAnimated) return;
    _hasAnimated = true;
    
    // Features header: delay 2000ms (après Hero)
    Future.delayed(const Duration(milliseconds: 2000), () {
      if (mounted) _headerController.forward();
    });
    
    // Features title: delay 2200ms
    Future.delayed(const Duration(milliseconds: 2200), () {
      if (mounted) _titleController.forward();
    });
    
    // Features subtitle: delay 2300ms
    Future.delayed(const Duration(milliseconds: 2300), () {
      if (mounted) _subtitleController.forward();
    });
    
    // Features cards: delay 2400ms
    Future.delayed(const Duration(milliseconds: 2400), () {
      if (mounted) _cardsController.forward();
    });
  }

  @override
  void dispose() {
    _headerController.dispose();
    _titleController.dispose();
    _subtitleController.dispose();
    _cardsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final features = [
      _Feature(icon: Icons.qr_code_2_rounded, title: 'Technologie QR Code', subtitle: 'Authentification instantanée via QR Code sécurisé. Plus besoin de mots de passe complexes.'),
      _Feature(icon: Icons.shield_rounded, title: 'Sécurité Maximale', subtitle: 'Cryptage de bout en bout et conformité aux standards internationaux de sécurité.'),
      _Feature(icon: Icons.flash_on_rounded, title: 'Signature Instantanée', subtitle: 'Signez vos documents en quelques secondes depuis n\'importe quel appareil mobile.'),
      _Feature(icon: Icons.devices_rounded, title: 'Multi-Plateforme', subtitle: 'Compatible avec tous vos appareils : web, mobile iOS et Android.'),
    ];

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 28),
      color: const Color(0xFFF8F9FA),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // En-tête de section avec animation fadeInUp
          AnimatedBuilder(
            animation: _headerAnimation,
            builder: (context, child) {
              return Transform.translate(
                offset: Offset(0, _headerAnimation.value),
                child: Opacity(
                  opacity: _headerController.value,
                  child: Center(
                    child: Column(
                      children: [
                        // Titre avec animation slideInRight
                        AnimatedBuilder(
                          animation: _titleAnimation,
                          builder: (context, child) {
                            return Transform.translate(
                              offset: Offset(_titleAnimation.value, 0),
                              child: Opacity(
                                opacity: _titleController.value,
                                child: RichText(
                                  textAlign: TextAlign.center,
                                  text: TextSpan(
                                    style: widget.textTheme.headlineLarge?.copyWith(
                                      fontSize: 28,
                                      fontWeight: FontWeight.w900,
                                      height: 1.2,
                                      letterSpacing: -0.02,
                                      color: Colors.black87,
                                    ).copyWith(fontWeight: FontWeight.w900),
                                    children: const [
                                      TextSpan(text: 'Des '),
                                      TextSpan(
                                        text: 'Fonctionnalités',
                                        style: TextStyle(color: _HomeScreenState.primaryBlue),
                                      ),
                                      TextSpan(text: ' '),
                                      TextSpan(
                                        text: 'Innovantes',
                                        style: TextStyle(color: _HomeScreenState.primaryBlue),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                        const SizedBox(height: 16),
                        
                        // Sous-titre avec animation slideInRight
                        AnimatedBuilder(
                          animation: _subtitleAnimation,
                          builder: (context, child) {
                            return Transform.translate(
                              offset: Offset(_subtitleAnimation.value, 0),
                              child: Opacity(
                                opacity: _subtitleController.value,
                                child: Text(
                                  'Découvrez tous les avantages de notre solution de signature électronique nouvelle génération.',
                                  textAlign: TextAlign.center,
                                  style: widget.textTheme.bodyLarge?.copyWith(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w400,
                                    height: 1.6,
                                    color: const Color(0xFF6C757D), // --dark-gray
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 24),
          
          // Cartes avec animation fadeInUp
          AnimatedBuilder(
            animation: _cardsAnimation,
            builder: (context, child) {
              return Transform.translate(
                offset: Offset(0, _cardsAnimation.value),
                child: Opacity(
                  opacity: _cardsController.value,
                  child: GridView.builder(
                    physics: const NeverScrollableScrollPhysics(),
                    shrinkWrap: true,
                    itemCount: features.length,
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 1,
                      mainAxisSpacing: 16,
                      crossAxisSpacing: 0,
                      childAspectRatio: 2.8,
                    ),
                    itemBuilder: (context, index) {
                      final f = features[index];
                      return Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0x1A0066CC),
                      blurRadius: 16,
                      offset: const Offset(0, 8),
                    ),
                  ],
                  border: Border.all(color: const Color(0x1A0066CC)),
                ),
                padding: const EdgeInsets.all(12),
                child: Row(
                  children: [
                    Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            _HomeScreenState.primaryBlue.withOpacity(0.08),
                            _HomeScreenState.primaryBlue.withOpacity(0.12),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: _HomeScreenState.primaryBlue.withOpacity(0.1),
                          width: 1,
                        ),
                      ),
                      child: Icon(
                        f.icon,
                        color: _HomeScreenState.primaryBlue,
                        size: 28,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            f.title,
                            style: widget.textTheme.titleMedium?.copyWith(
                              fontSize: 18,
                              fontWeight: FontWeight.w900,
                              color: Colors.black87,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            f.subtitle,
                            style: widget.textTheme.bodyMedium?.copyWith(
                              color: const Color(0xFF6C757D),
                              height: 1.5,
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      );
    },
  ),
        ],
      ),
    );
  }
}

class _CTASection extends StatefulWidget {
  const _CTASection({required this.textTheme});

  final TextTheme textTheme;

  @override
  State<_CTASection> createState() => _CTASectionState();
}

class _CTASectionState extends State<_CTASection> with TickerProviderStateMixin {
  late AnimationController _contentController;
  late AnimationController _titleController;
  late AnimationController _subtitleController;
  late AnimationController _stepsController;
  
  late Animation<double> _contentAnimation;
  late Animation<double> _titleAnimation;
  late Animation<double> _subtitleAnimation;
  late Animation<double> _stepsAnimation;
  
  bool _hasAnimated = false;

  @override
  void initState() {
    super.initState();
    
    // Initialize animation controllers
    _contentController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _titleController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _subtitleController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _stepsController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    
    // Initialize animations
    _contentAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _contentController,
      curve: Curves.easeOut,
    ));
    
    _titleAnimation = Tween<double>(
      begin: -50.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _titleController,
      curve: Curves.easeOut,
    ));
    
    _subtitleAnimation = Tween<double>(
      begin: -50.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _subtitleController,
      curve: Curves.easeOut,
    ));
    
    _stepsAnimation = Tween<double>(
      begin: 30.0,
      end: 0.0,
    ).animate(CurvedAnimation(
      parent: _stepsController,
      curve: Curves.easeOut,
    ));
    
    // Start animations with delays
    _startAnimations();
  }
  
  void _startAnimations() {
    if (_hasAnimated) return;
    _hasAnimated = true;
    
    // CTA content: delay 3000ms (après Features)
    Future.delayed(const Duration(milliseconds: 3000), () {
      if (mounted) _contentController.forward();
    });
    
    // CTA title: delay 3200ms
    Future.delayed(const Duration(milliseconds: 3200), () {
      if (mounted) _titleController.forward();
    });
    
    // CTA subtitle: delay 3300ms
    Future.delayed(const Duration(milliseconds: 3300), () {
      if (mounted) _subtitleController.forward();
    });
    
    // CTA steps: delay 3400ms
    Future.delayed(const Duration(milliseconds: 3400), () {
      if (mounted) _stepsController.forward();
    });
  }

  @override
  void dispose() {
    _contentController.dispose();
    _titleController.dispose();
    _subtitleController.dispose();
    _stepsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _contentAnimation,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, _contentAnimation.value),
          child: Opacity(
            opacity: _contentController.value,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 28),
              child: Container(
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF0066CC), Color(0xFF007BFF)],
                  ),
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: const [
                    BoxShadow(
                      color: Color(0x330066CC),
                      blurRadius: 18,
                      offset: Offset(0, 10),
                    ),
                  ],
                ),
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Titre avec animation slideInLeft
                    AnimatedBuilder(
                      animation: _titleAnimation,
                      builder: (context, child) {
                        return Transform.translate(
                          offset: Offset(_titleAnimation.value, 0),
                          child: Opacity(
                            opacity: _titleController.value,
                            child: Text(
                              'Comment ça marche ?',
                              style: widget.textTheme.titleLarge?.copyWith(
                                color: Colors.white,
                                fontSize: 24,
                                fontWeight: FontWeight.w900,
                              ).copyWith(fontWeight: FontWeight.w900),
                            ),
                          ),
                        );
                      },
                    ),
                    const SizedBox(height: 8),
                    
                    // Sous-titre avec animation slideInLeft
                    AnimatedBuilder(
                      animation: _subtitleAnimation,
                      builder: (context, child) {
                        return Transform.translate(
                          offset: Offset(_subtitleAnimation.value, 0),
                          child: Opacity(
                            opacity: _subtitleController.value,
                            child: Text(
                              'Découvrez les étapes simples pour vérifier l\'authenticité de vos documents.',
                              style: widget.textTheme.bodyLarge?.copyWith(
                                color: Colors.white.withOpacity(0.95),
                                fontSize: 16,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                    const SizedBox(height: 24),
                    
                    // Étapes de vérification avec animation fadeInUp
                    AnimatedBuilder(
                      animation: _stepsAnimation,
                      builder: (context, child) {
                        return Transform.translate(
                          offset: Offset(0, _stepsAnimation.value),
                          child: Opacity(
                            opacity: _stepsController.value,
                            child: _buildVerificationSteps(),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
            ),
          ),
      );
    },
  );
  }
  
  Widget _buildVerificationSteps() {
    final steps = [
      _VerificationStep(
        stepNumber: 1,
        icon: Icons.qr_code_scanner_rounded,
        title: 'Scanner le QR Code',
        description: 'Pointez votre caméra vers le QR Code du document à vérifier.',
      ),
      _VerificationStep(
        stepNumber: 2,
        icon: Icons.security_rounded,
        title: 'Vérification automatique',
        description: 'Notre système analyse et vérifie l\'authenticité du document.',
      ),
      _VerificationStep(
        stepNumber: 3,
        icon: Icons.verified_rounded,
        title: 'Résultat instantané',
        description: 'Recevez immédiatement le statut de vérification du document.',
      ),
    ];

    return Column(
      children: steps.asMap().entries.map((entry) {
        final index = entry.key;
        final step = entry.value;
        
        return Container(
          margin: EdgeInsets.only(bottom: index < steps.length - 1 ? 16 : 0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Numéro d'étape et icône
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(25),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.3),
                    width: 2,
                  ),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      step.icon,
                      color: Colors.white,
                      size: 20,
                    ),
                    Text(
                      '${step.stepNumber}',
                      style: widget.textTheme.bodySmall?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                        fontSize: 10,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 16),
              
              // Contenu de l'étape
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      step.title,
                      style: widget.textTheme.titleMedium?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      step.description,
                      style: widget.textTheme.bodyMedium?.copyWith(
                        color: Colors.white.withOpacity(0.9),
                        fontSize: 14,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}

class _VerificationStep {
  const _VerificationStep({
    required this.stepNumber,
    required this.icon,
    required this.title,
    required this.description,
  });

  final int stepNumber;
  final IconData icon;
  final String title;
  final String description;
}

class _Feature {
  const _Feature({
    required this.icon,
    required this.title,
    required this.subtitle,
  });
  final IconData icon;
  final String title;
  final String subtitle;
}
