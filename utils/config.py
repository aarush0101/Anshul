from utils.logger import getLogger


logger = getLogger(__name__)

class Config():
    '''
    Get a *bot* specific value form this config.
        
    Params
    ----------- 
    __key:
        Get a value from this config if it exists.

    Returns
    ----------- 
    str, int, float, obj

    Raises
    ----------- 
    ValueError:
                The key was not found.
    '''
    keys = {
            "Prefix": "+",
            "Guild_ID": 1148546198219788308,
            "Icon_URL": "https://img.icons8.com/pulsar-color/48/snail.png",
            "Bot_Name": "Your Mom",
            "Owner_Name": "oAnshul",
            "Copyright": "Aarush",
            "Success_Emoji": "<:checkMark:1172627738268541038>",
            "Error_Emoji": "<:noEntry:1172627159244873790>",
            "Owners": [1025341204235292724, 906543610269401148, 930119015785959474],
            "Log_channel_ID": 12,
            "Token": "MTIxNjc4Mjc3OTE1MzUxODYyMg.GEPVT3.x2qdHHAzxsEEEFhY7xEoSmsG7OFd1_yUrQR2Q8"
        }

    def __init__(self, __key):
        """
        Return the config entire(if found)
        """
        try:
            self.keys.get(__key)
        except Exception:
            raise ValueError("The requested value wasn't found.")
    def __update__(self, __item, __key):
        """
        Updates an internal key with the key received
        """
        if __item not in self.keys:
            raise ValueError("Configuration %s is invalid" % (__item,))
        
        self[__item] == __key

    def __delitem__(self, __item):
        return self.keys.pop(__item)
    
    def __getitem__(self, __item):
        """
        # DEPRECATED

        Return a config entire(if found)
        """
        return self.keys.get(__item)


