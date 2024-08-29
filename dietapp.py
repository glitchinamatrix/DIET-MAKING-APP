from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template for the home page (input form)
index_html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Diet Plan Calculator</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <style>
    body {
      background-image: url('{{ url_for('static', filename='min.jpg') }}');
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center center;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      background: rgba(255, 255, 255, 0.8);
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      max-width: 500px;
    }
    .form-group label {
      font-weight: bold;
    }
    .form-control {
      border-radius: 0;
    }
    .btn-custom {
      background-color: #007bff;
      color: #fff;
      border-radius: 0;
    }
    .btn-custom:hover {
      background-color: #0056b3;
    }
    .logo {
      display: block;
      margin: 0 auto 20px;
      max-width: 100px;  /* Adjust the max-width as needed */
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="form-container text-center">
      <img src="{{ url_for('static', filename='logo.jpeg') }}" class="logo">
      <h2>Diet Plan Calculator</h2>
      <form action="/calculate" method="post">
        <div class="form-group">
          <label for="age">Age:</label>
          <input type="number" id="age" name="age" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="weight">Weight (kg):</label>
          <input type="number" id="weight" name="weight" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="height">Height (cm):</label>
          <input type="number" id="height" name="height" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="gender">Gender:</label>
          <select id="gender" name="gender" class="form-control">
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>
        <div class="form-group">
          <label for="activity_level">Activity Level:</label>
          <select id="activity_level" name="activity_level" class="form-control">
            <option value="sedentary">Sedentary</option>
            <option value="lightly_active">Lightly Active</option>
            <option value="moderately_active">Moderately Active</option>
            <option value="very_active">Very Active</option>
            <option value="extra_active">Extra Active</option>
          </select>
        </div>
        <button type="submit" class="btn btn-custom btn-block">Calculate</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

# HTML template for the summary page
summary_html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Diet Plan Summary</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <style>
    body {
      background-image: url('{{ url_for('static', filename='min.jpg') }}');
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center center;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }
    .container {
      background: rgba(255, 255, 255, 0.8);
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      max-width: 500px;
    }
    .btn-custom {
      background-color: #007bff;
      color: #fff;
      border-radius: 0;
    }
    .btn-custom:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="summary-container text-center">
      <h2>Diet Plan Summary</h2>
      <img src="{{ url_for('static', filename='diet.jpg') }}" class="summary-image" style="max-width: 100%; height: auto; margin-bottom: 20px;">
      <p>Total Daily Calories: <strong>{{ calories }} kcal</strong></p>
      <p>Carbohydrates: <strong>{{ carbs }} g</strong></p>
      <p>Protein: <strong>{{ protein }} g</strong></p>
      <p>Fats: <strong>{{ fats }} g</strong></p>
      <a href="/" class="btn btn-custom btn-block">Calculate Again</a>
    </div>
  </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(index_html)

@app.route('/calculate', methods=['POST'])
def calculate():
    age = int(request.form['age'])
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    activity_level = request.form['activity_level']
    gender = request.form['gender']

    # Harris-Benedict BMR calculation
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # TDEE calculation based on activity level
    activity_factors = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
    tdee = bmr * activity_factors[activity_level]

    # Macronutrient distribution (example percentages)
    carbs = round((0.5 * tdee) / 4)
    protein = round((0.2 * tdee) / 4)
    fats = round((0.3 * tdee) / 9)

    return render_template_string(summary_html, calories=round(tdee), carbs=carbs, protein=protein, fats=fats)

if __name__ == '__main__':
    app.run(debug=True)
