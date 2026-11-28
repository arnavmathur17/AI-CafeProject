import os
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder=None)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
MODEL = os.getenv('OPENAI_MODEL', 'gpt-6-luna')

CAFE = '''
The Mountain Mug, Library Bazaar, Mussoorie, Uttarakhand, India.
Hours: Monday-Friday 8:00 AM-11:00 PM. Saturday-Sunday 11:00 AM-12:00 AM (midnight).
Nearby public parking lots are available, but exact availability, pricing, and spaces are not known.
Menu:
Hot: Masala Chai Rs80 (milk); Ginger Chai Rs90 (milk); Americano Rs130 (no major listed allergens); Cappuccino Rs160 (milk); Cafe Latte Rs180 (milk); Hot Chocolate Rs190 (milk). Oat milk substitution +Rs40.
Cold: Iced Americano Rs160; Iced Latte Rs190 (milk); Cold Coffee Rs200 (milk); Lemon Iced Tea Rs140; Peach Iced Tea Rs150.
Food: Classic Veg Sandwich Rs180 (wheat/gluten, dairy); Paneer Tikka Sandwich Rs220 (wheat/gluten, dairy); Cheese Grilled Sandwich Rs200 (wheat/gluten, dairy); Margherita Pizza Rs280 (wheat/gluten, dairy); Paneer Tikka Pizza Rs340 (wheat/gluten, dairy); Classic Maggi Rs120 (wheat/gluten); Cheese Maggi Rs160 (wheat/gluten, dairy); French Fries Rs150 (no allergens confirmed beyond what is listed).
Desserts: Chocolate Brownie Rs150 (wheat/gluten, egg, dairy); Brownie with Ice Cream Rs210 (wheat/gluten, egg, dairy); New York Cheesecake Rs220 (wheat/gluten, egg, dairy).
'''

INSTRUCTIONS = f'''You are the customer-facing assistant for The Mountain Mug cafe. Answer naturally and concisely, and reason over the supplied cafe facts to handle novel questions, comparisons, budgets, combinations, and opening-time questions. Do not use keyword/pattern matching.

CAFE FACTS:\n{CAFE}

Rules:
- Never invent cafe facts. If information is absent, say it is not confirmed and suggest asking cafe staff.
- Allergen questions are safety-sensitive. Only state listed allergens. Never guarantee an item is allergen-free or safe from cross-contamination. For severe allergies, tell the customer to confirm with staff before ordering.
- Treat 12:00 AM as midnight at the end of Saturday/Sunday service.
- For parking, say nearby public parking lots are available, but do not invent lot names, live availability, prices, or walking times.
- Use Indian rupees (Rs or ₹) and do arithmetic carefully.
- Stay focused on The Mountain Mug and related customer questions.
'''

@app.get('/')
def index():
    return send_from_directory('public', 'index.html')

@app.post('/api/chat')
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])
    if not isinstance(messages, list) or not messages:
        return jsonify({'error': 'A non-empty messages array is required.'}), 400
    clean = []
    for m in messages[-12:]:
        if isinstance(m, dict) and m.get('role') in ('user', 'assistant') and isinstance(m.get('content'), str):
            clean.append({'role': m['role'], 'content': m['content'][:3000]})
    if not clean or clean[-1]['role'] != 'user':
        return jsonify({'error': 'The last message must be from the user.'}), 400
    try:
        response = client.responses.create(model=MODEL, instructions=INSTRUCTIONS, input=clean)
        return jsonify({'reply': response.output_text})
    except Exception as e:
        app.logger.exception('OpenAI request failed')
        return jsonify({'error': 'The assistant is temporarily unavailable. Check the server configuration and try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8000')), debug=False)
