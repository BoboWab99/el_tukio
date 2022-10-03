# Async messages

class msg():
    @staticmethod
    def success(msg):
        return {
            'tag': 'SUCCESS',
            'content': msg
        }
    
    @staticmethod
    def info(msg):
        return {
            'tag': 'INFO',
            'content': msg
        }

    @staticmethod
    def warning(msg):
        return {
            'tag': 'WARNING',
            'content': msg
        }

    @staticmethod
    def error(msg):
        return {
            'tag': 'DANGER',
            'content': msg
        }
