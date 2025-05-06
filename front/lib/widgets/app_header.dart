import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class AppHeader extends StatelessWidget {
  const AppHeader({
    super.key,
    required this.textTheme,
  });

  final TextTheme textTheme;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 16, right: 16),
      child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text("Teaching Assistant",
                style: textTheme.titleSmall?.copyWith(
                  color: Colors.black,
                )),
            IconButton(
                onPressed: () {}, icon: Icon(CupertinoIcons.envelope))
          ]),
    );
  }
}