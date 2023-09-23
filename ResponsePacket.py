# ******************************************************************
# Response Packet Base Class and Extensions
# The basic version of a response packet and all the derived classes
# ******************************************************************
# Author: K. E. Brown
# Started: 9/23/2023
# Modified: 9/23/2023
# ******************************************************************

# Base class
class ResponsePacket:
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __str__(self):
        return f"User: {self.user}\nMessage: {self.message}"

    def execute(self):
        # Implement the logic to execute the response
        pass

# A Response Packet that calls another command
class CommandResponsePacket(ResponsePacket):
    def execute(self):
        pass

# A Response Packet that indicates a successful execution
class SuccessResponsePacket(ResponsePacket):
    def execute(self):
        pass

# A Response Packet that indicates an error in execution
class ErrorResponsePacket(ResponsePacket):
    def execute(self):
        pass

# A Response Packet that indicates a message should be sent
class MessageResponsePacket(ResponsePacket):
    def execute(self):
        pass

# A Response Packet which modifies one of a user's resources
class ResourceResponsePacket(ResponsePacket):
    def __init__(self, user, message, resource_name, amount):
        pass

    def __str__(self):
        return f"User: {self.user}\nMessage: {self.message}\nResource Name: {self.resource_name}\nAmount: {self.amount}"

    def execute(self):
        pass
    
# A Response Packet which modifies one of a user's groups
class GroupResponsePacket(ResponsePacket):
    def __init__(self, user, message, group_name):
        pass

    def __str__(self):
        return f"User: {self.user}\nMessage: {self.message}\nGroup Name: {self.group_name}"

    def execute(self):
        pass