import tkinter as tk
import requests
from tkinter import messagebox

class WeatherFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')

        self.api_key = 'your_openweathermap_api_key'  # Replace with your real API key
        self.city_var = tk.StringVar()

        tk.Label(self, text="Enter City:", bg='white', font=("Segoe UI", 12)).pack(pady=(20, 5))
        self.city_entry = tk.Entry(self, textvariable=self.city_var, font=("Segoe UI", 12), width=25)
        self.city_entry.pack(pady=5)

        self.fetch_btn = tk.Button(self, text="Get Weather ☁️", command=self.get_weather)
        self.fetch_btn.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Segoe UI", 12), bg='white', justify='center')
        self.result_label.pack(pady=20)

    def get_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Missing Input", "Please enter a city name.")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('cod') != 200:
                raise ValueError(data.get('message'))

            temp = data['main']['temp']
            desc = data['weather'][0]['description'].title()
            humidity = data['main']['humidity']
            wind = data['wind']['speed']

            result = f"City: {city.title()}\nTemp: {temp}°C\nWeather: {desc}\nHumidity: {humidity}%\nWind: {wind} m/s"
            self.result_label.config(text=result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve weather: {e}")
