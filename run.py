from app import app

if __name__ == '__main__':
    app.run(debug=True, port='8080', host='0.0.0.0')
    #app.run(ssl_context='adhoc')
    #app.run(ssl_context=('.ssl/cert.pem', '.ssl/privkey.pem'), debug=True)
    #app.run(ssl_context=('.ssl/cert.pem', '.ssl/privkey.pem'), host='0.0.0.0', port=5000, debug=True)
