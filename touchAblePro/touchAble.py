# LMH
from __future__ import with_statement

"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Nathan Ramella <nar@remix.net> or visit http://www.remix.net
# 
# Additional touchAble development:
# (c) 2014 Sigabort, Lee Huddleston, ZeroConfig; admin@sigabort.co, http://sigabort.co

This script is based off the Ableton Live supplied MIDI Remote Scripts, customised
for OSC request delivery and response. This script can be run without any extra
Python libraries out of the box. 

This is the second file that is loaded, by way of being instantiated through
__init__.py

"""


import Live
import aifc
import wave
import struct
import touchAbleCallbacks
import RemixNet
#import os.path
import OSC
import LiveUtils
import time
import unicodedata
import thread;
from _Generic.util import DeviceAppointer


from threading import Timer

from collections import defaultdict
from Logger import Logger

# LMH
from _Framework.ControlSurface import ControlSurface
from SessionComponent import TouchableSessionComponent

def repr3(input_str):
    try:
        x = input_str.encode("UTF-8")
        return x;
    except:
        return "hahahah"
    try:
        output_st = unicodedata.normalize('NFKD', input_str).encode('ascii','ignore')
        if output_st != None:
            return output_st
        else:
            return ''
    except:
        x = repr(input_str)
        return x[2:-1]

def repr33(input_str):
    try:
        output_st = unicodedata.normalize('NFKD', input_str).encode('ascii','ignore')
        if output_st != None:
            return output_st
        else:
            return ''
    except:
        x = repr(input_str)
        return x[2:-1]

def cut_string(input_str):
    
    info = (input_str[:331] + '..') if len(input_str) > 333 else input_str
    return (info)


class touchAble(ControlSurface):
    __module__ = __name__
    __doc__ = "Main class that establishes the touchAble Component"
    
    # Enable Logging
    _LOG = 0
    
    oldloop_start = {}
    oldloop_end = {}
    oldplay_start = {}
    oldplay_end = {}
    loop_length = {}
    trackid = {}
    clipid = {}
    oldlooping  = {}
    hotlooping = {}
    
    
    prlisten = defaultdict(dict)
    parameters_listeners = defaultdict(dict)
    """ need to be removed later!!!!!!!!!!!!!!!!!!! """
    """ simpler device """
    sample_listeners = defaultdict(dict)
    simpler_selected_slice_listener = defaultdict(dict)
    simpler_playing_position_listener = defaultdict(dict)
    simpler_playbackmode_listener = defaultdict(dict)
    simpler_slicing_playbackmode_listener = defaultdict(dict)
    """ compressor device """
    compressor_available_input_routing_channels_listener = defaultdict(dict)
    compressor_available_input_routing_types_listener = defaultdict(dict)
    compressor_input_routing_channel_listener = defaultdict(dict)
    compressor_input_routing_type_listener = defaultdict(dict)


    wavetable_filter_routing_listener = defaultdict(dict)
    wavetable_modulation_matrix_listener = defaultdict(dict)
    wavetable_mono_poly_listener = defaultdict(dict)
    wavetable_oscillator_1_effect_listener = defaultdict(dict)
    wavetable_oscillator_1_wavetable_category_listener = defaultdict(dict)
    wavetable_oscillator_1_wavetable_index_listener = defaultdict(dict)
    wavetable_oscillator_1_wavetables_listener = defaultdict(dict)
    wavetable_oscillator_2_effect_listener = defaultdict(dict)
    wavetable_oscillator_2_wavetable_category_listener = defaultdict(dict)
    wavetable_oscillator_2_wavetable_index_listener = defaultdict(dict)
    wavetable_oscillator_2_wavetables_listener = defaultdict(dict)
    wavetable_poly_voices_listener = defaultdict(dict)
    wavetable_unison_mode_listener = defaultdict(dict)
    wavetable_unison_voice_count_listener = defaultdict(dict)
    wavetable_visible_modulation_target_names_listener = defaultdict(dict)

    sample_slice_listener = defaultdict(dict)
    sample_slice_sensitivity_listener = defaultdict(dict)
    sample_gain_listener = defaultdict(dict)
    sample_end_marker_listener = defaultdict(dict)
    sample_start_marker_listener = defaultdict(dict)
    sample_warping_listener = defaultdict(dict)
    sample_warping_mode_listener = defaultdict(dict)
    
    chainslisten = defaultdict(dict)
    chaindevicelisten = defaultdict(dict)

    plisten = {}
    device_name_listen = defaultdict(dict)
    dlisten = {}
    clisten = {}
    slisten = {}
    sslisten = {}
    sclisten = {}
    snlisten = {}
    stlisten = {}
    pplisten = {}
    cnlisten = {}
    smlisten = {}
    emlisten = {}
    lslisten = {}
    lelisten = {}
    
    
    fplisten = {}
    devices_listen = {}
    drum_pad_listen = defaultdict(dict)
    drum_pads_listen = {}
    clipwarplisten = {}
    clipwarpmodelisten = {}
    clipmutelisten = {}
    cliplooplisten = {}
    clipgainlisten = {}
    clipcoarselisten = {}
    clipfinelisten = {}

    noteBuffers = defaultdict(list)

    received_midi_cmd = 0

    cclisten = {}
    ablisten = {}
    Rablisten = {}
   
    mlisten = { "solo": {}, "mute": {}, "arm": {}, "current_monitoring_state": {}, "panning": {}, "volume": {}, "sends": {}, "name": {}, "oml": {}, "omr": {}, "color": {}, "available_input_routing_channels": {}, "available_input_routing_types": {}, "available_output_routing_channels": {}, "available_output_routing_types": {}, "input_routing_type": {}, "input_routing_channel": {}, "output_routing_channel": {}, "output_routing_type": {}    }
    rlisten = { "solo": {}, "mute": {}, "panning": {}, "volume": {}, "sends": {}, "name": {}, "color": {}, "available_output_routing_channels": {}, "available_output_routing_types": {}, "output_routing_channel": {}, "output_routing_type": {}   }
    masterlisten = { "panning": {}, "volume": {}, "crossfader": {} }
    scenelisten = {}
    scene = 0
    track = 0
    width = 16
    offsetx = 0
    metermode = 1
    isCheckingLoop = 0
    viewwidth = 8
    updateTime = 0
    maxSampleLength = 4096.0
    onetap = 0
    script_version = 402
    app_main_version = 2000
    app_minor_version = 2000
    app_sub_minor_version = 2000
    listeners_updated = 0
    noteListeners = {}
    loading = 0
    should_check_if_load = 0
    did_init_osc_server = 0
    did_init = 0
    def __init__(self, c_instance):
        self._touchAble__c_instance = c_instance
        # LMH
        ControlSurface.__init__( self, c_instance )
        self.locked_device = self.song().view.selected_track.view.selected_device
        self.lock_to_device(self.locked_device)
        self._device_appointer = DeviceAppointer(song=self.song(), appointed_device_setter=self._set_appointed_device)
    
        self._device_selection_follows_track_selection = True
        
        if self._device_selection_follows_track_selection == True:
            self.log_message("devices DO follow track selection..")
        else:
            self.log_message("devices DO NOT!!! follow track selection..")

        self.show_message("loading touchAble Pro Control Surface..")
      
        self.basicAPI = 0 
        self.do_init()      
        #thread.start_new_thread(self.do_init())


    # LMH
    def _log( self, msg, force = False ):
        if self._LOG or force:
            self.log_message( msg )


    def do_init(self):
        if self.did_init_osc_server == 0:
            self.did_init_osc_server = 1
            self.oscServer = RemixNet.OSCServer(self, '127.0.0.1', 9111, None, 9008)

            self.callbackManager = self.oscServer.callbackManager
            self.callbackManager.add(self.offsetxCB, "/offsetx")
            self.callbackManager.add(self.onetapCB, "/onetap")
            self.callbackManager.add(self.tracksCB, "/script/load")
            self.callbackManager.add(self.meterModeCB, "/metermode")
            self.callbackManager.add(self.positionsCB, "/positions")
            #self.callbackManager.add(self.updateCB, "/script/update")
            self.callbackManager.add(self.getVersion, "/getVersion")
            self.callbackManager.add(self.keepLoop, "/keepLoop")
            self.callbackManager.add(self.clearHiddenLoops, "/clearLoops")
            self.callbackManager.add(self.getActiveLoops, "/getLoops")
            self.callbackManager.add(self.changeLoopCB, "/loopChange")
            self.callbackManager.add(self.jumpForwardCB, "/jumpForward")
            self.callbackManager.add(self.jumpBackwardCB, "/jumpBackward")
            self.callbackManager.add(self.jumpLoopForward, "/jumpLoopForward")
            self.callbackManager.add(self.jumpLoopBackward, "/jumpLoopBackward")
            self.callbackManager.add(self.clip_loopstats2, "/get/clip/loopstats")
            self.callbackManager.add(self.request_loop_data, "/clip/request_loop_data")
        
            self.callbackManager.add(self.deviceLoad, "/browser/load/device")
            self.callbackManager.add(self.chainLoad, "/browser/load/chain")

            self.callbackManager.add(self.expand_device, "/expand_device")
            self.callbackManager.add(self.move_device, "/move_device")
            self.callbackManager.add(self.simpler_gain, "/simpler_gain")
            self.callbackManager.add(self.update_simpler_waveformcb, "/update_simpler_waveform")
            self.callbackManager.add(self.simpler_sensitivity, "/simpler_sensitivity")
            self.callbackManager.add(self.simpler_pad_slicing, "/simpler_pad_slicing")
            self.callbackManager.add(self.simpler_slicing_playback_mode, "/simpler_slicing_playback_mode")
            self.callbackManager.add(self.simpler_start_marker, "/simpler_start_marker")
            self.callbackManager.add(self.simpler_end_marker, "/simpler_end_marker")
            self.callbackManager.add(self.simpler_selected_slice, "/simpler_selected_slice")
            self.callbackManager.add(self.simpler_slicing_type, "/simpler_slicing_type")
            self.callbackManager.add(self.reverse_sample, "/reverse_sample")
            self.callbackManager.add(self.crop_sample, "/crop_sample")
            self.callbackManager.add(self.warp_double, "/warp_double")
            self.callbackManager.add(self.warp_half, "/warp_half")
            self.callbackManager.add(self.warp_as, "/warp_as")
            self.callbackManager.add(self.warping, "/warping")
            self.callbackManager.add(self.warp_mode, "/warp_mode")
            self.callbackManager.add(self.convert_clip_to_simpler, "/converttosimpler")

            self.callbackManager.add(self.set_filter_routing, "/device/wavetable/set_filter_routing")
            self.callbackManager.add(self.set_mono_poly, "/device/wavetable/set_mono_poly")
            self.callbackManager.add(self.set_oscillator_1_effect, "/device/wavetable/set_oscillator_1_effect")
            self.callbackManager.add(self.set_oscillator_1_wavetable_category, "/device/wavetable/set_oscillator_1_wavetable_category")
            self.callbackManager.add(self.set_oscillator_1_wavetable_index, "/device/wavetable/set_oscillator_1_wavetable_index")
            self.callbackManager.add(self.set_oscillator_2_effect, "/device/wavetable/set_oscillator_2_effect")
            self.callbackManager.add(self.set_oscillator_2_wavetable_category, "/device/wavetable/set_oscillator_2_wavetable_category")
            self.callbackManager.add(self.set_oscillator_2_wavetable_index, "/device/wavetable/set_oscillator_2_wavetable_index")
            self.callbackManager.add(self.set_poly_voices, "/device/wavetable/set_poly_voices")
            self.callbackManager.add(self.set_unison_mode, "/device/wavetable/set_unison_mode")
            self.callbackManager.add(self.set_unison_voice_count, "/device/wavetable/set_unison_voice_count")
            self.callbackManager.add(self.set_modulation_value, "/device/wavetable/set_modulation_value")
            self.callbackManager.add(self.get_modulation_value, "/device/wavetable/get_modulation_value")
            self.callbackManager.add(self.get_modulation_targe_parameter_name, "/device/wavetable/get_modulation_targe_parameter_name")
            self.callbackManager.add(self.add_parameter_to_modulation, "/device/wavetable/add_parameter_to_modulation")
            self.callbackManager.add(self.get_modulation_matrix, "/device/wavetable/get_modulation_matrix")

            self.callbackManager.add(self.set_input_routing_channel, "/device/compressor/update_input_routing_channel")
            self.callbackManager.add(self.set_input_routing_type, "/device/compressor/update_input_routing_type")


        
            self.callbackManager.add(self.trackLoad, "/browser/load/track")
            self.callbackManager.add(self.returnLoad, "/browser/load/return")
            self.callbackManager.add(self.masterLoad, "/browser/load/master")
        
            self.callbackManager.add(self.clipLoad, "/browser/load/clip")
            self.callbackManager.add(self.drumpadLoad, "/browser/load/drum_pad")
            self.callbackManager.add(self.drumpadAudioEffectLoad, "/browser/load/drum_pad_audio_effect")
            self.callbackManager.add(self.previewItem, "/browser/start_stop_preview_item")

        
            self.callbackManager.add(self.clipQuantization, "/clip/view/set_quantization")
            self.callbackManager.add(self.clipIsTriplet, "/clip/view/set_is_triplet")
        
            self.callbackManager.add(self.clipSelected, "/clip/clip_selected")
            self.callbackManager.add(self.backFromClip, "/clip/clip_deselected")
            self.callbackManager.add(self.setClipNotes, "/clip/set_notes")
            self.callbackManager.add(self.setNoteVelocity, "/clip/set_note_velocity")
            self.callbackManager.add(self.addNote, "/clip/add_note2")
            self.callbackManager.add(self.addNotes, "/clip/add_notes2")
            self.callbackManager.add(self.updateNote, "/clip/update_note")
            self.callbackManager.add(self.updateNoteVelocity, "/clip/update_note_property")
            self.callbackManager.add(self.removeNote, "/clip/remove_note")
            self.callbackManager.add(self.removeNotes, "/clip/remove_notes")
            self.callbackManager.add(self.stretchNotes, "/clip/stretch_notes")
            self.callbackManager.add(self.getBrowserRoot, "/browser/get_root_items")
            self.callbackManager.add(self.clearNoteBuffer, "/clip/clear_notes")
            self.callbackManager.add(self.addNotesToBuffer, "/clip/add_notes")
            self.callbackManager.add(self.replaceCurrentNotesWithBuffer, "/clip/replace_notes")
            self.callbackManager.add(self.setGlobalGroove, "/set/global_groove")
            self.callbackManager.add(self.setExclusiveSolo, "/exclusive_solo")
            self.callbackManager.add(self.setExclusiveArm, "/exclusive_arm")




            self.callbackManager.add(self.session_record_chang, "/live/set/session_record")
            self.callbackManager.add(self.session_record_status_chang, "/live/set/trigger_session_record")
            self.callbackManager.add(self.re_enable_automation_enabled_chang, "/live/set/re_enable_automation")
            self.callbackManager.add(self.session_automation_record_chang, "/live/set/session_automation_record")
            self.callbackManager.add(self.simpler_playback_mode, "/live/track/device/simpler/playback_mode")

            self.callbackManager.add(self.sesion_capture_midi, "/live/set/capture_midi")
            self.callbackManager.add(self.tapTempo, "/set/tap_tempo")


            self.callbackManager.add(self.track_input_type, "/live/track/input_type")
            self.callbackManager.add(self.track_input_channel, "/live/track/input_channel")
            self.callbackManager.add(self.track_output_type, "/live/track/output_type")
            self.callbackManager.add(self.track_output_channel, "/live/track/output_channel")


            self.callbackManager.add(self.broadcast, "/broadcast")
            self.callbackManager.add(self.print_app_version, "/print_app_version")
            self.callbackManager.add(self.print_string, "/print_string")
            self.callbackManager.add(self.update_all_listenersCB, "/update_listeners")




            #self.oscServer.sendOSC('/remix/oscserver/startup', 1)
            self.logger = self._LOG and Logger() or 0
            self.log("Logging Enabled")
            self.mlcache = []
            self.mrcache = [] 
            self.mmcache = 0

            # LMH
            with self.component_guard():
                self._create_session()
        
            # listener
            #self.update_all_listeners()
            #thread.start_new_thread(self.update_all_listeners())
            #self.oscServer.sendOSC("/update_all_listeners",1)

            self.mlcache = [-3 for i in range(2000)]
            self.mrcache = [-3 for i in range(2000)]
            self.mmcache = -1

            self.callbackManager.add(self.getStatus, "/script/ping")

            self.did_init = 1
            #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", "UPDAT ALL THE LISTENERS")
            self.log_message("did init osc server")
        else:
            pass

    def update_all_listenersCB(self,msg):
        #self.oscServer.sendOSCUDP("/NSLOG_REPLACE","update_all_the_listeners")

        if (self.listeners_updated != 1):
            self.listeners_updated = 1

            #self.oscServer.sendOSCUDP("/NSLOG_REPLACE","listeners updated before thread")
            #self.update_all_listeners()
            #self.log_message("updated all listeners")
            

            thread.start_new_thread(self.update_all_listeners, ())

        


    def print_string(self,msg):
        string = msg[2]
        self._log( string , True )

    def print_app_version(self,msg):
        app_version = msg[2]
        app_m_version = msg[3]
        app_sm_version = msg[4]
        if app_version <= self.app_main_version and app_m_version <= self.app_minor_version and app_sm_version < self.app_sub_minor_version:
            self.app_main_version = app_version
            self.app_minor_version = app_m_version
            self.app_sub_minor_version = app_sm_version
        log_text = "app version : " + str(self.app_main_version) + "." + str(self.app_minor_version) + "." + str(self.app_sub_minor_version)
        self._log( log_text , True )


    def _create_session(self):
        log_text = "_create_session : v " + str(self.script_version)
        #self._log( log_text , True )
        self.session = TouchableSessionComponent(touchAble = self, name = 'Session', num_tracks = 1, num_scenes = 1, is_enabled=True, auto_name=True, enable_skinning=True)
        self.session.set_show_highlight( True )

        #self._send_lsync_coords()
        self._log( "_create_session complete", True )

    def set_lsync_offsets(self,x,y,w,h):
        pass
        #self._log( "set_lsync_offsets: " + str( x ) + ", " + str( y ) + ", " + str( w ) + ", " + str( h ) )
        #self.session._set_lsync_offsets( x, y, w, h )
    
    def broadcast( self, msg ):

        #pass
        type = msg[2]
        if type == 3:
            w = msg[6]
            h = msg[7]
            pos_x = int(msg[8])
            pos_y = int(msg[9])
            
            self._touchAble__c_instance.set_session_highlight(pos_x, pos_y, w, h, False )

        else:
            pass
            #self._touchAble__c_instance.set_session_highlight(msg[2], msg[3], msg[4], msg[5], 0)

            #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", "broadcast");

            #self.session.notify_offset()

            #self.session._broadcast( msg )
    
    def _send_lsync_coords(self):
        pass
        #self._log( "_send_lsync_coords" )
        #self.session._send_lsync_coords( "6" )
        
    #self.log(str(Live.Application.get_application().view.available_main_views()))
        #self.song().master_track.create_device(str("EQEight"))
    
    def _set_appointed_device(self, device):
        #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", ("appointed device changed 1"))

        self.unlock_from_device(self.locked_device)
        #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", ("appointed device changed 2"))

        self.lock_to_device(device)
        #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", ("appointed device changed 3"))

        self.locked_device = device
        
        #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", ("appointed device changed 4"))
        
        pass
    
    def getBrowserRoot(self, msg):

        browser = self.application().browser

        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)

        steps = 1
        i = 0
        indices = []

        self.oscServer.sendOSC("/bundle/start", 1)
        self.oscServer.sendOSC("/browser/start", 1)


        for item in root_items:

            lis = list(indices)

            self.getChildren(item, steps, lis, i)

            i = i+1

        
        self.oscServer.sendOSC("/browser/end", 1)
        self.oscServer.sendOSC("/finish_loading", (1))
        self.oscServer.sendOSC("/bundle/end", 1)




    def getChildren(self, item, steps, indices, i):
        is_folder = 0
        if len(item.children)>0:
            is_folder = 1
        else:
            pass
        count = len(item.children)
        
        indices.append(int(i))
        indis = [repr3(item.name), int(steps), int(item.is_loadable), int(count)]
        for index in indices:
            indis.append(int(index))
        j = 0
        self.oscServer.sendOSC("/browser/item", tuple(indis))
        steps = steps+1

        if is_folder == 1:
            for subItem in item.children:

                lis = list(indices)
                self.getChildren(subItem, steps, lis, j)
                j = j+1
        else:
            pass

    def stopPreviewItem(self,msg):
        a = 1
    
    def previewItem(self,msg):

        start_stop = msg[2]
        steps = msg[3]

        browser = self.application().browser


        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)

        ind = msg[4]
        #self.oscServer.sendOSC("/browser/loadstart", 4)
        if ind >= len(root_items):
            if ind == 11:
                item = list(browser.user_folders)
            if ind == 12:
                item = list(browser.colors)
            subItem = item[msg[5]]
            for i in range(steps-2):
                index = msg[6+i]
                subItem = subItem.children[index]
            if start_stop == 1:
                browser.preview_item(subItem)
            else:
                browser.stop_preview()

        else:

            item = root_items[ind]
            for i in range(steps-1):
                index = msg[5+i]
                item = item.children[index]
            if start_stop == 1:
                browser.preview_item(item)
            else:
                browser.stop_preview()

    def tracksCB(self, msg):
        
        if self.loading == 0:
            self.loading = 1
            self.should_check_if_load = 0
            self.mlcache = [-3 for i in range(2000)]
            self.oscServer.sendOSCUDP("/NSLOG_REPLACE", ("loading1 = ", 1))

            thread.start_new_thread(self.basicAPI.tracksCB(msg))
        else:
            self.should_check_if_load = 1
            self.oscServer.sendOSCUDP("/NSLOG_REPLACE", ("should_check_if_load1 = ", 1))

        #self.basicAPI.tracksCB(msg)
        #self.updateTrackIOClipsDevices(msg)
        #thread.start_new_thread(self.updateTrackIOClipsDevices(msg),("Thread1",2,))
        #thread.start_new_thread(self.basicAPI.loadReturnsStartUp(),("Thread2",1,))
        #thread.start_new_thread(self.basicAPI.loadScenesStartUp(),("Thread3",3,))
        #thread.start_new_thread(self.basicAPI.loadBrowserStartUp(load_browser),("Thread4",4,))

    def updateTrackIOClipsDevices(self,msg):

        trackNumber = 0
        for track in LiveUtils.getTracks():
            self.basicAPI.sendTrackIO(trackNumber, track)
            self.basicAPI.sendTrackClips(trackNumber,track)
            self.basicAPI.load_devices_for_track(track, trackNumber, 0)
            #time.sleep(0.08)
            trackNumber = trackNumber + 1


    def updateCB(self):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update cb")

        self.positions()
        self.mastermeters()

        self.meters()
        
        self.songtime_change()
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "SENT UPDATE")



    def deviceLoad(self, msg):
        position = msg[2]
        type = msg[3]
        tid = msg[4]
        steps = msg[5]
        #self.oscServer.sendOSC("/browser/loadstart", 1)

        track = self.song().master_track
        if type == 0:
            track = self.song().tracks[tid]
        elif type == 2:
            track = self.song().return_tracks[tid]

        self.song().view.selected_track = track
        browser = self.application().browser
        
        #self.oscServer.sendOSC("/browser/loadstart", 2)


        if position == 1:
            track.view.device_insert_mode = Live.Track.DeviceInsertMode.selected_left
        elif position == 0:
            track.view.device_insert_mode = Live.Track.DeviceInsertMode.selected_right
        elif position == -1:
            track.view.device_insert_mode = Live.Track.DeviceInsertMode.default
        #self.oscServer.sendOSC("/browser/loadstart", 3)

        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)

        ind = msg[6]
        #self.oscServer.sendOSC("/browser/loadstart", 4)

        if ind >= len(root_items):
            if ind == 11:
                item = list(browser.user_folders)
            if ind == 12:
                item = list(browser.colors)
            subItem = item[msg[7]]

            for i in range(steps-2):
                message = "userfolder load " + str(i)


                index = msg[8+i]
                subItem = subItem.children[index]
            
            browser.load_item(subItem)


        else:
            item = root_items[msg[6]]

            for i in range(steps-1):
            
                index = msg[7+i]
                item = item.children[index]
        
            browser.load_item(item)


    def chainLoad(self, msg):
        type = msg[2]
        tid = msg[3]
        steps = msg[4]
        #self.oscServer.sendOSC("/browser/loadstart", 1)
        
        track = self.song().master_track
        if type == 0:
            track = self.song().tracks[tid]
        elif type == 2:
            track = self.song().return_tracks[tid]
    
        #self.song().view.selected_track = track
        browser = self.application().browser
        
        #self.oscServer.sendOSC("/browser/loadstart", 2)
        
        track.view.device_insert_mode = Live.Track.DeviceInsertMode.default
        #self.oscServer.sendOSC("/browser/loadstart", 3)
    

        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)
        
        item = root_items[msg[5]]
        #self.oscServer.sendOSC("/browser/loadstart", 4)
        
        for i in range(steps-1):
            
            index = msg[6+i]
            item = item.children[index]
        
            
        #self.oscServer.sendOSC("/browser/loadstart", 5)
        
        if not self.application().view.browse_mode:
            self.application().view.toggle_browse()

        browser.load_item(item)
        
        browser.hotswap_target = None


        if self.application().view.browse_mode:
            self.application().view.toggle_browse()

        #self.oscServer.sendOSC("/browser/loadstart", 6)






    def trackLoad(self, msg):
        trk = msg[2]
        steps = msg[3]
        #self.oscServer.sendOSC("/browser/loadstart", 1)

        track = self.song().tracks[trk]
        application = self.application()
        
        self.song().view.selected_track = track
        
        #Live.Application.get_application().view.show_view("Detail/DeviceChain")

        browser = self.application().browser
        
        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)
        
        item = root_items[msg[4]]
        #self.oscServer.sendOSC("/browser/loadstart", 2)

        for i in range(steps-1):
            #self.oscServer.sendOSC("/browser/loadstart", 3)

            index = msg[5+i]
            item = item.children[index]
        #self.oscServer.sendOSC("/browser/loadstart", 3)

        #if not Live.Application.get_application().view.browse_mode:
            #Live.Application.get_application().view.toggle_browse()
        #self.oscServer.sendOSC("/browser/loadstart", 4)

        browser.load_item(item)
        #self.oscServer.sendOSC("/browser/loadstart", 5)
                
        #if Live.Application.get_application().view.browse_mode:
            #Live.Application.get_application().view.toggle_browse()
        #self.oscServer.sendOSC("/browser/loadstart", 6)

    def returnLoad(self, msg):
        trk = msg[2]
        steps = msg[3]
        #self.oscServer.sendOSC("/browser/loadstart", 1)
        
        track = self.song().return_tracks[trk]
        application = self.application()
        
        self.song().view.selected_track = track
        
        #Live.Application.get_application().view.show_view("Detail/DeviceChain")
        
        browser = self.application().browser
        
        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)
        
        item = root_items[msg[4]]
        #self.oscServer.sendOSC("/browser/loadstart", 2)
        
        for i in range(steps-1):
            #self.oscServer.sendOSC("/browser/loadstart", 3)
            
            index = msg[5+i]
            item = item.children[index]
        #self.oscServer.sendOSC("/browser/loadstart", 3)
        
        #if not Live.Application.get_application().view.browse_mode:
        #Live.Application.get_application().view.toggle_browse()
        #self.oscServer.sendOSC("/browser/loadstart", 4)
        
        browser.load_item(item)
        #self.oscServer.sendOSC("/browser/loadstart", 5)
        
        #if Live.Application.get_application().view.browse_mode:
        #Live.Application.get_application().view.toggle_browse()
        #self.oscServer.sendOSC("/browser/loadstart", 6)

    
    def masterLoad(self, msg):
        steps = msg[2]
        self.oscServer.sendOSC("/browser/loadstart", 1)
        
        track = self.song().master_track
        application = self.application()
        
        self.song().view.selected_track = track
        
        #Live.Application.get_application().view.show_view("Detail/DeviceChain")
        
        browser = self.application().browser
        
        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)
        
        item = root_items[msg[3]]
        #self.oscServer.sendOSC("/browser/loadstart", 2)
        
        for i in range(steps-1):
            #self.oscServer.sendOSC("/browser/loadstart", 3)
            
            index = msg[4+i]
            item = item.children[index]
        #self.oscServer.sendOSC("/browser/loadstart", 3)
        
        #if not Live.Application.get_application().view.browse_mode:
        #Live.Application.get_application().view.toggle_browse()
        #self.oscServer.sendOSC("/browser/loadstart", 4)
        
        browser.load_item(item)
        #self.oscServer.sendOSC("/browser/loadstart", 5)
        
        #if Live.Application.get_application().view.browse_mode:
        #Live.Application.get_application().view.toggle_browse()
        self.oscServer.sendOSC("/browser/loadstart", 6)

    def get_device_for_message(self,msg):
    
        type = msg[2]
        tid = msg[3]
        did = msg[4]
    
        number_of_steps = msg[5]
        
        if type == 0:
            track = LiveUtils.getSong().tracks[tid]
        elif type == 2:
            track = LiveUtils.getSong().return_tracks[tid]
        elif type == 1:
            track = LiveUtils.getSong().master_track

        device = track.devices[did]

        for i in range(number_of_steps):
            chain_id = msg[6+i*2]
            device_id = msg[7+i*2]
    
            track = device.chains[chain_id]
            device = track.devices[device_id]

        return device


    def drumpadLoad(self, msg):
        #self.oscServer.sendOSC("/browser/load/drumpad", 1)
        trk = msg[2]
        dev = msg[3]
        
        number_of_steps = msg[4]
        
        track = self.song().tracks[trk]
        trackk = track;
        device = track.devices[dev]
        
        for i in range(number_of_steps):
            chain_id = msg[5+i*2]
            device_id = msg[6+i*2]
            
            track = device.chains[chain_id]
            device = track.devices[device_id]

        
        pad = 127-msg[5 + number_of_steps * 2]

        steps = msg[6 + number_of_steps * 2]
        #self.oscServer.sendOSC("/browser/loadstart", 1)
        
        
        browser = self.application().browser


        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)
        
        item = root_items[msg[7 + number_of_steps * 2]]
        
        for i in range(steps-1):
            
            index = msg[8 + number_of_steps * 2 +i]
            item = item.children[index]
        
        drum_pad = device.drum_pads[pad]
                    
                

            
        self.song().view.selected_track = trackk
        #self.song().view.select_device(device)
        self.application().view.show_view("Detail/DeviceChain")
            
        if isinstance(drum_pad, Live.DrumPad.DrumPad):
            if drum_pad.chains and drum_pad.chains[0].devices:
                self.song().view.select_device(drum_pad.chains[0].devices[0])
                drum_pad.canonical_parent.view.selected_chain = drum_pad.chains[0]
                browser.hotswap_target = drum_pad.chains[0]

            else:
                browser.hotswap_target = drum_pad

            
            drum_pad.canonical_parent.view.selected_drum_pad = drum_pad

            
            #self.oscServer.sendOSC("/browser/loadstart", 2)

            #browser.hotswap_target = drum_pad
                
            if not self.application().view.browse_mode:
                self.application().view.toggle_browse()

            browser.load_item(item)

            if self.application().view.browse_mode:
                self.application().view.toggle_browse()

        else:
            pass
   
        #self.oscServer.sendOSC("/browser/loadstart", 6)
    
    
    def drumpadAudioEffectLoad(self, msg):
        #self.oscServer.sendOSC("/browser/load/drumpad", 1)

        trk = msg[2]
        dev = msg[3]
        
        number_of_steps = msg[4]
        
        track = self.song().tracks[trk]
        device = track.devices[dev]
        
        for i in range(number_of_steps):
            chain_id = msg[5+i*2]
            device_id = msg[6+i*2]
            
            track = device.chains[chain_id]
            device = track.devices[device_id]
        
        pad = 127-msg[5 + number_of_steps * 2]
        
        steps = msg[6 + number_of_steps * 2]
        #self.oscServer.sendOSC("/browser/loadstart", 1)
        
        track = self.song().tracks[trk]
        device = track.devices[dev]
        
        
        browser = self.application().browser
        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)
        
        item = root_items[msg[7 + number_of_steps * 2]]
        
        for i in range(steps-1):
            
            index = msg[8 + number_of_steps * 2+i]
            item = item.children[index]
        
        drum_pad = device.drum_pads[pad]
        
        
        
        
        self.song().view.selected_track = track
        #self.song().view.select_device(device)
        self.application().view.show_view("Detail/DeviceChain")
        
        if isinstance(drum_pad, Live.DrumPad.DrumPad):
            if drum_pad.chains and drum_pad.chains[0].devices:
                self.song().view.select_device(drum_pad.chains[0].devices[0])
                drum_pad.canonical_parent.view.selected_chain = drum_pad.chains[0]
                browser.hotswap_target = drum_pad.chains[0]
                #self.oscServer.sendOSC("/browser/loadstart", 2)

            else:
                browser.hotswap_target = drum_pad
                #self.oscServer.sendOSC("/browser/loadstart", 3)


            #self.oscServer.sendOSC("/browser/loadstart", 4)

            
            
            drum_pad.canonical_parent.view.selected_drum_pad = drum_pad
            
            
            #self.oscServer.sendOSC("/browser/loadstart", 5)
            
            #browser.hotswap_target = drum_pad
            
            if not self.application().view.browse_mode:
                self.application().view.toggle_browse()
                
            browser.load_item(item)

            if self.application().view.browse_mode:
                self.application().view.toggle_browse()
                
            
        
        #self.oscServer.sendOSC("/browser/loadstart", 6)

    def clipLoad(self, msg):
        trk = msg[2]
        scene = msg[3]
        steps = msg[4]
        #self.oscServer.sendOSC("/browser/loadstart", 1)

        track = self.song().tracks[trk]
        ascene = self.song().scenes[scene]

        clip_slot = track.clip_slots[scene]
        
        """ self.song().view.highlighted_clip_slot = clip_slot """
        

        self.song().view.selected_track = track
        self.song().view.selected_scene = ascene
        

        self.application().view.show_view("Detail/Clip")
                
        #Live.Application.get_application().view.show_view("Detail/DeviceChain")
        
        browser = self.application().browser
        
        root_items = []
        root_items.append(browser.sounds)
        root_items.append(browser.drums)
        root_items.append(browser.instruments)
        root_items.append(browser.audio_effects)
        root_items.append(browser.midi_effects)
        root_items.append(browser.max_for_live)
        root_items.append(browser.plugins)
        root_items.append(browser.clips)
        root_items.append(browser.samples)
        root_items.append(browser.packs)
        root_items.append(browser.user_library)


        item = root_items[msg[5]]
        
        for i in range(steps-1):
            index = msg[6+i]
            item = item.children[index]


        self.song().view.selected_track = track
        self.song().view.selected_scene = ascene

    
        browser.load_item(item)


    def tapTempo(self, msg):
        self.song().tap_tempo()
    
    def onetapCB(self, msg):
        self.onetap = msg[2]
        
        
    def clipQuantization(self, msg):
        
        track = msg[2]
        scene = msg[3]
        quant = msg[4]
        trk = self.song().tracks[track]
        clip = trk.clip_slots[scene].clip
        


        if quant == 0:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_8_bars
        if quant == 1:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_4_bars
        if quant == 2:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_2_bars
        if quant == 3:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_bar
        if quant == 4:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_half
        if quant == 5:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_quarter
        if quant == 6:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_eighth
        if quant == 7:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_sixteenth
        if quant == 8:
            clip.view.grid_quantization = Live.Clip.GridQuantization.g_thirtysecond
        if quant == 9:
            clip.view.grid_quantization = Live.Clip.GridQuantization.no_grid
                


    def clipIsTriplet(self, msg):
        
        track = msg[2]
        scene = msg[3]
        is_triplet = msg[4]
        trk = self.song().tracks[track]
        clip = trk.clip_slots[scene].clip
    
        clip.view.grid_is_triplet = bool(is_triplet)

    def clipSelected(self, msg):

        track = msg[2]
        scene = msg[3]
        length = msg[4]
        trk = self.song().tracks[track]
        clip = trk.clip_slots[scene].clip
        
        
        
        if clip == None:
            a = Live.Application.get_application().get_major_version()
            if a >= 9:
                clipSlot = self.song().tracks[track].clip_slots[scene]
                clipSlot.create_clip(float(length))
                clip = clipSlot.clip
                if clip.name != None:
                    nm = cut_string(clip.name)
                else:
                    nm = " "
                self.oscServer.sendOSC("/clip", (track, scene, repr3(nm), clip.color, int(0),int(0)))

            else:
                pass



        key = '%s.%s' % (track, scene)

        cb = lambda :self.notesChanged(track, scene, clip)
        if self.noteListeners.has_key(clip) != 1:
            clip.add_notes_listener(cb)
            self.noteListeners[clip] = cb

        clip = self.song().tracks[track].clip_slots[scene].clip
                    
        self.song().view.selected_track = trk
        self.song().view.detail_clip = clip
        Live.Application.get_application().view.show_view("Detail/Clip")

        
        notes = [int(track)]
        notes.append(int(scene))
        count = 0
        
        clip.select_all_notes()
        
        clipNotes = clip.get_selected_notes()
        clip.deselect_all_notes()
        loopstart = 0
        looplength = 0
        start = 0
        end = 0
        looping = clip.looping
        
        if looping == 1:
            
            loopstart = clip.loop_start
            loopend = clip.loop_end
            
            clip.looping = 0            
            start = clip.loop_start
            end = clip.loop_end
            clip.looping = 1
        
        else:
            start = clip.loop_start
            end = clip.loop_end
            
            clip.looping = 1
            
            loopstart = clip.loop_start
            loopend = clip.loop_end
            clip.looping = 0
                    
        try:
            start = clip.start_marker
            end = clip.end_marker
        except:
            pass
        #self.oscServer.sendOSC("/bundle/start", (1))

        self.oscServer.sendOSC("/clip/requested_loop_stats", (int(track), int(scene), float(start), float(end), float(loopstart), float(loopend)))

        self.oscServer.sendOSC("/clip/start_receiving_notes", (int(track), int(scene)))
        
        noteBuffer = self.noteBuffers[key]

                
        for note in clipNotes:
            noteBuffer.append(note)
            for var in note:
                notes.append(float(var))
            count = count+1
            if count == 128:
                self.oscServer.sendOSC("/clip/receive_notes", tuple(notes))
                count = 0
                notes = [int(track)]
                notes.append(int(scene))
        
        self.oscServer.sendOSC("/clip/receive_notes", tuple(notes))
        self.oscServer.sendOSC("/clip/end_receiving_notes", (int(track), int(scene)))
        self.oscServer.sendOSC("/finish_loading", (1))
        #self.oscServer.sendOSC("/bundle/end", (1))


    def update_listeners_for_device(self, device, track, tid, did, type, num, number_of_steps, lis, device_id):

        self.add_device_listeners_for_track(track, int(tid), int(type))

        self.send_update_for_device(device, track, int(tid), int(did), int(type), int(num), int(number_of_steps), lis, int(device_id))



    def get_device_for_message(self,msg):

        type = msg[2]
        tid = msg[3]
        did = msg[4]
        
        number_of_steps = msg[5]
        
        if type == 0:
            track = LiveUtils.getSong().tracks[tid]
        elif type == 2:
            track = LiveUtils.getSong().return_tracks[tid]
        elif type == 1:
            track = LiveUtils.getSong().master_track

        device = track.devices[did]
        
        for i in range(number_of_steps):
            chain_id = msg[6+i*2]
            device_id = msg[7+i*2]
            
            track = device.chains[chain_id]
            device = track.devices[device_id]
        

        return device





    def set_filter_routing(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        filter_routing = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.filter_routing = filter_routing

    def set_mono_poly(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        mono_poly = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.mono_poly = mono_poly


    def set_oscillator_1_effect(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        effect_mode = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.oscillator_1_effect_mode = effect_mode



    def set_oscillator_1_wavetable_category(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        oscillator_1_wavetable_category = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.oscillator_1_wavetable_category = oscillator_1_wavetable_category

    def set_oscillator_1_wavetable_index(self, msg):
    

        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        oscillator_1_wavetable_index = msg[new_index]

        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.oscillator_1_wavetable_index = oscillator_1_wavetable_index


    def set_oscillator_2_effect(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        effect_mode = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.oscillator_2_effect_mode = effect_mode



    def set_oscillator_2_wavetable_category(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        oscillator_2_wavetable_category = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.oscillator_2_wavetable_category = oscillator_2_wavetable_category

    def set_oscillator_2_wavetable_index(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        oscillator_2_wavetable_index = msg[new_index]
        a_version = Live.Application.get_application().get_major_version()

        if device.class_name == 'InstrumentVector' and a_version >= 10:
            wavetable = device
            wavetable.oscillator_2_wavetable_index = oscillator_2_wavetable_index

    def set_input_routing_channel(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        input_routing_channel = msg[new_index]
        a_version = Live.Application.get_application().get_major_version()

        if device.class_name == 'Compressor2' and a_version >= 10:
            compressor = device
            compressor.input_routing_channel = compressor.available_input_routing_channels[input_routing_channel]

    def set_input_routing_type(self, msg):
    

        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        input_routing_type = msg[new_index]
        a_version = Live.Application.get_application().get_major_version()
        if device.class_name == 'Compressor2' and a_version >= 10:
            compressor = device
            compressor.input_routing_type = compressor.available_input_routing_types[input_routing_type]


    def set_poly_voices(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        effect_mode = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.oscillator_2_effect_mode = effect_mode


    def set_unison_mode(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        unison_mode = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.unison_mode = unison_mode

    def set_unison_voice_count(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        unison_voice_count = msg[new_index]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.unison_voice_count = unison_voice_count


    def set_modulation_value(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        target = msg[new_index]
        source = msg[new_index + 1]
        value = msg[new_index + 2]

        if device.class_name == 'InstrumentVector':
            wavetable = device
            wavetable.set_modulation_value(target, source, value)


    def get_modulation_value(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        target = msg[new_index]
        source = msg[new_index + 1]
    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            mod_val = wavetable.get_modulation_value(target,source)
        
            play_pos_data = [int(type)]
            play_pos_data.append(int(tid))
            play_pos_data.append(int(did))
            play_pos_data.append(int(number_of_steps))
        
            for index in range(number_of_steps * 2):
                play_pos_data.append(int(indices[index]))
        
            play_pos_data.append(float(mod_val))
        
            self.oscServer.sendOSC("/device/wavetable/set_modulation_value", play_pos_data)


    def get_modulation_targe_parameter_name(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        unison_voice_count = msg[new_index]
        target = msg[new_index]

        if device.class_name == 'InstrumentVector':
            wavetable = device
            mod_name = wavetable.get_modulation_target_parameter_name(target)


            play_pos_data = [int(type)]
            play_pos_data.append(int(tid))
            play_pos_data.append(int(did))
            play_pos_data.append(int(number_of_steps))
    
            for index in range(number_of_steps * 2):
                play_pos_data.append(int(indices[index]))
            
            play_pos_data.append(repr3(mod_name))
        
            self.oscServer.sendOSC("/device/wavetable/set_modulation_targe_parameter_name", play_pos_data)

    def add_parameter_to_modulation(self, msg):
    
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        parameter_inx = msg[new_index]

    
        if device.class_name == 'InstrumentVector':
            wavetable = device
            parameter = wavetable.parameters[parameter_inx]
            wavetable.add_parameter_to_modulation_matrix(parameter)



    def simpler_playback_mode(self, msg):
        
        
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        a_playback_mode = msg[new_index]
    
        if device.class_name == 'OriginalSimpler':
            simpler = device
            simpler.playback_mode = a_playback_mode

    
    


    def simpler_gain(self, msg):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "SETTING GAIN VALUE0")

        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "SETTING GAIN VALUE1")

        if device.class_name == 'OriginalSimpler':

            simpler = device
            gain_val = msg[new_index]
            sample = simpler.sample
            sample.gain = gain_val
            #self.oscServer.sendOSC("/NSLOG_REPLACE", "SETTING GAIN VALUE2")



    def simpler_pad_slicing(self, msg):

        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            gain_val = msg[new_index]
            sample = simpler.sample
            simpler.pad_slicing = gain_val


    def simpler_slicing_playback_mode(self, msg):
        
        
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2


        if device.class_name == 'OriginalSimpler':
            
            simpler = device
            gain_val = msg[new_index]
            sample = simpler.sample
            
            simpler.slicing_playback_mode = gain_val


    def simpler_sensitivity(self, msg):
        
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            gain_val = msg[new_index]
            sample = simpler.sample
            sample.slicing_sensitivity = gain_val


    def simpler_start_marker(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            start_marker = msg[new_index]
            sample = simpler.sample
            sample.start_marker = start_marker

    def simpler_end_marker(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            end_marker = msg[new_index]
            sample = simpler.sample
            sample.end_marker = end_marker

    def simpler_slicing_type(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            end_marker = msg[new_index]
            sample = simpler.sample
            sample.end_marker = end_marker

    def reverse_sample(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            simpler.reverse()


    def crop_sample(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            simpler.crop()

    def warp_half(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            simpler.warp_half()

    def warp_double(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            simpler.warp_double()

    def warp_as(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            simpler.warp_as()

    def warping(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler' and device.sample != None:
            device.sample.warping = msg[new_index]

    def warp_mode(self, msg):
    
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler' and device.sample != None:
            device.sample.warp_mode = msg[new_index]


    def simpler_selected_slice(self, msg):
    

        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        
        if device.class_name == 'OriginalSimpler':
            simpler = device
            sample = simpler.sample
            selected_slice = msg[new_index]
            
            messsage = "new slice " + str(selected_slice) + "old slice " + str(simpler.view.selected_slice)

            sample.insert_slice(selected_slice)
            sample.remove_slice(simpler.view.selected_slice)
            simpler.view.selected_slice = selected_slice

    def move_device(self, msg):


        type = msg[2]
        track_id = msg[3]
        device_id = msg[4]
        new_index = msg[5]
        number_of_steps = msg[6]


        if type == 1:
            
            track = LiveUtils.getSong().tracks[track_id]
        elif type == 3:
            
            track = LiveUtils.getSong().return_tracks[track_id]
        else:
            
            track = LiveUtils.getSong().master_track
        
        device = track.devices[device_id]
        
        for i in range(number_of_steps):
            chain_id = msg[7+i*2]
            device_id = msg[8+i*2]
            
            chain = device.chains[chain_id]
            device = chain.devices[device_id]


        self.oscServer.sendOSC("/NSLOG_REPLACE", "select device & track")

        LiveUtils.getSong().view.selected_track = track
        LiveUtils.getSong().view.select_device(device)
        
        self.oscServer.sendOSC("/NSLOG_REPLACE", "selected device & track")


        parent = device.canonical_parent
        device_index = list(parent.devices).index(device)
        self.oscServer.sendOSC("/NSLOG_REPLACE", "move device" + str(device_index))
        self.oscServer.sendOSC("/NSLOG_REPLACE", "move device" + str(device.name))
        self.oscServer.sendOSC("/NSLOG_REPLACE", "old index " + str(device_index) + "new index " + str(new_index))

        """ self.oscServer.sendOSC("/NSLOG_REPLACE", "move right" + str(device_index))
        LiveUtils.getSong().move_device(device, parent, new_index) """
        
        if new_index > device_index:
        
            if new_index > len(parent.devices) + 1 and isinstance(parent, Live.Chain.Chain):
                self.oscServer.sendOSC("/NSLOG_REPLACE", "move out" + str(new_index))
                move_behind=True
                self.move_out(parent.canonical_parent, move_behind,device)

            elif new_index < len(parent.devices):
                right_device = parent.devices[new_index]
                if right_device.can_have_chains and right_device.view.is_showing_chain_devices and right_device.view.selected_chain:
                    self.oscServer.sendOSC("/NSLOG_REPLACE", "move int" + str(new_index))
                    move_to_end = False
                    self.move_in(right_device, move_to_end,device)
                else:
                    self.oscServer.sendOSC("/NSLOG_REPLACE", "move right" + str(new_index))
                    LiveUtils.getSong().move_device(device, parent, new_index)

        else:
            parent = device.canonical_parent
            if new_index > 0:
                left_device = parent.devices[new_index]
                if left_device.can_have_chains and left_device.view.is_showing_chain_devices and left_device.view.selected_chain:
                    move_to_end=True
                    self.move_in(left_device, move_to_end,device)
                else:
                    LiveUtils.getSong().move_device(device, parent, new_index)
            else:
                LiveUtils.getSong().move_device(device, parent, new_index)
                #elif isinstance(parent, Live.Chain.Chain):
                #move_behind = False
                #self.move_out(parent,move_behind, device)

    def move_out(self, rack, move_behind,device):
        parent = rack.canonical_parent
        rack_index = list(parent.devices).index(rack)
        LiveUtils.getSong().move_device(device, parent, rack_index + 1 if move_behind else rack_index)
    
    def move_in(self, rack, move_to_end,device):
        chain = rack.view.selected_chain
        if chain:
            LiveUtils.getSong().move_device(device, chain, len(chain.devices) if move_to_end else 0)








    def expand_device(self, msg):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", ("try to expand"))

        type = msg[2]
        tid = msg[3]
        did = msg[4]
        
        number_of_steps = msg[5]

        
        if type == 0:
            track = LiveUtils.getSong().tracks[tid]
        elif type == 2:
            track = LiveUtils.getSong().return_tracks[tid]
        elif type == 1:
            track = LiveUtils.getSong().master_track
        
        device = track.devices[did]
        num = len(track.devices)
        indices = []
        device_id = -1


        for i in range(number_of_steps):
            chain_id = msg[6+i*2]
            device_id = msg[7+i*2]

            chain = device.chains[chain_id]
            indices.append(int(chain_id))
            
            device = chain.devices[device_id]
            num = len(chain.devices)
            
            indices.append(int(device_id))
        

        if device.class_name == 'OriginalSimpler':

            for parameter in device.parameters:
                if parameter.name == 'Pe On':
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                elif parameter.name == 'L On':
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                elif parameter.name == 'Fe On':
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                elif parameter.name == 'F On':
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                else:
                    pass
          
          
            self.send_update_for_device(device, track, tid, did, type, num, number_of_steps, indices, -1)
            
            device_data = [int(type)]
            device_data.append(int(tid))
            device_data.append(int(did))
            device_data.append(int(number_of_steps))
            
            for index in range(number_of_steps * 2):
                device_data.append(int(indices[index]))
        
            self.oscServer.sendOSC("/device/simpler/ui_update", (tuple(device_data)))

        elif device.class_name == 'MultiSampler':
        
            for parameter in device.parameters:
                
                
                if parameter.name == 'Osc On':
                    
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                elif parameter.name == 'Pe On':
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                
                elif parameter.name == 'Shaper On':
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value

                elif parameter.name == 'L 1 On':
                    
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                elif parameter.name == 'L 2 On':
                    
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                elif parameter.name == 'L 3 On':
                    
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                elif parameter.name == 'Ae On':
                    
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                elif parameter.name == 'F On':
                            
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                elif parameter.name == 'Fe On':
                            
                    old_value = parameter.value
                    parameter.value = 1
                    parameter.value = old_value
                
                else:
                    pass
    



                

    def clearNoteBuffer(self, msg):
        track = msg[2]
        scene = msg[3]
        clip = self.song().tracks[track].clip_slots[scene].clip

        key = '%s.%s' % (track, scene)
        self.noteBuffers[key] = []
            


    
    def addNotesToBuffer(self, msg):
        track = msg[2]
        scene = msg[3]
        noteCount = (len(msg)-4)/5
        key = '%s.%s' % (track, scene)

        
        noteBuffer = self.noteBuffers[key]

            
        for i in range(noteCount):
            noteDescription = []
            ind = 4 + (i*5)
            pitch = msg[(ind+0)]
            time = msg[(ind+1)]
            length = msg[(ind+2)]
            velocity = msg[(ind+3)]
            mute = msg[(ind+4)]
            
            noteDescription.append(int(pitch))
            noteDescription.append(float(time))
            noteDescription.append(float(length))
            noteDescription.append(float(velocity))
            noteDescription.append(bool(mute))
            
            noteBuffer.append(noteDescription)
            


    def replaceCurrentNotesWithBuffer(self, msg):
        track = msg[2]
        scene = msg[3]
        clip = self.song().tracks[track].clip_slots[scene].clip
        clip.select_all_notes()
        key = '%s.%s' % (track, scene)
                    
        noteBuffer = self.noteBuffers[key]

       
        clip.replace_selected_notes(tuple(noteBuffer))
        clip.deselect_all_notes()
            
                
    
    def setClipNotes(self, msg):
        track = msg[2]
        scene = msg[3]
        clip = self.song().tracks[track].clip_slots[scene].clip
        
        clip.select_all_notes()
        newClipNotes = []
        
        noteCount = (len(msg)-4)/5

        newNotes = []
        for i in range(noteCount):
            noteDescription = []
            ind = 4 + (i*5)
            pitch = msg[(ind+0)]
            time = msg[(ind+1)]
            length = msg[(ind+2)]
            velocity = msg[(ind+3)]
            mute = msg[(ind+4)]

            noteDescription.append(int(pitch))
            noteDescription.append(float(time))
            noteDescription.append(float(length))
            noteDescription.append(float(velocity))
            noteDescription.append(bool(mute))            

            newClipNotes.append(noteDescription)

            
        clip.replace_selected_notes(tuple(newClipNotes))
        clip.deselect_all_notes()


    def setNoteVelocity(self, msg):

        track = msg[2]
        scene = msg[3]

        pitch = int(msg[4])
        time = float(msg[5])
        length = float(msg[6])
        velocity = float(msg[7])
        mute = bool(msg[8])
        
        clip = self.song().tracks[track].clip_slots[scene].clip
        
        #clip.remove_notes(time, pitch, length, 1)
        
        newClipNotes = []
        noteDescription = []

        noteDescription.append(pitch)
        noteDescription.append(time)
        noteDescription.append(length)
        noteDescription.append(velocity)
        noteDescription.append(mute)
        
        newClipNotes.append(noteDescription)
        clip.set_notes(tuple(newClipNotes))


            
    def addNote(self, msg):
        
        track = msg[2]
        scene = msg[3]
        
        pitch = int(msg[4])
        time = float(msg[5])
        length = float(msg[6])
        velocity = float(msg[7])
        mute = bool(msg[8])
       
        clip = self.song().tracks[track].clip_slots[scene].clip
                
        newClipNotes = []
        noteDescription = []
        
        noteDescription.append(pitch)
        noteDescription.append(time)
        noteDescription.append(length)
        noteDescription.append(velocity)
        noteDescription.append(mute)
        
        newClipNotes.append(noteDescription)
        clip.set_notes(tuple(newClipNotes))
    
    
    def addNotes(self, msg):
        
        track = msg[2]
        scene = msg[3]
        
        noteCount = (len(msg)-4)/5
        
        newClipNotes = []

        for i in range(noteCount):
            noteDescription = []
            ind = 4 + (i*5)
            pitch = int(msg[(ind+0)])
            time = float(msg[(ind+1)])
            length = float(msg[(ind+2)])
            velocity = float(msg[(ind+3)])
            mute = bool(msg[(ind+4)])
        
            noteDescription.append(pitch)
            noteDescription.append(time)
            noteDescription.append(length)
            noteDescription.append(velocity)
            noteDescription.append(mute)
        
            newClipNotes.append(noteDescription)
        
        clip = self.song().tracks[track].clip_slots[scene].clip
        clip.set_notes(tuple(newClipNotes))


    def selectNotes(self, msg):
    
        track = msg[2]
        scene = msg[3]
        
        pitch_min = int(msg[4])
        pitch_max = int(msg[5])

        time = float(msg[6])
        length = float(msg[7])
        
        velocity = float(msg[8])

        clip = self.song().tracks[track].clip_slots[scene].clip
    
    
        clip.remove_notes(time, pitch_min, length, pitch_max)
        clip.set_notes(time, pitch_min, length, pitch_max)
    
    
    def deselectNote(self, msg):
        
        track = msg[2]
        scene = msg[3]
        
        pitch_min = int(msg[4])
        pitch_max = int(msg[5])
        
        time = float(msg[6])
        length = float(msg[6])
        
        clip = self.song().tracks[track].clip_slots[scene].clip
        
        clip.get_notes(time, pitch_min, length, 127)

    def updateNoteVelocity(self, msg):

        track = msg[2]
        scene = msg[3]

        noteCount = (len(msg)-4)/5
        clip = self.song().tracks[track].clip_slots[scene].clip

        newSelectedNotes = []
        
        stringstring = str(noteCount)
        

        for i in range(noteCount):
            ind = 4 + (i*5)
            pitch = int(msg[(ind+0)])
            time = float(msg[(ind+1)])
            length = float(msg[(ind+2)])
            velocity = float(msg[(ind+3)])
            mute = bool(msg[(ind+4)])
            selectedNotes = []
            
            """ a_string = "pitch " + str(pitch) + " time: " + str(time) + " length: " + str(length) + " vel: " + str(velocity) +  " sasdasd"
        
            self.oscServer.sendOSC("/NSLOG_REPLACE", a_string) """

            selectedNotes = clip.get_notes(time - 0.001, pitch, length + 0.001, 1)
            
            a_length = len(selectedNotes)
            aNote = selectedNotes[0]
            lst = list(aNote)
            lst[3] = velocity
            lst[4] = mute
            aaNote = tuple(lst)
            newSelectedNotes.append(aaNote)

        clip.set_notes(tuple(newSelectedNotes))


    def updateNote(self, msg):
        
        track = msg[2]
        scene = msg[3]
        
        pitch = int(msg[4])
        time = float(msg[5])
        length = float(msg[6])
        velocity = float(msg[7])
        mute = bool(msg[8])
        
        oldpitch = int(msg[9])
        oldtime = float(msg[10])
        oldlength = float(msg[11])
        
        clip = self.song().tracks[track].clip_slots[scene].clip
        
        clip.remove_notes(oldtime - 0.001, oldpitch, oldlength - 0.002, 1)
        
        newClipNotes = []
        noteDescription = []
        
        noteDescription.append(pitch)
        noteDescription.append(time)
        noteDescription.append(length)
        noteDescription.append(velocity)
        noteDescription.append(mute)
        
        newClipNotes.append(noteDescription)
        clip.set_notes(tuple(newClipNotes))

    
    
    def removeNote(self, msg):
        
        track = msg[2]
        scene = msg[3]
        
        pitch = int(msg[4])
        time = float(msg[5])
        length = float(msg[6])
        
        clip = self.song().tracks[track].clip_slots[scene].clip
        clip.remove_notes(time - 0.001, pitch, length - 0.002, 1)
    
    def removeNotes(self, msg):
        
        track = msg[2]
        scene = msg[3]
        
        pitch = int(msg[4])
        time = float(msg[5])
        length = float(msg[6])
        
        clip = self.song().tracks[track].clip_slots[scene].clip
        clip.remove_notes(time - 0.001, pitch, length - 0.002, 1)
    
    
    
    def stretchNotes(self, msg):
        
        track = msg[2]
        scene = msg[3]
        factor = msg[4]
        clip = self.song().tracks[track].clip_slots[scene].clip

        clipLength = 0
        looping = 0
        if clip.looping:
            clip.looping = 0

            clip.loop_end = (clip.loop_end-clip.loop_start)*factor + clip.loop_start
            
            clip.looping = 1
            looping = 1
            clip.loop_end = (clip.loop_end-clip.loop_start)*factor + clip.loop_start

        else:
            clip.loop_end = (clip.loop_end-clip.loop_start)*factor + clip.loop_start
            
            clip.looping = 1
            clip.loop_end = (clip.loop_end-clip.loop_start)*factor + clip.loop_start
            clip.looping = 0
    

        
        clip.select_all_notes()
        notes = clip.get_selected_notes()


        newClipNotes = []
        
        for note in notes:
            noteDescription = []

            pitch = int(note[0])
            time = float(note[1])
            length = float(note[2])
            velocity = float(note[3])
            mute = bool(note[4])


            length = length*factor
            time = time*factor
            
            noteDescription.append(pitch)
            noteDescription.append(time)
            noteDescription.append(length)
            noteDescription.append(velocity)
            noteDescription.append(mute)
        
            newClipNotes.append(noteDescription)

    
        clip.replace_selected_notes(tuple(newClipNotes))
    
        
        is_audio_clip = int(0)
        warp = 0
        start = 0
        end = 0
        loop_start = 0
        loop_end = 0;
            

        if clip.looping == 1:
            loop_start = clip.loop_start
            loop_end = clip.loop_end
            
            clip.looping = int(0)
            start = clip.loop_start
            end = clip.loop_end
        else:
            start = clip.loop_start
            end = clip.loop_end
            
            clip.looping = 1
            loop_start = clip.loop_start
            loop_end = clip.loop_end

        if looping == 1:
            clip.looping = 1
        else:
            clip.looping = 0

        self.oscServer.sendOSC("/clip/loopstats", (int(track), int(scene), looping, start, end, loop_start, loop_end, is_audio_clip, int(warp)))

    def notesChanged2(self, track, scene, clip):
        notes = [int(track)]
        notes.append(int(scene))
        count = 0
        clip = self.song().tracks[int(track)].clip_slots[int(scene)].clip

        clipNotes = []
        clipNotes = clip.get_selected_notes()
    
        start = clip.start_marker
        end = clip.end_marker
        loopstart = clip.loop_start
        loopend = clip.loop_end
        self.oscServer.sendOSC("/clip/requested_loop_stats", (int(track), int(scene), float(start), float(end), float(loopstart), float(loopend)))
        
        self.oscServer.sendOSC("/clip/start_updating_notes", 1)

        key = '%s.%s' % (track, scene)
    
        noteBuffer = []
        self.noteBuffers[key] = noteBuffer
        
        for note in clipNotes:
            
            for var in note:
                notes.append(float(var))
        
            noteBuffer.append(note)
            
            count = count+1
            if count == 128:
                self.oscServer.sendOSC("/clip/update_notes", tuple(notes))
                count = 0
                notes = [int(track)]
                notes.append(int(scene))
            

        self.oscServer.sendOSC("/clip/update_notes", tuple(notes))
        self.oscServer.sendOSC("/clip/end_updating_notes", 1)



    def notesChanged(self, track, scene, clip):
        notes = [int(track)]
        notes.append(int(scene))
        count = 0
        clip = self.song().tracks[int(track)].clip_slots[int(scene)].clip
        a = Live.Application.get_application().get_major_version()
        clipNotes = []
        
        #if a >= 9:
        clipNotes = clip.get_notes(float(0), int(0), float(100000), int(127))
        #else:

        
        
        """ clipNotes2 = []



        clip.deselect_all_notes()
        clip.select_all_notes()
        
        clipNotes = clip.get_selected_notes()
        
        clip.deselect_all_notes() """
        
        loopstart = 0
        looplength = 0
        start = 0
        end = 0
        looping = 0
        loopend = 0
        version = 0
            
        
        #self.oscServer.sendOSC("/bundle/start", (1))
        start = clip.start_marker
        end = clip.end_marker
        loopstart = clip.loop_start
        loopend = clip.loop_end
        self.oscServer.sendOSC("/clip/requested_loop_stats", (int(track), int(scene), float(start), float(end), float(loopstart), float(loopend)))

        self.oscServer.sendOSC("/clip/start_receiving_notes", (int(track), int(scene)))



        key = '%s.%s' % (track, scene)

        noteBuffer = []
        self.noteBuffers[key] = noteBuffer

        for note in clipNotes:

            for var in note:
                notes.append(float(var))
            
            noteBuffer.append(note)

            count = count+1
            if count == 128:
                self.oscServer.sendOSC("/clip/receive_notes", tuple(notes))
                count = 0
                notes = [int(track)]
                notes.append(int(scene))

        self.oscServer.sendOSC("/clip/receive_notes", tuple(notes))
        self.oscServer.sendOSC("/clip/end_receiving_notes", (int(track), int(scene)))

        #self.oscServer.sendOSC("/finish_loading", (1))
        #self.oscServer.sendOSC("/bundle/end", (1))

        clipNotes2 = clip.get_selected_notes()
        if len(clipNotes2) >= 1:
            self.notesChanged2(track, scene, clip)
            return


    def backFromClip(self, msg):
                
        track = msg[2]
        scene = msg[3]
        
        key = '%s.%s' % (track, scene)
        clip = self.song().tracks[track].clip_slots[scene].clip

        if clip.notes_has_listener(self.noteListeners[clip]) == 1:
            clip.remove_notes_listener(self.noteListeners[clip])
            del self.noteListeners[clip]
       
                
        
    def request_loop_data(self, msg):
        track = msg[2]
        scene = msg[3]
        clip = self.song().tracks[int(track)].clip_slots[int(scene)].clip
        loopstart = 0
        start = 0
        end = 0
        loopend = 0
            
        looping = clip.looping
            
        if looping == 1:
            
            loopstart = clip.loop_start
            loopend = clip.loop_end
            
            clip.looping = 0
            start = clip.loop_start
            end = clip.loop_end
            clip.looping = 1
        
        else:
            start = clip.loop_start
            end = clip.loop_end
            
            clip.looping = 1
            
            loopstart = clip.loop_start
            loopend = clip.loop_end
            clip.looping = 0
        
        try:
            start = clip.start_marker
            end = clip.end_marker
        except:
            pass
                
        self.oscServer.sendOSC("/clip/requested_loop_stats", (int(track), int(scene), float(start), float(end), float(loopstart), float(loopend)))


    

    def loopStartCB(self, msg):
        
        track = msg[2]
        scene = msg[3]
        self.oscServer.sendOSC("/clip/loopstart", 1)
        clip = self.song().tracks[int(track)].clip_slots[int(scene)].clip

        loopStart = msg[4]
        clip.loop_start = loopStart
        self.oscServer.sendOSC("/clip/loopstart", 2)
    
    
    def loopEndCB(self, msg):
        
        track = msg[2]
        scene = msg[3]
        self.oscServer.sendOSC("/clip/loopend", 1)

        clip = self.song().tracks[int(track)].clip_slots[int(scene)].clip

        loopEnd = msg[4]
        self.oscServer.sendOSC("/clip/loopend", 1)
        
        clip.loop_end = loopEnd
        self.oscServer.sendOSC("/clip/loopend", 2)


    def offsetxCB(self, msg):
        """Called when a /offsetx message is received.

        Messages:
        /offsetx     (offset)
        """
        self.offsetx = msg[2]
        self.oscServer.sendOSC("/offsetx", self.offsetx)
        
    def positionsCB(self, msg):
        self.positions()
        
    def meterModeCB(self, msg):

        self.metermode = msg[2]
        self.oscServer.sendOSC("/metermode", self.metermode)

    def sendScriptPong(self):

        #self.oscServer.sendOSC("/script/pong", 310)
        #self._log( "script/pong", True )
        xx = int(self.oscServer.tcpServer.srcPort)
        #self._log(str(xx), True )
        c = Live.Application.get_application().get_bugfix_version()
        b = Live.Application.get_application().get_minor_version()
        a = Live.Application.get_application().get_major_version()
        
        self.oscServer.sendOSCUDP("/script/pong", (415, int(xx), int(a), int(b), int(c),int(self.listeners_updated),int(self.received_midi_cmd)))


    def getStatus(self, msg):   
    	# LMH
        #self.session._ping( msg )
        #self.oscServer.sendOSC("/script/pong", 310)
        #self._log( "script/pong", True )
        xx = int(self.oscServer.tcpServer.srcPort)
        #self._log(str(xx), True )
        c = Live.Application.get_application().get_bugfix_version()
        b = Live.Application.get_application().get_minor_version()
        a = Live.Application.get_application().get_major_version()
        
        self.oscServer.sendOSC("/script/pong", (415, int(xx), int(a), int(b), int(c),int(self.listeners_updated),int(self.received_midi_cmd)))
    
    def getVersion(self, msg):
        
        c = Live.Application.get_application().get_bugfix_version()
        b = Live.Application.get_application().get_minor_version()
        a = Live.Application.get_application().get_major_version()
        self.oscServer.sendOSC("/live/version", (int(a), int(b), int(c)))

    
    
    def getActiveLoops(self, msg):

        for clip in self.oldloop_start:
            if clip != None:
                tr = int(self.trackid[clip])
                cl = int(self.clipid[clip])
                ll = float(self.loop_length[clip])
                self.oscServer.sendOSC('/clip/hotlooping', (int(tr), int(cl), 1, float(ll)))
                
            
    def clearHiddenLoops(self, msg):
        for clip in self.oldloop_start:
            if clip != None:
                if clip.is_playing == 1:
                    clip.looping = 0
                    
                    clip.loop_end = float(self.oldplay_end[clip])
                    clip.loop_start = float(self.oldplay_start[clip])
                    
                    clip.looping = 1
                    
                    clip.loop_end = float(self.oldloop_end[clip])
                    clip.loop_start = float(self.oldloop_start[clip])
                    
                    if clip.loop_end > float(self.oldloop_end[clip]):
                        clip.loop_end = float(self.oldloop_end[clip])
                    else:
                        pass
                    
                    if clip.loop_end < float(self.oldloop_end[clip]):
                        clip.loop_end = float(self.oldloop_end[clip])
                    else:
                        pass
                    
                    clip.looping = int(self.oldlooping[clip])
                    
                    tr = int(self.trackid[clip])
                    cl = int(self.clipid[clip])

                    del self.oldplay_start[clip]
                    del self.oldplay_end[clip]
                    del self.oldloop_start[clip]
                    del self.oldloop_end[clip]
                    del self.oldlooping[clip]
                    del self.hotlooping[clip]
                    del self.loop_length[clip]
                    del self.trackid[clip]
                    del self.clipid[clip]
                    self.oscServer.sendOSC('/clip/hotlooping', (int(tr), int(cl), 0, float(4)))
                else:
                    pass
            else:
                pass
            
   
    
    def changeLoopCB(self, msg):
        
        tr = msg[2]
        cl = msg[3]
        length = msg[4]
        
        clip2 = LiveUtils.getClip(tr, cl)
        clip2.loop_end = clip2.loop_start + length
        clip2.looping = 0
        clip2.loop_end = clip2.loop_start + length
        clip2.looping = 1
        for clip in self.loop_length:
            if clip != None:
                if clip == clip2:
                    self.loop_length[clip] = float(length)
        
        self.oscServer.sendOSC('/clip/hotlooping', (int(tr), int(cl), 1, float(length)))

                    
    def clip_loopstats(self, clip, tid, cid):
        
        clip = LiveUtils.getClip(tid, cid)
        isLooping = int(clip.looping)
        self.oscServer.sendOSC('/clip/sdsd', (tid, cid))

        if clip.looping == 1:
            loop_start = clip.loop_start
            loop_end = clip.loop_end
            
            clip.looping = 0
            start = clip.loop_start
            end = clip.loop_end
        else:
            start = clip.loop_start
            end = clip.loop_end
            
            clip.looping = 1
            loop_start = clip.loop_start
            loop_end = clip.loop_end
        
        clip.looping = isLooping
        self.oscServer.sendOSC('/clip/loopstats', (tid, cid, isLooping, start, end, loop_start, loop_end))
    

    def clip_loopstats2(self, msg):
                    
        tid = msg[2]
        cid = msg[3]
                                                
        clip = LiveUtils.getClip(tid, cid)
            
        isLooping = int(clip.looping)
        
        if clip.looping == 1:
            loop_start = clip.loop_start
            loop_end = clip.loop_end
                            
            clip.looping = int(0)
            start = clip.loop_start
            end = clip.loop_end
        else:
            start = clip.loop_start
            end = clip.loop_end
                            
            clip.looping = 1
            loop_start = clip.loop_start
            loop_end = clip.loop_end
                        
        clip.looping = isLooping
        self.oscServer.sendOSC('/clip/loopstats', (tid, cid, isLooping, start, end, loop_start, loop_end))

    
    #self.oscServer.sendOSC('/oldLoopData', (track, clip, looping, loopStart, loopLength))

    def keepLoop(self, msg):
        tr = msg[2]
        cl = msg[3]
        clip2 = LiveUtils.getClip(tr, cl)
        for clip in self.oldloop_start:
            if clip != None:
                if clip == clip2:
                    del self.oldplay_start[clip]
                    del self.oldplay_end[clip]
                    del self.oldloop_start[clip]
                    del self.oldloop_end[clip]
                    del self.oldlooping[clip]
                    del self.hotlooping[clip]
                    del self.loop_length[clip]
                    del self.trackid[clip]
                    del self.clipid[clip]
                    self.oscServer.sendOSC('/clip/hotlooping', (int(tr), int(cl), 0, float(4)))
    
    def jumpForwardCB(self, msg):
        
        tr = msg[2]
        cl = msg[3]
        length = msg[4]
        clip = LiveUtils.getClip(tr, cl)
        
        clip.move_playing_pos(length)
    
    def jumpBackwardCB(self, msg):
        
        tr = msg[2]
        cl = msg[3]
        length = msg[4]
        clip = LiveUtils.getClip(tr, cl)
        
        clip.move_playing_pos(length)
    
    
    def jumpLoopForward(self, msg):
        
        tr = msg[2]
        cl = msg[3]
        length = msg[4]
        
        clip = LiveUtils.getClip(tr, cl)
        clip.looping = 1
        start = clip.loop_start
        
        clip.loop_end = clip.loop_end + length
        clip.move_playing_pos(length)
        clip.loop_start = start + length
        
        #end = clip.loop_end
        #start = clip.loop_start
        #size = end - start
        
        #clip.looping = 0
        
        
        #clip.loop_end = end
        #clip.loop_start = start

        #if end > start + length:
        #clip.loop_start = start + length
        #else:
        #clip.loop_start = end - length
        #clip.looping = 1

    
    
    
    
    def jumpLoopBackward(self, msg):
        
        tr = msg[2]
        cl = msg[3]
        length = msg[4]
        clip = LiveUtils.getClip(tr, cl)
        start = clip.loop_start
        
        clip.looping = 1
        
        size = clip.loop_end - start
        
        if start+length > 0:
            clip.loop_start = start + length
            #clip.move_playing_pos(size)
            clip.loop_end = clip.loop_end + length
            #start = clip.loop_start
        else:
            clip.loop_start = 0
            clip.loop_end = size
            #start = 0
        clip.move_playing_pos(length)
                
        #end = clip.loop_end
        #start = clip.loop_start
        #clip.looping = 0
            
        #clip.loop_end = end
        #clip.loop_start = start
        #clip.looping = 1
            
            
######################################################################
# Standard Ableton Methods

    def connect_script_instances(self, instanciated_scripts):
        """
        Called by the Application as soon as all scripts are initialized.
        You can connect yourself to other running scripts here, as we do it
        connect the extension modules
        """
        return

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        #self.oscServer.sendOSC('/NSLOG_REPLACE', "refresh_state.")

        """
        To be called from any components, as soon as their internal state changed in a 
        way, that we do need to remap the mappings that are processed directly by the 
        Live engine.
        Dont assume that the request will immediately result in a call to
        your build_midi_map function. For performance reasons this is only
        called once per GUI frame.
        """
        return
    
    def update_display(self):
        """
        This function is run every 100ms, so we use it to initiate our Song.current_song_time
        listener to allow us to process incoming OSC commands as quickly as possible under
        the current listener scheme.
        """
        ######################################################
        # START OSC LISTENER SETUP


        if self.basicAPI == 0:
            # By default we have set basicAPI to 0 so that we can assign it after
            # initialization. We try to get the current song and if we can we'll
            # connect our basicAPI callbacks to the listener allowing us to 
            # respond to incoming OSC every 60ms.
            #
            # Since this method is called every 100ms regardless of the song time
            # changing, we use both methods for processing incoming UDP requests
            # so that from a resting state you can initiate play/clip triggering.
            
            try:
                doc = self.song()
            except:
                return
            try:
                # LMH
                self.basicAPI = touchAbleCallbacks.touchAbleCallbacks(self._touchAble__c_instance, self.oscServer, self)
                # Commented for stability
                #doc.add_current_song_time_listener(self.oscServer.processIncomingUDP)
                #self.oscServer.sendOSC("/server/refresh", (1))

                
            except:
                return
    
            
            # If our OSC server is listening, try processing incoming requests.
            # Any 'play' initiation will trigger the current_song_time listener
            # and bump updates from 100ms to 60ms.

        
        
            
        if self.oscServer:
            try:
                #self.oscServer.sendOSC('/processingOSC', (1))
                
                self.oscServer.processIncomingUDP()
        
            except:
                pass
        #self.updateTime = self.updateTime +4
        #if self.updateTime >= 100:

        self.sendScriptPong()
        #if self.oscServer:
            #self.positions()
            #self.mastermeters()
            #self.meters()
            #self.songtime_change()


            #self.updateTime = 0

            
        # END OSC LISTENER SETUP
        ######################################################

    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices 
        that this script is assigned to.
        """
        pass

    def receive_midi(self,midi_bytes):
        #self.oscServer.sendOSC('/midi/received', (midi_bytes))
        #if self.did_init_osc_server == 0:
            #self.do_init()
            #self.do_init()
            #thread.start_new_thread(self.do_init(),("osc_init",1,))

        if midi_bytes[0] == 240 and self.did_init == 1:
            self.received_midi_cmd = 1
            if midi_bytes[1] == 2:
                self.updateCB()
            elif self.oscServer:
                try:
                    #self.oscServer.sendOSCUDP("/NSLOG_REPLACE", "DATA RECEIVED 0")
                    self.oscServer.processIncomingUDP()
                except:
                    pass
        else:
            pass
        
        
            
    def can_lock_to_devices(self):
        return True
    
    def lock_to_device(self, device):
        ControlSurface.lock_to_device(self, device)
        self.log_message("locking to device..")
        pass
    def unlock_from_device(self, device):
        ControlSurface.unlock_from_device(self, device)
        self.log_message("unlocking from device..")
        pass

    def suggest_input_port(self):
        return 'touchAble Script Input'

    def suggest_output_port(self):
        return ''

    def suggest_map_mode(self, cc_no, channel):
        return Live.MidiMap.MapMode.absolute
    
    def __handle_display_switch_ids(self, switch_id, value):
        pass
    
    
######################################################################
# Useful Methods


    def getOSCServer(self):
        return self.oscServer
    
    def application(self):
        """returns a reference to the application that we are running in"""
        return Live.Application.get_application()

    def song(self):
        """returns a reference to the Live Song that we do interact with"""
        return self._touchAble__c_instance.song()

    def handle(self):
        """returns a handle to the c_interface that is needed when forwarding MIDI events via the MIDI map"""
        return self._touchAble__c_instance.handle()
    def log(self, msg):
        if self._LOG == 1:
            self.logger.log(msg) 
            
    def getslots(self):
        tracks = self.song().tracks

        clipSlots = []
        for track in tracks:
            clipSlots.append(track.clip_slots)
        return clipSlots


    def positions(self):
        tracks = self.song().tracks
        pos = 0
        ps = 0
        if self.song().is_playing != 4:
            #self.oscServer.sendOSC("/bundle/start", 1)
            for i in range(len(tracks)):
                track = tracks[i]
                if track.is_foldable != 1:
                    if track.playing_slot_index != -2:
                        if track.playing_slot_index != -1:
                            ps = track.playing_slot_index
                            clip = track.clip_slots[ps].clip
                            playing_pos = 0
                            pos = 0
                            try:
                                playing_pos = clip.playing_position
                                if clip.looping == 1:
                                    if clip.playing_position < clip.loop_start:
                                        #clip.looping = 0
                                        start = clip.loop_start
                                        end = clip.loop_end
                                        #clip.looping = 1
                                        pos = 1 - round((end - clip.playing_position) / end, 6)
                                            #pos = round((clip.loop_start - clip.playing_position) / (clip.loop_start - start), 3)
                                    else:
                                        pos = round((clip.playing_position - clip.loop_start) / (clip.loop_end - clip.loop_start), 6)

                                else:
                                    pos = round((clip.playing_position-clip.loop_start) / (clip.loop_end - clip.loop_start), 6)
                            except:
                                asddd = 1

                            self.oscServer.sendOSC('/clip/playing_position',(i, ps, pos, playing_pos))
                        else:
                            pass
                    else:
                        pass

                else:
                    pass
            #self.oscServer.sendOSC("/bundle/end", (1))

        else:
            pass

            


    def meters(self):
        #self.oscServer.sendOSC("/bundle/start", 1)
        tracks = self.song().tracks
        vall = 0
        valr = 0
        for i in range (len(tracks)):
            track = tracks[i]
            if track.has_audio_output:
                vall = track.output_meter_left
                valr = track.output_meter_right
            else:
                vall = -1.0 * track.output_meter_level -1.0
                valr = 0
            
            vall = round(vall, 4)
            valr = round(valr, 4)
            sum = vall + valr
            if sum != self.mlcache[i]:
                self.oscServer.sendOSC('/track/meter',(i,vall, valr))
                self.mlcache[i] = sum
            else:
                pass
        #self.oscServer.sendOSC("/bundle/end", (1))


            

    def mastermeters(self):
        tracks = self.song().return_tracks
        vall = self.song().master_track.output_meter_left
        valr = self.song().master_track.output_meter_right
        
        vall = round(vall, 4)
        valr = round(valr, 4)

        if vall != self.mmcache:
            self.oscServer.sendOSC('/master/meter',(vall, valr))
            if vall == 0:
                self.oscServer.sendOSC('/master/meter',(0.0000000001,0000000.1))   
            self.mmcache = vall                    
        i = 0
        for track in tracks:
            vall = track.output_meter_left
            valr = track.output_meter_right

            vall = round(vall, 4)
            valr = round(valr, 4)

            if vall != self.mrcache[i]:
                self.oscServer.sendOSC('/return/meter',(i, vall, valr))
                self.mrcache[i] = vall
            else:
                pass
            i = i+1

        

        
######################################################################
# Used Ableton Methods

    def disconnect(self):
        
        try:
            try:
                self.rem_clip_listeners()
            except:
                self.log_message("rem_clip_listeners failed")
            
            
            try:
                self.rem_mixer_listeners()
            except:
                self.log_message("rem_mixer_listeners failed")
            
            
            try:
                self.rem_scene_listeners()
            except:
                self.log_message("rem_scene_listeners failed")
            
            
            try:
                self.rem_xFader_listeners()
            except:
                self.log_message("rem_xFader_listeners failed")
            
            
            try:
                self.rem_tempo_listener()
            except:
                self.log_message("rem_tempo_listener failed")
            
            
            try:
                self.rem_overdub_listener()
            except:
                self.log_message("rem_overdub_listener failed")
            
            
            try:
                self.rem_metronome_listener()
            except:
                self.log_message("rem_metronome_listener failed")
            
            
           
            try:
                self.rem_session_record_listener()
                self.rem_session_record_status_listener()
                self.rem_re_enable_automation_enabled_listener()
                self.rem_session_automation_record_listener()
                self.rem_arrangement_overdub_listener()

            except:
                self.log_message("remove live 9 listeners failed")


            try:
                self.rem_record_listener()
            except:
                self.log_message("rem_record_listener failed")

            try:
                self.rem_scenes_listener()
            except:
                self.log_message("rem_scenes_listener failed")
            
            try:
                self.rem_tracks_listener()
            except:
                self.log_message("rem_tracks_listener failed")
            
            try:
                self.rem_all_device_listeners()
            except:
                self.log_message("rem_all_device_listeners failed")
            
            try:
                self.rem_transport_listener()
            except:
                self.log_message("rem_transport_listener failed")
            
            try:
                self.rem_scenes_listeners()
            except:
                self.log_message("rem_scenes_listeners failed")
            
            try:
                self.rem_quant_listeners()
            except:
                self.log_message("rem_quant_listeners failed")
                    
            self.oscServer.sendOSC('/remix/oscserver/shutdown', 1)
            self.oscServer.shutdown()

        except:
            self.oscServer.sendOSC('/remix/oscserver/shutdown', 1)
            self.oscServer.shutdown()
                
                


    def build_midi_map(self, midi_map_handle):
        pass

    
    def refresh_state(self):
        pass


    def update_all_listeners(self):

        self.oscServer.sendOSC("/NSLOG_REPLACE", "update all listener")

        self.add_clip_listeners()
        self.add_mixer_listeners()
        self.add_scene_listeners()
        self.add_xFader_listeners()
        self.add_RxFader_listeners()
        self.add_tempo_listener()
        self.add_overdub_listener()
        self.add_metronome_listener()
        try:
            self.add_session_record_listener()
            self.add_session_record_status_listener()
            self.add_re_enable_automation_enabled_listener()
            self.add_session_automation_record_listener()
            self.add_arrangement_overdub_listener()
            self.oscServer.sendOSC('/remix/oscserver/startup', 2)
        
        except:
            self.oscServer.sendOSC("live/", 8)

        self.add_record_listener()
        self.add_tracks_listener()
        self.add_scenes_listener()
        self.add_device_listeners()
        self.add_transport_listener()
        self.add_scenes_listeners()
        self.add_quant_listeners()
        self.tracks_change()

        self.oscServer.sendOSC("/NSLOG_REPLACE","listeners updated AFTER thread")

    def update_track_listeners(self):
        self.add_clip_listeners()
        self.add_mixer_listeners()
        self.add_xFader_listeners()
        self.add_device_listeners()
    
    
    def update_return_listeners(self):
        self.add_mixer_listeners()
        self.add_RxFader_listeners()
        self.add_device_listeners()

    def update_scene_listeners(self):
        self.add_clip_listeners()
        self.add_scenes_listeners()
        self.add_scenes_listener()


    def update_state(self):
        i = 0
        for track in self.song().tracks:
            self.oscServer.sendOSC("/track/is_grouped", (int(i), int(track.is_grouped)))
            self.oscServer.sendOSC("/track/is_visible", (int(i), int(track.is_visible)))
            i = i+1
        self.oscServer.sendOSC("/track/update_state", (1))




######################################################################
# Add / Remove Listeners   
    def add_scene_listeners(self):
        self.rem_scene_listeners()
        if self.song().view.selected_scene_has_listener(self.scene_change) != 1:
            self.song().view.add_selected_scene_listener(self.scene_change)

        if self.song().view.selected_track_has_listener(self.track_change) != 1:
            self.song().view.add_selected_track_listener(self.track_change)
             
      
    def add_xFader_listeners(self):
        self.rem_xFader_listeners()
        tracks = self.song().tracks
        for tr in range (len(tracks)):
            track = tracks[tr]
            self.add_xfade_listener(track, tr)
    
    def add_xfade_listener(self, track, tr):
        cb = lambda :self.xfade_assign_changed(track, tr)
        if self.ablisten.has_key(track) != 1:
            track.mixer_device.add_crossfade_assign_listener(cb)
            self.ablisten[track] = cb
        else:
            pass
    
    def rem_xFader_listeners(self):
        for track in self.ablisten:
            if track != None:
                if track.mixer_device.crossfade_assign_has_listener(self.ablisten[track]) == 1:
                    track.mixer_device.remove_crossfade_assign_listener(self.ablisten[track])
            else:
                pass
        self.ablisten = {}


    def xfade_assign_changed(self, track, tr):
        assign = 0
        assign = track.mixer_device.crossfade_assign
        self.oscServer.sendOSC("/track/crossfade_assign", (int(tr), int(assign)))
                
    
    
    
    
    def add_RxFader_listeners(self):
        self.rem_RxFader_listeners()
        tracks = self.song().return_tracks
        for tr in range (len(tracks)):
            track = tracks[tr]
            self.add_Rxfade_listener(track, tr)
    
    def add_Rxfade_listener(self, track, tr):
        cb = lambda :self.Rxfade_assign_changed(track, tr)
        if self.Rablisten.has_key(track) != 1:
            track.mixer_device.add_crossfade_assign_listener(cb)
            self.Rablisten[track] = cb
        else:
            pass
    
    def rem_RxFader_listeners(self):
        for track in self.Rablisten:
            if track != None:
                if track.mixer_device.crossfade_assign_has_listener(self.Rablisten[track]) == 1:
                    track.mixer_device.remove_crossfade_assign_listener(self.Rablisten[track])
            else:
                pass
        self.Rablisten = {}
    
    
    def Rxfade_assign_changed(self, track, tr):
        assign = 0
        assign = track.mixer_device.crossfade_assign
        self.oscServer.sendOSC("/return/crossfade_assign", (int(tr), int(assign)))                    

    
    
    
    
    
    def rem_scene_listeners(self):
        if self.song().view.selected_scene_has_listener(self.scene_change) == 1:
            self.song().view.remove_selected_scene_listener(self.scene_change)
            
        if self.song().view.selected_track_has_listener(self.track_change) == 1:
            self.song().view.remove_selected_track_listener(self.track_change)

      

    def track_change(self):
        selected_track = self.song().view.selected_track
        tracks = self.song().tracks
        returns = self.song().return_tracks

        index = 0
        selected_index = 0
        for track in tracks:
            if track == selected_track:
                selected_index = index
                self.oscServer.sendOSC("/set/selected_track", (0, (selected_index)))
            index = index + 1


        
        index = 0
        for ret in returns:
            if ret == selected_track:
                selected_index = index
                self.oscServer.sendOSC("/set/selected_track", (2, (selected_index)))
            index = index + 1


        if selected_track == self.song().master_track:
            self.oscServer.sendOSC("/set/selected_track", 1)

            

    def scene_change(self):
        selected_scene = self.song().view.selected_scene
        scenes = self.song().scenes
        index = 0
        selected_index = 0
        for scene in scenes:
            index = index + 1        
            if scene == selected_scene:
                selected_index = index
                
        if selected_index != self.scene:
            self.scene = selected_index
            self.oscServer.sendOSC("/set/selected_scene", (selected_index))
	
    def add_tempo_listener(self):
        self.rem_tempo_listener()
            
        if self.song().tempo_has_listener(self.tempo_change) != 1:
            self.song().add_tempo_listener(self.tempo_change)
        
    def rem_tempo_listener(self):
        if self.song().tempo_has_listener(self.tempo_change) == 1:
            self.song().remove_tempo_listener(self.tempo_change)
    
    def tempo_change(self):
        tempo = LiveUtils.getTempo()
        self.oscServer.sendOSC("/set/tempo", (tempo))

    def add_quant_listeners(self):
        self.rem_quant_listeners()

        if self.song().clip_trigger_quantization_has_listener(self.quant_change) != 1:
            self.song().add_clip_trigger_quantization_listener(self.quant_change)
            
        if self.song().midi_recording_quantization_has_listener(self.quant_change) != 1:
            self.song().add_midi_recording_quantization_listener(self.quant_change)
        
    def rem_quant_listeners(self):
        if self.song().clip_trigger_quantization_has_listener(self.quant_change) == 1:
            self.song().remove_clip_trigger_quantization_listener(self.quant_change)
        if self.song().midi_recording_quantization_has_listener(self.quant_change) == 1:
            self.song().remove_midi_recording_quantization_listener(self.quant_change)

    def quant_change(self):
        tquant = self.song().clip_trigger_quantization
        rquant = self.song().midi_recording_quantization
        self.oscServer.sendOSC("/set/quantization", (int(self.song().clip_trigger_quantization), int(self.song().midi_recording_quantization)))   
        
	
    def add_transport_listener(self):
        if self.song().is_playing_has_listener(self.transport_change) != 1:
            self.song().add_is_playing_listener(self.transport_change)
        #if self.song().current_song_time_has_listener(self.songtime_change) != 1:
            #self.song().add_current_song_time_listener(self.songtime_change)
            
    def rem_transport_listener(self):
        if self.song().is_playing_has_listener(self.transport_change) == 1:
            self.song().remove_is_playing_listener(self.transport_change)
        #if self.song().master_track.mixer_device.cue_volume(self.cuelevel) == 1:
            #self.song().master_track.mixer_device.addc(self.cuev level)
    
    def transport_change(self):
        self.oscServer.sendOSC("/set/playing_status", (self.song().is_playing and 2 or 1))

    def songtime_change(self):
        denom = self.song().signature_denominator
        numer = self.song().signature_numerator
        self.oscServer.sendOSC("/set/playing_position", (self.song().current_song_time,float(numer),float(denom)))


    def add_session_record_listener(self):
        self.rem_session_record_listener()
        
        if self.song().session_record_has_listener(self.session_record_change) != 1:
            self.song().add_session_record_listener(self.session_record_change)

    def rem_session_record_listener(self):
        if self.song().session_record_has_listener(self.session_record_change) == 1:
            self.song().remove_session_record_listener(self.session_record_change)


    def add_session_record_status_listener(self):
        self.rem_session_record_status_listener()
        
        if self.song().session_record_status_has_listener(self.session_record_status_changed) != 1:
            self.song().add_session_record_status_listener(self.session_record_status_changed)
    
    def rem_session_record_status_listener(self):
        if self.song().session_record_status_has_listener(self.session_record_status_changed) == 1:
            self.song().remove_session_record_status_listener(self.session_record_status_changed)


    def add_re_enable_automation_enabled_listener(self):
        self.rem_re_enable_automation_enabled_listener()
        
        if self.song().re_enable_automation_enabled_has_listener(self.re_enable_automation_enabled_changed) != 1:
            self.song().add_re_enable_automation_enabled_listener(self.re_enable_automation_enabled_changed)
    
    def rem_re_enable_automation_enabled_listener(self):
        if self.song().re_enable_automation_enabled_has_listener(self.re_enable_automation_enabled_changed) == 1:
            self.song().remove_re_enable_automation_enabled_listener(self.re_enable_automation_enabled_changed)



    def add_session_automation_record_listener(self):
        self.rem_session_automation_record_listener()
        
        if self.song().session_automation_record_has_listener(self.session_automation_record_change) != 1:
            self.song().add_session_automation_record_listener(self.session_automation_record_change)
    
    def rem_session_automation_record_listener(self):
        if self.song().session_automation_record_has_listener(self.session_automation_record_change) == 1:
            self.song().remove_session_automation_record_listener(self.session_automation_record_change)

    
    def add_arrangement_overdub_listener(self):
        self.rem_arrangement_overdub_listener()
        
        if self.song().arrangement_overdub_has_listener(self.overdub_change) != 1:
            self.song().add_arrangement_overdub_listener(self.overdub_change)
    
    def rem_arrangement_overdub_listener(self):
        if self.song().arrangement_overdub_has_listener(self.overdub_change) == 1:
            self.song().remove_arrangement_overdub_listener(self.overdub_change)



    def session_record_change(self):
        overdub = self.song().session_record
        self.oscServer.sendOSC("/live/set/session_record", (int(overdub)+1))
    
        trackNumber = 0
        numberOfTracks = len(self.song().tracks)
        for i in range(numberOfTracks):
            track = self.song().tracks[i]
            if track.can_be_armed == 1:
                if track.arm == 1:
                    if track.playing_slot_index != -2:
                        if track.playing_slot_index != -1:
                            tid = trackNumber
                            cid = track.playing_slot_index
                            if track.clip_slots[cid].clip.is_audio_clip == 0:
                                if overdub == 1:
                                    self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 3))
                                else:
                                    self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 1))
                            else:
                                self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 3))
        
            trackNumber = trackNumber+1
    

    def session_record_status_changed(self):
        overdub = self.song().session_record_status
        self.oscServer.sendOSC("/live/set/session_record_status", (int(overdub)+1))

    def re_enable_automation_enabled_changed(self):
        overdub = self.song().re_enable_automation_enabled
        self.oscServer.sendOSC("/live/set/re_enable_automation_enabled", (int(overdub)+1))

    def session_automation_record_change(self):
        overdub = self.song().session_automation_record
        self.oscServer.sendOSC("/live/set/session_automation_record", (int(overdub)+1))

    
    
    def session_record_chang(self, msg):
        
        session_record = msg[2]

        
        self.song().session_record = session_record
    
    def sesion_capture_midi(self, msg):
        
        self.song().capture_midi()
    
    
    def session_record_status_chang(self, msg):
        
        newActive = 0

        selected_scene = self.song().view.selected_scene

        index = 0
        selected_index = 0
        for scene in self.song().scenes:
            if scene == selected_scene:
                selected_index = index
            index = index + 1

        

        tracks = self.song().tracks
        
        for track in tracks:
            if track.can_be_armed:
                if track.arm:
                    if track.clip_slots[selected_index].clip != None:
                        newActive = 1;
                        break

        if newActive == 1:
            
            maxScenes = len(self.song().scenes)
            startIndex = selected_index
            sceneIsEmpty = 0
            newSceneIndex = 0
            
            for i in range(startIndex, maxScenes):
                sceneIsEmpty = 1
                for track in tracks:
                    if track.can_be_armed:
                        if track.arm:
                            if track.clip_slots[i].clip != None:
                                sceneIsEmpty = 0;

                                break
                if sceneIsEmpty == 1:
                    newSceneIndex = i
                    break
            
            if len(self.song().scenes) == newSceneIndex:
                self.song().create_scene()
            
            newScene = self.song().scenes[newSceneIndex]
            self.song().view.selected_scene = newScene

            for track in tracks:
                if track.can_be_armed:
                    if track.arm:
                        track.stop_all_clips()
                            




    def re_enable_automation_enabled_chang(self, msg):
        self.song().re_enable_automation()
    
    
    def session_automation_record_chang(self, msg):
        
        session_automation_record = msg[2]
        
        self.song().session_automation_record = session_automation_record


    def add_overdub_listener(self):
        self.rem_overdub_listener()
    
        if self.song().overdub_has_listener(self.overdub_change) != 1:
            self.song().add_overdub_listener(self.overdub_change)
	    
    def rem_overdub_listener(self):
        if self.song().overdub_has_listener(self.overdub_change) == 1:
            self.song().remove_overdub_listener(self.overdub_change)

    def add_metronome_listener(self):
        self.rem_metronome_listener()
    
        if self.song().metronome_has_listener(self.metronome_change) != 1:
            self.song().add_metronome_listener(self.metronome_change)
	    
    def rem_metronome_listener(self):
        if self.song().metronome_has_listener(self.metronome_change) == 1:
            self.song().remove_metronome_listener(self.metronome_change)

    def metronome_change(self):
        metronome = LiveUtils.getSong().metronome
        self.oscServer.sendOSC("/set/metronome_status", (int(metronome) + 1))
        
    def overdub_change(self):
        try:
            overdub = LiveUtils.getSong().arrangement_overdub
        except:
            overdub = LiveUtils.getSong().overdub

        self.oscServer.sendOSC("/set/overdub_status", (int(overdub) + 1))
        trackNumber = 0
        if self.application().get_major_version() == 8:
            for track in self.song().tracks:
                if track.can_be_armed == 1:
                    if track.arm == 1:
                        if track.playing_slot_index != -2:
                            tid = trackNumber
                            cid = track.playing_slot_index
                            if track.clip_slots[cid].clip.is_audio_clip == 0:
                                if overdub == 1:
                                    self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 3))
                                else:
                                    self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 1))
                            else:
                                self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 3))
        
                trackNumber = trackNumber+1



    def add_record_listener(self):
        self.rem_record_listener()
    
        if self.song().record_mode_has_listener(self.record_change) != 1:
            self.song().add_record_mode_listener(self.record_change)
	    
    def rem_record_listener(self):
        if self.song().record_mode_has_listener(self.record_change) == 1:
            self.song().remove_record_mode_listener(self.record_change)

    def record_change(self):
        record = LiveUtils.getSong().record_mode
        self.oscServer.sendOSC("/set/recording_status", (int(record) + 1))
	
    def add_tracks_listener(self):
        self.rem_tracks_listener()
    
        if self.song().tracks_has_listener(self.tracks_change) != 1:
            self.song().add_tracks_listener(self.tracks_change)
    
        if self.song().visible_tracks_has_listener(self.update_state) != 1:
            self.song().add_visible_tracks_listener(self.update_state)
        
        if self.song().return_tracks_has_listener(self.returns_change) != 1:
            self.song().add_return_tracks_listener(self.returns_change)

    def rem_tracks_listener(self):
        if self.song().tracks_has_listener(self.tracks_change) == 1:
            self.song().remove_tracks_listener(self.tracks_change)
        
        if self.song().visible_tracks_has_listener(self.update_state) == 1:
            self.song().remove_visible_tracks_listener(self.update_state)
        
        if self.song().return_tracks_has_listener(self.returns_change) == 1:
            self.song().remove_return_tracks_listener(self.returns_change)
    
    def tracks_change(self):
        self.update_track_listeners()
        self.oscServer.sendOSC("/server/refresh", (1))

    def returns_change(self):
        self.update_return_listeners()
        self.oscServer.sendOSC("/server/refresh", (1))

    def add_scenes_listener(self):
        self.rem_scenes_listener()
    
        if self.song().scenes_has_listener(self.scenes_change) != 1:
            self.song().add_scenes_listener(self.scenes_change)


    def scenes_change(self):
        self.update_scene_listeners()
        self.oscServer.sendOSC("/server/refresh", (1))

    
    def rem_scenes_listener(self):
        if self.song().scenes_has_listener(self.scenes_change) == 1:
            self.song().remove_scenes_listener(self.scenes_change)

            
    def rem_clip_listeners(self):
        self.log("** Remove Listeners **")
    
        for slot in self.slisten:
            if slot != None:
                if slot.has_clip_has_listener(self.slisten[slot]) == 1:
                    slot.remove_has_clip_listener(self.slisten[slot])
                    
        self.slisten = {}
    

        for slot in self.sslisten:
            if slot != None:
                if slot.has_stop_button_has_listener(self.sslisten[slot]) == 1:
                    slot.remove_has_stop_button_listener(self.sslisten[slot])
                    
        self.sslisten = {}
    
        
        for clip in self.clisten:
            if clip != None:
                if clip.playing_status_has_listener(self.clisten[clip]) == 1:
                    clip.remove_playing_status_listener(self.clisten[clip])
                
        self.clisten = {}

        for clip in self.pplisten:
            if clip != None:
                if clip.playing_position_has_listener(self.pplisten[clip]) == 1:
                    clip.remove_playing_position_listener(self.pplisten[clip])
                
        self.pplisten = {}
    

        for clip in self.cnlisten:
            if clip != None:
                if clip.name_has_listener(self.cnlisten[clip]) == 1:
                    clip.remove_name_listener(self.cnlisten[clip])
                
        self.cnlisten = {}
        
        for clip in self.smlisten:
            if clip != None:
                if clip.start_marker_has_listener(self.smlisten[clip]) == 1:
                    clip.remove_start_marker_listener(self.smlisten[clip])
                    
        self.smlisten = {}
        
        for clip in self.emlisten:
            if clip != None:
                if clip.end_marker_has_listener(self.emlisten[clip]) == 1:
                    clip.remove_end_marker_listener(self.emlisten[clip])

        self.emlisten = {}
        
        for clip in self.lslisten:
            if clip != None:
                if clip.loop_start_has_listener(self.lslisten[clip]) == 1:
                    clip.remove_loop_start_listener(self.lslisten[clip])
                    
        self.lslisten = {}
        
        for clip in self.lelisten:
            if clip != None:
                if clip.loop_end_has_listener(self.lelisten[clip]) == 1:
                    clip.remove_loop_end_listener(self.lelisten[clip])

        self.lelisten = {}
        
        for clip in self.cliplooplisten:
            if clip != None:
                if clip.looping_has_listener(self.cliplooplisten[clip]) == 1:
                    clip.remove_looping_listener(self.cliplooplisten[clip])
                    
        self.cliplooplisten = {}
        
        for clip in self.clipwarplisten:
            if clip != None:
                if clip.warping_has_listener(self.clipwarplisten[clip]) == 1:
                    clip.remove_warping_listener(self.clipwarplisten[clip])
                    
        self.clipwarplisten = {}
        
        
        
        for clip in self.clipwarpmodelisten:
            if clip != None:
                if clip.warp_mode_has_listener(self.clipwarpmodelisten[clip]) == 1:
                    clip.remove_warp_mode_listener(self.clipwarpmodelisten[clip])
                    
        self.clipwarpmodelisten = {}



        for clip in self.clipmutelisten:
            if clip != None:
                if clip.muted_has_listener(self.clipmutelisten[clip]) == 1:
                    clip.remove_muted_listener(self.clipmutelisten[clip])
        
        self.clipmutelisten = {}
        
        for clip in self.clipgainlisten:
            if clip != None:
                if clip.gain_has_listener(self.clipgainlisten[clip]) == 1:
                    clip.remove_gain_listener(self.clipgainlisten[clip])
                    
        self.clipgainlisten = {}
        
        for clip in self.clipcoarselisten:
            if clip != None:
                if clip.pitch_coarse_has_listener(self.clipcoarselisten[clip]) == 1:
                    clip.remove_pitch_coarse_listener(self.clipcoarselisten[clip])
                    
        self.clipcoarselisten = {}
        
        for clip in self.clipfinelisten:
            if clip != None:
                if clip.pitch_fine_has_listener(self.clipfinelisten[clip]) == 1:
                    clip.remove_pitch_fine_listener(self.clipfinelisten[clip])
        
        self.clipfinelisten = {}
        


        for clip in self.cclisten:
            if clip != None:
                if clip.color_has_listener(self.cclisten[clip]) == 1:
                    clip.remove_color_listener(self.cclisten[clip])
                
        self.cclisten = {}

        for clip in self.noteListeners:
            if clip != None:
                if clip.notes_has_listener(self.noteListeners[clip]) == 1:
                    clip.remove_notes_listener(self.noteListeners[clip])

        self.noteListeners = {}

        for clip in self.fplisten:
            if clip != None:
                if clip.file_path_has_listener(self.fplisten[clip]) == 1:
                    clip.remove_file_path_listener(self.fplisten[clip])
        
        self.fplisten = {}


    def add_scenes_listeners(self):
        self.rem_scenes_listeners()
        scenes = self.song().scenes
        for sc in range (len(scenes)):
            scene = scenes[sc]
            self.add_scenelistener(scene, sc)

    def rem_scenes_listeners(self):
        for scene in self.sclisten:
            if scene != None:
                if scene.color_has_listener(self.sclisten[scene]) == 1:
                    scene.remove_color_listener(self.sclisten[scene])
            else:
                pass
        self.sclisten = {}

        for scene in self.snlisten:
            if scene != None:
                if scene.name_has_listener(self.snlisten[scene]) == 1:
                    scene.remove_name_listener(self.snlisten[scene])
            else:
                pass
        self.snlisten = {}
        
        for scene in self.stlisten:
            if scene != None:
                if scene.is_triggered_has_listener(self.stlisten[scene]) == 1:
                    scene.remove_is_triggered_listener(self.stlisten[scene])
            else:
                pass
        self.stlisten = {}
            

    def add_scenelistener(self, scene, sc):
        cb = lambda :self.scene_color_changestate(scene, sc)
        if self.sclisten.has_key(scene) != 1:
            scene.add_color_listener(cb)
            self.sclisten[scene] = cb
        else:
            pass
            
        cb2 = lambda :self.scene_name_changestate(scene, sc)
        if self.snlisten.has_key(scene) != 1:
            scene.add_name_listener(cb2)
            self.snlisten[scene] = cb2
        else:
            pass
                
        cb3 = lambda :self.scene_triggered(scene, sc)
        if self.stlisten.has_key(scene) != 1:
            scene.add_is_triggered_listener(cb3)
            self.stlisten[scene] = cb3
        else:
            pass
        

    def scene_color_changestate(self, scene, sc):
        nm = ""
        nm = scene.name
        if scene.color == 0:
            self.oscServer.sendOSC("/scene", (sc, repr3(nm), 0))
        else:
            self.oscServer.sendOSC("/scene", (sc, repr3(nm), scene.color))

    def scene_name_changestate(self, scene, sc):
        nm = ""
        nm = scene.name
        if scene.color == 0:
            self.oscServer.sendOSC("/scene", (sc, repr3(nm), 0))
        else:
            self.oscServer.sendOSC("/scene", (sc, repr3(nm), scene.color))

    def scene_triggered(self, scene, sc):
        
        self.oscServer.sendOSC("/scene/fired", int(sc+1))



    def add_clip_listeners(self):
        self.rem_clip_listeners()
        tracks = self.getslots()
        for track in range(len(tracks)):
            for clip in range(len(tracks[track])):
                c = tracks[track][clip]
                if c.clip != None:
                    self.add_cliplistener(c.clip, track, clip) 
                self.add_slotlistener(c, track, clip)
                
    def add_cliplistener(self, clip, tid, cid):
        cb = lambda :self.clip_changestate(clip, tid, cid)
        
        if self.clisten.has_key(clip) != 1:
            clip.add_playing_status_listener(cb)
            self.clisten[clip] = cb
        
        #if clip.is_audio_clip == 0:
        #cb4 = lambda :self.notesChanged(tid, cid, clip)
        #if self.noteListeners.has_key(clip) != 1:
        # clip.add_notes_listener(cb4)
        # self.noteListeners[clip] = cb4
            

        cb3 = lambda :self.clip_name(clip, tid, cid)
        if self.cnlisten.has_key(clip) != 1:
            clip.add_name_listener(cb3)
            self.cnlisten[clip] = cb3

        if self.cclisten.has_key(clip) != 1:
            clip.add_color_listener(cb3)
            self.cclisten[clip] = cb3

        cb4 = lambda :self.clip_marker(clip, tid, cid)

        if self.smlisten.has_key(clip) != 1:
            clip.add_start_marker_listener(cb4)
            self.smlisten[clip] = cb4
                
        if self.emlisten.has_key(clip) != 1:
            clip.add_end_marker_listener(cb4)
            self.emlisten[clip] = cb4


        if self.lslisten.has_key(clip) != 1:
            clip.add_loop_start_listener(cb4)
            self.lslisten[clip] = cb4
        
        if self.lelisten.has_key(clip) != 1:
            clip.add_loop_end_listener(cb4)
            self.lelisten[clip] = cb4
    
        
        cb5 = lambda :self.file_path_changed(clip, tid, cid)

        if self.fplisten.has_key(clip) != 1 and clip.is_audio_clip:
            clip.add_file_path_listener(cb5)
            self.fplisten[clip] = cb5

        cb6 = lambda :self.clip_loop_status_changed(clip, tid, cid)

        if self.cliplooplisten.has_key(clip) != 1:
            clip.add_looping_listener(cb6)
            self.cliplooplisten[clip] = cb6

        cb7 = lambda :self.clip_warping_status_changed(clip, tid, cid)

        if self.clipwarplisten.has_key(clip) != 1 and clip.is_audio_clip:
            clip.add_warping_listener(cb7)
            self.clipwarplisten[clip] = cb7




        cb007 = lambda :self.clip_warping_mode_changed(clip, tid, cid)

        if self.clipwarpmodelisten.has_key(clip) != 1 and clip.is_audio_clip:
            clip.add_warp_mode_listener(cb007)
            self.clipwarpmodelisten[clip] = cb007


        
        cb8 = lambda :self.clip_muted_status_changed(clip, tid, cid)
    
        if self.clipmutelisten.has_key(clip) != 1:
            clip.add_muted_listener(cb8)
            self.clipmutelisten[clip] = cb8

        cb9 = lambda :self.clip_gain_changed(clip, tid, cid)

        if self.clipgainlisten.has_key(clip) != 1 and clip.is_audio_clip:
            clip.add_gain_listener(cb9)
            self.clipgainlisten[clip] = cb9

        cb10 = lambda :self.clip_coarse_changed(clip, tid, cid)
    
        if self.clipcoarselisten.has_key(clip) != 1 and clip.is_audio_clip:
            clip.add_pitch_coarse_listener(cb10)
            self.clipcoarselisten[clip] = cb10
        
        cb11 = lambda :self.clip_fine_changed(clip, tid, cid)

        if self.clipfinelisten.has_key(clip) != 1 and clip.is_audio_clip:
            clip.add_pitch_fine_listener(cb11)
            self.clipfinelisten[clip] = cb11




    def add_slotlistener(self, slot, tid, cid):
        cb = lambda :self.slot_changestate(slot, tid, cid)

        if self.slisten.has_key(slot) != 1:
            slot.add_has_clip_listener(cb)
            self.slisten[slot] = cb

        cb2 = lambda :self.stop_changestate(slot, tid, cid)
        if self.sslisten.has_key(slot) != 1:
            tracks = self.song().tracks
            track = tracks[tid]
            if track.is_foldable != 1:
                slot.add_has_stop_button_listener(cb2)
                self.sslisten[slot] = cb2
            else:
                pass


    
    def rem_mixer_listeners(self):
        # Master Track
        for type in ("volume", "panning", "crossfader"):
            for tr in self.masterlisten[type]:
                if tr != None:
                    cb = self.masterlisten[type][tr]
                
                    test = eval("tr.mixer_device." + type+ ".value_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.mixer_device." + type + ".remove_value_listener(cb)")

        # Normal Tracks
        for type in ("arm", "solo", "mute", "current_monitoring_state", "available_input_routing_channels", "available_input_routing_types", "available_output_routing_channels", "available_output_routing_types", "input_routing_channel", "input_routing_type", "output_routing_channel", "output_routing_type"):
            for tr in self.mlisten[type]:
                if tr != None:
                    cb = self.mlisten[type][tr]
                    
                    if type == "arm":
                        if tr.can_be_armed == 1:
                            if tr.arm_has_listener(cb) == 1:
                                tr.remove_arm_listener(cb)
                    elif type == "current_monitoring_state":
                            if tr.can_be_armed == 1:
                                if tr.current_monitoring_state_has_listener(cb) == 1:
                                    tr.remove_current_monitoring_state_listener(cb)    
                    else:
                        test = eval("tr." + type+ "_has_listener(cb)")
                
                        if test == 1:
                            eval("tr.remove_" + type + "_listener(cb)")
                
        for type in ("volume", "panning"):
            for tr in self.mlisten[type]:
                if tr != None:
                    cb = self.mlisten[type][tr]
                
                    test = eval("tr.mixer_device." + type+ ".value_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.mixer_device." + type + ".remove_value_listener(cb)")
         
        for tr in self.mlisten["sends"]:
            if tr != None:
                for send in self.mlisten["sends"][tr]:
                    if send != None:
                        cb = self.mlisten["sends"][tr][send]

                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)
                        
                        
        for tr in self.mlisten["name"]:
            if tr != None:
                cb = self.mlisten["name"][tr]

                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)

        for tr in self.mlisten["color"]:
            if tr != None:
                cb = self.mlisten["color"][tr]

                try:
                    if tr.color_has_listener(cb) == 1:
                        tr.remove_color_listener(cb)
                except:
                    pass
                    

        for tr in self.mlisten["oml"]:
            if tr != None:
                cb = self.mlisten["oml"][tr]

                if tr.output_meter_left_has_listener(cb) == 1:
                    tr.remove_output_meter_left_listener(cb)                    

        for tr in self.mlisten["omr"]:
            if tr != None:
                cb = self.mlisten["omr"][tr]

                if tr.output_meter_right_has_listener(cb) == 1:
                    tr.remove_output_meter_right_listener(cb)
                    
        # Return Tracks                
        for type in ("solo", "mute", "available_output_routing_channels", "available_output_routing_types", "output_routing_channel", "output_routing_type"):
            for tr in self.rlisten[type]:
                if tr != None:
                    cb = self.rlisten[type][tr]
                
                    test = eval("tr." + type+ "_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.remove_" + type + "_listener(cb)")
                
        for type in ("volume", "panning"):
            for tr in self.rlisten[type]:
                if tr != None:
                    cb = self.rlisten[type][tr]
                
                    test = eval("tr.mixer_device." + type+ ".value_has_listener(cb)")
                
                    if test == 1:
                        eval("tr.mixer_device." + type + ".remove_value_listener(cb)")
         
        for tr in self.rlisten["sends"]:
            if tr != None:
                for send in self.rlisten["sends"][tr]:
                    if send != None:
                        cb = self.rlisten["sends"][tr][send]
                
                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)

        for tr in self.rlisten["name"]:
            if tr != None:
                cb = self.rlisten["name"][tr]

                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)

        for tr in self.rlisten["color"]:
            if tr != None:
                cb = self.rlisten["color"][tr]
                try:
                    if tr.color_has_listener(cb) == 1:
                        tr.remove_color_listener(cb)
                except:
                    pass
        self.mlisten = { "solo": {}, "mute": {}, "arm": {}, "current_monitoring_state": {}, "panning": {}, "volume": {}, "sends": {}, "name": {}, "oml": {}, "omr": {}, "color": {}, "available_input_routing_channels": {}, "available_input_routing_types": {}, "available_output_routing_channels": {}, "available_output_routing_types": {}, "input_routing_type": {}, "input_routing_channel": {}, "output_routing_channel": {}, "output_routing_type": {}    }
        self.rlisten = { "solo": {}, "mute": {}, "panning": {}, "volume": {}, "sends": {}, "name": {}, "color": {}, "available_output_routing_channels": {}, "available_output_routing_types": {}, "output_routing_channel": {}, "output_routing_type": {}   }
        self.masterlisten = { "panning": {}, "volume": {}, "crossfader": {} }
    
    
    def add_mixer_listeners(self):


        self.rem_mixer_listeners()
        
        # Master Track
        tr = self.song().master_track
        for type in ("volume", "panning", "crossfader"):
            self.add_master_listener(0, type, tr)
        
        #self.add_meter_listener(0, tr, 2)
        
        # Normal Tracks
        tracks = self.song().tracks
        for track in range(len(tracks)):
            tr = tracks[track]

            self.add_trname_listener(track, tr, 0)
            
            #if tr.has_audio_output:
                #self.add_meter_listener(track, tr)                
            
            for type in ("arm", "solo", "mute", "current_monitoring_state"):
                if type == "arm":
                    if tr.can_be_armed == 1:
                        self.add_mixert_listener(track, type, tr)

                elif type == "current_monitoring_state":
                    if tr.can_be_armed == 1:          
                        self.add_mixert_listener(track, type, tr)
                        
                else:
                    self.add_mixert_listener(track, type, tr)

            for type in ("available_input_routing_channels", "available_input_routing_types", "available_output_routing_channels", "available_output_routing_types", "input_routing_channel", "input_routing_type", "output_routing_channel", "output_routing_type"):
                self.add_routing_listener(track, type, 0, tr)
            for type in ("volume", "panning"):
                self.add_mixerv_listener(track, type, tr)
                
            for sid in range(len(tr.mixer_device.sends)):
                self.add_send_listener(track, tr, sid, tr.mixer_device.sends[sid])
        
        # Return Tracks
        tracks = self.song().return_tracks
        for track in range(len(tracks)):
            tr = tracks[track]

            self.add_trname_listener(track, tr, 1)
            #self.add_meter_listener(track, tr, 1)
            
            for type in ("available_output_routing_channels", "available_output_routing_types"):
                self.add_routing_listener(track, type, 2, tr, 1)
            
            for type in ("solo", "mute"):
                self.add_retmixert_listener(track, type, tr)
                
            for type in ("volume", "panning"):
                self.add_retmixerv_listener(track, type, tr)
            
            for sid in range(len(tr.mixer_device.sends)):
                self.add_retsend_listener(track, tr, sid, tr.mixer_device.sends[sid])
    
    
    # Add track listeners
    def add_send_listener(self, tid, track, sid, send):
        if self.mlisten["sends"].has_key(track) != 1:
            self.mlisten["sends"][track] = {}
                    
        if self.mlisten["sends"][track].has_key(send) != 1:
            cb = lambda :self.send_changestate(tid, track, sid, send)
            
            self.mlisten["sends"][track][send] = cb
            send.add_value_listener(cb)
    
    def add_mixert_listener(self, tid, type, track):
        if self.mlisten[type].has_key(track) != 1:
            cb = lambda :self.mixert_changestate(type, tid, track)
            
            self.mlisten[type][track] = cb
            eval("track.add_" + type + "_listener(cb)")

    def add_routing_listener(self, tid, type, track_type, track, r = 0):
        if self.mlisten[type].has_key(track) != 1:
            cb = lambda :self.routing_stuff_changed(type, track_type, tid, track, r)
            
            self.mlisten[type][track] = cb
            eval("track.add_" + type + "_listener(cb)")


            
    def add_mixerv_listener(self, tid, type, track):
        if self.mlisten[type].has_key(track) != 1:
            cb = lambda :self.mixerv_changestate(type, tid, track)
            
            self.mlisten[type][track] = cb
            eval("track.mixer_device." + type + ".add_value_listener(cb)")

    # Add master listeners
    def add_master_listener(self, tid, type, track):
        if self.masterlisten[type].has_key(track) != 1:
            cb = lambda :self.mixerv_changestate(type, tid, track, 2)
            
            self.masterlisten[type][track] = cb
            eval("track.mixer_device." + type + ".add_value_listener(cb)")
            
            
    # Add return listeners
    def add_retsend_listener(self, tid, track, sid, send):
        if self.rlisten["sends"].has_key(track) != 1:
            self.rlisten["sends"][track] = {}
                    
        if self.rlisten["sends"][track].has_key(send) != 1:
            cb = lambda :self.send_changestate(tid, track, sid, send, 1)
            
            self.rlisten["sends"][track][send] = cb
            send.add_value_listener(cb)
    
    def add_retmixert_listener(self, tid, type, track):
        if self.rlisten[type].has_key(track) != 1:
            cb = lambda :self.mixert_changestate(type, tid, track, 1)
            
            self.rlisten[type][track] = cb
            eval("track.add_" + type + "_listener(cb)")
            
    def add_retmixerv_listener(self, tid, type, track):
        if self.rlisten[type].has_key(track) != 1:
            cb = lambda :self.mixerv_changestate(type, tid, track, 1)
            
            self.rlisten[type][track] = cb
            eval("track.mixer_device." + type + ".add_value_listener(cb)")      


    # Track name listener
    def add_trname_listener(self, tid, track, ret = 0):
        cb = lambda :self.trname_changestate(tid, track, ret)

        if ret == 1:
            if self.rlisten["name"].has_key(track) != 1:
                self.rlisten["name"][track] = cb
            if self.rlisten["color"].has_key(track) != 1:
                self.rlisten["color"][track] = cb

        else:
            if self.mlisten["name"].has_key(track) != 1:
                self.mlisten["name"][track] = cb
            if self.mlisten["color"].has_key(track) != 1:
                self.mlisten["color"][track] = cb

        
        track.add_name_listener(cb)
        try:
            track.add_color_listener(cb)
        except:
            pass
        
    # Output Meter Listeners
    def add_meter_listener(self, tid, track, r = 0):
        cb = lambda :self.meter_changestate(tid, track, 0, r)

        if self.mlisten["oml"].has_key(track) != 1:
            self.mlisten["oml"][track] = cb

        track.add_output_meter_left_listener(cb)

 

######################################################################
# Listener Callbacks
        
    # Clip Callbacks
    def clip_name(self, clip, tid, cid):
        ascnm = ""
        nm = ""
        play = 0
        audioclip = 0

        if clip.name != None:
            nm = cut_string(clip.name)
            #ascnm = (nm.encode('ascii', 'replace'))
        if clip.is_playing == 1:
            play = 1
        if clip.is_triggered == 1:
            play = 2
        if clip.is_recording == 1:
            if clip.is_playing == 1:
                play = 3
        if clip.is_audio_clip:
            audioclip = 1

        nm = repr3(nm)
        self.oscServer.sendOSC('/clip', (tid, cid, nm, clip.color, play, int(audioclip)))


    def clip_marker(self, clip, tid, cid):
        ascnm = ""
        nm = ""
        play = 0
        start_marker_pos = clip.start_marker
        end_marker_pos = clip.end_marker
        #clip_loop_value = clip.looping
        #clip.looping = 1
        loop_start_pos = clip.loop_start
        loop_end_pos = clip.loop_end
        #clip.looping = clip_loop_value
        a_length = clip.length

        self.oscServer.sendOSC("/clip/marker", (tid, cid, nm, start_marker_pos, end_marker_pos, loop_start_pos, loop_end_pos, a_length))
    
    
    def clip_loop_status_changed(self, clip, tid, cid):
        
        is_looping = clip.looping

        self.oscServer.sendOSC("/clip/looping", (tid, cid, int(is_looping)))
    
    def clip_warping_status_changed(self, clip, tid, cid):
        
        is_looping = clip.warping
        
        self.oscServer.sendOSC("/clip/warping", (tid, cid,  int(is_looping)))
    
    
    def clip_warping_mode_changed(self, clip, tid, cid):
        
        warp_mode = clip.warp_mode
        
        self.oscServer.sendOSC("/clip/warp_mode", (tid, cid,  int(warp_mode)))



    def clip_muted_status_changed(self, clip, tid, cid):
        is_looping = clip.muted
        
        self.oscServer.sendOSC("/clip/muted", (tid, cid,  int(is_looping)))
    
    
    def clip_gain_str_changed(self, clip, tid, cid):
        
        gain_string = clip.gain_display_string
        
        self.oscServer.sendOSC("/clip/gain_str_changed", (tid, cid,  repr3(gain_string)))
     
    def clip_gain_changed(self, clip, tid, cid):

        gain_val = clip.gain
        
        self.oscServer.sendOSC("/clip/gain_changed", (tid, cid,  gain_val))
        
        self.clip_gain_str_changed(clip, tid, cid)

    

    def clip_coarse_changed(self, clip, tid, cid):
        
        coarse_val = clip.pitch_coarse
        
        self.oscServer.sendOSC("/clip/coarse_changed", (tid, cid,  float(coarse_val)))

    def clip_fine_changed(self, clip, tid, cid):
        
        fine_val = clip.pitch_fine
        
        self.oscServer.sendOSC("/clip/fine_changed", (tid, cid,  float(fine_val)))


    
    def file_path_changed(self, clip, tid, cid):
        self.oscServer.sendOSC("/NSLOG_REPLACE", "file_path_changed")


    def clip_loopchanged(self, clip, tid, cid):
        
        if self.isCheckingLoop != 1:
            self.isCheckingLoop = 1
            self.oscServer.sendOSC('/clip/loopchanged', (tid, cid))
        else:
            self.isCheckingLoop = 0


    def clip_position(self, clip, tid, cid):
        """if clip.is_playing:
            self.oscServer.sendOSC('/live/clip/position', (tid, cid, clip.playing_position, clip.length, clip.loop_start, clip.loop_end))"""
        
    def stop_changestate(self, slot, tid, cid):
        if slot.clip != None:
            pass
        else:
            if slot.has_stop_button == 1:
                self.oscServer.sendOSC('/clip', (tid, cid, "stop", 2500134, 0, int(0), int(0)))
                self.oscServer.sendOSC('/clipslot/stop', (tid, cid))
            else:
                self.oscServer.sendOSC('/clipslot/empty', (tid, cid))

                


    
    def slot_changestate(self, slot, tid, cid):
        ascnm = ""
        nm = ""
        # Added new clip
        if slot.clip != None:
            self.add_cliplistener(slot.clip, tid, cid)
            play = 0
            audioclip = 0
            
            if slot.clip.is_audio_clip:
                audioclip = 1
            if slot.clip.name != None:
                nm = cut_string(slot.clip.name)
                #ascnm = (nm.encode('ascii', 'replace'))
            if slot.clip.is_playing == 1:
                play = 1
 
            if slot.clip.is_triggered == 1:
                play = 2

            if slot.clip.is_recording == 1:
                if slot.clip.is_playing == 1:
                    play = 3
                    if self.onetap == 1:
                        slot.clip.fire()
                    else:
                        pass
            
                else:
                    pass
            else:
                pass
            self.oscServer.sendOSC('/clip/playing_status', (tid, cid, play))
            self.oscServer.sendOSC('/clip', (tid, cid, repr3(nm), slot.clip.color, play, int(audioclip)))
        
            clip = slot.clip

            is_audio_clip = int(clip.is_audio_clip)
            
            isLooping = int(clip.looping)
            is_audio_clip = int(clip.is_audio_clip)
            
            warp = 0
            if is_audio_clip == 1:
                warp = int(clip.warping)
            else:
                pass
            loop_start = clip.loop_start
            loop_end = clip.loop_end
    
            try:
                start = clip.start_marker
                end = clip.end_marker
            except:
                start = clip.loop_start
                end = clip.loop_end


            self.oscServer.sendOSC('/clip/loopstats', (tid, cid, isLooping, start, end, loop_start, loop_end, is_audio_clip, int(warp)))
    
        else:
            self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 0))
            self.stop_changestate(slot, tid, cid)
            if slot.has_stop_button_has_listener != 1:
                cb2 = lambda :self.stop_changestate(slot, tid, cid)
                slot.add_has_stop_button_listener(cb2)
            if self.clisten.has_key(slot.clip) == 1:
                slot.clip.remove_playing_status_listener(self.clisten[slot.clip])
                
            if self.pplisten.has_key(slot.clip) == 1:
                slot.clip.remove_playing_position_listener(self.pplisten[slot.clip])

            if self.cnlisten.has_key(slot.clip) == 1:
                slot.clip.remove_name_listener(self.cnlisten[slot.clip])
            
            if self.smlisten.has_key(slot.clip) == 1:
                slot.clip.remove_start_marker_listener(self.smlisten[slot.clip])

            if self.emlisten.has_key(slot.clip) == 1:
                slot.clip.remove_end_marker_listener(self.emlisten[slot.clip])
            
            if self.lslisten.has_key(slot.clip) == 1:
                slot.clip.remove_loop_start_listener(self.lslisten[slot.clip])
                    
            if self.lelisten.has_key(slot.clip) == 1:
                slot.clip.remove_loop_end_listener(self.lelisten[slot.clip])
            
            if self.cliplooplisten.has_key(slot.clip) == 1:
                slot.clip.remove_looping_listener(self.cliplooplisten[slot.clip])
                    
            if self.clipwarplisten.has_key(slot.clip) == 1:
                slot.clip.remove_warping_listener(self.clipwarplisten[slot.clip])
            
            
            if self.clipwarpmodelisten.has_key(slot.clip) == 1:
                slot.clip.remove_warp_mode_listener(self.clipwarpmodelisten[slot.clip])
            
            
            if self.clipmutelisten.has_key(slot.clip) == 1:
                slot.clip.remove_muted_listener(self.clipmutelisten[slot.clip])
            
            if self.clipgainlisten.has_key(slot.clip) == 1:
                slot.clip.remove_gain_listener(self.clipgainlisten[slot.clip])
            
            if self.clipcoarselisten.has_key(slot.clip) == 1:
                slot.clip.remove_pitch_coarse_listener(self.clipcoarselisten[slot.clip])
        
            if self.clipfinelisten.has_key(slot.clip) == 1:
                slot.clip.remove_pitch_fine_listener(self.clipfinelisten[slot.clip])
            
            if self.fplisten.has_key(slot.clip) == 1 and slot.clip.is_audio_clip:
                slot.clip.remove_file_path_listener(self.fplisten[slot.clip])

            if self.cclisten.has_key(slot.clip) == 1:
                slot.clip.remove_color_listener(self.cclisten[slot.clip])
            
            if self.noteListeners.has_key(slot.clip) == 1:
                slot.clip.remove_notes_listener(self.noteListeners[slot.clip])
        
                
    
    
    def clip_changestate(self, clip, x, y):
        playing = 0
        
        if clip.is_playing == 1:
            playing = 1
            if clip.is_recording == 1:
                playing = 3
            if self.song().tracks[x].arm == 1 and clip.is_audio_clip == 0:
                if self.song().overdub == 1:
                    playing = 3
                else:
                    playing = 1
        else:
            pass
        if clip.is_triggered == 1:
            playing = 2
        else:
            pass
        
        self.oscServer.sendOSC('/clip/playing_status', (x, y, playing))
        #self.log("Clip changed x:" + str(x) + " y:" + str(y) + " status:" + str(playing)) 
        
        
    # Mixer Callbacks
    def mixerv_changestate(self, type, tid, track, r = 0):
        val = eval("track.mixer_device." + type + ".value")
        types = { "panning": "pan", "volume": "volume", "crossfader": "crossfader" }
        
        if r == 2:
            self.oscServer.sendOSC('/master/' + types[type], (float(val)))
            if val == 0:
                self.oscServer.sendOSC('/master/' + types[type], (float(0.00000001)))

        elif r == 1:
            self.oscServer.sendOSC('/return/' + types[type], (tid, float(val)))
        else:
            self.oscServer.sendOSC('/track/' + types[type], (tid, val))        


    def routing_stuff_changed(self, type, track_type, tid, track, r = 0):
        """if type == "available_input_routing_types":
            
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("available_input_routing_types"))
        elif type == "available_input_routing_channels":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("available_input_routing_channels"))
        elif type == "available_output_routing_types":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("available_output_routing_types"))
        elif type == "available_output_routing_channels":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("available_output_routing_channels"))
        elif type == "input_routing_type":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("input_routing_type"))
        elif type == "input_routing_channel":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("input_routing_channel"))
        elif type == "output_routing_type":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("output_routing_type"))
        elif type == "output_routing_channel":
            self.oscServer.sendOSC("/NSLOG_REPLACE", ("output_routing_channel"))
        
        else:
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("NO ROUTING SHIT WTF"))
            pass"""
        
        self.sendTrackIO(tid, track, type, track_type)
        #self.oscServer.sendOSC("/NSLOG_REPLACE", ("NO ROUTING SHIT WTF2"))
            
    
    
    def mixert_changestate(self, type, tid, track, r = 0):
        val = eval("track." + type)
        #self.oscServer.sendOSC("/NSLOG_REPLACE", ("mixert_changestate"))

        if r == 1:
            self.oscServer.sendOSC('/return/' + type, (tid, int(val)))
        else:
            self.oscServer.sendOSC('/track/' + type, (tid, int(val)))
            if type == "arm":
                if val == 0:
                    if LiveUtils.getTrack(tid).playing_slot_index != -2:
                        cid = LiveUtils.getTrack(tid).playing_slot_index
                        self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 1))
                    else:
                        pass
                    
                elif val == 1:
                    if LiveUtils.getTrack(tid).playing_slot_index != -2:
                        cid = LiveUtils.getTrack(tid).playing_slot_index
                        if LiveUtils.getSong().overdub == 1 or LiveUtils.getTrack(tid).has_midi_input == 0:
                            self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 3))

                        else:
                            self.oscServer.sendOSC('/clip/playing_status', (tid, cid, 1))

                    else:
                        pass
            else:
                pass


                    
    
    def send_changestate(self, tid, track, sid, send, r = 0):
        val = send.value
        
        if r == 1:
            self.oscServer.sendOSC('/return/send', (tid, sid, float(val)))   
        else:
            self.oscServer.sendOSC('/track/send', (tid, sid, float(val)))   


    # Track name changestate
    def trname_changestate(self, tid, track, r = 0):
        self.oscServer.sendOSC("/NSLOG_REPLACE", "name track changestate")
        #trackTotal = len(LiveUtils.getTracks())
        #sceneTotal = len(LiveUtils.getScenes())
        #returnsTotal = len(LiveUtils.getSong().return_tracks)
        #self.oscServer.sendOSC("/set/size", (trackTotal, sceneTotal, returnsTotal))
        if r == 1:
            nm = track.name
            col = 0
            grouptrack = 0
            try:
                col = track.color
            except:
                pass
            #ascnm = (nm.encode('ascii', 'replace'))
            self.oscServer.sendOSC('/return', (tid, repr3(nm), col))
        else:
            nm = track.name
            col = 0
            is_midi_track = track.has_midi_input
            
            try:
                col = track.color
            except:
                pass
            if track.is_foldable == 1:
                grouptrack = 1
            else:
                grouptrack = 0
            #ascnm = (nm.encode('ascii', 'replace'))

            live_pointer = str(track._live_ptr)

            self.oscServer.sendOSC('/track', (tid, repr3(nm), col, grouptrack, int(is_midi_track),live_pointer))
            #self.devices_changed(track, tid, r)
            
    # Meter Changestate
    def meter_changestate(self, tid, track, lr, r = 0):

        vall = track.output_meter_left
        #valr = track.output_meter_right
        tracknr = (tid - self.offsetx)
        if r == 2:
            if lr == 0:
                #if vall > valr:              
                self.oscServer.sendOSC('/live/master/meter', (float(vall)))
                #else:
                    #self.oscServer.sendOSC('/live/master/meter', (float(valr)))
        elif r == 1:
            if lr == 0:
                #if vall > valr:            
                self.oscServer.sendOSC('/live/return/meter', (tid, float(vall)))
                #else:
                    #self.oscServer.sendOSC('/live/return/meter', (tid, float(valr)))        
        else:
            if lr == 0:
                if tracknr >= 0:
                    if tracknr <= 7:
                        
                        #if vall > valr:
                        self.oscServer.sendOSC('/live/track/meter', (tracknr, float(vall)))
                        #else:
                            #self.oscServer.sendOSC('/live/track/meter', (tracknr, float(valr)))


        self.mlcache[track] = vall

                          
    
    # Device Listeners
    
    
    def add_device_listeners_for_track(self, track, tid, type):

        self.remove_device_listeners_of_track(track, tid, type)
        
        self.add_devices_listener(track, tid, type)

        key = '%s.%s' % (type, tid)

        self.prlisten[key] = {}
        self.parameters_listeners[key] = {}
        self.sample_listeners[key] = {}
        self.simpler_playbackmode_listener[key] = {}
        self.simpler_selected_slice_listener[key] = {}
        self.simpler_playing_position_listener[key] = {}
        self.chainslisten[key] = {}

        self.chaindevicelisten[key] = {}
        self.drum_pad_listen[key] = {}
        
        
        """ compressor device """
        self.compressor_available_input_routing_channels_listener[key] = {}
        self.compressor_available_input_routing_types_listener[key] = {}
        self.compressor_input_routing_channel_listener[key] = {}
        self.compressor_input_routing_type_listener[key] = {}
        
        self.wavetable_filter_routing_listener[key] = {}
        self.wavetable_modulation_matrix_listener[key] = {}
        self.wavetable_mono_poly_listener[key] = {}
        self.wavetable_oscillator_1_effect_listener[key] = {}
        self.wavetable_oscillator_1_wavetable_category_listener[key] = {}
        self.wavetable_oscillator_1_wavetable_index_listener[key] = {}
        self.wavetable_oscillator_1_wavetables_listener[key] = {}
        self.wavetable_oscillator_2_effect_listener[key] = {}
        self.wavetable_oscillator_2_wavetable_category_listener[key] = {}
        self.wavetable_oscillator_2_wavetable_index_listener[key] = {}
        self.wavetable_oscillator_2_wavetables_listener[key] = {}
        self.wavetable_poly_voices_listener[key] = {}
        self.wavetable_unison_mode_listener[key] = {}
        self.wavetable_unison_voice_count_listener[key] = {}
        self.wavetable_visible_modulation_target_names_listener[key] = {}

        drum_pad_listen = self.drum_pad_listen[key]

        a = Live.Application.get_application().get_major_version()
        number_of_steps = 0
        i = 0
        indices = []

        if len(track.devices) >= 1:

            for did in range(len(track.devices)):
                
                device = track.devices[did]
                lis = list(indices)
                self.add_listener_for_device(track, tid, did, type, device, 0, lis, -1)
            


    def add_listener_for_device(self, track, tid, did, type, device, number_of_steps, indices, i):
        
        #self.oscServer.sendOSC("/NSLOG_REPLACE", ("add_listener_for_device", repr3(device.name)))

        #self.expand_device_dev(device)
        
        a = Live.Application.get_application().get_major_version()
        key = '%s.%s' % (type, tid)

        if i != -1:
            indices.append(int(i))
            number_of_steps = number_of_steps+1
        else:
            indic = []
            indices = list(indic)
        

        prlisten = self.prlisten[key]
        parameters_listeners = self.parameters_listeners[key]
        sample_listeners = self.sample_listeners[key]
        chaindevicelisten = self.chaindevicelisten[key]
        
        tr = device.canonical_parent
        
        num = len(tr.devices)
        lis = list(indices)


        cb = lambda :self.update_listeners_for_device(device, track, tid, did, type, num, number_of_steps, lis, -1)


        if parameters_listeners.has_key(device) != 1:
            device.add_parameters_listener(cb)
            parameters_listeners[device] = cb
        
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "try add sample listener for simpler")
        a_version = Live.Application.get_application().get_major_version()
        if device.class_name == 'OriginalSimpler':
            self.add_listener_for_simpler(device, track, tid, did, type, num, number_of_steps, lis)
        
        if device.class_name == 'InstrumentVector' and a_version >= 10:
            self.add_listener_for_wavetable(device, track, tid, did, type, num, number_of_steps, lis)

        if device.class_name == 'Compressor2' and a_version >= 10:
            self.add_listener_for_compressor(device, track, tid, did, type, num, number_of_steps, lis)


        if a >= 9:
            if type == 0:
                if device.can_have_drum_pads == 1:
                    key = '%s.%s' % (type, tid)
                    drum_pad_listen = self.drum_pad_listen[key]
                    for drum_id in range(len(device.drum_pads)):
                        drum_pad = device.drum_pads[drum_id]
                        #self.oscServer.sendOSC("/NSLOG_REPLACE", "ADDING DRUM PAD LISTENER")
                        
                        self.add_drum_pad_listener(drum_pad_listen, drum_pad, int(tid), int(did), number_of_steps, lis)
        
        
            if device.can_have_chains == 1:
                
                chainslisten = self.chainslisten[key]
                if chainslisten.has_key(device) != 1:
                    device.add_chains_listener(cb)
                    chainslisten[device] = cb


                for chain_id in range(len(device.chains)):
                    chain = device.chains[chain_id]

                    self.add_chain_devices_listener(track, tid, type, chain)
                    
                    listt = list(indices)
                    listt.append(int(chain_id))

                    for device_id in range(len(chain.devices)):
                        dev = chain.devices[device_id]

                        lis = list(listt)
                        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update add listener for device from itself" + device.name)

                        self.add_listener_for_device(track, tid, did, type, dev, number_of_steps, lis, device_id)
    
    
    
    
    

        #self.oscServer.sendOSC('/adding_device_listeners_for_device2', (int(type), int(tid), int(did), int(number_of_steps), tuple(indis)))
        
        #self.oscServer.sendOSC('/adding_device_listeners_for_device2', (tuple(indices)))


        if len(device.parameters) >= 1:
            for pid in range(len(device.parameters)):
                param = device.parameters[pid]
                self.add_parameter_listener(prlisten, param, int(tid), int(did), int(pid), int(type), int(number_of_steps), tuple(indices))

        #self.oscServer.sendOSC('/adding_device_listeners_for_device3', (tuple(indices)))




    def add_parameter_listener(self, prlisten, param, tid, did, pid, type, number_of_steps, indices):
        cb = lambda :self.param_changestate(param, int(tid), int(did), int(pid), int(type), int(number_of_steps), indices)
        if prlisten.has_key(param) != 1:
            param.add_value_listener(cb)
            prlisten[param] = cb


    
    def remove_device_listeners_of_track(self, track, tid, type):

        self.remove_devices_listener(track, tid, type)
        key = '%s.%s' % (type, tid)

        if self.prlisten.has_key(key) == 1:
            #self.oscServer.sendOSC('/live/track/device_listeners_found', 1)

            prlisten = self.prlisten[key]

            for pr in prlisten:
                if pr != None:
                    ocb = prlisten[pr]
                    if pr.value_has_listener(ocb) == 1:
                        pr.remove_value_listener(ocb)
            del self.prlisten[key]
                                                    
           

        if self.parameters_listeners.has_key(key) == 1:
           #self.oscServer.sendOSC('/live/track/device_listeners_found', 1)
           
            parameters_listeners = self.parameters_listeners[key]
               
            for pr in parameters_listeners:
                if pr != None:
                    ocb = parameters_listeners[pr]
                    if pr.parameters_has_listener(ocb) == 1:
                        pr.remove_parameters_listener(ocb)
            del self.parameters_listeners[key]


        """if self.sample_listeners.has_key(key) == 1:
    #self.oscServer.sendOSC('/live/track/device_listeners_found', 1)
            self.oscServer.sendOSC("/NSLOG_REPLACE", "try to remove sample listener for simpler")

            sample_listeners = self.sample_listeners[key]
        
            for pr in sample_listeners:
                if pr != None:
                    ocb = sample_listeners[pr]
                    if pr.sample_has_listener(ocb) == 1:
                        self.oscServer.sendOSC("/NSLOG_REPLACE", "still try to remove sample listener for simpler")

                        pr.remove_sample_listener(ocb)
                        self.oscServer.sendOSC("/NSLOG_REPLACE", "remove sample listener for simpler")

            del self.sample_listeners[key]"""


        
        if self.compressor_available_input_routing_channels_listener.has_key(key) == 1:
            compressor_available_input_routing_channels_listener = self.compressor_available_input_routing_channels_listener[key]
            for pr in compressor_available_input_routing_channels_listener:
                if pr != None:
                    ocb = compressor_available_input_routing_channels_listener[pr]
                    if pr.available_input_routing_channels_has_listener(ocb) == 1:
                        pr.remove_available_input_routing_channels_listener(ocb)
            del self.compressor_available_input_routing_channels_listener[key]
        
        
        
        """if self.compressor_available_input_routing_types_listener.has_key(key) == 1:
            compressor_available_input_routing_types_listener = self.compressor_available_input_routing_types_listener[key]
            for pr in compressor_available_input_routing_types_listener:
                if pr != None:
                    ocb = compressor_available_input_routing_types_listener[pr]
                    if pr.available_input_routing_types_has_listener(ocb) == 1:
                        pr.remove_available_input_routing_types_listener(ocb)
            del self.compressor_available_input_routing_types_listener[key] """
    
    
        if self.compressor_input_routing_channel_listener.has_key(key) == 1:
            compressor_input_routing_channel_listener = self.compressor_input_routing_channel_listener[key]
            for pr in compressor_input_routing_channel_listener:
                if pr != None:
                    ocb = compressor_input_routing_channel_listener[pr]
                    if pr.input_routing_channel_has_listener(ocb) == 1:
                        pr.remove_input_routing_channel_listener(ocb)
            del self.compressor_input_routing_channel_listener[key]
    
    
    
        if self.compressor_input_routing_type_listener.has_key(key) == 1:
            compressor_input_routing_type_listener = self.compressor_input_routing_type_listener[key]
            for pr in compressor_input_routing_type_listener:
                if pr != None:
                    ocb = compressor_input_routing_type_listener[pr]
                    if pr.input_routing_type_has_listener(ocb) == 1:
                        pr.remove_input_routing_type_listener(ocb)
            del self.compressor_input_routing_type_listener[key]
    
        if self.simpler_slicing_playbackmode_listener.has_key(key) == 1:
            simpler_slicing_playbackmode_listener = self.simpler_slicing_playbackmode_listener[key]
            for pr in simpler_slicing_playbackmode_listener:
                if pr != None:
                    ocb = simpler_slicing_playbackmode_listener[pr]
                    if pr.slicing_playback_mode_has_listener(ocb) == 1:
                        pr.remove_slicing_playback_mode_listener(ocb)


            del self.simpler_slicing_playbackmode_listener[key]




        if self.simpler_selected_slice_listener.has_key(key) == 1:
            simpler_selected_slice_listener = self.simpler_selected_slice_listener[key]
            
            for pr in simpler_selected_slice_listener:
                if pr != None:
                    ocb = simpler_selected_slice_listener[pr]
                    if pr.selected_slice_has_listener(ocb) == 1:
                        pr.remove_selected_slice_listener(ocb)
    
            del self.simpler_selected_slice_listener[key]
    

        if self.simpler_playing_position_listener.has_key(key) == 1:
            simpler_playing_position_listener = self.simpler_playing_position_listener[key]
        
            for pr in simpler_playing_position_listener:
                if pr != None:
                    ocb = simpler_playing_position_listener[pr]
                    if pr.playing_position_has_listener(ocb) == 1:
                        pr.remove_playing_position_listener(ocb)
    
            del self.simpler_playing_position_listener[key]
    

            
        if self.wavetable_filter_routing_listener.has_key(key) == 1:
            wavetable_filter_routing_listener = self.wavetable_filter_routing_listener[key]
            
            for pr in wavetable_filter_routing_listener:
                if pr != None:
                    ocb = wavetable_filter_routing_listener[pr]
                    if pr.filter_routing_has_listener(ocb) == 1:
                        pr.remove_filter_routing_listener(ocb)
            
            del self.wavetable_filter_routing_listener[key]
            
        if self.wavetable_modulation_matrix_listener.has_key(key) == 1:
            wavetable_modulation_matrix_listener = self.wavetable_modulation_matrix_listener[key]
            
            for pr in wavetable_modulation_matrix_listener:
                if pr != None:
                    ocb = wavetable_modulation_matrix_listener[pr]
                    if pr.modulation_matrix_changed_has_listener(ocb) == 1:
                        pr.remove_modulation_matrix_changed_listener(ocb)
            
            del self.wavetable_modulation_matrix_listener[key]

        if self.wavetable_mono_poly_listener.has_key(key) == 1:
            wavetable_mono_poly_listener = self.wavetable_mono_poly_listener[key]
    
            for pr in wavetable_mono_poly_listener:
                if pr != None:
                    ocb = wavetable_mono_poly_listener[pr]
                    if pr.mono_poly_has_listener(ocb) == 1:
                        pr.remove_mono_poly_listener(ocb)
            
            del self.wavetable_mono_poly_listener[key]

        if self.wavetable_oscillator_1_effect_listener.has_key(key) == 1:
            wavetable_oscillator_1_effect_listener = self.wavetable_oscillator_1_effect_listener[key]
    
            for pr in wavetable_oscillator_1_effect_listener:
                if pr != None:
                    ocb = wavetable_oscillator_1_effect_listener[pr]
                    if pr.oscillator_1_effect_mode_has_listener(ocb) == 1:
                        pr.remove_oscillator_1_effect_mode_listener(ocb)
            
            del self.wavetable_oscillator_1_effect_listener[key]

        if self.wavetable_oscillator_1_wavetable_category_listener.has_key(key) == 1:
            wavetable_oscillator_1_wavetable_category_listener = self.wavetable_oscillator_1_wavetable_category_listener[key]
    
            for pr in wavetable_oscillator_1_wavetable_category_listener:
                if pr != None:
                    ocb = wavetable_oscillator_1_wavetable_category_listener[pr]
                    if pr.oscillator_1_wavetable_category_has_listener(ocb) == 1:
                        pr.remove_oscillator_1_wavetable_category_listener(ocb)
            
            del self.wavetable_oscillator_1_wavetable_category_listener[key]



        if self.wavetable_oscillator_1_wavetable_index_listener.has_key(key) == 1:
            wavetable_oscillator_1_wavetable_index_listener = self.wavetable_oscillator_1_wavetable_index_listener[key]
    
            for pr in wavetable_oscillator_1_wavetable_index_listener:
                if pr != None:
                    ocb = wavetable_oscillator_1_wavetable_index_listener[pr]
                    if pr.oscillator_1_wavetable_index_has_listener(ocb) == 1:
                        pr.remove_oscillator_1_wavetable_index_listener(ocb)
            
            del self.wavetable_oscillator_1_wavetable_index_listener[key]



        if self.wavetable_oscillator_1_wavetables_listener.has_key(key) == 1:
            wavetable_oscillator_1_wavetables_listener = self.wavetable_oscillator_1_wavetables_listener[key]

            for pr in wavetable_oscillator_1_wavetables_listener:
                if pr != None:
                    ocb = wavetable_oscillator_1_wavetables_listener[pr]
                    if pr.oscillator_1_wavetables_has_listener(ocb) == 1:
                        pr.remove_oscillator_1_wavetables_listener(ocb)
            
            del self.wavetable_oscillator_1_wavetables_listener[key]

        if self.wavetable_oscillator_2_effect_listener.has_key(key) == 1:
            wavetable_oscillator_2_effect_listener = self.wavetable_oscillator_1_effect_listener[key]
    
            for pr in wavetable_oscillator_2_effect_listener:
                if pr != None:
                    ocb = wavetable_oscillator_2_effect_listener[pr]
                    if pr.oscillator_2_effect_mode_has_listener(ocb) == 1:
                        pr.remove_oscillator_2_effect_mode_listener(ocb)
            
            del self.wavetable_oscillator_2_effect_listener[key]
        
        if self.wavetable_oscillator_2_wavetable_category_listener.has_key(key) == 1:
            wavetable_oscillator_2_wavetable_category_listener = self.wavetable_oscillator_2_wavetable_category_listener[key]
            
            for pr in wavetable_oscillator_2_wavetable_category_listener:
                if pr != None:
                    ocb = wavetable_oscillator_2_wavetable_category_listener[pr]
                    if pr.oscillator_2_wavetable_category_has_listener(ocb) == 1:
                        pr.remove_oscillator_2_wavetable_category_listener(ocb)
            
            del self.wavetable_oscillator_2_wavetable_category_listener[key]



        if self.wavetable_oscillator_2_wavetable_index_listener.has_key(key) == 1:
            wavetable_oscillator_2_wavetable_index_listener = self.wavetable_oscillator_2_wavetable_index_listener[key]
        
            for pr in wavetable_oscillator_2_wavetable_index_listener:
                if pr != None:
                    ocb = wavetable_oscillator_2_wavetable_index_listener[pr]
                    if pr.oscillator_2_wavetable_index_has_listener(ocb) == 1:
                        pr.remove_oscillator_2_wavetable_index_listener(ocb)
            
            del self.wavetable_oscillator_2_wavetable_index_listener[key]
        
        
        
        if self.wavetable_oscillator_2_wavetables_listener.has_key(key) == 1:
            wavetable_oscillator_2_wavetables_listener = self.wavetable_oscillator_2_wavetables_listener[key]
            
            for pr in wavetable_oscillator_2_wavetables_listener:
                if pr != None:
                    ocb = wavetable_oscillator_2_wavetables_listener[pr]
                    if pr.oscillator_2_wavetables_has_listener(ocb) == 1:
                        pr.remove_oscillator_2_wavetables_listener(ocb)

            del self.wavetable_oscillator_2_wavetables_listener[key]

        
        if self.wavetable_poly_voices_listener.has_key(key) == 1:
            wavetable_poly_voices_listener = self.wavetable_poly_voices_listener[key]
            
            for pr in wavetable_poly_voices_listener:
                if pr != None:
                    ocb = wavetable_poly_voices_listener[pr]
                    if pr.poly_voices_has_listener(ocb) == 1:
                        pr.remove_poly_voices_listener(ocb)
            
            del self.wavetable_poly_voices_listener[key]
            
            
        if self.wavetable_unison_mode_listener.has_key(key) == 1:
            wavetable_unison_mode_listener = self.wavetable_unison_mode_listener[key]
            
            for pr in wavetable_unison_mode_listener:
                if pr != None:
                    ocb = wavetable_unison_mode_listener[pr]
                    if pr.unison_mode_has_listener(ocb) == 1:
                        pr.remove_unison_mode_listener(ocb)

            del self.wavetable_unison_mode_listener[key]
        

        if self.wavetable_unison_voice_count_listener.has_key(key) == 1:
            wavetable_unison_voice_count_listener = self.wavetable_unison_voice_count_listener[key]
            
            for pr in wavetable_unison_voice_count_listener:
                if pr != None:
                    ocb = wavetable_unison_voice_count_listener[pr]
                    if pr.unison_voice_count_has_listener(ocb) == 1:
                        pr.remove_unison_voice_count_listener(ocb)
            
            del self.wavetable_unison_voice_count_listener[key]
            
            
            
        
        if self.wavetable_visible_modulation_target_names_listener.has_key(key) == 1:
            wavetable_visible_modulation_target_names_listener = self.wavetable_visible_modulation_target_names_listener[key]
            
            for pr in wavetable_visible_modulation_target_names_listener:
                if pr != None:
                    ocb = wavetable_visible_modulation_target_names_listener[pr]
                    if pr.visible_modulation_target_names_has_listener(ocb) == 1:
                        pr.remove_visible_modulation_target_names_listener(ocb)

            del self.wavetable_visible_modulation_target_names_listener[key]


        if self.chainslisten.has_key(key) == 1:
            #self.oscServer.sendOSC('/live/track/device_listeners_found', 1)
            
            chainslisten = self.chainslisten[key]
            
            for dev in chainslisten:
                if dev != None:
                    ocb = chainslisten[dev]
                    if dev.chains_has_listener(ocb) == 1:
                        dev.remove_chains_listener(ocb)
            del self.chainslisten[key]
    
    
    
        if self.drum_pad_listen.has_key(track) == 1:

            drum_pad_listen = self.drum_pad_listen[key]
        
            for drum_pad in drum_pad_listen:
                if drum_pad != None:
                    ocb = drum_pad_listen[drum_pad]
                    if drum_pad.name_has_listener(ocb) == 1:
                        drum_pad.remove_name_listener(ocb)
            del self.drum_pad_listen[key]
            
    
    
    def add_device_listeners(self):
        self.do_add_device_listeners(self.song().tracks,0)
        self.do_add_device_listeners(self.song().return_tracks,2)
        self.do_add_device_listeners([self.song().master_track],1)
        self.add_app_device_listener()

        #self.oscServer.sendOSC('/track/adding_all_listeners', 2)

    def add_app_device_listener(self):
        self.rem_app_device_listener()
            
        if self.song().appointed_device_has_listener(self.device_changestate) != 1:
            self.song().add_appointed_device_listener(self.device_changestate)


    def rem_app_device_listener(self):
        if self.song().appointed_device_has_listener(self.device_changestate) == 1:
            self.song().remove_appointed_device_listener(self.device_changestate)
    
    
    def do_add_device_listeners(self, tracks, type):
        for tid in range(len(tracks)):
            track = tracks[tid]
            self.add_device_listeners_for_track(track, tid, type)


    def do_remove_device_listeners(self, tracks, type):
        for tid in range(len(tracks)):
            track = tracks[tid]
            self.remove_device_listeners_of_track(track, tid, type)

    def rem_all_device_listeners(self):
        #self.oscServer.sendOSC('/live/track/removing_all_dev_listeners', 1)

        
        self.do_remove_device_listeners(self.song().tracks,0)
        self.do_remove_device_listeners(self.song().return_tracks,2)
        self.do_remove_device_listeners([self.song().master_track],1)
        #self.oscServer.sendOSC('/live/track/removing_all_dev_listeners', 2)

        for key in self.drum_pad_listen:
        
            #self.oscServer.sendOSC('/live/track/removing_all_dev_listeners', 3)
            drum_pad_listen = self.drum_pad_listen[key]
            for drum_pad in drum_pad_listen:
                if drum_pad != None:
                    ocb = drum_pad_listen[drum_pad]
                    if drum_pad.name_has_listener(ocb) == 1:
                        drum_pad.remove_name_listener(ocb)
    
        #self.oscServer.sendOSC('/live/track/removing_all_dev_listeners', 4)
        self.drum_pad_listen = {}


    
        
    def add_paramlistener(self, param, tid, did, pid, type):
        cb = lambda :self.param_changestate(param, tid, did, pid, type)
        
        if self.prlisten.has_key(param) != 1:
            param.add_value_listener(cb)
            self.prlisten[param] = cb

        

    def add_drum_pad_listener(self, drum_pad_listen, drum_pad, i, j, number_of_steps, indices):
        cb = lambda :self.drum_pad_changed(drum_pad, i, j, number_of_steps, indices)
        if drum_pad_listen.has_key(drum_pad) != 1:
            drum_pad.add_name_listener(cb)
            drum_pad_listen[drum_pad] = cb
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "ADDED DRUM PAD LISTENER")


    def add_drumpads_listener(self, device, i, j, number_of_steps, indices):
        cb = lambda :self.drum_pads_changed(device.drum_pads, i, j, number_of_steps, indices)
        if self.drum_pads_listen.has_key(device) != 1:
            device.add_drum_pads_listener(cb)
            self.drum_pads_listen[device] = cb


    def drum_pads_changed(self, drum_pads, i, j, number_of_steps, indices):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", str("DRUM PADSSS CHANGED !!!!!!!11111"))

        drum_pads_tuple = [0, i, j, number_of_steps]
        for index in range(number_of_steps * 2):
            drum_pads_tuple.append(int(indices[index]))

        for drum_pad in drum_pads:
            drum_pads_tuple.append(int(drum_pad.note))
            drum_pads_tuple.append(repr3(drum_pad.name))
            drum_pads_tuple.append(int(drum_pad.mute))
            drum_pads_tuple.append(int(drum_pad.solo))
        self.oscServer.sendOSC("/track/device/drumpads", tuple(drum_pads_tuple))
    

    def drum_pad_changed(self, drum_pad, i, j, number_of_steps, indices):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", str("DRUM PAD CHANGED !!!!!!!11111"))

        drum_pad_tuple = [0, i, j, number_of_steps]
        for index in range(number_of_steps * 2):
            drum_pad_tuple.append(int(indices[index]))
                
        drum_pad_tuple.append(int(drum_pad.note))
        drum_pad_tuple.append(repr3(drum_pad.name))
        drum_pad_tuple.append(int(drum_pad.mute))
        drum_pad_tuple.append(int(drum_pad.solo))
        self.oscServer.sendOSC("/track/device/drumpad", tuple(drum_pad_tuple))


    
    def param_changestate(self, param, tid, did, pid, type, number_of_steps, indices):
        if type == 1:
            indis = [type, 0, did, pid, param.value, repr3(param.__str__()), number_of_steps]
            for index in range(number_of_steps * 2):
                indis.append(int(indices[index]))
            indis.append(int(param.is_enabled))
            indis.append(int(param.automation_state))
            self.oscServer.sendOSC('/master/device/parameter', (tuple(indis)))
        elif type == 2:
            indis = [type, tid, did, pid, param.value, repr3(param.__str__()), number_of_steps]
            for index in range(number_of_steps * 2):
                indis.append(int(indices[index]))
            indis.append(int(param.is_enabled))
            indis.append(int(param.automation_state))
            self.oscServer.sendOSC('/return/device/parameter', (tuple(indis)))
        else:
            indis = [type, tid, did, pid, param.value, repr3(param.__str__()), number_of_steps]
            for index in range(number_of_steps * 2):
                indis.append(int(indices[index]))
            indis.append(int(param.is_enabled))
            indis.append(int(param.automation_state))
            self.oscServer.sendOSC('/track/device/parameter', (tuple(indis)))


    def add_devices_listener(self, track, tid, type):

        key = '%s.%s' % (type, tid)

        cb = lambda :self.devices_changed(track, tid, type)
        if self.devices_listen.has_key(key) != 1:
            track.add_devices_listener(cb)
            self.devices_listen[key] = cb



    def add_chain_devices_listener(self, track, tid, type, chain):
    
        key = '%s.%s' % (type, tid)
        chaindevicelisten = self.chaindevicelisten[key]
        
        cb = lambda :self.devices_changed(track, tid, type)
        if chaindevicelisten.has_key(chain) != 1:
            chain.add_devices_listener(cb)
            chaindevicelisten[chain] = cb


    def device_changestate(self):
        
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "Appointed device checked")

        device = self.song().appointed_device
        if device == None:
            return
        else:
            pass
        
        track = device.canonical_parent
        did = 0
        type = 0
        number_of_steps = 0
        indices = []

        while track.canonical_parent != self.song():

            if number_of_steps % 2 != 0:
                indices.append(self.tuple_idx(track.chains, device))
            else:
                indices.append(self.tuple_idx(track.devices, device))
    

            number_of_steps = number_of_steps + 1
            
            device = track
            track = device.canonical_parent



        if track.canonical_parent == self.song():

            did = self.tuple_idx(track.devices, device)
            #self.oscServer.sendOSC("/NSLOG_REPLACE", (str("selected device DID")))

            #self.oscServer.sendOSC("/NSLOG_REPLACE", (str("selected device DID"), int(did)))


            tid = self.tuple_idx(self.song().tracks, track)
            type = 0

            if tid < 0:

                tid = self.tuple_idx(self.song().return_tracks, track)
                
                if tid >= 0:
                    type = 2
                else:
                    type = 1
                    tid = 0
        indis = [type, tid, did, int(number_of_steps/2)]

        for i in range(len(indices)):
            indis.append(int(indices[len(indices)-1-i]))
       
        self.oscServer.sendOSC('/selected_device', tuple(indis))

    def tuple_idx(self, tuple, obj):
        for i in xrange(0,len(tuple)):
            if (tuple[i] == obj):
                return i
        return -1
    

    def remove_devices_listener(self, track, tid, type):

        key = '%s.%s' % (type, tid)
        
        if self.devices_listen.has_key(key) == 1:
            ocb = self.devices_listen[key]
            if track.devices_has_listener(ocb) == 1:
                track.remove_devices_listener(ocb)
            del self.devices_listen[key]

        if self.chaindevicelisten.has_key(key) == 1:
                                                    
            chaindevicelisten = self.chaindevicelisten[key]
                                                    
            for pr in chaindevicelisten:
                if pr != None:
                    ocb = chaindevicelisten[pr]
                    if pr.devices_has_listener(ocb) == 1:
                        pr.remove_devices_listener(ocb)
            del self.chaindevicelisten[key]


    def send_update_for_device(self, device, track, tid, did, type, num, number_of_steps, indices, i):
        

        if i != -1:
            
            indices.append(int(i))
            number_of_steps = number_of_steps+1

        elif i == -1 and number_of_steps == 0:
            indic = []
            indices = list(indic)



        nm = repr3(device.name)
        params = device.parameters
        onoff = params[0].value
        numParams = len(params)
        cnam = repr3(device.class_name)
        
        
        tr = tid
        dev = did
        
        
        po = [type]
        po.append(int(tr))
        po.append(int(dev))
        
        is_selected = 0
        
        if device == self.song().appointed_device:
            is_selected = 1
        else:
            pass


        po2 = [type]
        po2.append(int(tr))
        po2.append(int(dev))
        po2.append(repr3(track.name))
        po2.append(repr3(device.name))
        po2.append(int(is_selected))
        
        po.append(int(number_of_steps))
        po2.append(int(number_of_steps))
        
        
        
        po4 = [type]
        po4.append(int(tr))
        po4.append(int(dev))
        po4.append(int(number_of_steps))


        for index in range(number_of_steps * 2):
            po.append(int(indices[index]))
            po2.append(int(indices[index]))
            po4.append(int(indices[index]))



        for j in range(len(params)):
            para = params[j]
            po.append(para.min)
            po.append(para.max)
            po.append(para.is_quantized+1)
            val = para.value
            po2.append(float(val))
            po2.append(repr3(para.name))
            po2.append(repr3(para.__str__()))
            po4.append(int(para.is_enabled))
            automation_state = 0
            if params[j].automation_state:
                automation_state = params[j].automation_state
            po4.append(int(automation_state))


        try:
            can_have_chains = device.can_have_chains
        except:
            can_have_chains = 0
        
        try:
            can_have_drumpads = device.can_have_drum_pads and device.has_drum_pads and device.class_name == 'MultiSampler' or device.class_name == "DrumGroupDevice"
        except:
            can_have_drumpads = 0

        self.update_simpler_parameters(device, track, tid, did, type , number_of_steps, indices)
        #self.oscServer.sendOSC("/NSLOG_REPLACE", ("0 adding device:"))
        index_in_indices = number_of_steps * 2 -1

        #self.oscServer.sendOSC("/NSLOG_REPLACE", ("0 adding device: ", "on track:", int(tid), int(did), "number of steps:", int(number_of_steps), "last step:", int(index_in_indices), "name:", repr3(device.name), "can have chains:", int(can_have_chains), "can have drumpads:", int(can_have_drumpads)))

        live_pointer = str(device._live_ptr)
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "pointer start" + str(live_pointer))

        if type == 0:

            
            po3 = [0, tid, did, nm, onoff, num, numParams, int(can_have_drumpads), cnam, int(can_have_chains), number_of_steps]
            
            for index in range(number_of_steps * 2):
                po3.append(int(indices[index]))

            if can_have_drumpads or can_have_chains:
                po3.append(int(device.has_macro_mappings))
        
            po3.append(str(live_pointer))

            self.oscServer.sendOSC("/track/device", (tuple(po3)))
            self.oscServer.sendOSC("/device/range", tuple(po))
            self.oscServer.sendOSC("/track/device/parameters", tuple(po2))
            self.oscServer.sendOSC("/track/device/parameters/enabled", tuple(po4))
            
            if can_have_drumpads:
                
                #self.oscServer.sendOSC("/NSLOG_REPLACE", (str("SENDING DRUMPADS"), int(21)))
                drum_pads_tuple = [type, tid, did, number_of_steps]
                for index in range(number_of_steps * 2):
                    drum_pads_tuple.append(int(indices[index]))
                
                
                for drum_pad in device.drum_pads:
                    drum_pads_tuple.append(int(drum_pad.note))
                    drum_pads_tuple.append(repr3(drum_pad.name))
                    drum_pads_tuple.append(int(drum_pad.mute))
                    drum_pads_tuple.append(int(drum_pad.solo))
                self.oscServer.sendOSC("/track/device/drumpads", tuple(drum_pads_tuple))
                #self.oscServer.sendOSC("/NSLOG_REPLACE", (str("SENDING DRUMPADS"), int(3)))
        
        elif type == 2:
            po3 = [2, tid, did, nm, onoff, num, numParams, int(can_have_drumpads), cnam, int(can_have_chains), number_of_steps]
            for index in range(number_of_steps * 2):
                po3.append(int(indices[index]))

            po3.append(str(live_pointer))

            self.oscServer.sendOSC("/return/device", (tuple(po3)))
            
            self.oscServer.sendOSC("/device/range", tuple(po))
            self.oscServer.sendOSC("/return/device/parameters", tuple(po2))
            self.oscServer.sendOSC("/return/device/parameters/enabled", tuple(po4))
        
        elif type == 1:
            po3 = [1, 0, did, nm, onoff, num, numParams, int(can_have_drumpads), cnam, int(can_have_chains), number_of_steps]
            for index in range(number_of_steps * 2):
                po3.append(int(indices[index]))

            po3.append(str(live_pointer))

            self.oscServer.sendOSC("/master/device", (tuple(po3)))

            self.oscServer.sendOSC("/device/range", tuple(po))
            self.oscServer.sendOSC("/master/device/parameters", tuple(po2))
            self.oscServer.sendOSC("/master/device/parameters/enabled", tuple(po4))
        

        
        if can_have_chains == 1:
            for chain_id in range(len(device.chains)):
                
                chain = device.chains[chain_id]

                #self.oscServer.sendOSC("/NSLOG_REPLACE", ("0 adding chain_id: ", int(chain_id), "on track:", int(tid), int(did), int(number_of_steps), "name:", repr3(chain.name)))
                
                indis = list(indices)
                indis.append(int(chain_id))
                #self.oscServer.sendOSC("/NSLOG_REPLACE", ("1 adding chain_id: ", int(chain_id), "name:", repr3(chain.name)))

                po3 = [type, tid, did, repr3(chain.name), number_of_steps]
                for index in range(number_of_steps * 2 + 1):
                    po3.append(int(indis[index]))
                
                #self.oscServer.sendOSC("/NSLOG_REPLACE", ("2 adding chain_id: ", int(chain_id), "name:", repr3(chain.name)))

                self.oscServer.sendOSC("/device_chain", (tuple(po3)))
                
                for device_id in range(len(chain.devices)):
                    dev = chain.devices[device_id]
                    
                    lis = list(indis)
                    
                    self.send_update_for_device(dev, track, tid, did, type, len(chain.devices), number_of_steps, lis, device_id)





    def devices_changed(self, track, tid, type):
        a = Live.Application.get_application().get_major_version()
        
        
        for a_tid in range(len(LiveUtils.getSong().tracks)):
            atrack = LiveUtils.getSong().tracks[a_tid]
            if atrack == track:
                tid = a_tid
        
        self.oscServer.sendOSC("/devices_empty", (int(type), int(tid)))


        did = 0
        
        number_of_steps = 0
        i = 0
        indices = []
        
        for device in track.devices:
            
            lis = list(indices)

            self.send_update_for_device(device, track, tid, did, type, len(track.devices), number_of_steps, lis, -1)

            did = did+1

        self.oscServer.sendOSC('/devices_loaded', (int(type), int(tid)))
        self.add_device_listeners_for_track(track, int(tid), int(type))


    def convert_clip_to_simpler(self,msg):
    
        tid = msg[2]
        cid = msg[3]

        clip = LiveUtils.getClip(tid, cid)
    
        Live.Conversions.create_midi_track_with_simpler(clip)
    
    def setGlobalGroove(self,msg):
    
        global_groove = msg[2]
        self.oscServer.sendOSC("/NSLOG_REPLACE", "try to groove set")

        LiveUtils.getSong().groove_amountProperty = global_groove
    
    def setExclusiveSolo(self,msg):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "solo")

        global_groove = msg[2]
        LiveUtils.getSong().exclusive_solo = global_groove
        self.oscServer.sendOSC("/NSLOG_REPLACE", "solo set")

    def setExclusiveArm(self,msg):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "arm")

        global_groove = msg[2]        
        LiveUtils.getSong().exclusive_arm = global_groove
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "arm set")

    
    def sendGlobalGroove(self):
    
        self.oscServer.sendOSC("/set/global_groove_amount", LiveUtils.getSong().groove_amountProperty)
    
    def add_listener_for_compressor(self, device, track, tid, did, type, num, number_of_steps, indices):
        cb1 = lambda :self.update_available_input_routing_channels(device, track, tid, did, type , number_of_steps, indices);
    
        cb2 = lambda :self.update_available_input_routing_types(device, track, tid, did, type , number_of_steps, indices);
    
        cb3 = lambda :self.update_input_routing_channel(device, track, tid, did, type , number_of_steps, indices);
        
        cb4 = lambda :self.update_input_routing_type(device, track, tid, did, type , number_of_steps, indices);
        key = '%s.%s' % (type, tid)

        compressor_available_input_routing_channels_listener  = self.compressor_available_input_routing_channels_listener[key]
        compressor_available_input_routing_types_listener = self.compressor_available_input_routing_types_listener[key]
        compressor_input_routing_channel_listener = self.compressor_input_routing_channel_listener[key]
        compressor_input_routing_type_listener  = self.compressor_input_routing_type_listener[key]

        if compressor_available_input_routing_channels_listener.has_key(device) != 1:
            self.update_available_input_routing_channels(device, track, tid, did, type , number_of_steps, indices)
            device.add_available_input_routing_channels_listener(cb1)
            compressor_available_input_routing_channels_listener[device] = cb1

        
        if compressor_available_input_routing_types_listener.has_key(device.view) != 1:
            self.update_available_input_routing_types(device, track, tid, did, type , number_of_steps, indices)
            device.add_available_input_routing_types_listener(cb2)
            compressor_available_input_routing_types_listener[device.view] = cb2

        if compressor_input_routing_channel_listener.has_key(device) != 1:
            self.update_input_routing_channel(device, track, tid, did, type , number_of_steps, indices)
            device.add_input_routing_channel_listener(cb3)
            compressor_input_routing_channel_listener[device] = cb3
        
        if compressor_input_routing_type_listener.has_key(device) != 1:
            self.update_input_routing_type(device, track, tid, did, type , number_of_steps, indices)
            device.add_input_routing_type_listener(cb4)
            compressor_input_routing_type_listener[device] = cb4



    def add_listener_for_simpler(self, device, track, tid, did, type, num, number_of_steps, indices):
        
        
        #cb = lambda :self.update_sample(device, track, tid, did, type , number_of_steps, indices);
        
        cb1 = lambda :self.update_playbackmode(device, track, tid, did, type , number_of_steps, indices);
        
        cb2 = lambda :self.update_selected_slice(device, track, tid, did, type , number_of_steps, indices);
        
        cb3 = lambda :self.update_simpler_playing_position(device, track, tid, did, type , number_of_steps, indices);
        
        
        cb5 = lambda :self.update_slicing_playback_mode(device, track, tid, did, type , number_of_steps, indices);
        
        key = '%s.%s' % (type, tid)
        simpler_playbackmode_listener  = self.simpler_playbackmode_listener[key]
        simpler_slicing_playbackmode_listener = self.simpler_slicing_playbackmode_listener[key]
        sample_listeners  = self.sample_listeners[key]
        simpler_selected_slice_listener = self.simpler_selected_slice_listener[key]
        simpler_playing_position_listener = self.simpler_playing_position_listener[key]

        simpler = device

        
        """ if sample_listeners.has_key(device) != 1:
            self.update_sample(simpler, track, tid, did, type , number_of_steps, indices)
            device.add_sample_listener(cb)
            sample_listeners[device] = cb """
            
        if simpler_playbackmode_listener.has_key(device) != 1:
            self.update_playbackmode(simpler, track, tid, did, type , number_of_steps, indices)
            device.add_playback_mode_listener(cb1)
            simpler_playbackmode_listener[device] = cb1
        
        if simpler_selected_slice_listener.has_key(device.view) != 1:
            self.update_selected_slice(simpler, track, tid, did, type , number_of_steps, indices)
            device.view.add_selected_slice_listener(cb2)
            simpler_selected_slice_listener[device.view] = cb2
        
        if simpler_playing_position_listener.has_key(device) != 1:
            self.update_simpler_playing_position(device, track, tid, did, type , number_of_steps, indices)
            device.add_playing_position_listener(cb3)
            simpler_playing_position_listener[device] = cb3
        

        
        if simpler_slicing_playbackmode_listener.has_key(device) != 1:
            self.update_slicing_playback_mode(device, track, tid, did, type , number_of_steps, indices)
            device.add_slicing_playback_mode_listener(cb5)
            simpler_slicing_playbackmode_listener[device] = cb5
        
        
    
        if simpler.sample != None:
                self.add_listener_for_simpler_sample(device, track, tid, did, type, number_of_steps, indices)

    def add_listener_for_wavetable(self, device, track, tid, did, type, num, number_of_steps, indices):



    
        cb1 = lambda :self.update_wavetable_filter_routing(device, track, tid, did, type , number_of_steps, indices);
        
        
        cb3 = lambda :self.update_wavetable_mono_poly(device, track, tid, did, type , number_of_steps, indices);
        
        cb4 = lambda :self.update_wavetable_oscillator_1_effect(device, track, tid, did, type , number_of_steps, indices);
        
        cb5 = lambda :self.update_wavetable_oscillator_1_wavetable_category(device, track, tid, did, type , number_of_steps, indices);

        cb7 = lambda :self.update_wavetable_oscillator_1_wavetables(device, track, tid, did, type , number_of_steps, indices);

        cb6 = lambda :self.update_wavetable_oscillator_1_wavetable_index(device, track, tid, did, type , number_of_steps, indices);
        
        cb8 = lambda :self.update_wavetable_oscillator_2_effect_enabled(device, track, tid, did, type , number_of_steps, indices);
        
        cb9 = lambda :self.update_wavetable_oscillator_2_wavetable_category_mode(device, track, tid, did, type , number_of_steps, indices);
        
        cb11 = lambda :self.update_wavetable_oscillator_2_wavetables(device, track, tid, did, type , number_of_steps, indices);

        cb10 = lambda :self.update_wavetable_oscillator_2_wavetable_index(device, track, tid, did, type , number_of_steps, indices);


        cb12 = lambda :self.update_wavetable_poly_voices(device, track, tid, did, type , number_of_steps, indices);
        
        cb13 = lambda :self.update_wavetable_unison_mode(device, track, tid, did, type , number_of_steps, indices);
        
        cb14 = lambda :self.update_wavetable_unison_voice_count(device, track, tid, did, type , number_of_steps, indices);
        
        cb15 = lambda :self.update_wavetable_visible_modulation_target_names(device, track, tid, did, type , number_of_steps, indices);
        
        cb2 = lambda :self.update_wavetable_modulation_matrix(device, track, tid, did, type , number_of_steps, indices);

        
        key = '%s.%s' % (type, tid)
        
        wavetable_filter_routing_listener  = self.wavetable_filter_routing_listener[key]
        wavetable_modulation_matrix_listener = self.wavetable_modulation_matrix_listener[key]
        wavetable_mono_poly_listener = self.wavetable_mono_poly_listener[key]
        wavetable_oscillator_1_effect_listener  = self.wavetable_oscillator_1_effect_listener[key]
        wavetable_oscillator_1_wavetable_category_listener = self.wavetable_oscillator_1_wavetable_category_listener[key]
        wavetable_oscillator_1_wavetable_index_listener = self.wavetable_oscillator_1_wavetable_index_listener[key]
        wavetable_oscillator_1_wavetables_listener  = self.wavetable_oscillator_1_wavetables_listener[key]
        wavetable_oscillator_2_effect_listener = self.wavetable_oscillator_2_effect_listener[key]
        wavetable_oscillator_2_wavetable_category_listener = self.wavetable_oscillator_2_wavetable_category_listener[key]
        wavetable_oscillator_2_wavetable_index_listener  = self.wavetable_oscillator_2_wavetable_index_listener[key]
        wavetable_oscillator_2_wavetables_listener = self.wavetable_oscillator_2_wavetables_listener[key]
        wavetable_poly_voices_listener = self.wavetable_poly_voices_listener[key]
        wavetable_unison_mode_listener = self.wavetable_unison_mode_listener[key]
        wavetable_unison_voice_count_listener  = self.wavetable_unison_voice_count_listener[key]
        wavetable_visible_modulation_target_names_listener = self.wavetable_visible_modulation_target_names_listener[key]
    
        wavetable = device
        
        self.update_oscillator_wavetable_categories(wavetable, track, tid, did, type , number_of_steps, indices)

        if wavetable_filter_routing_listener.has_key(device) != 1:
            self.update_wavetable_filter_routing(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_filter_routing_listener(cb1)
            wavetable_filter_routing_listener[device] = cb1
        

        
        if wavetable_mono_poly_listener.has_key(device) != 1:
            self.update_wavetable_mono_poly(device, track, tid, did, type , number_of_steps, indices)
            device.add_mono_poly_listener(cb3)
            wavetable_mono_poly_listener[device] = cb3
        
        if wavetable_oscillator_1_effect_listener.has_key(device) != 1:
            self.update_wavetable_oscillator_1_effect(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_1_effect_mode_listener(cb4)
            wavetable_oscillator_1_effect_listener[device] = cb4

        if wavetable_oscillator_1_wavetable_category_listener.has_key(device) != 1:
            self.update_wavetable_oscillator_1_wavetable_category(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_1_wavetable_category_listener(cb5)
            wavetable_oscillator_1_wavetable_category_listener[device] = cb5
        
        if wavetable_oscillator_1_wavetable_index_listener.has_key(device.view) != 1:
            self.update_wavetable_oscillator_1_wavetable_index(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_1_wavetable_index_listener(cb6)
            wavetable_oscillator_1_wavetable_index_listener[device] = cb6
        
        if wavetable_oscillator_1_wavetables_listener.has_key(device) != 1:
            self.update_wavetable_oscillator_1_wavetables(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_1_wavetables_listener(cb7)
            wavetable_oscillator_1_wavetables_listener[device] = cb7
        
        if wavetable_oscillator_2_effect_listener.has_key(device) != 1:
            self.update_wavetable_oscillator_2_effect_enabled(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_2_effect_mode_listener(cb8)
            wavetable_oscillator_2_effect_listener[device] = cb8

        if wavetable_oscillator_2_wavetable_category_listener.has_key(device) != 1:
            self.update_wavetable_oscillator_2_wavetable_category_mode(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_2_wavetable_category_listener(cb9)
            wavetable_oscillator_2_wavetable_category_listener[device] = cb9
    
        if wavetable_oscillator_2_wavetable_index_listener.has_key(device) != 1:
            self.update_wavetable_oscillator_2_wavetable_index(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_2_wavetable_index_listener(cb10)
            wavetable_oscillator_2_wavetable_index_listener[device] = cb10
        
        if wavetable_oscillator_2_wavetables_listener.has_key(device.view) != 1:
            self.update_wavetable_oscillator_2_wavetables(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_oscillator_2_wavetables_listener(cb11)
            wavetable_oscillator_2_wavetables_listener[device] = cb11
        
        if wavetable_poly_voices_listener.has_key(device) != 1:
            self.update_wavetable_poly_voices(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_poly_voices_listener(cb12)
            wavetable_poly_voices_listener[device] = cb12

        if wavetable_unison_mode_listener.has_key(device) != 1:
            self.update_wavetable_unison_mode(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_unison_mode_listener(cb13)
            wavetable_unison_mode_listener[device] = cb13

        if wavetable_unison_voice_count_listener.has_key(device) != 1:
            self.update_wavetable_unison_voice_count(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_unison_voice_count_listener(cb14)
            wavetable_unison_voice_count_listener[device] = cb14
    
        if wavetable_visible_modulation_target_names_listener.has_key(device) != 1:
            self.update_wavetable_visible_modulation_target_names(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_visible_modulation_target_names_listener(cb15)
            wavetable_visible_modulation_target_names_listener[device] = cb15
                
        if wavetable_modulation_matrix_listener.has_key(device.view) != 1:
            self.update_wavetable_modulation_matrix(wavetable, track, tid, did, type , number_of_steps, indices)
            device.add_modulation_matrix_changed_listener(cb2)
            wavetable_modulation_matrix_listener[device] = cb2
                

    def update_available_input_routing_channels(self, device, track, tid, did, type , number_of_steps, indices):
   
        data = [int(type)]
        data.append(int(tid))
        data.append(int(did))
        data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            data.append(int(indices[index]))

        data.append(int(len(device.available_input_routing_channels)))


        for index in range(len(device.available_input_routing_channels)):
            input_routing = device.available_input_routing_channels[index]
            data.append(repr3(input_routing.display_name))
        
        self.oscServer.sendOSC("/device/compressor/update_available_input_routing_channels", data)
   

    def update_available_input_routing_types(self, device, track, tid, did, type , number_of_steps, indices):
       
        data = [int(type)]
        data.append(int(tid))
        data.append(int(did))
        data.append(int(number_of_steps))
       
        for index in range(number_of_steps * 2):
            data.append(int(indices[index]))
               
        data.append(int(len(device.available_input_routing_types)))
               
               
        for index in range(len(device.available_input_routing_types)):
            input_type = device.available_input_routing_types[index]
            data.append(repr3(input_type.display_name))
                       
        self.oscServer.sendOSC("/device/compressor/update_available_input_routing_types", data)
            
            
   
    def update_input_routing_channel(self,device, track, tid, did, type , number_of_steps, indices):
        
        data = [int(type)]
        data.append(int(tid))
        data.append(int(did))
        data.append(int(number_of_steps))
            
        for index in range(number_of_steps * 2):
            data.append(int(indices[index]))
        
        number = 0
        
        for index in range(len(device.available_input_routing_channels)):
            input_type = device.available_input_routing_channels[index]
            if input_type == device.input_routing_channel:
                number = index
        
        data.append(int(number))
            
        self.oscServer.sendOSC("/device/compressor/update_input_routing_channel", data)

        
    def update_input_routing_type(self, device, track, tid, did, type , number_of_steps, indices):

        data = [int(type)]
        data.append(int(tid))
        data.append(int(did))
        data.append(int(number_of_steps))

        number = 0
    
        for index in range(len(device.available_input_routing_types)):
            input_type = device.available_input_routing_types[index]
            if input_type == device.input_routing_type:
                number = index
        
        data.append(int(number))
        
        self.oscServer.sendOSC("/device/compressor/update_input_routing_type", data)

    def update_oscillator_wavetable_categories(self, device, track, tid, did, type , number_of_steps, indices):

        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))

        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        play_pos_data.append(int(len(device.oscillator_wavetable_categories)))

        
        for index in range(len(device.oscillator_wavetable_categories)):
            filter_routing = device.oscillator_wavetable_categories[index]
            play_pos_data.append(repr3(filter_routing))
        
        self.oscServer.sendOSC("/device/wavetable/update_oscillator_wavetable_categories", play_pos_data)


    def update_wavetable_filter_routing(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
    
        filter_routing = device.filter_routing
        play_pos_data.append(int(filter_routing))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_filter_routing", play_pos_data)

    def get_modulation_matrix(self,msg):
            
        
        device = self.get_device_for_message(msg)
        number_of_steps = msg[5]
        new_index = 6+(number_of_steps)*2
        target = msg[new_index]
        source = msg[new_index + 1]
        
        if device.class_name == 'InstrumentVector':
            wavetable = device
            mod_val = wavetable.get_modulation_value(target,source)
            
            play_pos_data = [int(type)]
            play_pos_data.append(int(tid))
            play_pos_data.append(int(did))
            play_pos_data.append(int(number_of_steps))
            
            for index in range(number_of_steps * 2):
                play_pos_data.append(int(indices[index]))
        
            play_pos_data.append(float(mod_val))
    
            self.oscServer.sendOSC("/device/wavetable/set_modulation_value", play_pos_data)
    

    def update_wavetable_modulation_matrix(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        

        play_pos_data.append(int(len(device.visible_modulation_target_names) * 5))
        
        for index in range(len(device.visible_modulation_target_names)):
            for index2 in range(5):
                play_pos_data.append(float(device.get_modulation_value(index,index2)))
            

        self.oscServer.sendOSC("/device/wavetable/update_wavetable_modulation_matrix", play_pos_data)


    def update_wavetable_mono_poly(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
    
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        mono_poly = device.mono_poly
        play_pos_data.append(int(mono_poly))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_mono_poly", play_pos_data)


    def update_wavetable_oscillator_1_effect(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        oscillator_1_effect_mode = device.oscillator_1_effect_mode
        play_pos_data.append(int(oscillator_1_effect_mode))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_1_effect", play_pos_data)


    def update_wavetable_oscillator_1_wavetable_category(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
    
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        oscillator_1_wavetable_category = device.oscillator_1_wavetable_category
        play_pos_data.append(int(oscillator_1_wavetable_category))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_1_wavetable_category", play_pos_data)
            


    def update_wavetable_oscillator_1_wavetable_index(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        oscillator_1_wavetable_index = device.oscillator_1_wavetable_index
        play_pos_data.append(int(oscillator_1_wavetable_index))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_1_wavetable_index", play_pos_data)



    def update_wavetable_oscillator_1_wavetables(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
    
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))

        play_pos_data.append(int(len(device.oscillator_1_wavetables)))

        for index in range(len(device.oscillator_1_wavetables)):
            filter_routing = device.oscillator_1_wavetables[index]
            play_pos_data.append(repr3(filter_routing))

        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_1_wavetables", play_pos_data)

    
    def update_wavetable_oscillator_2_effect_enabled(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        oscillator_2_effect_mode = device.oscillator_2_effect_mode
        play_pos_data.append(int(oscillator_2_effect_mode))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_2_effect_enabled", play_pos_data)


    def update_wavetable_oscillator_2_wavetable_category_mode(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
    
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        oscillator_2_wavetable_category = device.oscillator_2_wavetable_category
        play_pos_data.append(int(oscillator_2_wavetable_category))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_2_wavetable_category_mode", play_pos_data)



    def update_wavetable_oscillator_2_wavetable_index(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        oscillator_2_wavetable_index = device.oscillator_2_wavetable_index
        play_pos_data.append(int(oscillator_2_wavetable_index))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_2_wavetable_index", play_pos_data)


    def update_wavetable_oscillator_2_wavetables(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
    
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        play_pos_data.append(int(len(device.oscillator_2_wavetables)))

        for index in range(len(device.oscillator_2_wavetables)):
            filter_routing = device.oscillator_2_wavetables[index]
            play_pos_data.append(repr3(filter_routing))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_oscillator_2_wavetables", play_pos_data)

    
    def update_wavetable_poly_voices(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        poly_voices = device.poly_voices
        play_pos_data.append(int(poly_voices))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_poly_voices", play_pos_data)





    def update_wavetable_unison_mode(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        unison_mode = device.unison_mode
        play_pos_data.append(int(unison_mode))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_unison_mode", play_pos_data)



    def update_wavetable_unison_voice_count(self, device, track, tid, did, type , number_of_steps, indices):
    
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))
    
        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))
        
        unison_voice_count = device.unison_voice_count
        play_pos_data.append(int(unison_voice_count))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_unison_voice_count", play_pos_data)


    def update_wavetable_visible_modulation_target_names(self, device, track, tid, did, type , number_of_steps, indices):
        
        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))

        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))

        play_pos_data.append(int(len(device.visible_modulation_target_names)))

        for index in range(len(device.visible_modulation_target_names)):
            filter_routing = device.visible_modulation_target_names[index]
            play_pos_data.append(repr3(filter_routing))
        
        self.oscServer.sendOSC("/device/wavetable/update_wavetable_visible_modulation_target_names", play_pos_data)




    def update_slicing_playback_mode(self, device, track, tid, did, type , number_of_steps, indices):
    
        slicing_pp_mode_data = [int(type)]
        slicing_pp_mode_data.append(int(tid))
        slicing_pp_mode_data.append(int(did))
        slicing_pp_mode_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            slicing_pp_mode_data.append(int(indices[index]))
    
        slicing_pp_mode = device.slicing_playback_mode
        slicing_pp_mode_data.append(int(slicing_pp_mode))
        
        self.oscServer.sendOSC("/device/simpler/update_simpler_slicing_pp_mode", slicing_pp_mode_data)
            

    def update_simpler_playing_position(self, device, track, tid, did, type , number_of_steps, indices):

        play_pos_data = [int(type)]
        play_pos_data.append(int(tid))
        play_pos_data.append(int(did))
        play_pos_data.append(int(number_of_steps))

        for index in range(number_of_steps * 2):
            play_pos_data.append(int(indices[index]))

        play_pos = device.playing_position
        play_pos_data.append(play_pos)

        self.oscServer.sendOSC("/device/simpler/update_simpler_playing_position", play_pos_data)


    def update_selected_slice(self, device, track, tid, did, type , number_of_steps, indices):

        slice_data = [int(type)]
        slice_data.append(int(tid))
        slice_data.append(int(did))
        slice_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            slice_data.append(int(indices[index]))
        
        if device.sample != None:
        
            #message = "selected slice " + str(device.view.selected_slice)
            #self.oscServer.sendOSC("/NSLOG_REPLACE", message)

            sel_slice_val = device.view.selected_slice
            if sel_slice_val >= 0:
                slice_data.append(sel_slice_val)
                self.oscServer.sendOSC("/device/simpler/update_selected_slice", slice_data)


    def update_playbackmode(self, simpler, track, tid, did, type , number_of_steps, indices):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "playbackmode got updated")

        waveform_data = [int(type)]
        waveform_data.append(int(tid))
        waveform_data.append(int(did))
        waveform_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            waveform_data.append(int(indices[index]))

        waveform_data.append(int(simpler.playback_mode))

        #self.oscServer.sendOSC("/NSLOG_REPLACE", str(simpler.playback_mode))

        self.oscServer.sendOSC("/device/simpler/update_playback_mode", waveform_data)



    def update_sample(self, simpler, track, tid, did, type , number_of_steps, indices):
    
        self.add_listener_for_simpler_sample(simpler, track, tid, did, type, number_of_steps, indices)
    
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "sample got updated")
        #self.update_simpler_waveform(simpler, track, tid, did, type, number_of_steps, indices, 0, 1)


    def update_simpler_waveformcb(self, msg):
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb")

        type = msg[2]
        tid = msg[3]
        did = msg[4]
        start_in_percent = msg[5]
        end_in_percent = msg[6]

        number_of_steps = msg[7]
        
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb0")

        if type == 0:
            track = LiveUtils.getSong().tracks[tid]
        elif type == 2:
            track = LiveUtils.getSong().return_tracks[tid]
        elif type == 1:
            track = LiveUtils.getSong().master_track
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb05")

        device = track.devices[did]
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb1115")

        num = len(track.devices)
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb15")

        indices = []
        device_id = -1
        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb25")

        #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb1")

        for i in range(number_of_steps):
            chain_id = msg[8+i*2]
            device_id = msg[9+i*2]
        
            chain = device.chains[chain_id]
            indices.append(int(chain_id))
            
            device = chain.devices[device_id]
            num = len(chain.devices)
            
            indices.append(int(device_id))

        if device.class_name == 'OriginalSimpler':
            simpler = device
            #self.oscServer.sendOSC("/NSLOG_REPLACE", "update_simpler_waveformcb2")

            self.update_simpler_waveform(simpler, track, tid, did, type, number_of_steps, indices, start_in_percent, end_in_percent)




    def update_simpler_waveform(self, simpler, track, tid, did, type, number_of_steps, indices, start_in_percent, end_in_percent):
        try:
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("update_simpler_waveform"))

            sample = simpler.sample
            
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("update_simpler_waveform2"))
            
            sample_length = simpler.sample.length
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("update_simpler_waveform3"))

            path = simpler.sample.file_path
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("update_simpler_waveform4"))

            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("update_simpler_waveform3"))

            reset_data = [int(type)]
            reset_data.append(int(tid))
            reset_data.append(int(did))
            reset_data.append(int(number_of_steps))
        
            # self.oscServer.sendOSC("/NSLOG_REPLACE", (str(path)))

            for index in range(number_of_steps * 2):
                reset_data.append(int(indices[index]))
        
            reset_data.append(str(path))
            reset_data.append(float(start_in_percent))
            reset_data.append(float(end_in_percent))
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("reset_waveform"))

            self.oscServer.sendOSC("/device/simpler/reset_waveform", (tuple(reset_data)))
    
            if simpler.sample.warping:
                try:
                    waveform_data = [int(tid)]
                    waveform_data.append(int(cid))
                    waveform_data.append(float(simpler.sample.sample_to_beat_time(simpler.sample.sample_length)))
            
                    self.oscServer.sendOSC("/device/simpler/sample_length", (tuple(waveform_data)))
                except:
                    pass
            else:
                pass
        
        except:
            #self.oscServer.sendOSC("/NSLOG_REPLACE", ("no wave file found"))
            pass



    def remove_listener_for_simpler_sample(self, device, track, tid, did, type, number_of_steps, indices):

        simpler = device



    def add_listener_for_simpler_sample(self, device, track, tid, did, type, number_of_steps, indices):



        simpler = device
        sample = simpler.sample
        
        if not sample:
            return
        
        key = '%s.%s' % (type, tid)
        sample_slice_listener  = self.sample_slice_listener[key]
        sample_gain_listener  = self.sample_gain_listener[key]
        sample_end_marker_listener = self.sample_end_marker_listener[key]
        sample_start_marker_listener = self.sample_start_marker_listener[key]
        sample_warping_listener = self.sample_warping_listener[key]
        sample_warping_mode_listener = self.sample_warping_mode_listener[key]
        sample_slice_sensitivity_listener = self.sample_slice_sensitivity_listener[key]

        self.update_simpler_sample_parameters(device, track, tid, did, type , number_of_steps, indices)
        

        cb = lambda :self.update_slices(device, track, tid, did, type, number_of_steps, indices,sample);
        
        cb1 = lambda :self.update_gain(device, track, tid, did, type, number_of_steps, indices,sample);
        
        cb2 = lambda :self.update_slice_sensitivity(device, track, tid, did, type, number_of_steps, indices,sample);
        
        cb3 = lambda :self.update_marker(device, track, tid, did, type, number_of_steps, indices,sample);

        cb4 = lambda :self.update_sample_warping(device, track, tid, did, type, number_of_steps, indices,sample);

        cb5 = lambda :self.update_sample_warping_mode(device, track, tid, did, type, number_of_steps, indices,sample);
        
        if sample_slice_listener.has_key(sample) != 1:
            sample.add_slices_listener(cb)
            sample_slice_listener[device] = cb
    
        if sample_gain_listener.has_key(sample) != 1:
            sample.add_gain_listener(cb1)
            sample_gain_listener[device] = cb1
    
        if sample_slice_sensitivity_listener.has_key(sample) != 1:
            sample.add_slicing_sensitivity_listener(cb2)
            sample_slice_sensitivity_listener[device] = cb2

        if sample_end_marker_listener.has_key(sample) != 1:
            sample.add_end_marker_listener(cb3)
            sample_end_marker_listener[device] = cb3

        if sample_start_marker_listener.has_key(sample) != 1:
            sample.add_start_marker_listener(cb3)
            sample_start_marker_listener[device] = cb3

        if sample_warping_listener.has_key(sample) != 1:
            sample.add_warping_listener(cb4)
            sample_warping_listener[device] = cb4

        if sample_warping_mode_listener.has_key(sample) != 1:
            sample.add_warp_mode_listener(cb5)
            sample_warping_mode_listener[device] = cb5



    def update_compressor_parameters(self,device, track, tid, did, type , number_of_steps, indices):

        a_version = Live.Application.get_application().get_major_version()

        if device.class_name == 'Compressor2' and a_version >= 10:

            self.update_available_input_routing_channels(device, track, tid, did, type , number_of_steps, indices)
            self.update_available_input_routing_types(device, track, tid, did, type , number_of_steps, indices)
            self.update_input_routing_channel(device, track, tid, did, type , number_of_steps, indices)
            self.update_input_routing_type(device, track, tid, did, type , number_of_steps, indices)

    def update_wavetable_parameters(self,device, track, tid, did, type , number_of_steps, indices):

        if device.class_name == 'InstrumentVector':
            self.update_oscillator_wavetable_categories(device, track, tid, did, type , number_of_steps, indices)

            self.update_wavetable_filter_routing(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_modulation_matrix(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_mono_poly(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_oscillator_1_effect(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_oscillator_1_wavetable_category(device, track, tid, did, type , number_of_steps, indices);

            self.update_wavetable_oscillator_1_wavetables(device, track, tid, did, type , number_of_steps, indices);

            self.update_wavetable_oscillator_1_wavetable_index(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_oscillator_2_effect_enabled(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_oscillator_2_wavetable_category_mode(device, track, tid, did, type , number_of_steps, indices);

            self.update_wavetable_oscillator_2_wavetables(device, track, tid, did, type , number_of_steps, indices);

            self.update_wavetable_oscillator_2_wavetable_index(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_poly_voices(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_unison_mode(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_unison_voice_count(device, track, tid, did, type , number_of_steps, indices);
        
            self.update_wavetable_visible_modulation_target_names(device, track, tid, did, type , number_of_steps, indices);

    def update_simpler_parameters(self,device, track, tid, did, type , number_of_steps, indices):

        if device.class_name == 'OriginalSimpler':
            self.update_sample(device, track, tid, did, type , number_of_steps, indices);

            self.update_playbackmode(device, track, tid, did, type , number_of_steps, indices);

            self.update_slicing_playback_mode(device, track, tid, did, type , number_of_steps, indices);

            self.update_selected_slice(device, track, tid, did, type , number_of_steps, indices);

            self.update_simpler_playing_position(device, track, tid, did, type , number_of_steps, indices);

            self.update_slicing_playback_mode(device, track, tid, did, type , number_of_steps, indices);

            self.update_simpler_sample_parameters(device, track, tid, did, type , number_of_steps, indices);


    def update_simpler_sample_parameters(self,device, track, tid, did, type , number_of_steps, indices):
        
        if device.sample != None:
            self.update_slices(device, track, tid, did, type, number_of_steps, indices,device.sample);
            self.update_gain(device, track, tid, did, type, number_of_steps, indices,device.sample);
            self.update_slice_sensitivity(device, track, tid, did, type, number_of_steps, indices,device.sample);
            self.update_marker(device, track, tid, did, type, number_of_steps, indices,device.sample);
            self.update_sample_warping(device, track, tid, did, type, number_of_steps, indices,device.sample);
            self.update_sample_warping_mode(device, track, tid, did, type, number_of_steps, indices,device.sample);


    def update_sample_warping(self, device, track, tid, did, type, number_of_steps, indices,sample):

        warping_data = [int(type)]
        warping_data.append(int(tid))
        warping_data.append(int(did))
        warping_data.append(int(number_of_steps))
            
        for index in range(number_of_steps * 2):
            warping_data.append(int(indices[index]))
        
        warping_data.append(sample.warping)

        self.oscServer.sendOSC("/device/simpler/update_warping", (tuple(warping_data)))
    
    def update_sample_warping_mode(self, device, track, tid, did, type, number_of_steps, indices,sample):
    
        warping_mode = sample.warp_mode
        
        warping_mode_data = [int(type)]
        warping_mode_data.append(int(tid))
        warping_mode_data.append(int(did))
        warping_mode_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            warping_mode_data.append(int(indices[index]))

        """ for obj_string in dir(device.sample):
            self.oscServer.sendOSC("/NSLOG_REPLACE", obj_string) """
        
        warping_mode_data.append(warping_mode)
        
        self.oscServer.sendOSC("/device/simpler/update_warping_mode", (tuple(warping_mode_data)))
    

    def update_slices(self, device, track, tid, did, type, number_of_steps, indices, sample):
    
        slices = sample.slices
        length = sample.length
        
        mess = "update slices  " + str(range(len(slices)))
        
        """ self.oscServer.sendOSC("/NSLOG_REPLACE", mess) """
        
        slice_data = [int(type)]
        slice_data.append(int(tid))
        slice_data.append(int(did))
        slice_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            slice_data.append(int(indices[index]))
        
        slice_data.append(int(len(slices)))
        
        for pid in range(len(slices)):
            slice = slices[pid]
            message = str(pid) + str(slice)
            """ self.oscServer.sendOSC("/NSLOG_REPLACE", (message)) """
            slice_val = slice*self.maxSampleLength/length
            slice_data.append(float(slice))


        self.oscServer.sendOSC("/device/simpler/update_slices", (tuple(slice_data)))


    def update_gain(self, device, track, tid, did, type, number_of_steps, indices, sample):
        
        gain = sample.gain

        gain_string = sample.gain_display_string()

        gain_data = [int(type)]
        gain_data.append(int(tid))
        gain_data.append(int(did))
        gain_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            gain_data.append(int(indices[index]))
        
        """ for obj_string in dir(device.sample):
            self.oscServer.sendOSC("/NSLOG_REPLACE", obj_string) """

        gain_data.append(gain)
        gain_data.append(gain_string.__str__())
        self.oscServer.sendOSC("/device/simpler/update_gain", (tuple(gain_data)))
    
    
    
    
    def update_slice_sensitivity(self, device, track, tid, did, type, number_of_steps, indices, sample):
        
        slicing_sensitivity = sample.slicing_sensitivity
        
        gain_data = [int(type)]
        gain_data.append(int(tid))
        gain_data.append(int(did))
        gain_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            gain_data.append(int(indices[index]))
        
        """ for obj_string in dir(sample):
            self.oscServer.sendOSC("/NSLOG_REPLACE", obj_string) """
        
        gain_data.append(slicing_sensitivity)
        self.oscServer.sendOSC("/device/simpler/slicing_sensitivity", (tuple(gain_data)))
    


    def update_marker(self, device, track, tid, did, type, number_of_steps, indices, sample):

        start_marker = sample.start_marker
        end_marker = sample.end_marker
        
        length = sample.length

        marker_data = [int(type)]
        marker_data.append(int(tid))
        marker_data.append(int(did))
        marker_data.append(int(number_of_steps))
        
        for index in range(number_of_steps * 2):
            marker_data.append(int(indices[index]))
        
        """ for obj_string in dir(sample):
            self.oscServer.sendOSC("/NSLOG_REPLACE", obj_string) """
        
        """ start_val = float(start_marker*self.maxSampleLength)/length
        end_val = float(end_marker*self.maxSampleLength)/length """


        marker_data.append(start_marker)
        marker_data.append(end_marker)
        
        self.oscServer.sendOSC("/device/simpler/update_marker", (tuple(marker_data)))

    def track_input_type(self, msg):

        tid = msg[2]
        type = msg[3]
        
        
        track = self.song().tracks[int(tid)]
        
        track.input_routing_type = track.available_input_routing_types[int(type)]



    def track_input_channel(self, msg):
    
        tid = msg[2]
        type = msg[3]
    
        track = self.song().tracks[int(tid)]
        track.input_routing_channel = track.available_input_routing_channels[type]

    def track_output_type(self, msg):
    
        tid = msg[2]
        type = msg[3]
    
        track = self.song().tracks[int(tid)]
        track.output_routing_type = track.available_output_routing_types[type]

    def track_output_channel(self, msg):
    
        tid = msg[2]
        type = msg[3]
    
        track = self.song().tracks[int(tid)]
        track.output_routing_channel = track.available_output_routing_channels[type]


    def sendTrackIO(self, trackNumber, track, type = "", track_type = 0):
        #for current_type in ("available_input_routing_channels", "available_input_routing_types", "available_output_routing_channels", "available_output_routing_types", "input_routing_channel", "input_routing_type", "output_routing_channel", "output_routing_type"):
            


        input_routing_type_number = 0
        input_routing_channel_number = 0
        output_routing_type_number = 0
        output_routing_channel_number = 0
        name = repr3(track.name)
        if type == "":
            io_data = [track_type, trackNumber, name, type]
            

        if type == "input_routing_type" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            track_input_route_type = track.input_routing_type
            track_input_route_type_name = track_input_route_type.display_name
            io_data.append(repr3(track_input_route_type_name))
            found_port = 0
            for i in range(len(track.available_input_routing_types)):
                rout_type = track.available_input_routing_types[i]
                if rout_type == track.input_routing_type:
                    input_routing_type_number = i
                    io_data.append(input_routing_type_number)
                    found_port = 1
                    break
            if found_port == 0:
                io_data.append(0)
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)



        if type == "input_routing_channel" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            track_input_routing_channel = track.input_routing_channel
            track_input_routing_channel_name = track_input_routing_channel.display_name
            io_data.append(repr3(track_input_routing_channel_name))
            found_port = 0
            for i in range(len(track.available_input_routing_channels)):
                rout_type = track.available_input_routing_channels[i]
                if rout_type == track.input_routing_channel:
                    input_routing_channel_number = i
                    io_data.append(input_routing_channel_number)
                    found_port = 1
                    break
            if found_port == 0:
                io_data.append(0)
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)



        if type == "output_routing_type" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            track_output_route_type = track.output_routing_type
            track_output_route_type_name = track_output_route_type.display_name
            io_data.append(repr3(track_output_route_type_name))
            found_port = 0
            for i in range(len(track.available_output_routing_types)):
                rout_type = track.available_output_routing_types[i]
                if rout_type == track.output_routing_type:
                    output_routing_type_number = i
                    io_data.append(output_routing_type_number)
                    found_port = 1
                    break
            if found_port == 0:
                io_data.append(0)
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)



        if type == "output_routing_channel" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            track_output_routing_channel = track.output_routing_channel
            track_output_routing_channel_name = track_output_routing_channel.display_name
            io_data.append(repr3(track_output_routing_channel_name))
            found_port = 0
            for i in range(len(track.available_output_routing_channels)):
                rout_type = track.available_output_routing_channels[i]
                if rout_type == track.output_routing_channel:
                    output_routing_channel_number = i
                    io_data.append(output_routing_channel_number)
                    found_port = 1
                    break
            if found_port == 0:
                io_data.append(0)
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)






        if type == "available_input_routing_channels" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            io_data.append(len(track.available_input_routing_channels))
            for i in range(len(track.available_input_routing_channels)):
                rout_type = track.available_input_routing_channels[i]
                route_name = rout_type.display_name
                io_data.append(repr3(route_name))
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)



        if type == "available_input_routing_types" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            io_data.append(len(track.available_input_routing_types))
            for i in range(len(track.available_input_routing_types)):
                rout_type = track.available_input_routing_types[i]
                route_name = rout_type.display_name
                io_data.append(repr3(route_name))
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)



        if type == "available_output_routing_channels" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            io_data.append(len(track.available_output_routing_channels))
            for i in range(len(track.available_output_routing_channels)):
                rout_type = track.available_output_routing_channels[i]
                route_name = rout_type.display_name
                io_data.append(repr3(route_name))
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)




        if type == "available_output_routing_types" or type == "":
            if type != "":
                io_data = [track_type, trackNumber, name, type]
            io_data.append(len(track.available_output_routing_types))
            for i in range(len(track.available_output_routing_types)):
                rout_type = track.available_output_routing_types[i]
                route_name = rout_type.display_name
                io_data.append(repr3(route_name))
            if type != "":
                self.oscServer.sendOSC("/track/io", io_data)




        if type == "":
            self.oscServer.sendOSC("/track/io", io_data)
        
        

