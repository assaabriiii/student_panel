// import 'package:flutter_bloc/flutter_bloc.dart';
// import '../../data/repositories/auth_repository.dart';

// part 'auth_event.dart';
// part 'auth_state.dart';

// class AuthBloc extends Bloc<AuthEvent, AuthState> {
//   final AuthRepository authRepository;

//   AuthBloc({required this.authRepository}) : super(AuthInitial()) {
//     on<LoginRequested>(_onLoginRequested);
//     on<SignupRequested>(_onSignupRequested);
//   }

//   Future<void> _onLoginRequested(LoginRequested event, Emitter<AuthState> emit) async {
//     emit(AuthLoading());
//     try {
//       final response = await authRepository.login(email: event.email, password: event.password);
//       emit(AuthSuccess(token: response['token'], role: response['role']));
//     } catch (e) {
//       emit(AuthError(message: e.toString()));
//     }
//   }

//   Future<void> _onSignupRequested(SignupRequested event, Emitter<AuthState> emit) async {
//     emit(AuthLoading());
//     try {
//       final response = await authRepository.signup(
//         name: event.name,
//         email: event.email,
//         password: event.password,
//         role: event.role,
//       );
//       emit(AuthSuccess(token: response['token'], role: response['role']));
//     } catch (e) {
//       emit(AuthError(message: e.toString()));
//     }
//   }
// }