# API Documentation

## Endpoints

### 1. University Number Login
- **URL:** `/login/`
- **Method:** POST
- **Description:** Authenticates a user using their university number and returns a token.
- **Request Body:**
  - `university_number`: string
- **Response:**
  - `id`: integer
  - `username`: string
  - `university_number`: string
  - `email`: string
  - `token`: string

### 2. Dashboard
- **URL:** `/dashboard/`
- **Method:** GET
- **Description:** Retrieves the user's subjects, feedback items, and recent exercises.
- **Authentication:** Required
- **Response:**
  - `subjects`: List of subjects
  - `feedback_items`: List of feedback items
  - `recent_exercises`: List of recent exercises

### 3. TA Dashboard
- **URL:** `/ta_dashboard/`
- **Method:** GET
- **Description:** Provides TA-specific dashboard information.
- **Authentication:** Required
- **Response:**
  - `ta_subjects`: List of TA subjects
  - `exercises`: List of exercises

### 4. Mark Attendance
- **URL:** `/mark_attendance/`
- **Method:** POST
- **Description:** Allows TAs to mark attendance for their subjects.
- **Authentication:** Required
- **Request Body:**
  - `subject_id`: integer
  - `attendance`: List of attendance records
- **Response:**
  - `detail`: Confirmation message