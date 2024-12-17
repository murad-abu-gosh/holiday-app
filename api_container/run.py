from app.gemini_api_handler import gemini_app



if __name__ == '__main__':
    gemini_app.run(debug=True, host='0.0.0.0', port=5002)