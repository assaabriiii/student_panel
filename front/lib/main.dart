import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:ta_app/gen/assets.gen.dart';
import 'package:ta_app/screens/auths/login_screen.dart';
import 'package:ta_app/screens/student/home.dart';
import 'package:ta_app/widgets/custom_bottom_nav.dart';
import 'screens/auths/login_screen2.dart';

void main() {
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.white,
    statusBarIconBrightness: Brightness.dark,
    systemNavigationBarColor: Colors.white,
    systemNavigationBarIconBrightness: Brightness.dark,
  ));
  runApp(const MyApp());
}

const Color primaryColor = Color(0xff0466c8);
const Color primaryVarientColor = Color(0xff5C0AFF);
const secondaryTextColor = Color(0xffAFBED0);

class MyApp extends StatelessWidget {
  static const titleFontFamily = "Flaemische";
  static ThemeData themeData = ThemeData(
    textTheme: GoogleFonts.poppinsTextTheme(
      TextTheme(
        headlineMedium: TextStyle(fontFamily: Assets.fonts.flaemischeKanzleischrift, fontWeight: FontWeight.w600),
        titleSmall: TextStyle(fontFamily: Assets.fonts.instagramSans),
      ),
    ),
    inputDecorationTheme: const InputDecorationTheme(
        floatingLabelBehavior: FloatingLabelBehavior.auto,
        labelStyle: TextStyle(color: secondaryTextColor),
        iconColor: secondaryTextColor),
    colorScheme: ColorScheme.light(
      primaryFixed: Colors.white,
      primary: primaryColor,
      onSurface: Colors.black,
      onPrimary: Colors.black,
      secondary: primaryColor,
      onSecondary: Colors.white,
    ),
    useMaterial3: true,
  );
  const MyApp({super.key});
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Teaching Assistant',
      theme: themeData,
      home: Stack(
        children: [
          Positioned.fill(child: LoginScreen()),
          // Positioned(left: 0, bottom: 0, right: 0, child: CustomBottomNavigation())
        ],
      ),
    );
  }
}
