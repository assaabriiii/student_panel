import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:ta_app/data/repositories/data.dart';
import 'package:ta_app/gen/assets.gen.dart';
import 'package:ta_app/main.dart';
import 'package:ta_app/widgets/assignment_list.dart';
import 'package:ta_app/widgets/course_list.dart';
import 'package:ta_app/widgets/story_list.dart';
import '../../widgets/app_header.dart';

class StudentHomeScreen extends StatefulWidget {
  @override
  _StudentHomeScreen createState() => _StudentHomeScreen();
}

class _StudentHomeScreen extends State<StudentHomeScreen> {
  @override
  Widget build(BuildContext context) {
    final TextTheme textTheme = Theme.of(context).textTheme;
    final stories = AppDatabase.stories;
    return Scaffold(
      backgroundColor: Color(0xfff0f0f0),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Column(
            children: [
              AppHeader(textTheme: textTheme),
              SizedBox(
                height: 10,
              ),
              StoryList(stories: stories, themeData: MyApp.themeData),
              SizedBox(
                height: 10,
              ),
              CourseList(),
              AssignemntList(),
              SizedBox(
                height: 5,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
