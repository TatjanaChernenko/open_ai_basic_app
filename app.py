import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": generate_prompt(animal),
                }
            ],
            model="gpt-3.5-turbo",
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return f"""Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {animal.capitalize()}
Names:"""


if __name__ == "__main__":
    app.run(debug=True)
