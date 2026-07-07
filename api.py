from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from packages.core.core.session import Session
from packages.core.core.agent import Agent

app = Flask(__name__)
CORS(app)

# In-memory store of sessions (for now — resets when server restarts)
sessions = {}
agents = {}


@app.route("/api/create_session", methods=["POST"])
def create_session():
    session_id = str(len(sessions) + 1)
    sessions[session_id] = Session()
    return jsonify({"session_id": session_id})


@app.route("/api/create_agent", methods=["POST"])
def create_agent():
    data = request.json
    name = data["name"]
    system_prompt = data.get("system_prompt", "")
    agents[name] = Agent(name=name, system_prompt=system_prompt)
    return jsonify({"status": "created", "name": name})


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    session_id = data["session_id"]
    agent_name = data["agent_name"]
    message = data["message"]

    session = sessions[session_id]
    agent = agents[agent_name]
    event = agent.generate(message, session)

    return jsonify({
        "id": event.id,
        "agent_name": event.agent_name,
        "content": event.content,
        "parent_id": event.parent_id
    })


@app.route("/api/history/<session_id>", methods=["GET"])
def history(session_id):
    session = sessions[session_id]
    events = session.history()
    return jsonify([
        {
            "id": e.id,
            "agent_name": e.agent_name,
            "content": e.content,
            "parent_id": e.parent_id
        }
        for e in events
    ])


if __name__ == "__main__":
    app.run(debug=True, port=5000)