from flask import Flask, render_template, request, jsonify, session
from agents.tutor_agent import TutorAgent
from agents.biology_agent import BiologyAgent
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize agents
tutor = TutorAgent()
biology_agent = BiologyAgent(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/')
def home():
    # Initialize session variables if they don't exist
    if 'conversations' not in session:
        session['conversations'] = []
    # Return conversations in reverse order (latest first)
    return render_template('index.html', conversations=session['conversations'][::-1])

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Please enter a valid question.'}), 400

    # Subject keyword sets
    biology_keywords = {
        'cell', 'dna', 'rna', 'mitosis', 'meiosis', 'photosynthesis',
        'respiration', 'ecosystem', 'biome', 'enzyme', 'protein',
        'evolution', 'taxonomy', 'genetics', 'chromosome', 'mutation'
    }
    physics_keywords = {
        'force', 'energy', 'motion', 'velocity', 'acceleration', 'gravity',
        'newton', 'thermodynamics', 'optics', 'wave', 'quantum', 'relativity',
        'electric', 'magnetic', 'current', 'voltage', 'resistance', 'power', 'work'
    }
    math_keywords = {
        'algebra', 'geometry', 'calculus', 'equation', 'function', 'integral',
        'derivative', 'matrix', 'vector', 'probability', 'statistics', 'theorem',
        'number', 'polynomial', 'trigonometry', 'logarithm', 'limit', 'series'
    }
    chemistry_keywords = {
        'atom', 'molecule', 'reaction', 'acid', 'base', 'salt', 'organic',
        'inorganic', 'bond', 'element', 'compound', 'periodic', 'catalyst',
        'oxidation', 'reduction', 'stoichiometry', 'solution', 'ion', 'electron'
    }

    # Detect subject
    lower_query = query.lower()
    if any(word in lower_query for word in biology_keywords):
        subject = 'Biology'
        answer = biology_agent.process_question(query)
    elif any(word in lower_query for word in physics_keywords):
        subject = 'Physics'
        answer = tutor.handle_query(query)
    elif any(word in lower_query for word in math_keywords):
        subject = 'Math'
        answer = tutor.handle_query(query)
    elif any(word in lower_query for word in chemistry_keywords):
        subject = 'Chemistry'
        answer = tutor.handle_query(query)
    else:
        subject = 'Other'
        answer = tutor.handle_query(query)

    # Store conversation in session
    conversations = session.get('conversations', [])
    conversations.append({
        'id': len(conversations),
        'query': query,
        'answer': answer,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'subject': subject
    })
    session['conversations'] = conversations
    # Return conversations in reverse order (latest first)
    return jsonify({
        'answer': answer,
        'conversations': conversations[::-1]
    })

@app.route('/edit', methods=['POST'])
def edit_question():
    data = request.json
    question_id = data.get('id')
    new_query = data.get('query', '').strip()
    
    if not new_query:
        return jsonify({'error': 'Please enter a valid question.'}), 400
    
    conversations = session.get('conversations', [])
    if 0 <= question_id < len(conversations):
        # Determine if it's a biology question
        biology_keywords = {
            'cell', 'dna', 'rna', 'mitosis', 'meiosis', 'photosynthesis',
            'respiration', 'ecosystem', 'biome', 'enzyme', 'protein',
            'evolution', 'taxonomy', 'genetics', 'chromosome', 'mutation'
        }
        
        is_biology = any(keyword in new_query.lower() for keyword in biology_keywords)
        
        # Get new answer from appropriate agent
        if is_biology:
            answer = biology_agent.process_question(new_query)
        else:
            answer = tutor.handle_query(new_query)
            
        conversations[question_id].update({
            'query': new_query,
            'answer': answer,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'subject': 'Biology' if is_biology else 'Other'
        })
        session['conversations'] = conversations
        return jsonify({
            'answer': answer,
            'conversations': conversations[::-1]  # Return in reverse order
        })
    
    return jsonify({'error': 'Invalid question ID.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
