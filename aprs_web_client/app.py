import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from flask import Flask, render_template, request
from flask import request as req
from utils import mac_for_ip

from datetime import datetime as dt

from subprocess import call

import audiogen
from .afsk import afsk
from .afsk.afsk.ax25 import UI

app = Flask(__name__)


@app.route("/")
def index():
    message_sent = False
    logger.info(mac_for_ip(req.remote_addr))
    if 'message' in request.args.keys():
        src = b'RP1CCN'
        dst = b'DV1QNE'
        time_sent = "".join(dt.now().isoformat().split('.')[:-1])
        info = "-".join([time_sent, request.args.get('message')])

        logging.info(info)

        packet = UI(
                source = src,
                destination = dst,
                info = info.encode(encoding='UTF-8')
        )


        logger.info(r"Encoding packet:'{0}'".format(packet))
        logger.debug(r"Packet:\n{0!r}".format(packet.unparse()))

        audio = afsk.encode(packet.unparse())

        logger.info("Generating wav file")
        with open('aprs_test_message.wav', 'wb') as f:
            audiogen.sampler.write_wav(f, audio)

        freq = "145"
        logger.info("Sending packet at %s" % freq)

        call([
            "sudo",
            "./fm_transmitter/fm_transmitter",
            "-f",
            freq,
            "aprs_test_message.wav"
        ])


        logger.info("Packet Sent!")

        message_sent = True


    return render_template(
            "index.html",
            message_sent=message_sent,
            received_packets=open("received_packets.log").read()
            )
