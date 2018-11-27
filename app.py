from flask import *
import pdfkit, os, uuid

app = Flask(__name__)

Download_PATH = 'wkhtmltopdf/bin/wkhtmltopdf.exe'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Download_FOLDER = os.path.join(APP_ROOT, Download_PATH)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route("/api/wkhtmltopdf_url", methods=['POST'])
def wkhtmltopdfurl():
    url = request.form['URL']
    try:
        filename = str(uuid.uuid4()) + '.pdf'
        config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
        pdfkit.from_url(url, filename, configuration=config)
        pdfDownload = open(filename, 'rb').read()
        os.remove(filename)
        return Response(
            pdfDownload,
            mimetype="application/pdf",
            headers={
                "Content-disposition": "attachment; filename=" + filename,
                "Content-type": "application/force-download"
            }
        )
    except ValueError:
        print("Oops! ")


@app.route("/api/wkhtmltopdf_template", methods=['POST'])
def wkhtmltopdf_template():
    filename = str(uuid.uuid4()) + '.pdf'
    config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
    body = '''
    <!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Title of the document</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

<body>
 <div class="panel panel-primary">
        <div class="panel-body">
          <div class="row" style="border:1px solid lightgrey;margin:10px ">
            <div class="col-md-4" style="padding:10px;">
            <h1 align="center" style="color:#216CEC;border-bottom:1px solid grey">konnect 247</h1>
            <br>
              <p><b> Dear Customer,</b></p>
              <p style="margin-left:100px">Thank you for Choosing our Hotel, It is our pleasure to confirm your reservation as follows. </p>
              <table style="width:700px">
              <tr style="height:10">
              <td style="width:350px;"><p style="line-height:0.7 ">Arrival</p></td>
              <td style="width:350px;"><p style="float:center">Guest Name:</p></td>
              </tr>
              
              <tr style="height:10"
              <td style="width:350px;"><p style="line-height:0.7">"""+str(d[0]['customer_arrival_date'])+"""</p></td>
              <td style="width:350px;"><p >"""+str(d[0]['customer_name'])+"""</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Departure</p></td>
              <td style="width:350px"><p>Preferred Language</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_depature_date'])+"""</p></td>
              <td style="width:350px"><p >"""+str(d[0]['ivr_language'])+"""</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Hotel Name:</p></td>
              <td style="width:350px"><p >Channel</p></td>
              </tr>

              <tr>
              <td style="line-height:0.7;width:350px"><p >"""+str(d[0]['hotel_name'])+"""</p></td>
              <td style="width:350px"><p>"""+d[0]['channel']+"""</p></td>
              </tr>
              
              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Total Adult</p></td>
              <td style="width:350px"><p >Confirmation Number</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_adult'])+"""</p></td>
              <td style="width:350px"><p >"""+d[0]['customer_confirmation_number']+"""</p></td>
              </tr>
        
              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Total Child</p></td>
              <td style="width:350px"><p > Booked On</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_child'])+"""</p></td>
              <td style="width:350px"><p >"""+booked_on+"""</p></td>
              </tr>   
              
              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Total Price</p></td>
              <td style="width:350px"><p > No Of Rooms</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_amount'])+"""</p></td>
              <td style="width:350px"><p >"""+str(d[0]['customer_no_of_rooms'])+"""</p></td>
              </tr>
            </table>
                <hr>
                <p style="line-height:0.7">Room Type</p>
                <p style="line-height:0.7">"""+d[0]['customer_room_type']+"""</p> 
             
                <p style="line-height:0.7;padding-top:10px;">Guest Name</p>
                <p style="line-height:0.7">"""+str(d[0]['customer_name'])+""" </p>  
               
                <p style="line-height:0.7;padding-top:10px;">Max Guest</p>
                <p style="line-height:0.7">"""+str(d[0]['customer_adult']+d[0]['customer_child'])+"""</p>
                
                <p style="line-height:0.7;padding-top:10px;">Room Options</p>
               
               <p style="float:left">   <img src="https://www.riversidehotel.com.au/wp-content/uploads/2016/01/RH-12.jpg" alt="" width="400px" height="250px"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
               <span style="float:left;"> <table style=" border:1px solid gray; width:400px;height:250px">
                     <tbody style="border:1px solid gray">
                     """+t_body+"""
                     </tbody>
                   </table>
                   </span>
                </p> 
                 <br>
                 <p><b>Address:</b></p>
                 <p style="margin-left:30px;line-height:0.7"> No,25, 1st cross street,</p>
                 <p style="margin-left:30px;line-height:0.7"> New Colony,</p>
                 <p style="margin-left:30px;line-height:0.7"> Chrompet,</p>
                 <p style="margin-left:30px;line-height:0.7"> Chennai</p>
                 <h3>Regards,</h3>
                 <p>Admin- Hotel Management</p>
                 <hr>
                 <h5 align="center" style="color:red"> This is an Auto generated Email, Please do not reply.</h5> 
                 
              </div>
          
		    
            <br>
          </div>
        
        </div>
      </div>
            
</body>

</html>
     '''
    options = {
        'encoding': 'UTF-8'
    }
    pdfkit.from_string(body, filename, configuration=config, options=options)
    pdfDownload = open(filename, 'rb').read()
    os.remove(filename)
    return Response(
        pdfDownload,
        mimetype="application/pdf",
        headers={
            "Content-disposition": "attachment; filename=" + filename,
            "Content-type": "application/force-download"
        }
    )
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug='True')
