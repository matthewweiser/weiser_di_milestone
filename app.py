from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, show, save
from bokeh.resources import CDN
from bokeh.embed import file_html, components
import Quandl
import os

app = Flask(__name__)

@app.route('/getticker', methods = ['POST'])
def getticker():
    ticker = request.form['ticker']
    print("The ticker id is '" + ticker + "'")
    print "OK TICKER GET IS FINE..."
    #return render_template('/display')
    # query quadl using the stock ticker input, and filter the data to recent history:
    mydata = Quandl.get("WIKI/" + ticker, authtoken="3JBBpsoLx-__-4K8Z-za")
    print "got data..."
    x = mydata.index
    y = mydata['Close'].tolist()   #[6, 7, 2, 4, 5]
    if len(mydata.index) > 1000:
        x = x[ len(x)-1000:len(x) ]   #range(1000)
        y = y[ len(y)-1000:len(y)]

    # output to static HTML file
    print "ready to write html..."
    print x[1:10]
    print y[1:10]

    output_file("/home/vagrant/heroku_test/flask-demo/display.html", title="line plot example")
    # create a new plot with a title and axis labels
    p = figure(title= ticker + " Historical Closing Price", x_axis_label='Date', y_axis_label='Price', x_axis_type="datetime")
    # add a line renderer with legend and line thickness
    p.line(x, y, legend=ticker , line_width=2)
    save(p)
    #script, div = components(p)
    #return render_template('graph.html', script=script, div=div)
    return render_template('stockPricePlot.html')

    #plot = figure()
    #plot.circle([1,2], [3,4])
    #print "trying to use file_html"
    #html = file_html(p, CDN, "my plot")
    #print "trying to use file_html 2"
    #Html_file= open("/home/vagrant/heroku_test/flask-demo/display.html","w")
    #Html_file.write(html)
    #Html_file.close()
    print "redirecting"
    # create plot using bokeh for display in the redirect page:
    return redirect('/display')

@app.route('/display')
def display():
  print "in the display function..."
  #this html is bare bones in line display of the plot generated with the getticker function:
  return render_template('/home/vagrant/heroku_test/flask-demo/display.html')

@app.route('/')
def main():
  #return redirect('/index')
  #return render_template('stockPricePlot.html')
  return render_template('index.html')


if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0')
    #app.run()

