from PXT_Live.PushConsts import BTN_TYPE_C_VALUES #@UnresolvedImport

# ***************************** [SETTINGS NOTES] **************************

# It is recommended that you back this file up BEFORE modifying it. 

# Please DO NOT change any of the spacing in this file. 
 
# Please DO NOT change the name of this file or its file extension.  When done 
# making your changes to the settings below, just save the file.
 
# After saving this file, you will need to close/restart Live for your changes 
# to take effect.

# ***************************** [PAD COLOR] **************************
OFF =           BTN_TYPE_C_VALUES['OFF']
WHITE_DIM =     BTN_TYPE_C_VALUES['WHITE_DIM']
WHITE_HALF =    BTN_TYPE_C_VALUES['WHITE_HALF']
WHITE_FULL =    BTN_TYPE_C_VALUES['WHITE_FULL']
RED_DIM =       BTN_TYPE_C_VALUES['RED_DIM']
RED_HALF =      BTN_TYPE_C_VALUES['RED_HALF']
RED_FULL =      BTN_TYPE_C_VALUES['RED_FULL']
AMBER_DIM =     BTN_TYPE_C_VALUES['AMBER_DIM']
AMBER_HALF =    BTN_TYPE_C_VALUES['AMBER_HALF']
AMBER_FULL =    BTN_TYPE_C_VALUES['AMBER_FULL']
YELLOW_DIM =    BTN_TYPE_C_VALUES['YELLOW_DIM']
YELLOW_HALF =   BTN_TYPE_C_VALUES['YELLOW_HALF']
YELLOW_FULL =   BTN_TYPE_C_VALUES['YELLOW_FULL']
GREEN_DIM =     BTN_TYPE_C_VALUES['GREEN_DIM']
GREEN_HALF =    BTN_TYPE_C_VALUES['GREEN_HALF']
GREEN_FULL =    BTN_TYPE_C_VALUES['GREEN_FULL']
BLUE_DIM =      BTN_TYPE_C_VALUES['BLUE_DIM']
BLUE_HALF =     BTN_TYPE_C_VALUES['BLUE_HALF']
BLUE_FULL =     BTN_TYPE_C_VALUES['BLUE_FULL']
PURPLE_DIM =    BTN_TYPE_C_VALUES['PURPLE_DIM']
PURPLE_HALF =   BTN_TYPE_C_VALUES['PURPLE_HALF']
PURPLE_FULL =   BTN_TYPE_C_VALUES['PURPLE_FULL']

# ***************************** [PAD CHANNEL] **************************
CH_2 = 1
CH_3 = 2
CH_4 = 3
CH_5 = 4
CH_6 = 5
CH_7 = 6
CH_8 = 7
CH_9 = 8

# ***************************** [PAD MAP] **************************"

# The following settings allow you to customize the Pads in User Mode.

# Pad Row 1 is the uppermost row of Pads. Each Pad Row contains the settings of its 8 Pads.

# For each Pad, you'll specify:
#    - The color to use for the Pad.  The available colors are listed above under PAD COLOR.
#    - The MIDI channel to use for the Pad.  The available channels are listed above under PAD CHANNEL.
#    - The note number to use for the Pad.  This HAS to be in the range of 0 - 127.
    
# You should NOT change anything other than the settings described above.  In particular, you should NOT
# remove any of the parentheses or commas below.  Changes of that sort will result in PXT-Live Plus not loading.

# Incorrect settings, spelling or captialization in your definitions (such as specifying 200 as a 
# note number or Green as a color) may also result in PXT-Live Plus not loading or your settings being ignored.  

# It is recommended that you copy the PAD COLOR and PAD CHANNEL names listed above and paste them into your 
# definitions as opposed to typing them yourself. 

PAD_MAP = ((
            # Pad Row 1
            (GREEN_FULL, CH_4, 48),
            (GREEN_FULL, CH_4, 49),
            (GREEN_FULL, CH_4, 50),
            (GREEN_FULL, CH_4, 51),
            (PURPLE_FULL, CH_5, 48),
            (PURPLE_FULL, CH_5, 49),
            (PURPLE_FULL, CH_5, 50),
            (PURPLE_FULL, CH_5, 51)
            ),(
            # Pad Row 2
            (GREEN_FULL, CH_4, 44),
            (GREEN_FULL, CH_4, 45),
            (GREEN_FULL, CH_4, 46),
            (GREEN_FULL, CH_4, 47),
            (PURPLE_FULL, CH_5, 44),
            (PURPLE_FULL, CH_5, 45),
            (PURPLE_FULL, CH_5, 46),
            (PURPLE_FULL, CH_5, 47)
            ),(
            # Pad Row 3
            (GREEN_FULL, CH_4, 40),
            (GREEN_FULL, CH_4, 41),
            (GREEN_FULL, CH_4, 42),
            (GREEN_FULL, CH_4, 43),
            (PURPLE_FULL, CH_5, 40),
            (PURPLE_FULL, CH_5, 41),
            (PURPLE_FULL, CH_5, 42),
            (PURPLE_FULL, CH_5, 43)
            ),(
            # Pad Row 4 
            (GREEN_FULL, CH_4, 36),
            (GREEN_FULL, CH_4, 37),
            (GREEN_FULL, CH_4, 38),
            (GREEN_FULL, CH_4, 39),
            (PURPLE_FULL, CH_5, 36),
            (PURPLE_FULL, CH_5, 37),
            (PURPLE_FULL, CH_5, 38),
            (PURPLE_FULL, CH_5, 39)
            ),(
            # Pad Row 5 
            (RED_FULL, CH_2, 48),
            (RED_FULL, CH_2, 49),
            (RED_FULL, CH_2, 50),
            (RED_FULL, CH_2, 51),
            (BLUE_FULL, CH_3, 48),
            (BLUE_FULL, CH_3, 49),
            (BLUE_FULL, CH_3, 50),
            (BLUE_FULL, CH_3, 51)
            ),(
            # Pad Row 6
            (RED_FULL, CH_2, 44),
            (RED_FULL, CH_2, 45),
            (RED_FULL, CH_2, 46),
            (RED_FULL, CH_2, 47),
            (BLUE_FULL, CH_3, 44),
            (BLUE_FULL, CH_3, 45),
            (BLUE_FULL, CH_3, 46),
            (BLUE_FULL, CH_3, 47)
            ),(
            # Pad Row 7
            (RED_FULL, CH_2, 40),
            (RED_FULL, CH_2, 41),
            (RED_FULL, CH_2, 42),
            (RED_FULL, CH_2, 43),
            (BLUE_FULL, CH_3, 40),
            (BLUE_FULL, CH_3, 41),
            (BLUE_FULL, CH_3, 42),
            (BLUE_FULL, CH_3, 43)
            ),(
            # Pad Row 8
            (RED_FULL, CH_2, 36),
            (RED_FULL, CH_2, 37),
            (RED_FULL, CH_2, 38),
            (RED_FULL, CH_2, 39),
            (BLUE_FULL, CH_3, 36),
            (BLUE_FULL, CH_3, 37),
            (BLUE_FULL, CH_3, 38),
            (BLUE_FULL, CH_3, 39)
            ))

