#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Aprs Full Duplex Pluto
# Generated: Sat Aug 11 15:35:13 2018
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from detectMarkSpace import detectMarkSpace  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import afsk


class aprs_full_duplex_pluto(gr.top_block):

    def __init__(self, pluto_uri='usb:1.5.5'):
        gr.top_block.__init__(self, "Aprs Full Duplex Pluto")

        ##################################################
        # Parameters
        ##################################################
        self.pluto_uri = pluto_uri

        ##################################################
        # Variables
        ##################################################
        self.audio_samp = audio_samp = 24000
        self.source_samp = source_samp = 44100
        self.samp_rate = samp_rate = audio_samp*22
        self.refresh_rate = refresh_rate = 10
        self.cutoff_frequency = cutoff_frequency = 100e3
        self.center_frequency = center_frequency = 435e6
        self.Decay = Decay = 0.1
        self.Attack = Attack = 0.8

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0_0_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate,
                decimation=source_samp,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.pluto_source_0 = iio.pluto_source(pluto_uri, int(center_frequency), samp_rate, 20000000, 0x8000, True, True, True, "manual", 64.0, '', True)
        self.pluto_sink_0 = iio.pluto_sink(pluto_uri, int(center_frequency), samp_rate, 20000000, 0x8000, False, 10.0, '', True)
        self.detectMarkSpace_1_0_0 = detectMarkSpace(
            decay=Decay,
            samp_rate=audio_samp,
            attack=Attack,
            Frequency=2200,
        )
        self.detectMarkSpace_0_0_0 = detectMarkSpace(
            decay=Decay,
            samp_rate=audio_samp,
            attack=Attack,
            Frequency=1200,
        )
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/pi/aprs_web_client/aprs_test_message.wav', True)
        self.blocks_sub_xx_0_0_0_0 = blocks.sub_ff(1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/home/pi/aprs_web_client/full_duplex.log', True)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.band_pass_filter_0_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, audio_samp, 950, 2450, 100, firdes.WIN_HAMMING, 6.76))
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=source_samp,
        	quad_rate=source_samp,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_samp,
        	quad_rate=int(samp_rate),
        	tau=75e-6,
        	max_dev=5e3,
          )
        self.afsk_ax25decode_1_0 = afsk.ax25decode(audio_samp, 5)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.afsk_ax25decode_1_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.rational_resampler_xxx_0_0_0_0, 0))    
        self.connect((self.band_pass_filter_0_0_0, 0), (self.detectMarkSpace_0_0_0, 0))    
        self.connect((self.band_pass_filter_0_0_0, 0), (self.detectMarkSpace_1_0_0, 0))    
        self.connect((self.blocks_sub_xx_0_0_0_0, 0), (self.afsk_ax25decode_1_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.detectMarkSpace_0_0_0, 0), (self.blocks_sub_xx_0_0_0_0, 0))    
        self.connect((self.detectMarkSpace_1_0_0, 0), (self.blocks_sub_xx_0_0_0_0, 1))    
        self.connect((self.pluto_source_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.band_pass_filter_0_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0_0, 0), (self.pluto_sink_0, 0))    

    def get_pluto_uri(self):
        return self.pluto_uri

    def set_pluto_uri(self, pluto_uri):
        self.pluto_uri = pluto_uri

    def get_audio_samp(self):
        return self.audio_samp

    def set_audio_samp(self, audio_samp):
        self.audio_samp = audio_samp
        self.set_samp_rate(self.audio_samp*22)
        self.detectMarkSpace_1_0_0.set_samp_rate(self.audio_samp)
        self.detectMarkSpace_0_0_0.set_samp_rate(self.audio_samp)
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.audio_samp, 950, 2450, 100, firdes.WIN_HAMMING, 6.76))

    def get_source_samp(self):
        return self.source_samp

    def set_source_samp(self, source_samp):
        self.source_samp = source_samp

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.pluto_source_0.set_params(int(self.center_frequency), self.samp_rate, 20000000, True, True, True, "manual", 64.0, '', True)
        self.pluto_sink_0.set_params(int(self.center_frequency), self.samp_rate, 20000000, 10.0, '', True)

    def get_refresh_rate(self):
        return self.refresh_rate

    def set_refresh_rate(self, refresh_rate):
        self.refresh_rate = refresh_rate

    def get_cutoff_frequency(self):
        return self.cutoff_frequency

    def set_cutoff_frequency(self, cutoff_frequency):
        self.cutoff_frequency = cutoff_frequency

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.pluto_source_0.set_params(int(self.center_frequency), self.samp_rate, 20000000, True, True, True, "manual", 64.0, '', True)
        self.pluto_sink_0.set_params(int(self.center_frequency), self.samp_rate, 20000000, 10.0, '', True)

    def get_Decay(self):
        return self.Decay

    def set_Decay(self, Decay):
        self.Decay = Decay
        self.detectMarkSpace_1_0_0.set_decay(self.Decay)
        self.detectMarkSpace_0_0_0.set_decay(self.Decay)

    def get_Attack(self):
        return self.Attack

    def set_Attack(self, Attack):
        self.Attack = Attack
        self.detectMarkSpace_1_0_0.set_attack(self.Attack)
        self.detectMarkSpace_0_0_0.set_attack(self.Attack)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--pluto-uri", dest="pluto_uri", type="string", default='usb:1.5.5',
        help="Set pluto_uri [default=%default]")
    return parser


def main(top_block_cls=aprs_full_duplex_pluto, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(pluto_uri=options.pluto_uri)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
