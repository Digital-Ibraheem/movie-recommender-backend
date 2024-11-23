# ML Movie Recommendation App

(Yes the design is ugly, at least it works :))
https://creative-madeleine-a22059.netlify.app/

Welcome to the **ML Movie Recommendation App**! This project provides personalized movie recommendations using a **collaborative filtering recommendation system**. It’s an efficient and interactive way to explore new movies based on your preferences and those of like-minded users.

**NOTE**: It will likely take about a minute for anything to load due to the free server limitations by Render

---

## 🛠 How It Works

1. **Search for a Movie**  
   Start by typing the title of a movie you’re interested in. Our search algorithm dynamically suggests relevant titles, ensuring a seamless search experience.

2. **Get Tailored Recommendations**  
   Once you select a movie, the app identifies users with similar preferences. It then compiles a list of other movies these users enjoyed, delivering tailored recommendations.

3. **Optimized Data Handling**  
   The original ratings dataset was massive (673MB), which posed challenges for processing and performance. Using Python, I filtered the dataset to include only ratings above 3.5, reducing its size to a more manageable 41MB without sacrificing quality.

---

## 🌟 Features

- **Collaborative Filtering**  
  Recommends movies by analyzing the preferences of similar users.
  
- **Dynamic Search**  
  Instantly suggests movie titles as you type.
  
- **Optimized Performance**  
  Smaller dataset (41MB) enables faster and more responsive recommendations.

---

## 💻 Technologies Used

### Backend  
- **Python**  
  Used for data processing and recommendation logic.  
- **Flask**  
  Powers the API endpoints for search and recommendations.  

### Frontend  
- **React**  
  Ensures a smooth and user-friendly UI experience.

### Libraries & Tools  
- **Pandas, NumPy, scikit-learn**  
  For data preprocessing, similarity calculations, and search functionality.  
- **Axios & CORS**  
  Ensures seamless communication between frontend and backend.

---

## 🚀 Setup Instructions

### Clone the Repository  
```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```
## 🔧 Challenges Faced
### Large Dataset

- The original ratings file was 673MB, which made it impractical for quick processing.
- Using Python, I filtered the dataset to include only ratings above 3.5, reducing its size to 41MB, significantly improving performance.
  
### Frontend-Backend Integration
- Debugging CORS issues and configuring environment variables for API endpoints required careful testing.

