ENCODERS_CC_MAP = {}
ENCODERS_NAME_MAP = {}

# ***************************** [SETTINGS NOTES] **************************

# It is recommended that you back this file up BEFORE modifying it.

# Please DO NOT change any of the spacing in this file. 
 
# Please DO NOT change the name of this file or its file extension.  When done 
# making your changes to the settings below, just save the file.
 
# After saving this file, you will need to close/restart Live for your changes 
# to take effect.


# ***************************** [CC MAP] **************************

# The following settings allow you to add additional pages of CCs for the Encoders
# to send in Midi Mode.  You can navigate between these pages via Shift + In/Out.   

# Each of the listings below defines the CC#s for one Encoder.  For example, 
# ENCODERS_CC_MAP[1] defines the CC#s for Encoder 1, ENCODERS_CC_MAP[2] defines the 
# CC#s for Encoder 2 and so on.

# For each Encoder, you can list as many CC#s as you like.  Each CC# that you list
# has to be in the range of 0 - 127 and each CC# (except for the last CC#) should be 
# followed by a comma.  The CC#s should be listed within the empty square brackets.  

# For example, to define one CC# for Encoder 1:  ENCODERS_CC_MAP[1] = [50]
# This defines that Encoder 1 will send CC#50 in the first (and only) additional page.

# As another example, to define three CC#s for Encoder 1:  ENCODERS_CC_MAP[1] = [50, 75, 100]
# This defines that Encoder 1 will send CC#50 in the first additional page, CC#75 in the
# second additional page and CC#100 in the third additional page.  

# The number of CC#s that you define for each Encoder HAVE to be equal.  For example, 
# if you define three CC#s for Encoder 1, you HAVE to define three CC#s for the other 
# seven Encoders.  Also, the number of CC#s that you define for each Encoder HAS to be 
# equal to the number of Names you define in the [NAME MAP] settings in the next section.   


ENCODERS_CC_MAP[1] = []
ENCODERS_CC_MAP[2] = []
ENCODERS_CC_MAP[3] = []
ENCODERS_CC_MAP[4] = []
ENCODERS_CC_MAP[5] = []
ENCODERS_CC_MAP[6] = []
ENCODERS_CC_MAP[7] = []
ENCODERS_CC_MAP[8] = []


# ***************************** [NAME MAP] **************************

# The following settings allow you to specify the names to show in the Display
# for the CC#s defined in your [CC MAP] settings in the previous section.

# Each of the listings below defines the names to show for one Encoder.  For example, 
# ENCODERS_NAME_MAP[1] defines the names for Encoder 1, ENCODERS_NAME_MAP[2] defines the 
# names for Encoder 2 and so on.

# For each Encoder, the number of names you list HAS to be equal to the number of CC#s 
# you defined for the Encoder in your [CC MAP] settings.  Each name that you list
# should be enclosed in single quotes, should NOT contain single quotes within the name,
# should be 8 characters long or less and (with the exception of the last name) should be followed 
# by a comma.  The names should be listed within the empty square brackets.  

# For example, to define one name for Encoder 1:  ENCODERS_NAME_MAP[1] = ['LFO Rate']
# This defines that the Display section under Encoder 1 will display LFO Rate in the first 
# (and only) additional page.

# As another example, to define three names for Encoder 1:  
# ENCODERS_NAME_MAP[1] = ['LFO Rate', 'Porta', 'Misc']
# This defines that the Display section under Encoder 1 will display LFO Rate in the first 
# additional page, Porta in the second additional page and Misc in the third additional page.

# Again, for each Encoder, the number of names you list HAS to be equal to the number of CC#s 
# you defined for the Encoder in your [CC MAP] settings.  


ENCODERS_NAME_MAP[1] = []
ENCODERS_NAME_MAP[2] = []
ENCODERS_NAME_MAP[3] = []
ENCODERS_NAME_MAP[4] = []
ENCODERS_NAME_MAP[5] = []
ENCODERS_NAME_MAP[6] = []
ENCODERS_NAME_MAP[7] = []
ENCODERS_NAME_MAP[8] = []
