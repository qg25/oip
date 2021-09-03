
from rpiToArduino import rpi2Arduino
from flask import Flask, render_template, jsonify
import threading


FULL_CYCLE = "FC"
HALF_CYCLE = "HC"
STAIN_CHECK = "SC"
DRY_CHECK = "DC"
DRY_CHECK2 = "DC2"

WASHING = 1
DRYING = 2
STERILIZING = 3
JOB_SELECTED = ""
isDry = False

app = Flask(__name__)


class flaskApp:
    def __init__(self):
        @app.route('/')
        def index():
            global JOB_SELECTED
            JOB_SELECTED = ""
            
            return render_template("index.html")


        @app.route('/wash_syringes')
        def wash_syringes():
            global JOB_SELECTED
            JOB_SELECTED = FULL_CYCLE
            
            return render_template('washSyringe.html')


        @app.route('/dry_syringes')
        def dry_syringes():
            global JOB_SELECTED
            if not JOB_SELECTED:
                JOB_SELECTED = HALF_CYCLE
                
            return render_template('drySyringe.html')


        @app.route('/sterilize_syringes')
        def sterilize_syringes():
            return render_template('sterilizeSyringe.html')


        @app.route('/check_stains')
        def check_stains():
            return_value = comms.communications(STAIN_CHECK)
            return jsonify(result=return_value)


        @app.route('/check_wetness')
        def check_wetness():
            global isDry
            if not isDry:
                return_value = comms.communications(DRY_CHECK)
                isDry = True
            else:
                return_value = comms.communications(DRY_CHECK2)
                isDry = False
            return jsonify(result=return_value)


        @app.route('/wash_syringes_process')
        def wash_syringes_process():
            return_value = comms.communications(WASHING)
            return jsonify(result=return_value)


        @app.route('/dry_syringes_process')
        def dry_syringes_process():
            return_value = comms.communications(DRYING)
            return jsonify(result=return_value)


        @app.route('/sterilize_syringes_process')
        def sterilize_syringes_process():
            return_value = comms.communications(STERILIZING)
                
            if JOB_SELECTED == FULL_CYCLE:
                comms.communications("Full-Cycle")
            elif JOB_SELECTED == HALF_CYCLE:
                comms.communications("Half-Cycle")

            return jsonify(result=return_value)

        app.run(host='0.0.0.0')

if __name__ == '__main__':
    t = threading.Thread(target=flaskApp)
    t.start()

    comms = rpi2Arduino()
