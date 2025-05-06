import 'package:flutter/material.dart';

import '../carousel/carousel_slider.dart';
import '../data/repositories/data.dart';

class CourseList extends StatelessWidget {
  const CourseList({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final categories = AppDatabase.categories;
    return CarouselSlider.builder(
      itemCount: categories.length,
      itemBuilder: (context, index, realIndex) {
        return CourseItem(
          left: realIndex == 0 ? 32 : 8,
          right: realIndex == categories.length - 1 ? 32 : 8,
          category: categories[realIndex],
        );
      },
      options: CarouselOptions(
        scrollDirection: Axis.horizontal,
        viewportFraction: 0.8,
        aspectRatio: 1.3,
        scrollPhysics: const BouncingScrollPhysics(),
        initialPage: 0,
        disableCenter: true,
        autoPlay: true,
        enableInfiniteScroll: false,
        enlargeCenterPage: true,
        enlargeStrategy: CenterPageEnlargeStrategy.scale
      ),
    );
  }
}

class CourseItem extends StatelessWidget {
  final Category category;
  final double left;
  final double right;
  const CourseItem(
      {super.key,
      required this.category,
      required this.left,
      required this.right});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.fromLTRB(left, 0, right, 0),
      child: Stack(
        children: [
          Positioned.fill(
              top: 100,
              right: 50,
              left: 50,
              bottom: 16,
              child: Container(
                decoration: const BoxDecoration(boxShadow: [
                  BoxShadow(blurRadius: 20, color: Color(0xaa0D253C))
                ]),
              )),
          Positioned.fill(
            child: Container(
              margin: const EdgeInsets.fromLTRB(0, 0, 0, 16),
              decoration: BoxDecoration(
                color: Colors.blue,
                borderRadius: BorderRadius.circular(32),
              ),
              foregroundDecoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(32),
                  gradient: const LinearGradient(
                    begin: Alignment.bottomCenter,
                    end: Alignment.center,
                    colors: [Color(0xff0D253C), Colors.transparent],
                  )),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(32),
                child: Image.asset("subject_imgs/${category.imageFileName}",
                    fit: BoxFit.cover),
              ),
            ),
          ),
          Positioned(
            bottom: 56,
            left: 32,
            child: Text(category.title,
                style: Theme.of(context)
                    .textTheme
                    .labelMedium!
                    .apply(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}