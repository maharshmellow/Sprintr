#!/home/maharshmellow/anaconda3/bin/python3.5
# -*- coding: UTF-8 -*-

import cgitb
import cgi
import hashlib
import mysql.connector
import time

#cgitb.enable()              # TODO remove this line after done

print("Content-Type: text/html;charset=utf-8")
print()

def main():
    form = cgi.FieldStorage()
    email = form.getvalue("b")
    bookName = form.getvalue("a") # hashed email + cow seed
    lastTime= form.getvalue("c")   # lastlogin time

    response = validateParameters(email, bookName, lastTime)
    if response:
        bookData = getBookData(bookName)
        showPage(bookData, 0, email, bookName)
    else:
        print("<script>window.location.replace('https://www.maharsh.net/error')</script>")

    # if all true: load book, get book ending value, set index to that value, and display the output

def validateParameters(email, bookName, lastTime):
    cnx = mysql.connector.connect(user="FILLER_USERNAME", password="FILLER_PASSWORD", host="FILLER_HOST", database="FILLER_DBNAME")
    cursor = cnx.cursor(buffered=True)

    # check if the bookName matches the email
    if hashlib.sha512((email+"cow").encode("utf-8")).hexdigest() != bookName:
        return(False)

    # check if the email and last login match and that the email exits
    query = ("SELECT * FROM users WHERE email=%s AND lastlogin=%s")
    cursor.execute(query, (email, lastTime))
    if cursor.rowcount == 0:
        return(False)

    # check if the user logged-in in the last 5 seconds
    if time.time() - float(lastTime) > 5:
        return(False)

    return(True)

def getBookData(bookName):
    import pickle
    bookFile = open("/var/www/books/"+bookName+".obj", "rb")
    data = pickle.load(bookFile)
    bookFile.close()

    return(data)

def showPage(data, index, email, bookName):

    output = """<!DOCTYPE html>
    <html>
      <head>
        <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css' integrity='sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7' crossorigin='anonymous'>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>

        <title>Sprintr Reader</title>

        <style>
          @font-face {
            font-family: FC;
            src: url('https://www.maharsh.net/reader/fonts/rreg.ttf');
          }
          body{
            background-color: #000021;
          }
          .linemarker{
            max-width: 500px;
            overflow: hiddenn;
          }
          #topLineMarker{
            margin-top: 200px;
          }
          #bottomLineMarker{
            /*margin-top: 100px;*/
          }
          #wordBox{
            color: #dddddd;
            font-family: FC;
            font-size: 60px;
            max-width: 600px
          }
          #wordBox:hover{
            background-color: #000021;
            opacity: 0.5;
            cursor: pointer;
          }
          .center-block {float: none !important}

          .unselectable{
            user-drag: none;
            user-select: none;
            -moz-user-select: none;
            -webkit-user-drag: none;
            -webkit-user-select: none;
            -ms-user-select: none;
          }
          #loginPageLogo{
            width: 120px;
            padding-top: 30px;
            padding-bottom: 30px;
            opacity: 1;
          }
          #pivotchar{
            color: #f5003c;
            font-family: FC;
          }
          #cont {
              width: 600px;
              margin: 0 auto;
          }

          .item {
              width: 600px;
              height: 350px;
              text-align: center;
          }

          .item span {
              font-size: large;
              line-height: 50px;
              padding-left: 30px;
              padding-right: 30px;
          }

          .coloured,
          .coloured a {
              color: #29111E;
          }
          .coloured:hover {
              color: #F5003C;
              cursor: pointer;
          }
          button {
              -webkit-appearance: none;
              outline: none;
              border: 0;
              background: transparent;
          }

        </style>
      </head>
      <body onload='read()'>

        <div id='reader' class='container'>
          <div class='row'>
              <img src='https://www.maharsh.net/reader/logo.png' id='loginPageLogo' class='center-block img-responsive unselectable'></img>
          </div>


          <div class='row'>
            <div class='col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-2'>
              <img class='linemarker center-block unselectable'id='topLineMarker' src='https://www.maharsh.net/reader/Line%20Marker.png' style='height: 4px;'></img>
            </div>
          </div>
          <div class='row'>

            <div class='col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-2 col-xs-12 ' id='wordBox'>
              <span class='center-block text-center unselectable'><span id='leftSubword'></span><span id='pivotchar'></span><span id="rightSubword"></span></span>
            </div>

          </div>
          <div class='row'>

            <div class='col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-2'>
                <img class='linemarker center-block unselectable'id='bottomLineMarker' src='https://www.maharsh.net/reader/Line%20Marker.png' style='height: 4px;'></img>
              </div>

          </div>
          <div class='row' id='cont'>

              <div class='item'>
                  <button id='goBackButton' onclick='goBack();'><span class='glyphicon glyphicon-menu-left coloured'></span></button>
                  <button id='goForwardButton' onclick='goForward();'><span class='glyphicon glyphicon-menu-right coloured'></span></button>

                  <input id='uploadInput' type='file' name='uploadInput' style='display:none;'>
                  <button onclick='upload();'><span class='glyphicon glyphicon-cloud-upload coloured'></span></button>

                  <button id='toggleContrastButton' onclick='toggleContrast();'><span class='glyphicon glyphicon-adjust coloured'></span></button>
                  <button id='slowDownButton' onclick='slowDown();'><span class='glyphicon glyphicon-menu-down coloured'></span></button>
                  <button id='speedUpButton' onclick='speedUp();'><span class='glyphicon glyphicon-menu-up coloured'></span></button>

              </div>

          </div>

        </div>
      </body>

      <script type='text/javascript'>
        var pauseToggle = true;
        var contrast = 1; // start with black background and white text
        var index = 0;
        var wpm = 350;

        function read(){
          console.log('reader start');


          //paste the data here using python
    """

    output += "data = " + str(data) + ";"
    output += """


          var myFunction = function(){
            document.getElementById('leftSubword').innerHTML = data[index][0];
            document.getElementById('pivotchar').innerHTML = data[index][1];
            document.getElementById('rightSubword').innerHTML = data[index][2];
            var timeoutLength = getTimeoutLength(data[index], wpm);
            timeout = setTimeout(myFunction, timeoutLength);

            if (pauseToggle === false){
                index += 1;    // if not paused: increase the index
                if ((index + 1) % 50 == 0){
                    // autosave
                    client = new XMLHttpRequest();
                    client.open('POST', '/cgi-bin/sprintr/autosave.cgi', true);
                    client.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                    var requestString = 'email="""
    output +=  str(email)
    output += """' + '&position=' + index;
                    client.send(requestString);

                }
            }
            else{
                // change text to 'press to play'
                document.getElementById('wordBox').style.color = '#f5003c';
                document.getElementById('leftSubword').innerHTML = 'press to';
                document.getElementById('pivotchar').innerHTML = ' ';
                document.getElementById('rightSubword').innerHTML = 'play';
            }
          }
          var timeout = setTimeout(myFunction, 0);


        }
        function getTimeoutLength(wordData, wpm){
            var length = wordData[3];
            var punctuationID = wordData[4];

            var timeout = (60000/wpm)+(((length * 10000)/wpm - 100));

            if ([1, 2, 3].indexOf(punctuationID) > -1){
                timeout = timeout + 500;
            }
            else if ([4, 5, 6].indexOf(punctuationID) > -1){
                timeout = timeout + (250);
            }

            return(timeout);
        }
        function toggleContrast() {
            if (contrast == 1) {
                // change to white background - dark text
                document.body.style.background = '#F5F5F5';
                document.getElementById('wordBox').style.color = '#26121e';
                document.getElementById('loginPageLogo').src = 'https://www.maharsh.net/reader/logo1.png';
                contrast = 0;

            } else {
                // change to dark background - white text
                // #dddddd, #000021
                document.body.style.background = '#000021';
                document.getElementById('wordBox').style.color = '#dddddd';
                document.getElementById('loginPageLogo').src = 'https://www.maharsh.net/reader/logo.png';
                contrast = 1;


            }
        }

        function slowDown(){
              // decrease the speed by 25 words per minute
              wpm = wpm - 25;
          }

        function speedUp(){
            //increase the speed by 25 words per minute
            wpm = wpm + 25;
        }

        function goBack(){
              // go back by 100 words (or the start if have less than 100 so far)
              if (index >= 100) {
                  index = index - 100;
              }
              else{
                  index = 0;
              }
        }

        function goForward(){
            if (data.length - index <= 100) {
                index = index + (data.length - index);
            }
            else {
                index = index + 100;
            }
        }

        //UPLOAD
        function upload(){
            document.getElementById('uploadInput').click();
        }
        client = new XMLHttpRequest();

        document.getElementById('uploadInput').onchange = function(){
            pauseToggle = true;
            var file = document.getElementById('uploadInput');
            var formData = new FormData();
            formData.append('upload', file.files[0]);"""

    output += "formData.append('email', '" + str(email) + "');"
    output += "formData.append('code', '" + str(bookName) + "');"

    output += """

            client.open('post', 'https://www.maharsh.net/cgi-bin/sprintr/uploadtest.cgi', true);
            client.send(formData);

        }

        client.onreadystatechange = function(){
            if (client.readyState == 4 && client.status == 200) {
                var responseText = client.responseText;

                if (responseText == 1){
                    // success
                    if (confirm('Start Reading New Book?') == true){
                        window.location.replace('https://www.maharsh.net/sprintr/');
                    }
                    // else: do nothing

                }
                else if (responseText == 2){
                    // file error
                    window.alert('File Error');
                }
                else if (responseText == 0){
                    // upload error
                    window.alert('Upload Error');
                }
                else if (responseText == 10){
                    // file too large
                    window.alert('File Too Large (Limit = 1MB)');
                }
                else{
                    window.alert('Server Error');
                }

            }
        }

        //END UPLOAD


        document.getElementById('wordBox').onclick = function() {
            console.log('click');
            if (pauseToggle === false) {
                pauseToggle = true;

                document.getElementById('leftSubword').innerHTML = 'press to';
                document.getElementById('pivotchar').innerHTML = ' ';
                document.getElementById('rightSubword').innerHTML = 'play';
                document.getElementById('wordBox').style.color = '#f5003c';

            } else {
                pauseToggle = false;
                if (contrast == 0) {
                    document.getElementById('wordBox').style.color = '#26121e';
                } else {
                    document.getElementById('wordBox').style.color = '#dddddd';
                }

                document.getElementById('leftSubword').innerHTML = '&nbsp;';
                document.getElementById('pivotchar').innerHTML = '&nbsp;';
                document.getElementById('rightSubword').innerHTML = '&nbsp;';
            }
        }
      </script>
    </html>"""

    print(output.encode("ascii", "ignore").decode("ascii"))

try:
    main()
except:
    print("<script>window.location.replace('https://www.maharsh.net/error.html')</script>")
