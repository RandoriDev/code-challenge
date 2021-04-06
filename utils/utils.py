""" module Utils. """


class Utils():
    """ Utils Class """
    @staticmethod
    def compareDicts(dict1: dict, dict2: dict) -> bool:
        """ compare Dicts """
        tmp_dict = dict1.keys() - dict2.keys()
        return len(tmp_dict) == 0

    @staticmethod
    def remove_line_key(obj):
        """ remove_line_key """
        if type(obj) == dict:

            obj1 = {}

            for key in obj.keys():

                new_key = key.replace("_", "")

                if new_key != key:
                    obj1[new_key] = Utils.remove_line_key(obj[key])
                else:
                    obj1[key] = Utils.remove_line_key(obj[key])

        elif type(obj) == list:
            l = []
            for item in obj:
                l.append(Utils.remove_line_key(item))
            obj1 = l
        else:
            obj1 = obj
        return obj1
