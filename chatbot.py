import joblib


model = joblib.load("insurance_model.pkl")

def get_user_input():
    print("Welcome to InsuranceBot! I'll help you estimate your medical insurance cost.")
    age = int(input("Enter your age: "))
    sex = input("Enter your sex (male/female): ").lower()
    bmi = float(input("Enter your BMI: "))
    children = int(input("Enter number of children: "))
    smoker = input("Are you a smoker? (yes/no): ").lower()
    region = input("Enter your region (northeast, northwest, southeast, southwest): ").lower()

    
    sex = 1 if sex == "male" else 0
    smoker = 1 if smoker == "yes" else 0
    region_dict = {"northeast": 0, "northwest": 1, "southeast": 2, "southwest": 3}
    region = region_dict.get(region, 0)

    return [[age, sex, bmi, children, smoker, region]]

def main():
    user_data = get_user_input()
    prediction = model.predict(user_data)
    print(f"\nYour estimated insurance cost is: ${prediction[0]:.2f}")

if __name__ == "__main__":
    main()
