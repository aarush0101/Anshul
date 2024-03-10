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
    def __init__(self, __key):
        for value in Config.keys:
            if value != Config.default_values:
                await self.reset()
                
        try:
            for key in Config.keys:
                if key == __key:
                    return key
            raise ValueError("The requested value wasn't found")
        except Exception:
            raise ValueError("The requested value wasn't found.")

    keys = {
            "Prefix": "+",
            "Guild_ID": 1,
            "Owner_ID": 2,
            "Icon_URL": "https://img.icons8.com/pulsar-color/48/snail.png",
            "Bot_Name": "Your Mom",
            "Owner_Name": "oAnshul",
            "Copyright": "Aarush"
        }
    default_values = {
        
    }
