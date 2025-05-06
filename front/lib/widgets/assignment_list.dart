import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:ta_app/data/repositories/data.dart';
import 'package:ta_app/gen/assets.gen.dart';
import 'package:ta_app/main.dart';

class AssignemntList extends StatelessWidget {
  const AssignemntList({super.key});
  @override
  Widget build(BuildContext context) {
    final posts = AppDatabase.posts;
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 16, right: 16),
          child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text("Latest Assignments",
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: Colors.black, fontWeight: FontWeight.w600)),
                IconButton(
                    onPressed: () {},
                    icon: Icon(CupertinoIcons.slider_horizontal_3))
              ]),
        ),
        ListView.builder(
          shrinkWrap: true,
          physics: const ClampingScrollPhysics(),
          itemCount: posts.length,
          itemExtent: 141,
          itemBuilder: (context, index) {
            final post = posts[index];
            return Assignment(post: post);
          },
        ),
        const SizedBox(height: 75),

      ],
    );
  }
}

class Assignment extends StatelessWidget {
  final PostData post;
  const Assignment({
    super.key,
    required this.post,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 149,
      margin: const EdgeInsets.fromLTRB(32, 8, 32, 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [
          BoxShadow(
            color: Color(0x1a5282FF),
            blurRadius: 10,
            offset: Offset(0, 10),
          ),
        ],
      ),
      child: Row(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  post.caption,
                  style: TextStyle(
                      fontFamily: Assets.fonts.instagramSans,
                      fontWeight: FontWeight.w600,
                      fontSize: 14,
                      color: Theme.of(context).colorScheme.primary),
                ),
                const SizedBox(
                  height: 3,
                ),
                Text(post.title,
                    style: TextStyle(
                        fontFamily: Assets.fonts.instagramSans,
                        fontWeight: FontWeight.w400,
                        fontSize: 14)),
                Expanded(
                  child: Text(post.status.name,
                      style: TextStyle(
                        fontFamily: Assets.fonts.instagramSans,
                        fontWeight: FontWeight.w400,
                        fontSize: 12,
                        color: post.status == Status.late
                            ? Colors.red
                            : post.status == Status.submitted
                                ? Colors.blue
                                : post.status == Status.evaluated
                                    ? Colors.green
                                    : Theme.of(context).colorScheme.primary,
                      )),
                ),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Icon(CupertinoIcons.upload_circle,
                        size: 16, color: Theme.of(context).colorScheme.primary),
                    const SizedBox(
                      width: 4,
                    ),
                    Text(post.uploaded,
                        style: TextStyle(
                            fontFamily: Assets.fonts.instagramSans,
                            fontWeight: FontWeight.w400,
                            fontSize: 12)),
                    const SizedBox(
                      width: 16,
                    ),
                    Icon(CupertinoIcons.calendar,
                        size: 16, color: Theme.of(context).colorScheme.primary),
                    const SizedBox(
                      width: 4,
                    ),
                    Text(post.deadline,
                        style: TextStyle(
                            fontFamily: Assets.fonts.instagramSans,
                            fontWeight: FontWeight.w400,
                            fontSize: 12)),
                    const SizedBox(
                      width: 10,
                    ),
                    Text("By: ${post.postedBy}",
                        style: TextStyle(
                            fontFamily: Assets.fonts.instagramSans,
                            fontWeight: FontWeight.w200,
                            fontStyle: FontStyle.italic,
                            color: Colors.black.withOpacity(0.7),
                            fontSize: 12)),
                  ],
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
