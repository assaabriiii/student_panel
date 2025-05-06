// import '../services/api_service.dart';

// class AuthRepository {
//   final ApiService apiService;

//   AuthRepository({required this.apiService});

//   Future<Map<String, dynamic>> login({required String email, required String password}) async {
//     final response = await apiService.post(
//       '/login', // Django endpoint
//       data: {'email': email, 'password': password},
//     );
//     return {
//       'token': response['token'], // Adjust based on Django response
//       'role': response['role'], // e.g., 'student', 'ta', 'professor'
//     };
//   }

//   Future<Map<String, dynamic>> signup({
//     required String name,
//     required String email,
//     required String password,
//     required String role,
//   }) async {
//     final response = await apiService.post(
//       '/signup', // Django endpoint
//       data: {
//         'name': name,
//         'email': email,
//         'password': password,
//         'role': role,
//       },
//     );
//     return {
//       'token': response['token'],
//       'role': response['role'],
//     };
//   }
// }