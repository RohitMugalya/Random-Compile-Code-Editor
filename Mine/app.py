from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Initialize shuffled line numbers mapping
line_mapping = {}

def generate_shuffled_mapping(num_lines):
    """Generate a shuffled mapping for line numbers."""
    lines = list(range(1, num_lines + 1))
    shuffled_lines = lines.copy()
    random.shuffle(shuffled_lines)
    return dict(zip(lines, shuffled_lines))

@app.route('/')
def index():
    global line_mapping
    # Generate a mapping for 20 lines (can be adjusted)
    line_mapping = generate_shuffled_mapping(20)
    return render_template('index.html', line_mapping=line_mapping)

@app.route('/submit', methods=['POST'])
def submit():
    global line_mapping
    # Get the submitted code
    code = request.form['code']
    # Split code into lines
    lines = code.split('\n')
    # Reorder lines using the mapping
    reordered_lines = [None] * len(lines)
    for original_line_num, shuffled_line_num in line_mapping.items():
        if shuffled_line_num <= len(lines):
            reordered_lines[original_line_num - 1] = lines[shuffled_line_num - 1]
    # Join lines and print
    reordered_code = '\n'.join(reordered_lines)
    print("Reordered Code:\n", reordered_code)
    return jsonify({"message": "Code submitted and reordered successfully!"})

if __name__ == '__main__':
    app.run(debug=True)