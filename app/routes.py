from flask import Blueprint, request, jsonify, render_template
from app.services.google_sheets_service import GoogleSheetsService
from app.utils.format_utils import format_data
from app.utils.validation_utils import extract_spreadsheet_id

import os


main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def index():
    return render_template('spread.html')


@main_bp.route('/read', methods=['POST'])
def read_entries():
    data = request.json
    spreadsheet_url = data.get('spreadsheet_url')
    spreadsheet_id = extract_spreadsheet_id(spreadsheet_url)

    if not spreadsheet_id:
        return jsonify({'error': 'Invalid Google Spreadsheet URL'}), 400

    google_sheets_service = GoogleSheetsService()
    values = google_sheets_service.read_sheet(spreadsheet_id)

    if not values:
        return jsonify({'message': 'No data found.'})

    headers = values[0]
    data = [dict(zip(headers, row)) for row in values[1:]]
    formatted_data = format_data(data)

    return jsonify({'formatted_data': formatted_data})


@main_bp.route('/manage', methods=['POST'])
def manage_entry():
    data = request.get_json()
    spreadsheet_url = data.get('spreadsheet_url')
    action = data.get('action')
    entry_dict = data.get('entry_dict')

    google_sheets_service = GoogleSheetsService(spreadsheet_url)

    if action == 'add':
        google_sheets_service.add_entry(entry_dict)
        return jsonify({'message': 'Entry added successfully.'})

    elif action == 'update':
        match_dict = entry_dict.get('match_dict')
        update_dict = entry_dict.get('update_dict')

        if not match_dict or not update_dict:
            return jsonify({'error': 'Both match_dict and update_dict are required for update action.'})

        result = google_sheets_service.update_entry(match_dict, update_dict)
        return jsonify(result)

    elif action == 'delete':
        result = google_sheets_service.delete_entry(entry_dict)
        return jsonify(result)

    return jsonify({'error': 'Invalid action.'})
