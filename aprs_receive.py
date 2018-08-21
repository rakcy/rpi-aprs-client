#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Aprs Receive
# Generated: Tue Aug 21 13:33:21 2018
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
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import afsk
import osmosdr
import time


class aprs_receive(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Aprs Receive")

        ##################################################
        # Variables
        ##################################################
        self.audio_samp = audio_samp = 48000
        self.samp_rate = samp_rate = audio_samp*20
        self.cutoff_frequency = cutoff_frequency = 100e3
        self.center_frequency = center_frequency = 145e6
        self.Decay = Decay = 0.1
        self.Attack = Attack = 0.8

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(center_frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(0, 0)
        self.rtlsdr_source_0.set_if_gain(0, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(2e6, 0)
          
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
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
        self.blocks_sub_xx_0_0_0_0 = blocks.sub_ff(1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, 'aprs_web_client/received_packets.log', True)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.band_pass_filter_0_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, audio_samp, 950, 2450, 100, firdes.WIN_HAMMING, 6.76))
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_samp,
        	quad_rate=int(samp_rate),
        	tau=75e-6,
        	max_dev=5e3,
          )
        self.afsk_ax25decode_1_0 = afsk.ax25decode(audio_samp, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.afsk_ax25decode_1_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.band_pass_filter_0_0_0, 0), (self.detectMarkSpace_0_0_0, 0))    
        self.connect((self.band_pass_filter_0_0_0, 0), (self.detectMarkSpace_1_0_0, 0))    
        self.connect((self.blocks_sub_xx_0_0_0_0, 0), (self.afsk_ax25decode_1_0, 0))    
        self.connect((self.detectMarkSpace_0_0_0, 0), (self.blocks_sub_xx_0_0_0_0, 0))    
        self.connect((self.detectMarkSpace_1_0_0, 0), (self.blocks_sub_xx_0_0_0_0, 1))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.band_pass_filter_0_0_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.analog_nbfm_rx_0, 0))    

    def get_audio_samp(self):
        return self.audio_samp

    def set_audio_samp(self, audio_samp):
        self.audio_samp = audio_samp
        self.set_samp_rate(self.audio_samp*20)
        self.detectMarkSpace_1_0_0.set_samp_rate(self.audio_samp)
        self.detectMarkSpace_0_0_0.set_samp_rate(self.audio_samp)
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.audio_samp, 950, 2450, 100, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_cutoff_frequency(self):
        return self.cutoff_frequency

    def set_cutoff_frequency(self, cutoff_frequency):
        self.cutoff_frequency = cutoff_frequency

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.rtlsdr_source_0.set_center_freq(self.center_frequency, 0)

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


def main(top_block_cls=aprs_receive, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
