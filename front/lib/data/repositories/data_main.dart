// Updated Status enum to include submitted and evaluated
enum Status {
  late,
  completed,
  notStarted,
  inProgress,
  submitted, // Added
  evaluated, // Added
}

class StoryData {
  final int id;
  final String name;
  final String imageFileName;
  final bool isViewed;
  final String iconFileName;

  StoryData({
    required this.iconFileName,
    required this.id,
    required this.name,
    required this.imageFileName,
    required this.isViewed,
  });
}

class Category {
  final int id;
  final String title;
  final String imageFileName;

  Category({
    required this.id,
    required this.title,
    required this.imageFileName,
  });
}

class PostData {
  final int id;
  final String caption;
  final String title;
  final String uploaded;
  final String deadline;
  final bool isBookmarked;
  final String postedBy;
  final Status status;

  PostData({
    required this.status,
    required this.id,
    required this.caption,
    required this.title,
    required this.uploaded,
    required this.deadline,
    required this.isBookmarked,
    required this.postedBy,
  });
}

class AppDatabase {
  static List<StoryData> get stories {
    return [
      StoryData(
        id: 1001,
        name: 'Emilia',
        imageFileName: 'story_1.jpg',
        isViewed: false,
        iconFileName: "category_1.png",
      ),
      StoryData(
        id: 1002,
        name: 'Richard',
        imageFileName: 'story_2.jpg',
        isViewed: false,
        iconFileName: "category_2.png",
      ),
      StoryData(
        id: 1003,
        name: 'Jasmine',
        imageFileName: 'story_3.jpg',
        isViewed: true,
        iconFileName: "category_3.png",
      ),
      StoryData(
        id: 1004,
        name: 'Lucas',
        imageFileName: 'story_4.jpg',
        isViewed: false,
        iconFileName: "category_4.png",
      ),
      StoryData(
        id: 1005,
        name: 'Isabella',
        imageFileName: 'story_5.jpg',
        isViewed: false,
        iconFileName: "category_1.png",
      ),
    ];
  }

  static List<Category> get categories {
    return [
      Category(id: 104, title: 'Data Structure', imageFileName: 'ds.jpg'),
      Category(id: 103, title: 'Network', imageFileName: 'network.jpg'),
      Category(
          id: 105, title: 'Artificial Intelligence', imageFileName: 'ai.jpg'),
      Category(id: 106, title: 'Algorithms', imageFileName: 'algo.jpg'),
      Category(id: 102, title: 'Automata', imageFileName: 'linz.jpg'),
    ];
  }

  static List<PostData> get posts {
    return [
      PostData(
        id: 1,
        status: Status.submitted, // Changed to submitted
        title: 'Algorithm',
        caption: 'Dynamic Programming',
        isBookmarked: false,
        uploaded: '5',
        deadline: '21 May 2024',
        postedBy: 'Reza Tahmasbi',
      ),
      PostData(
        id: 0,
        status: Status.late,
        title: 'Data Structure',
        caption: 'Stack and Queue',
        isBookmarked: false,
        uploaded: '10',
        deadline: '12 Apr 2024',
        postedBy: 'Amir Sabry',
      ),
      PostData(
        id: 2,
        status: Status.evaluated, // Changed to evaluated
        title: 'Network',
        caption: 'Network Protocols',
        isBookmarked: false,
        uploaded: '32',
        deadline: '22 Mar 2024',
        postedBy: 'Erfan Jalali',
      ),
      PostData(
        id: 0,
        status: Status.submitted,
        title: 'ALU Design',
        caption: 'Computer Architecture',
        isBookmarked: false,
        uploaded: '12',
        deadline: '11 Mar 2025',
        postedBy: 'Amir Sabry',
      ),
      PostData(
        id: 2,
        status: Status.evaluated, // Changed to evaluated
        title: 'Network',
        caption: 'Network Protocols',
        isBookmarked: false,
        uploaded: '32',
        deadline: '15 Jan 2025',
        postedBy: 'Reza Tahmasni',
      ),
    ];
  }

  static List<OnboardingItem> get onboardingItems {
    List<OnboardingItem> items = [];
    for (var i = 0; i < 4; i++) {
      items.add(OnboardingItem(
        "Read the article you want instantly",
        "You can read thousands of articles on Blog Club, save them in the application and share them with your loved ones",
      ));
    }
    return items;
  }
}

class OnboardingItem {
  final String title;
  final String description;

  OnboardingItem(this.title, this.description);
}
