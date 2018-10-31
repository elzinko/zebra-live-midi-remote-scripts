from PlusChordType import PlusChordType

# ***************************** [SETTINGS NOTES] **************************

# It is recommended that you back this file up BEFORE modifying it. 

# Please DO NOT change any of the spacing in this file. 
 
# Please DO NOT change the name of this file or its file extension.  When done 
# making your changes to the settings below, just save the file.
 
# After saving this file, you will need to close/restart Live for your changes 
# to take effect.


# ***************************** [CHORD TYPES] **************************"

# The following settings allow you to customize the Chord Types that will be available
# in Chord Mode.

# For each Chord Type, you can change:
#    - The name of the type.  The name should be 8 characters or less and should be enclosed in single quotes.

#    - The intervals for the type.  These are defined in a comma-separated list (enclosed in parentheses) following
#      the name.  Intervals are defined based on their distance from the root.  The minimum number of intervals is 2 
#      and the maximum number of intervals is 6.  The first interval HAS to be 0, the other intervals HAVE to be 
#      positive numbers.  The maximum value for an interval is 23.  
    
# You should NOT change anything other than the settings described above.  In particular, you should NOT
# remove any of the parentheses or commas below.  Changes of that sort will result in PXT-Live Plus not loading.

# Incorrect settings in your definitions (such as specifying an interval with a value of 25) will also result in 
# PXT-Live Plus not loading.  


# The chord types available from the Track Select buttons. 
UPPER_CHORD_TYPES = [
    PlusChordType('Major',      (0, 4, 7)),
    PlusChordType('Maj7',       (0, 4, 7, 11)),
    PlusChordType('Maj7-5',     (0, 4, 6, 11)),
    PlusChordType('6',          (0, 4, 7, 9)),
    PlusChordType('Add2',       (0, 2, 4, 7)),
    PlusChordType('7',          (0, 4, 7, 10)),
    PlusChordType('Sus',        (0, 5, 7)),
    PlusChordType('Aug',        (0, 4, 8))
]

# The chord types available from the Track State buttons. 
LOWER_CHORD_TYPES = [
    PlusChordType('Minor',       (0, 3, 7)),
    PlusChordType('Min7',        (0, 3, 7, 10)),
    PlusChordType('Min7-5',      (0, 3, 7, 11)),
    PlusChordType('Min6',        (0, 3, 7, 9)),
    PlusChordType('MinAdd2',     (0, 2, 3, 7)),
    PlusChordType('7-5',         (0, 4, 6, 10)),
    PlusChordType('Sus2',        (0, 2, 7)),
    PlusChordType('Dim',         (0, 3, 6))
]    