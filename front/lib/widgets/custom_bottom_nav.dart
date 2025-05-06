
import 'package:flutter/material.dart';

class CustomBottomNavigation extends StatelessWidget {
  const CustomBottomNavigation({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 90,
      child: Stack(
        children: [
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: Container(
              height: 70,
              decoration: BoxDecoration(
                color: Colors.white,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  ButtonNavifationItem(
                    iconFileName: "Home.png",
                    title: "Home",
                    activeIonFileName: "Home.png",
                  ),
                  ButtonNavifationItem(
                    iconFileName: "Articles.png",
                    title: "Article",
                    activeIonFileName: "Articles.png",
                  ),
                  ButtonNavifationItem(
                    iconFileName: "Search.png",
                    title: "Search",
                    activeIonFileName: "Search.png",
                  ),
                  ButtonNavifationItem(
                    iconFileName: "Menu.png",
                    title: "Menu",
                    activeIonFileName: "Menu.png",
                  ),
                ],
              ),
            ),
          ),
          // Center(
          //   child: Container(
          //     width: 75,
          //     height: 75,
          //     alignment: Alignment.topCenter,
          //     child: Container(
          //       // height: 55,
          //       decoration: BoxDecoration(
          //         borderRadius: BorderRadius.circular(32),
          //         color: Theme.of(context).primaryColor,
          //       ),
          //       child: IconButton(
          //         onPressed: () {},
          //         icon: Icon(CupertinoIcons.add),
          //         color: Colors.white,
          //       ),
          //     ),
          //   ),
          // )
        ],
      ),
    );
  }
}

class ButtonNavifationItem extends StatelessWidget {
  final String iconFileName;
  final String title;
  final String activeIonFileName;

  const ButtonNavifationItem(
      {super.key,
      required this.iconFileName,
      required this.title,
      required this.activeIonFileName});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Image.asset("/icons/$iconFileName",
            width: 24, height: 24, color: Theme.of(context).primaryColor),
        const SizedBox(height: 5),
        Text(title, style: Theme.of(context).textTheme.bodySmall,)
      ],
    );
  }
}
