from app.db_handler import db_app



if __name__ == '__main__':
    db_app.run(debug=True, host='0.0.0.0', port=5001)