import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:ta_app/gen/assets.gen.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  static const int loginTab = 0;
  static const int signUpTab = 1;
  int selectedTabIndex = loginTab;
  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final tabTextStyle = TextStyle(
      color: themeData.colorScheme.onPrimary,
      fontSize: 18,
      fontWeight: FontWeight.bold,
    );
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Padding(padding: const EdgeInsets.only(top: 32, bottom: 32)),
            Image.asset(
              'assets/Shahrood-University-of-Technology-Logo.png',
              height: 120,
              fit: BoxFit.contain,
            ),
            SizedBox(
              height: 16,
            ),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(32),
                    topRight: Radius.circular(32),
                  ),
                  color: themeData.colorScheme.primary,
                ),
                child: Column(
                  children: [
                    SizedBox(
                      height: 60,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          TextButton(
                              onPressed: () {
                                setState(() {
                                  selectedTabIndex = loginTab;
                                });
                              },
                              child: Text("Login".toUpperCase(),
                                  style: tabTextStyle.apply(
                                      color: selectedTabIndex == loginTab
                                          ? Colors.white
                                          : Colors.white54))),
                          TextButton(
                              onPressed: () {
                                setState(() {
                                  selectedTabIndex = signUpTab;
                                });
                              },
                              child: Text("Sign up".toUpperCase(),
                                  style: tabTextStyle.apply(
                                      color: selectedTabIndex == signUpTab
                                          ? Colors.white
                                          : Colors.white54))),
                        ],
                      ),
                    ),
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: const BorderRadius.only(
                              topRight: Radius.circular(32),
                              topLeft: Radius.circular(32)),
                          color: themeData.colorScheme.surface,
                        ),
                        child: SingleChildScrollView(
                          child: Padding(
                            padding: const EdgeInsets.fromLTRB(32, 48, 32, 32),
                            child: selectedTabIndex == loginTab
                                ? _Login(themeData: themeData)
                                : _SignUp(themeData: themeData),
                          ),
                        ),
                      ),
                    )
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}

class _Login extends StatelessWidget {
  const _Login({
    super.key,
    required this.themeData,
  });

  final ThemeData themeData;

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      // SizedBox(height: 32,),
      Text(
        "Welcome back",
        style: themeData.textTheme.labelMedium!.apply(fontWeightDelta: 1),
      ),
      const SizedBox(
        height: 8,
      ),
      Text("Sign in with your account",
          style:
              themeData.textTheme.headlineMedium!.apply(fontSizeFactor: 0.7)),
      const SizedBox(
        height: 16,
      ),
      const TextField(
        decoration: InputDecoration(
            label: Text(
          "Username",
        )),
      ),
      const PasswordTextField(),
      const SizedBox(
        height: 24,
      ),
      ElevatedButton(
        style: ButtonStyle(
            minimumSize: MaterialStateProperty.all(
              Size(MediaQuery.of(context).size.width, 60),
            ),
            shape: MaterialStateProperty.all(RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12)))),
        onPressed: () {},
        child: Text("Login".toUpperCase()),
      ),
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text("Forget your password?"),
          const SizedBox(
            width: 8,
          ),
          TextButton(
            onPressed: () {},
            child: const Text("Reset here"),
          ),
        ],
      ),
      const SizedBox(
        height: 16,
      ),
      const Center(
          child: Text("OR SIGN IN WITH", style: TextStyle(letterSpacing: 2))),
      const SizedBox(
        height: 16,
      ),
      // Row(mainAxisAlignment: MainAxisAlignment.center, children: [
      //   Assets.img.icons.google.image(width: 36, height: 36),
      //   const SizedBox(
      //     width: 24,
      //   ),
      //   Assets.img.icons.facebook.image(width: 36, height: 36),
      //   const SizedBox(
      //     width: 24,
      //   ),
      //   Assets.img.icons.twitter.image(width: 36, height: 36),
      //   const SizedBox(
      //     width: 24,
      //   ),
      // ])
    ]);
  }
}

class _SignUp extends StatelessWidget {
  const _SignUp({
    super.key,
    required this.themeData,
  });

  final ThemeData themeData;

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      // SizedBox(height: 32,),
      Text(
        "Welcome to blog club",
        style: themeData.textTheme.labelMedium!.apply(fontWeightDelta: 1),
      ),
      const SizedBox(
        height: 8,
      ),
      Text("Please enter your information",
          style:
              themeData.textTheme.headlineMedium!.apply(fontSizeFactor: 0.7)),
      const SizedBox(
        height: 16,
      ),
      const TextField(
        decoration: InputDecoration(
            label: Text(
          "Fullname",
        )),
      ),
      const TextField(
        decoration: InputDecoration(
            label: Text(
          "Username",
        )),
      ),
      const PasswordTextField(),
      const SizedBox(
        height: 24,
      ),
      ElevatedButton(
        style: ButtonStyle(
            minimumSize: MaterialStateProperty.all(
              Size(MediaQuery.of(context).size.width, 60),
            ),
            shape: MaterialStateProperty.all(RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12)))),
        onPressed: () {},
        child: Text("Sign up".toUpperCase()),
      ),

      const SizedBox(
        height: 16,
      ),
      const Center(
          child: Text("OR SIGN UP WITH", style: TextStyle(letterSpacing: 2))),
      const SizedBox(
        height: 16,
      ),
      // Row(mainAxisAlignment: MainAxisAlignment.center, children: [
      //   Assets.img.icons.google.image(width: 36, height: 36),
      //   const SizedBox(
      //     width: 24,
      //   ),
      //   Assets.img.icons.facebook.image(width: 36, height: 36),
      //   const SizedBox(
      //     width: 24,
      //   ),
      //   Assets.img.icons.twitter.image(width: 36, height: 36),
      //   const SizedBox(
      //     width: 24,
      //   ),
      // ])
    ]);
  }
}

class PasswordTextField extends StatefulWidget {
  const PasswordTextField({
    super.key,
  });

  @override
  State<PasswordTextField> createState() => _PasswordTextFieldState();
}

class _PasswordTextFieldState extends State<PasswordTextField> {
  bool obscureText = true;
  @override
  Widget build(BuildContext context) {
    return TextField(
      obscureText: obscureText,
      enableSuggestions: false,
      autocorrect: false,
      decoration: InputDecoration(
          label: const Text(
            "Password",
          ),
          suffix: InkWell(
              onTap: () {
                setState(() {
                  obscureText = !obscureText;
                });
              },
              child: Text(
                obscureText ? "show" : "Hide",
                style: TextStyle(
                    fontSize: 14, color: Theme.of(context).colorScheme.primary),
              ))),
    );
  }
}
