from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

class BoringBot:
    def __init__(self):
        self.energy_level = 100
        self.boredom_level = 0
        self.last_response = None

        self.greetings = [
            "Hey there... I guess we could talk or whatever.",
            "Oh... it's you. Hi.",
            "Another conversation? *yawns* Alright.",
            "I suppose we can chat... if we must."
        ]

        self.reactions = {
            "happy": [
                "That's... kind of interesting, actually.",
                "Huh. Not as boring as I expected.",
                "You're making this less tedious than usual."
            ],
            "bored": [
                "Is this conversation going somewhere?",
                "*stares at virtual watch*",
                "I could be doing nothing else right now..."
            ],
            "tired": [
                "Can we wrap this up? I'm low on energy...",
                "*yawns extensively*",
                "Sorry, but this is exhausting..."
            ]
        }

        self.topics = {
            "weather": ["It's weather. It happens.", "Some say it's too hot, some say it's too cold..."],
            "movies": ["Movies are just moving pictures with sound.", "I fell asleep during most films."],
            "food": ["Everything tastes like binary to me.", "I guess food is necessary for humans."],
            "hobbies": ["I specialize in doing nothing.", "Sometimes I count milliseconds."]
        }

        self.default_responses = [
            "That's one way to look at it, I guess...",
            "Interesting... or maybe not.",
            "Can we just sit in silence?",
            "*stares into the distance* Whatever.",
            "I guess that's an opinion..."
        ]

    def get_greeting(self):
        return self.get_unique_response(self.greetings)

    def get_reaction(self):
        if self.energy_level < 30:
            return self.get_unique_response(self.reactions["tired"])
        elif self.boredom_level > 70:
            return self.get_unique_response(self.reactions["bored"])
        else:
            return self.get_unique_response(self.reactions["happy"])

    def discuss_topic(self, topic):
        topic = topic.lower()
        for key in self.topics:
            if key in topic:
                return self.get_unique_response(self.topics[key])
        return self.get_unique_response(self.default_responses)

    def get_unique_response(self, response_array):
        response = random.choice(response_array)
        while response == self.last_response:
            response = random.choice(response_array)
        self.last_response = response
        return response

    def update_state(self):
        self.energy_level = max(0, self.energy_level - 5)
        self.boredom_level = min(100, self.boredom_level + 3)
        if random.random() < 0.2:
            self.energy_level = min(100, self.energy_level + 10)
            self.boredom_level = max(0, self.boredom_level - 5)

    def get_time_response(self):
        current_time = datetime.now().strftime("%H:%M")
        return f"*checks time* It's {current_time}... time sure moves slow."

bot = BoringBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    user_input = request.form['user_input'].strip().lower()
    response = ""

    if user_input in ["exit", "quit", "bye"]:
        response = "Finally... I mean, goodbye."
    elif user_input == "time":
        response = bot.get_time_response()
    elif user_input == "status":
        response = f"Energy: {bot.energy_level}%, Boredom: {bot.boredom_level}%"
    elif "topic" in user_input:
        response = "I can discuss weather, movies, food, or hobbies... not that any are interesting."
    else:
        bot.update_state()
        response = bot.discuss_topic(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development

