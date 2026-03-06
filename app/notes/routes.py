from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import Note
from app.extensions import db

# Define the Blueprint for notes-related routes
notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/', methods=['GET'])
@login_required
def index():
    """
    Fetch all notes belonging to the currently logged-in user
    and render the main index page.
    """
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', notes=notes)


@notes_bp.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    """
    Create a new note for the current user.
    Expects JSON data with a 'content' field.
    """
    data = request.get_json()
    new_note = Note(content=data['content'], author=current_user)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully'}), 201


@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note_put(note_id):
    """
    Completely update a note (Full Update).
    If a field is missing in the request, it defaults to empty/false.
    """
    note = Note.query.get_or_404(note_id)

    # Check if the current user owns this note
    if note.author != current_user:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    note.content = data.get('content', '')
    note.is_important = data.get('is_important', False)

    db.session.commit()
    return jsonify({'message': 'Note completely updated'})


@notes_bp.route('/api/notes/<int:note_id>', methods=['PATCH'])
@login_required
def update_note_patch(note_id):
    """
    Partially update a note.
    Only updates fields provided in the JSON request body.
    """
    note = Note.query.get_or_404(note_id)

    # Check if the current user owns this note
    if note.author != current_user:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()

    # Update only the fields present in the request
    if 'content' in data:
        note.content = data['content']
    if 'is_important' in data:
        note.is_important = data['is_important']

    db.session.commit()
    return jsonify({'message': 'Note partially updated'})


@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """
    Delete a specific note after verifying ownership.
    """
    note = Note.query.get_or_404(note_id)

    # Check if the current user owns this note
    if note.author != current_user:
        return jsonify({'error': 'Unauthorized access'}), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})