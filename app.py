import os
import time
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

# Check required environment variables
required_vars = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "ASSISTANT_ID"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"WARNING: Missing environment variables: {', '.join(missing_vars)}")

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
)

ASSISTANT_ID = os.getenv("ASSISTANT_ID")


#  Chat function
def run_assistant(user_input: str) -> str:
    try:
        # Create thread once
        if "thread_id" not in session:
            thread = client.beta.threads.create()
            session["thread_id"] = thread.id

        thread_id = session["thread_id"]

        # Add user message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for completion
        start_time = time.time()
        while run.status in ["queued", "in_progress"]:
            if time.time() - start_time > 60:  # 1 min timeout
                return "Error: Request timed out."
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

        if run.status == "completed":
            # Get latest assistant response
            messages = client.beta.threads.messages.list(
                thread_id=thread_id, limit=1
            )
            
            for msg in messages.data:
                if msg.role == "assistant":
                    for c in msg.content:
                        if c.type == "text":
                            return c.text.value
            return "No response."
            
        elif run.status == "failed":
            return f"Error: Run failed - {run.last_error}"
        elif run.status == "requires_action":
            return "Error: Assistant tried to run a tool (not implemented)."
        else:
            return f"Error: Run status {run.status}"

    except Exception as e:
        return f"Error: {str(e)}"


#  Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    reply = run_assistant(user_input)
    return jsonify({"reply": reply})


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "GET":
        try:
            assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
            return jsonify({
                "instructions": assistant.instructions,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == "POST":
        data = request.json
        new_instructions = data.get("instructions")
        
        try:
            client.beta.assistants.update(
                ASSISTANT_ID,
                instructions=new_instructions
            )
            return jsonify({"status": "updated"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/reset")
def reset():
    session.pop("thread_id", None)
    return jsonify({"status": "reset"})


# if __name__ == "__main__":
#     app.run(debug=True)     


# uncomment above to run locally, but for Azure deployment we use gunicorn with the command:
# gunicorn app:app --workers 3 --timeout 120 --bind 0.0.0.0:5000