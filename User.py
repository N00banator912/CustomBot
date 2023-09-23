# *********************************************************************
# IRC User Class
# Class to track values related to IRC client users
# *********************************************************************
# Author: K. E. Brown
# Started: 9/23/2023
# Modified: 9/23/2023
# *********************************************************************

class User:
    def __init__(self, username):
        self.username = username
        self.resources = {}  # Dictionary to store user's resources
        self.groups = []     # List to store user's group memberships
        self.ranks = []      # List to store user's ranks
        self.message_count = 0  # Count of messages sent by the user

    def add_resource(self, resource_name, amount):
        # Add or update a resource for the user
        if resource_name in self.resources:
            self.resources[resource_name].add_amount(amount)
        else:
            self.resources.append()

    def remove_resource(self, resource_name, amount):
        # Remove a specified amount of a resource from the user
        if resource_name in self.resources:
            self.resources[resource_name].remove_amount(amount)

    def add_to_group(self, group_name):
        # Add the user to a group
        if group_name not in self.groups:
            self.groups.append(group_name)

    def remove_from_group(self, group_name):
        # Remove the user from a group
        if group_name in self.groups:
            self.groups.remove(group_name)

    def add_rank(self, rank_name):
        # Add a rank to the user
        if rank_name not in self.ranks:
            self.ranks.append(rank_name)

    def remove_rank(self, rank_name):
        # Remove a rank from the user
        if rank_name in self.ranks:
            self.ranks.remove(rank_name)

    def increment_message_count(self):
        # Increment the user's message count
        self.message_count += 1

    def __str__(self):
        return f"User: {self.username}\n" \
               f"Resources: {self.resources}\n" \
               f"Groups: {self.groups}\n" \
               f"Ranks: {self.ranks}\n" \
               f"Message Count: {self.message_count}"

class Resource:
    def __init__(self, name, initial_amount):
        self.name = name
        self.amount = initial_amount
        self.is_permanent = True
        
    def add_amount(self, amount):
        self.amount += amount
        
    def remove_amount(self, amount):
        self.amount -= amount
        if (self.amount <= 0):
            self.on_empty()

    def on_empty(self):
        pass

class Group:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, user):
        if user not in self.members:
            self.members.append(user)

    def remove_member(self, user):
        if user in self.members:
            self.members.remove(user)

class Rank:
    def __init__(self, name):
        self.name = name
