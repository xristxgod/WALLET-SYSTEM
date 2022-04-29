from src import init_app

if __name__ == '__main__':
    init_app().run(debug=True, host='0.0.0.0', port=8000)